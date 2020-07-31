# promgen-k8s

![ci](https://github.com/cmur2/promgen-k8s/workflows/ci/badge.svg)

A modular [Prometheus 2](https://prometheus.io) configuration file generator to monitor multiple [Kubernetes](https://kubernetes.io) clusters with a single Prometheus instance.

## Scenario

You have one Kubernetes cluster per environment (dev, qa, staging, production, etc.) for whichever reasons including e.g. special permission model, limiting the blast radius of problems related to Kubernetes or to test Kubernetes upgrades in staging environment first.
You have a separate Kubernetes cluster for operations that runs your monitoring and logging setup, CI pipeline, etc.
You want to monitor all environments/clusters with a single Prometheus instance located in the operations cluster.

Writing, modifying and maintaining the [prometheus.yml](https://github.com/prometheus/prometheus/blob/master/documentation/examples/prometheus-kubernetes.yml) for one Kubernetes cluster by hand is tedious and error prone. Doing so for multiple clusters that should share most of the configuration except for specific rules can become a nightmare.

promgen-k8s aims to provide a toolkit allowing you to easily generate a prometheus.yml tailored for monitoring multiple Kubernetes clusters with invididual scraping jobs and relabeling rules per cluster.

## Current State

promgen-k8s is currently in a very early state where it manages to generate the example  [prometheus-kubernetes.yml](https://github.com/prometheus/prometheus/blob/master/documentation/examples/prometheus-kubernetes.yml) for multiple clusters using [autodiscovery](https://prometheus.io/docs/operating/configuration/#%3Ckubernetes_sd_config%3E) including custom relabeling rules per cluster. It assumes that it can reach all Kubernetes apiservers by predictable DNS names using the provided secret files for authentication.

For ingresses, pod, service and service endpoint monitoring in remote clusters promgen-k8s uses the Kubernetes apiservers as an [HTTP proxy](https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-services/).

As ingresses and services are checked using the [blackbox-exporter](https://github.com/prometheus/blackbox_exporter/) promgen-k8s also assumes a `blackbox-exporter` pod and service in `monitoring` namespace running in each cluster (including remote clusters).

promgen-k8s is successfully used with Kubernetes 1.8 clusters on [AWS](http://aws.amazon.com/) created by [kops](https://github.com/kubernetes/kops).

## Example

The [example](example-generator.py) uses a [stub file](example-prometheus-stub.yml) for manual configuration and can be tested using `pip install promgen-k8s` and then `python example-generator.py`.

## Related Work

- [https://github.com/line/promgen]([https://github.com/line/promgen])

## Doing a Release

You need to have the [Poetry](https://python-poetry.org/docs/) dependency manager installed and a [PyPI](https://pypi.org/) account (a [test account](https://test.pypi.org/) works as well) including an authentication token.

### Testing the Release

One-time setup:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi TOKEN_FROM_TESTPYPI_ACCOUNT
```

Bump version in [pyproject.toml](pyproject.toml), update the [changelog](CHANGELOG.md) with new release and date and commit.

Build and release:

```bash
poetry publish -r testpypi --build
```

Check installation:

```bash
pip install --index-url https://test.pypi.org/simple/ promgen_k8s
```

### Official Release

One-time setup:

```bash
poetry config pypi-token.pypi TOKEN_FROM_PYPI_ACCOUNT
```

Bump version in [pyproject.toml](pyproject.toml), update the [changelog](CHANGELOG.md) with new release and date and commit.

Build and release:

```bash
poetry publish --build
```

Check installation:

```bash
pip install promgen_k8s
```

## License

promgen-k8s is licensed under the Apache License, Version 2.0. See LICENSE for more information.
