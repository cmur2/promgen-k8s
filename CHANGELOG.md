# Changelog

## 0.1.3

IMPROVEMENTS:

- Remove some unneeded since duplicated labels from pods, nodes and cadvisor jobs
- Fix typo in name of the `ServiceEndpointsJob`
- Provide unique instance label for all jobs, usually copied from the __address__ label
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

- Initial relase
