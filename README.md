# promgen-k8s

A modular [Prometheus 2](https://prometheus.io) configuration file generator to monitor multiple [Kubernetes](https://kubernetes.io) clusters with a single Prometheus instance.

## Scenario

You have one Kubernetes cluster per environment (dev, staging, production) for whichever reasons including e.g. special permission model, limiting the blast radius of problems related to Kubernetes or to test Kubernetes upgrades in staging environment first.
You have a separate Kubernetes cluster for operations that runs your monitoring and logging setup, CI pipeline, etc.
You want to monitor all environments/clusters with a single Prometheus instance located in the operations cluster.

Writing, modifying and maintaining the [prometheus.yml](https://github.com/prometheus/prometheus/blob/master/documentation/examples/prometheus-kubernetes.yml) for one Kubernetes cluster by hand is tedious and error prone. Doing so for multiple clusters that should share most of the configuration except for specific rules can become a nightmare.

promgen-k8s aims to provide a toolkit allowing you to easily generate a prometheus.yml tailored for monitoring multiple Kubernetes clusters with invididual scraping jobs and relabeling rules per cluster.

## Current State

promgen-k8s is currently in a very early state where it manages to generate the example  [prometheus-kubernetes.yml](https://github.com/prometheus/prometheus/blob/master/documentation/examples/prometheus-kubernetes.yml) for multiple clusters using [autodiscovery](https://prometheus.io/docs/operating/configuration/#%3Ckubernetes_sd_config%3E) including custom relabeling rules per cluster. It assumes that it can reach all Kubernetes apiservers under predictable DNS names using the provided secret files for authentication.

For pod, service and service endpoint monitoring in remote clusters promgen-k8s requires a proxy in each remote cluster as bastion since Kubernetes uses overlay networks with virtual addresses that are not reachable from outside of a cluster. The proxy can be a simple [Nginx](http://nginx.org) pod that forwards all incoming requests like `http://proxy/10.0.0.1:8080/metrics` to `http://10.0.0.1:8080/metrics` in its local cluster and is accessible e.g. through a load balancer. As services are checked using the blackbox-exporter promgen-k8s also assumes a `blackbox-exporter` pod running co-located to the Prometheus in the operations cluster.

promgen-k8s is successfully used with Kubernetes clusters on [AWS](http://aws.amazon.com/) created by [kops](https://github.com/kubernetes/kops).

## Example

The [example](example-generator.py) uses a [stub file](example-prometheus-stub.yml) for manual configuration and requires [pyyaml](http://pyyaml.org/) to be installed.

## Related

- [https://github.com/line/promgen]([https://github.com/line/promgen])

## License

promgen-k8s is licensed under the Apache License, Version 2.0. See LICENSE for more information.
