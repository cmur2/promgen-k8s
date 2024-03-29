from typing import (Optional)

from .cluster import *
from .prom_dsl import *


class CadvisorJob(GeneratorJob):

  def __init__(self,
               scrape_interval: Optional[str] = None,
               additional_relabel_configs: Optional[List[Any]] = None,
               additional_metric_relabel_configs: Optional[List[Any]] = None):
    self.type = 'cadvisor'
    self.scrape_interval = scrape_interval
    self.additional_relabel_configs = additional_relabel_configs or []
    self.additional_metric_relabel_configs = additional_metric_relabel_configs or []

  # Scrape config for Kubelet cAdvisor.
  #
  # This is required for Kubernetes 1.7.3 and later, where cAdvisor metrics
  # (those whose names begin with 'container_') have been removed from the
  # Kubelet metrics endpoint.  This job scrapes the cAdvisor endpoint to
  # retrieve those metrics.
  #
  # In Kubernetes 1.7.0-1.7.2, these metrics are only exposed on the cAdvisor
  # HTTP endpoint; use "replacement: /api/v1/nodes/${1}:4194/proxy/metrics"
  # in that case (and ensure cAdvisor's HTTP server hasn't been disabled with
  # the --cadvisor-port=0 Kubelet flag).
  #
  # This job is not necessary and should be removed in Kubernetes 1.6 and
  # earlier versions, or it will cause the metrics to be scraped twice.
  def generate(self, prom_conf: Dict[str, Any], cluster: Cluster) -> None:
    prom_conf['scrape_configs'].append({
      'job_name': f'{cluster.name}-kubernetes-cadvisor',
      'scheme': 'https',
      'kubernetes_sd_configs': [
        cluster.get_kubernetes_sd_config('node')
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

      'relabel_configs': [
        remove_label('__meta_kubernetes_node_label_node_role_kubernetes_io_node'),
        remove_label('__meta_kubernetes_node_label_node_role_kubernetes_io_master'),
        labelmap(regex='__meta_kubernetes_node_label_(.+)'),
        copy_value('__address__', 'instance'),
        set_value('__address__', f'{cluster.api_server}:443'),
        replace(source_labels=['__meta_kubernetes_node_name'],
          regex='(.+)', replacement='/api/v1/nodes/${1}:10255/proxy/metrics/cadvisor',
          target_label='__metrics_path__')
      ],

      'metric_relabel_configs': [
        replace(source_labels=['id'],
                regex=r'^/machine\.slice/machine-rkt\\x2d([^\\]+)\\.+/([^/]+)\.service$', replacement='${2}-${1}',
                target_label='rkt_container_name'),
        replace(source_labels=['id'],
                regex=r'^/system\.slice/(.+)\.service$', replacement='${1}',
                target_label='systemd_service_name'),
        drop(source_labels=['__name__'], regex='go_.*')
      ]
    }) # yapf: disable

    # set job's scrape_interval if defined
    if not self.scrape_interval is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = self.scrape_interval

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'].extend(self.additional_metric_relabel_configs)
