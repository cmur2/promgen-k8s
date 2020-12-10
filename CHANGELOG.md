# Changelog

## 0.2.2 (December 10, 2020)

CHANGES:

- Support Python 3 only
- Use [Poetry](https://python-poetry.org/docs/) dependency manager instead of [pipenv](https://pipenv.pypa.io/) for the project now as Poetry is more stable, supports [pyproject.toml](pyproject.toml]) file format and compatible Python version ranges

## 0.2.1 (October 21, 2019)

IMPROVEMENTS:

- Force usage of HTTPS for Kubernetes SD apiserver connections since newer Prometheus versions changed the default

## 0.2.0 (March 27, 2019)

CHANGES:

- Switch to kubelet HTTP port 10255 for scraping cadvisor and nodes metrics since that also works with kubelet `--authorization-mode=Webhook`

## 0.1.7 (December 17, 2018)

IMPROVEMENTS:

- Allow specifying `prometheus.io/module` annotation for blackbox ingress monitoring

## 0.1.6 (June 11, 2018)

IMPROVEMENTS:

- Add `kubernetes_container_name` label for all endpoints of pods where `prometheus.io/filterport: true`

## 0.1.5 (June 11, 2018)

IMPROVEMENTS:

- Add snapshot tests for generated YAML
- Allow specifying `prometheus.io/filterport: true` on pods to automatically discover all endpoints who's pod port name ends with `metrics` instead of using `prometheus.io/port`

## 0.1.4 (February 13, 2018)

IMPROVEMENTS:

- Allow specifying `prometheus.io/module` and `prometheus.io/path` annotations for blackbox service monitoring

## 0.1.3 (December 22, 2017)

IMPROVEMENTS:

- Remove some unneeded since duplicated labels from pods, nodes and cadvisor jobs
- Fix typo in name of the `ServiceEndpointsJob`
- Provide unique instance label for all jobs, usually copied from the `__address__` label
- Add `IngressesJob` for probing ingresses via the blackbox exporter (no HTTPS support)
- Allow setting the `scrape_interval` for nodes, cadvisor, services, service endpoints and ingresses jobs
- Support different scrape intervals for pods using `prometheus.io/interval` annotation
- Do not require proxies in remote clusters anymore for scraping pods, services, service endpoints or ingresses but blackbox-exporter might be needed instead

## 0.1.2 (November 7, 2017)

IMPROVEMENTS:

- Use cAdvisor metrics path compatible with Kubernetes 1.7.3 and above

## 0.1.1 (September 13, 2017)

IMPROVEMENTS:

- Do not use aliases in generated YAML

## 0.1.0 (September 13, 2017)

NEW FEATURES:

- Initial release
