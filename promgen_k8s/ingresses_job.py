
from .prom_dsl import *

class IngressesJob(object):
  def __init__(self, scrape_interval=None, additional_relabel_configs=None, additional_metric_relabel_configs=None):
    self.type = 'ingresses'
    self.scrape_interval = scrape_interval
    self.additional_relabel_configs = additional_relabel_configs or []
    self.additional_metric_relabel_configs = additional_metric_relabel_configs or []

  # Example scrape config for probing ingresses via the Blackbox Exporter.
  #
  # The relabeling allows the actual ingress scrape endpoint to be configured
  # via the following annotations:
  #
  # * `prometheus.io/probe`: Only probe services that have a value of `true`
  # * `prometheus.io/module`: If the Blackbox exporter module used is not named `http_2xx` override this.
  def generate(self, prom_conf, c):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-ingresses'.format(c.name),
      'scheme': 'https',
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('ingress') ],

      # This TLS & bearer token file config is used to connect to the actual scrape
      # endpoints for cluster components. This is separate to discovery auth
      # configuration because discovery & scraping are two separate concerns in
      # Prometheus. The discovery auth config is automatic if Prometheus runs inside
      # the cluster. Otherwise, more config options have to be provided within the
      # <kubernetes_sd_config>.
      'tls_config': { 'ca_file': c.ca_file },
      'bearer_token_file': c.bearer_token_file,

      'metrics_path': '/api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe',
      'params': {
        'module': ['http_2xx']
      },

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_ingress_annotation_prometheus_io_probe'], regex='true'),
        # Note: does not support any __meta_kubernetes_ingress_scheme except HTTP
        copy_value('__meta_kubernetes_ingress_annotation_prometheus_io_module', '__param_module'),
        replace(source_labels=['__address__','__meta_kubernetes_ingress_path'],
          separator=';', regex='(.+);(.+)', replacement='$1$2',
          target_label='__address__'),
        copy_value('__address__', '__param_target'),
        copy_value('__address__', 'instance'),
        set_value('__address__', '{0}:443'.format(c.api_server)),
        labelmap(regex='__meta_kubernetes_ingress_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_ingress_name', 'kubernetes_ingress_name')
      ]
    })

    # set job's scrape_interval if defined
    if not self.scrape_interval is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = self.scrape_interval

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'] = self.additional_metric_relabel_configs
