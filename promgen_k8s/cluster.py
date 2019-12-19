from typing import (Any, Dict, List)

import abc


class GeneratorJob(abc.ABC):
  @abc.abstractmethod
  def generate(self, prom_conf: Dict[str, Any], cluster: 'Cluster') -> None:
    pass


class Cluster():
  def __init__(self,
               name: str,
               public_domain='example.com',
               private_domain='example.loc',
               incluster=False,
               jobs: List[GeneratorJob] = None):
    self.name = name
    self.public_domain = public_domain
    self.private_domain = private_domain
    self.incluster = incluster
    self.jobs = jobs or []

    if self.incluster:
      self.bearer_token_file = '/var/run/secrets/kubernetes.io/serviceaccount/token'
      self.ca_file = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
      self.api_server = 'kubernetes.default.svc'
    else:
      self.bearer_token_file = '/var/run/kube_secrets/{0}_bearer_token'.format(self.name)
      self.ca_file = '/var/run/kube_secrets/{0}_ca_crt'.format(self.name)
      self.api_server = 'api.internal.{0}.{1}'.format(self.name, self.public_domain)

  def get_kubernetes_sd_config(self, role: str):
    if self.incluster:
      return {'role': role}

    return {
      'role': role,
      'api_server': 'https://{0}'.format(self.api_server),
      'tls_config': {
        'ca_file': self.ca_file
      },
      'bearer_token_file': self.bearer_token_file
    }
