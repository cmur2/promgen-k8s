
from .prom_dsl import *

class ServiceEndpointsJob(object):
  def __init__(self, scrape_interval=None, additional_relabel_configs=None, additional_metric_relabel_configs=None):
    self.type = 'service-endpoints'
    self.scrape_interval = scrape_interval
    self.additional_relabel_configs = additional_relabel_configs or []
    self.additional_metric_relabel_configs = additional_metric_relabel_configs or []

  # Scrape config for service endpoints.
  #
  # The relabeling allows the actual service scrape endpoint to be configured
  # via the following annotations:
  #
  # * `prometheus.io/scrape`: Only scrape services that have a value of `true`
  # * `prometheus.io/scheme`: If the metrics endpoint is secured then you will need
  # to set this to `https` & most likely set the `tls_config` of the scrape config.
  # * `prometheus.io/path`: If the metrics path is not `/metrics` override this.
  # * `prometheus.io/port`: If the metrics are exposed on a different port to the
  # service then set this appropriately.
  def generate(self, prom_conf, c):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-service-endpoints'.format(c.name),
      'scheme': 'https',
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('endpoints') ],

      # This TLS & bearer token file config is used to connect to the actual scrape
      # endpoints for cluster components. This is separate to discovery auth
      # configuration because discovery & scraping are two separate concerns in
      # Prometheus. The discovery auth config is automatic if Prometheus runs inside
      # the cluster. Otherwise, more config options have to be provided within the
      # <kubernetes_sd_config>.
      'tls_config': { 'ca_file': c.ca_file },
      'bearer_token_file': c.bearer_token_file,

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_scrape'], regex='true'),
        # Note: does not support any __meta_kubernetes_service_annotation_prometheus_io_scheme except HTTP
        replace(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_path'],
          regex='(.+)',
          target_label='__metrics_path__'),
        replace(source_labels=['__address__', '__meta_kubernetes_service_annotation_prometheus_io_port'],
          regex='([^:]+)(?::\\d+)?;(\\d+)', replacement='$1:$2',
          target_label='__address__'),
        replace(source_labels=['__meta_kubernetes_namespace', '__meta_kubernetes_pod_name', '__meta_kubernetes_service_annotation_prometheus_io_port', '__metrics_path__'],
          separator=';', regex='(.+);(.+);(.+);(.+)', replacement='/api/v1/namespaces/$1/pods/$2:$3/proxy$4',
          target_label='__metrics_path__'),
        copy_value('__address__', 'instance'),
        set_value('__address__', '{0}:443'.format(c.api_server)),
        labelmap(regex='__meta_kubernetes_service_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_service_name', 'kubernetes_service_name')
      ]
    })

    # set job's scrape_interval if defined
    if not self.scrape_interval is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = self.scrape_interval

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'] = self.additional_metric_relabel_configs

# backwards-compatibiliy for typo
class ServiceEndpoitsJob(ServiceEndpointsJob):
  pass
