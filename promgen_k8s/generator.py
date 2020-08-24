from typing import (Any, Dict, IO, List, Optional)

import yaml

from .cadvisor_job import *
from .cluster import *
from .nodes_job import *
from .pods_job import *
from .prom_dsl import *
from .service_endpoints_job import *
from .services_job import *


# via http://pyyaml.org/ticket/64 and http://signal0.com/2013/02/06/disabling_aliases_in_pyyaml.html
# pylint: disable=too-many-ancestors
class ListIndentingDumper(yaml.Dumper):
  def increase_indent(self, flow=False, indentless=False):
    return super().increase_indent(flow, False)

  def ignore_aliases(self, data):
    return True


class Generator():
  def __init__(self, clusters: List[Cluster], initial_prom_conf: Optional[Dict[str, Any]] = None):
    self.clusters = clusters
    self.initial_prom_conf = initial_prom_conf or {}

  def dump(self, yaml_file: IO) -> None:
    prom_conf = {}
    prom_conf.update(self.initial_prom_conf)

    if prom_conf['scrape_configs'] is None:
      prom_conf['scrape_configs'] = []

    # add jobs for k8s clusters
    for cluster in self.clusters:
      for job in cluster.jobs:
        job.generate(prom_conf, cluster)

    yaml.dump(prom_conf,
              yaml_file,
              encoding=('utf-8'),
              Dumper=ListIndentingDumper,
              default_flow_style=False,
              explicit_start=True)
