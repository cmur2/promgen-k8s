
from prom_dsl import *

class ServiceEndpoitsJob:
  def __init__(self, additional_relabel_configs=[], additional_metric_relabel_configs=[]):
    self.type = 'service-endpoints'
    self.additional_relabel_configs = additional_relabel_configs
    self.additional_metric_relabel_configs = additional_metric_relabel_configs

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
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('endpoints') ],

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_scrape'], regex=True),
        replace(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_scheme'],
          regex='(https?)',
          target_label='__scheme__'),
        replace(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_path'],
          regex='(.+)',
          target_label='__metrics_path__'),
        replace(source_labels=['__address__', '__meta_kubernetes_service_annotation_prometheus_io_port'],
          regex='([^:]+)(?::\\d+)?;(\\d+)', replacement='$1:$2',
          target_label='__address__'),
        labelmap(regex='__meta_kubernetes_service_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_service_name', 'kubernetes_service_name')
      ]
    })

    if not c.incluster:
      prom_conf['scrape_configs'][-1]['relabel_configs'].extend([
        replace(source_labels=['__address__', '__metrics_path__'],
          regex='([0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]*:[0-9]*);(.*)', replacement='/proxy/$1$2',
          target_label='__metrics_path__'),
        set_value('__address__', c.proxy)
      ])

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'] = self.additional_metric_relabel_configs
