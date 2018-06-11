
from .prom_dsl import *

class PodsJob(object):
  def __init__(self, interval_map=None, additional_relabel_configs=None, additional_metric_relabel_configs=None):
    self.type = 'pods'
    self.interval_map = interval_map or {}
    self.additional_relabel_configs = additional_relabel_configs or []
    self.additional_metric_relabel_configs = additional_metric_relabel_configs or []

  # Example scrape config for pods
  #
  # The relabeling allows the actual pod scrape endpoint to be configured via the
  # following annotations:
  #
  # * `prometheus.io/scrape`: Only scrape pods that have a value of `true`
  # * `prometheus.io/path`: If the metrics path is not `/metrics` override this.
  # * `prometheus.io/port`: Scrape the pod on the indicated port instead of the
  # pod's declared ports (default is a port-free target if none are declared).
  # * `prometheus.io/filterport`: If `true` and no `prometheus.io/port` given
  # then filter the pod's declared ports for those with name ending in 'metrics'.
  # * `prometheus.io/interval`: If present, use the given level instead
  # of the global default (must be configured appropriately)
  def generate(self, prom_conf, c):
    self.generate_interval(prom_conf, c, 'default', None)
    for name, value in self.interval_map.items():
      self.generate_interval(prom_conf, c, name, value)

  def generate_interval(self, prom_conf, c, interval_name, interval_value):
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-pods-{1}'.format(c.name, interval_name),
      'scheme': 'https',
      'kubernetes_sd_configs': [ c.get_kubernetes_sd_config('pod') ],

      # This TLS & bearer token file config is used to connect to the actual scrape
      # endpoints for cluster components. This is separate to discovery auth
      # configuration because discovery & scraping are two separate concerns in
      # Prometheus. The discovery auth config is automatic if Prometheus runs inside
      # the cluster. Otherwise, more config options have to be provided within the
      # <kubernetes_sd_config>.
      'tls_config': { 'ca_file': c.ca_file },
      'bearer_token_file': c.bearer_token_file,

      'relabel_configs': [
        keep(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_scrape'], regex='true'),
        None,
        # set prometheus.io/filterport to false if prometheus.io/port is given
        replace(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_port'],
          regex='(.+)', replacement='false',
          target_label='__meta_kubernetes_pod_annotation_prometheus_io_filterport'),
        # keep all if prometheus.io/filterport is false or only matching else
        keep(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_filterport', '__meta_kubernetes_pod_container_port_name'],
          separator=';', regex='(false;.*)|(true;.*metrics)'),
        # set prometheus.io/port to container port number if prometheus.io/filterport is true
        replace(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_filterport', '__meta_kubernetes_pod_container_port_number'],
          separator=';', regex='true;(.+)',
          target_label='__meta_kubernetes_pod_annotation_prometheus_io_port'),
        # set container name label for distinction if prometheus.io/filterport is true
        replace(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_filterport', '__meta_kubernetes_pod_container_name'],
          separator=';', regex='true;(.+)',
          target_label='kubernetes_container_name'),
        # allow overwriting scrape path via prometheus.io/path
        replace(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_path'],
          regex='(.+)',
          target_label='__metrics_path__'),
        # update address if prometheus.io/port is given
        replace(source_labels=['__address__', '__meta_kubernetes_pod_annotation_prometheus_io_port'],
          separator=';', regex='([^:]+)(?::\\d+)?;(\\d+)', replacement='$1:$2',
          target_label='__address__'),
        # rewrite scrape path to use Kubernetes apiserver proxy
        replace(source_labels=['__meta_kubernetes_namespace', '__meta_kubernetes_pod_name', '__meta_kubernetes_pod_annotation_prometheus_io_port', '__metrics_path__'],
          separator=';', regex='(.+);(.+);(.+);(.+)', replacement='/api/v1/namespaces/$1/pods/$2:$3/proxy$4',
          target_label='__metrics_path__'),
        copy_value('__address__', 'instance'),
        set_value('__address__', '{0}:443'.format(c.api_server)),
        labelmap(regex='__meta_kubernetes_pod_label_(.+)'),
        copy_value('__meta_kubernetes_namespace', 'kubernetes_namespace'),
        copy_value('__meta_kubernetes_pod_name', 'kubernetes_pod_name'),
        remove_label('pod_template_hash'),
        remove_label('controller_revision_hash'),
        remove_label('pod_template_generation')
      ],

      'metric_relabel_configs': [
        drop(source_labels=['__name__'], regex='go_.*')
      ]
    })

    if interval_name == 'default':
      prom_conf['scrape_configs'][-1]['relabel_configs'][1] = \
        drop(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_interval'], regex='.+')
    else:
      prom_conf['scrape_configs'][-1]['relabel_configs'][1] = \
        keep(source_labels=['__meta_kubernetes_pod_annotation_prometheus_io_interval'], regex=interval_name)

    # set job's scrape_interval if defined
    if not interval_value is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = interval_value

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'].extend(self.additional_metric_relabel_configs)
