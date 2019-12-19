from typing import (Optional)

from .cluster import *
from .prom_dsl import *


class NodesJob(GeneratorJob):
  def __init__(self,
               scrape_interval: Optional[str] = None,
               additional_relabel_configs: Optional[List[Any]] = None,
               additional_metric_relabel_configs: Optional[List[Any]] = None):
    self.type = 'nodes'
    self.scrape_interval = scrape_interval
    self.additional_relabel_configs = additional_relabel_configs or []
    self.additional_metric_relabel_configs = additional_metric_relabel_configs or []

  # Scrape config for nodes (kubelet).
  #
  # Rather than connecting directly to the node, the scrape is proxied though the
  # Kubernetes apiserver.  This means it will work if Prometheus is running out of
  # cluster, or can't connect to nodes for some other reason (e.g. because of
  # firewalling).
  def generate(self, prom_conf: Dict[str, Any], cluster: Cluster) -> None:
    prom_conf['scrape_configs'].append({
      'job_name': '{0}-kubernetes-nodes'.format(cluster.name),
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

      # Keep all node labels without their prefix, proxy against apiserver with
      # HTTPS by default
      'relabel_configs': [
        remove_label('__meta_kubernetes_node_label_node_role_kubernetes_io_node'),
        remove_label('__meta_kubernetes_node_label_node_role_kubernetes_io_master'),
        labelmap(regex='__meta_kubernetes_node_label_(.+)'),
        copy_value('__address__', 'instance'),
        set_value('__address__', '{0}:443'.format(cluster.api_server)),
        replace(source_labels=['__meta_kubernetes_node_name'],
                regex='(.+)', replacement='/api/v1/nodes/${1}:10255/proxy/metrics',
                target_label='__metrics_path__')
      ],

      'metric_relabel_configs': [
        drop(source_labels=['__name__'], regex='go_.*')
      ]
    }) # yapf: disable

    # set job's scrape_interval if defined
    if not self.scrape_interval is None:
      prom_conf['scrape_configs'][-1]['scrape_interval'] = self.scrape_interval

    # add additional configs
    prom_conf['scrape_configs'][-1]['relabel_configs'].extend(self.additional_relabel_configs)
    prom_conf['scrape_configs'][-1]['metric_relabel_configs'].extend(self.additional_metric_relabel_configs)
