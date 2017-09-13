
from prom_dsl import *

class PodsJob:
  def __init__(self, additional_relabel_configs=[], additional_metric_relabel_configs=[]):
    self.type = 'pods'
    self.additional_relabel_configs = additional_relabel_configs
    self.additional_metric_relabel_configs = additional_metric_relabel_configs

  # Example scrape config for pods
  #
  # The relabeling allows the actual pod scrape endpoint to be configured via the
  # following annotations:
  #
  # * `prometheus.io/scrape`: Only scrape pods that have a value of `true`
  # * `prometheus.io/path`: If the metrics path is not `/metrics` override this.
  # * `prometheus.io/port`: Scrape the pod on the indicated port instead of the
  # pod's declared ports (default is a port-free target if none are declared).
  def generate(self, prom_conf, c):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-pods'.format(c.name),
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('pod') ],

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_scrape'], regex=True),
        replace(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_path'],
          regex='(.+)',
          target_label='__metrics_path__'),
        replace(source_labels=['__address__', '__meta_kubernetes_pod_annotation_prometheus_io_port'],
          regex='([^:]+)(?::\\d+)?;(\\d+)', replacement='$1:$2',
          target_label='__address__'),
        labelmap(regex='__meta_kubernetes_pod_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_pod_name', 'kubernetes_pod_name'),
        remove_label('pod_template_hash'),
        remove_label('controller_revision_hash')
      ],

      'metric_relabel_configs': [
        drop(source_labels=['__name__'], regex='go_.*')
      ]
    })

    if not c.incluster:
      prom_conf['scrape_configs'][-1]['relabel_configs'].extend([
        replace(source_labels=['__meta_kubernetes_pod_host_ip','__address__','__metrics_path__'],
          regex='(172\\.2[0,2-9].[0-9]*\\.[0-9]*);([0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]*:[0-9]*);(.*)', replacement='/proxy/$2$3',
          target_label='__metrics_path__'),
        replace(source_labels=['__meta_kubernetes_pod_host_ip'],
          regex='(172\\.2[0,2-9].[0-9]*\\.[0-9]*)', replacement=c.proxy,
          target_label='__address__')
      ])

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'].extend(self.additional_metric_relabel_configs)
