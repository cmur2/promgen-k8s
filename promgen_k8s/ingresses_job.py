
from prom_dsl import *

class IngressesJob:
  def __init__(self, scrape_interval=None, additional_relabel_configs=[], additional_metric_relabel_configs=[]):
    self.type = 'ingresses'
    self.scrape_interval = scrape_interval
    self.additional_relabel_configs = additional_relabel_configs
    self.additional_metric_relabel_configs = additional_metric_relabel_configs

  # Example scrape config for probing ingresses via the Blackbox Exporter.
  #
  # The relabeling allows the actual ingress scrape endpoint to be configured
  # via the following annotations:
  #
  # * `prometheus.io/probe`: Only probe services that have a value of `true`
  def generate(self, prom_conf, c):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-ingresses'.format(c.name),
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('ingress') ],

      'metrics_path': '/probe',
      'params': {
        'module': ['http_2xx']
      },

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_ingress_annotation_prometheus_io_probe'], regex=True),
        # TODO: does not support any __meta_kubernetes_ingress_scheme except HTTP
        replace(source_labels=['__address__','__meta_kubernetes_ingress_path'],
          regex='(.+);(.+)', replacement='${1}${2}',
          target_label='__address__'),
        None,
        copy_value('__address__', 'instance'),
        set_value('__address__', 'blackbox-exporter'),
        copy_value('__param_target', 'instance'),
        labelmap(regex='__meta_kubernetes_ingress_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_ingress_name', 'kubernetes_ingress_name')
      ]
    })

    if c.incluster:
      prom_conf['scrape_configs'][-1]['relabel_configs'][2] = \
        copy_value('__address__', '__param_target')
    else:
      prom_conf['scrape_configs'][-1]['relabel_configs'][2] = \
        replace(source_labels=['__address__'],
          regex='(.*)', replacement=c.proxy+'/proxy/$1',
          target_label='__param_target')

    # set job's scrape_interval if defined
    if not self.scrape_interval is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = self.scrape_interval

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'] = self.additional_metric_relabel_configs
