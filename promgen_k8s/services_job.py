
from prom_dsl import *

class ServicesJob:
  def __init__(self, additional_relabel_configs=[], additional_metric_relabel_configs=[]):
    self.type = 'services'
    self.additional_relabel_configs = additional_relabel_configs
    self.additional_metric_relabel_configs = additional_metric_relabel_configs

  # Example scrape config for probing services via the Blackbox Exporter.
  #
  # The relabeling allows the actual service scrape endpoint to be configured
  # via the following annotations:
  #
  # * `prometheus.io/probe`: Only probe services that have a value of `true`
  def generate(self, prom_conf, c):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-services'.format(c.name),
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('service') ],

      'metrics_path': '/probe',
      'params': {
        'module': ['http_2xx']
      },

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_service_annotation_prometheus_io_probe'], regex=True),
        None,
        set_value('__address__', 'blackbox-exporter'),
        copy_value('__param_target', 'instance'),
        labelmap(regex='__meta_kubernetes_service_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_service_name', 'kubernetes_service_name')
      ]
    })

    if c.incluster:
      prom_conf['scrape_configs'][-1]['relabel_configs'][1] = \
        copy_value('__address__', '__param_target')
    else:
      prom_conf['scrape_configs'][-1]['relabel_configs'][1] = replace(
        source_labels=['__address__'],
        regex='([^.]+)\\.default\\.svc:\\d+$', replacement=c.proxy+'/proxy/$1/',
        target_label='__param_target')

    # add additional_relabel_configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'] = self.additional_metric_relabel_configs
