from distutils.core import setup

setup(
  name='promgen-k8s',
  version='0.1.7',
  packages=['promgen_k8s'],
  url='https://github.com/cmur2/promgen-k8s',
  license='Apache 2.0',
  author='cmur2',
  author_email='cmur2@mycrobase.de',
  description='A modular Prometheus 2 configuration file generator to monitor multiple Kubernetes clusters with a single Prometheus instance.',
  install_requires=['PyYAML']
)
