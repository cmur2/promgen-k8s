from typing import (Optional)

from .cluster import *
from .prom_dsl import *


class ServicesJob(GeneratorJob):
  def __init__(self,
               scrape_interval: Optional[str] = None,
               additional_relabel_configs: Optional[List[Any]] = None,
               additional_metric_relabel_configs: Optional[List[Any]] = None):
    self.type = 'services'
    self.scrape_interval = scrape_interval
    self.additional_relabel_configs = additional_relabel_configs or []
    self.additional_metric_relabel_configs = additional_metric_relabel_configs or []

  # Example scrape config for probing services via the Blackbox Exporter.
  #
  # The relabeling allows the actual service scrape endpoint to be configured
  # via the following annotations:
  #
  # * `prometheus.io/probe`: Only probe services that have a value of `true`
  # * `prometheus.io/path`: If the probe path is not `/` override this.
  # * `prometheus.io/module`: If the Blackbox exporter module used is not named `http_2xx` override this.
  def generate(self, prom_conf: Dict[str, Any], cluster: Cluster) -> None:
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-services'.format(cluster.name),
      'scheme': 'https',
      'kubernetes_sd_configs': [
        cluster.get_kubernetes_sd_config('service')
      ],

      # This TLS & bearer token file config is used to connect to the actual scrape
      # endpoints for cluster components. This is separate to discovery auth
      # configuration because discovery & scraping are two separate concerns in
      # Prometheus. The discovery auth config is automatic if Prometheus runs inside
      # the cluster. Otherwise, more config options have to be provided within the
      # <kubernetes_sd_config>.
      'tls_config': {
        'ca_file': cluster.ca_file
      },
      'bearer_token_file': cluster.bearer_token_file,

      'metrics_path': '/api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe',
      'params': {
        'module': ['http_2xx']
      },

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_probe'], regex='true'),
        copy_value('__meta_kubernetes_service_annotation_prometheus_io_module', '__param_module'),
        copy_value('__address__', '__param_target'),
        replace(source_labels=['__param_target', '__meta_kubernetes_service_annotation_prometheus_io_path'],
                separator=';', regex='(.+);(.+)', replacement='$1$2',
                target_label='__param_target'),
        copy_value('__address__', 'instance'),
        set_value('__address__', '{0}:443'.format(cluster.api_server)),
        labelmap(regex='__meta_kubernetes_service_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_service_name', 'kubernetes_service_name')
      ]
    }) # yapf: disable

    # set job's scrape_interval if defined
    if not self.scrape_interval is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = self.scrape_interval

    # add additional_relabel_configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'] = self.additional_metric_relabel_configs
