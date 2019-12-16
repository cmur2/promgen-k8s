#!/usr/bin/env python

import yaml

import promgen_k8s as g
from promgen_k8s.prom_dsl import *

CLUSTERS = [
  g.Cluster('staging', jobs=[
    g.NodesJob(),
    g.IngressesJob(),
    g.CadvisorJob(),
    g.ServiceEndpointsJob(),
    g.ServicesJob(additional_relabel_configs=[
      # reverse.default.svc:443 should prompt for authentication in staging environment
      replace(source_labels=['__param_target'],
        regex='reverse.default.svc:443', replacement='https_401',
        target_label='__param_module')
    ]),
    g.PodsJob()
  ]),
  g.Cluster('production', jobs=[
    g.NodesJob(),
    g.IngressesJob(),
    g.CadvisorJob(),
    g.ServiceEndpointsJob(),
    g.ServicesJob(),
    g.PodsJob()
  ]),
  # The incluster property marks the cluster in which Prometheus in running
  g.Cluster('operations', incluster=True, jobs=[
    g.NodesJob(),
    g.IngressesJob(),
    g.CadvisorJob(),
    g.ServiceEndpointsJob(),
    g.ServicesJob(),
    g.PodsJob(interval_map={'long': '1h'})
  ])
]

if __name__ == "__main__":
  # read in the stub config
  with open('example-prometheus-stub.yml', 'r') as f:
    stub_prom_conf = yaml.load(f, Loader=yaml.SafeLoader)

  generator = g.Generator(CLUSTERS, initial_prom_conf=stub_prom_conf)

  # write out merged result
  with open('example-prometheus.yml', 'w') as f:
    generator.dump(f)
