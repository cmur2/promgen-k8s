# import unittest
import io

import promgen_k8s as g
from promgen_k8s.prom_dsl import *


class TestPromgenK8s:
  def test_generate(self, snapshot):
    stub_prom_conf = {
      'global': {
        'scrape_interval': '1m',
        'evaluation_interval': '1m'
      },
      'rule_files': ['/etc/alert.rules'],
      'scrape_configs': []
    }
    clusters = [
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
    ]  # yapf: disable
    generator = g.Generator(clusters, initial_prom_conf=stub_prom_conf)
    assert generator is not None
    tmp_file = io.BytesIO()
    generator.dump(tmp_file)
    assert tmp_file.getvalue().decode('utf-8') == snapshot
    tmp_file.close()
