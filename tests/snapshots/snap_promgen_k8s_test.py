# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestPromgenK8s::test_generate 1'] = '''---
global:
  evaluation_interval: 1m
  scrape_interval: 1m
rule_files:
  - /etc/alert.rules
scrape_configs:
  - bearer_token_file: /var/run/kube_secrets/staging_bearer_token
    job_name: staging-kubernetes-nodes
    kubernetes_sd_configs:
      - api_server: api.internal.staging.example.com
        bearer_token_file: /var/run/kube_secrets/staging_bearer_token
        role: node
        tls_config:
          ca_file: /var/run/kube_secrets/staging_ca_crt
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_node
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_master
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.staging.example.com:443
        target_label: __address__
      - action: replace
        regex: (.+)
        replacement: /api/v1/nodes/${1}/proxy/metrics
        source_labels:
          - __meta_kubernetes_node_name
        target_label: __metrics_path__
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/staging_ca_crt
  - bearer_token_file: /var/run/kube_secrets/staging_bearer_token
    job_name: staging-kubernetes-ingresses
    kubernetes_sd_configs:
      - api_server: api.internal.staging.example.com
        bearer_token_file: /var/run/kube_secrets/staging_bearer_token
        role: ingress
        tls_config:
          ca_file: /var/run/kube_secrets/staging_ca_crt
    metric_relabel_configs: []
    metrics_path: /api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe
    params:
      module:
        - http_2xx
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_ingress_annotation_prometheus_io_probe
      - action: replace
        regex: (.+);(.+)
        replacement: ${1}${2}
        source_labels:
          - __address__
          - __meta_kubernetes_ingress_path
        target_label: __address__
      - action: replace
        source_labels:
          - __address__
        target_label: __param_target
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.staging.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_ingress_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_ingress_name
        target_label: kubernetes_ingress_name
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/staging_ca_crt
  - bearer_token_file: /var/run/kube_secrets/staging_bearer_token
    job_name: staging-kubernetes-cadvisor
    kubernetes_sd_configs:
      - api_server: api.internal.staging.example.com
        bearer_token_file: /var/run/kube_secrets/staging_bearer_token
        role: node
        tls_config:
          ca_file: /var/run/kube_secrets/staging_ca_crt
    metric_relabel_configs:
      - action: replace
        regex: ^/machine\\.slice/machine-rkt\\\\x2d([^\\\\]+)\\\\.+/([^/]+)\\.service$
        replacement: ${2}-${1}
        source_labels:
          - id
        target_label: rkt_container_name
      - action: replace
        regex: ^/system\\.slice/(.+)\\.service$
        replacement: ${1}
        source_labels:
          - id
        target_label: systemd_service_name
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_node
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_master
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.staging.example.com:443
        target_label: __address__
      - action: replace
        regex: (.+)
        replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
        source_labels:
          - __meta_kubernetes_node_name
        target_label: __metrics_path__
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/staging_ca_crt
  - bearer_token_file: /var/run/kube_secrets/staging_bearer_token
    job_name: staging-kubernetes-service-endpoints
    kubernetes_sd_configs:
      - api_server: api.internal.staging.example.com
        bearer_token_file: /var/run/kube_secrets/staging_bearer_token
        role: endpoints
        tls_config:
          ca_file: /var/run/kube_secrets/staging_ca_crt
    metric_relabel_configs: []
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_scrape
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        source_labels:
          - __address__
          - __meta_kubernetes_service_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_service_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.staging.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_service_name
        target_label: kubernetes_service_name
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/staging_ca_crt
  - bearer_token_file: /var/run/kube_secrets/staging_bearer_token
    job_name: staging-kubernetes-services
    kubernetes_sd_configs:
      - api_server: api.internal.staging.example.com
        bearer_token_file: /var/run/kube_secrets/staging_bearer_token
        role: service
        tls_config:
          ca_file: /var/run/kube_secrets/staging_ca_crt
    metric_relabel_configs: []
    metrics_path: /api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe
    params:
      module:
        - http_2xx
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_probe
      - action: replace
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_module
        target_label: __param_module
      - action: replace
        source_labels:
          - __address__
        target_label: __param_target
      - action: replace
        regex: (.+);(.+)
        replacement: $1$2
        separator: ;
        source_labels:
          - __param_target
          - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __param_target
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.staging.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_service_name
        target_label: kubernetes_service_name
      - action: replace
        regex: reverse.default.svc:443
        replacement: https_401
        source_labels:
          - __param_target
        target_label: __param_module
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/staging_ca_crt
  - bearer_token_file: /var/run/kube_secrets/staging_bearer_token
    job_name: staging-kubernetes-pods-default
    kubernetes_sd_configs:
      - api_server: api.internal.staging.example.com
        bearer_token_file: /var/run/kube_secrets/staging_bearer_token
        role: pod
        tls_config:
          ca_file: /var/run/kube_secrets/staging_ca_crt
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_scrape
      - action: drop
        regex: .+
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_interval
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        separator: ;
        source_labels:
          - __address__
          - __meta_kubernetes_pod_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_pod_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.staging.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_name
        target_label: kubernetes_pod_name
      - action: replace
        replacement: ''
        target_label: pod_template_hash
      - action: replace
        replacement: ''
        target_label: controller_revision_hash
      - action: replace
        replacement: ''
        target_label: pod_template_generation
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/staging_ca_crt
  - bearer_token_file: /var/run/kube_secrets/production_bearer_token
    job_name: production-kubernetes-nodes
    kubernetes_sd_configs:
      - api_server: api.internal.production.example.com
        bearer_token_file: /var/run/kube_secrets/production_bearer_token
        role: node
        tls_config:
          ca_file: /var/run/kube_secrets/production_ca_crt
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_node
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_master
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.production.example.com:443
        target_label: __address__
      - action: replace
        regex: (.+)
        replacement: /api/v1/nodes/${1}/proxy/metrics
        source_labels:
          - __meta_kubernetes_node_name
        target_label: __metrics_path__
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/production_ca_crt
  - bearer_token_file: /var/run/kube_secrets/production_bearer_token
    job_name: production-kubernetes-ingresses
    kubernetes_sd_configs:
      - api_server: api.internal.production.example.com
        bearer_token_file: /var/run/kube_secrets/production_bearer_token
        role: ingress
        tls_config:
          ca_file: /var/run/kube_secrets/production_ca_crt
    metric_relabel_configs: []
    metrics_path: /api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe
    params:
      module:
        - http_2xx
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_ingress_annotation_prometheus_io_probe
      - action: replace
        regex: (.+);(.+)
        replacement: ${1}${2}
        source_labels:
          - __address__
          - __meta_kubernetes_ingress_path
        target_label: __address__
      - action: replace
        source_labels:
          - __address__
        target_label: __param_target
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.production.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_ingress_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_ingress_name
        target_label: kubernetes_ingress_name
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/production_ca_crt
  - bearer_token_file: /var/run/kube_secrets/production_bearer_token
    job_name: production-kubernetes-cadvisor
    kubernetes_sd_configs:
      - api_server: api.internal.production.example.com
        bearer_token_file: /var/run/kube_secrets/production_bearer_token
        role: node
        tls_config:
          ca_file: /var/run/kube_secrets/production_ca_crt
    metric_relabel_configs:
      - action: replace
        regex: ^/machine\\.slice/machine-rkt\\\\x2d([^\\\\]+)\\\\.+/([^/]+)\\.service$
        replacement: ${2}-${1}
        source_labels:
          - id
        target_label: rkt_container_name
      - action: replace
        regex: ^/system\\.slice/(.+)\\.service$
        replacement: ${1}
        source_labels:
          - id
        target_label: systemd_service_name
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_node
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_master
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.production.example.com:443
        target_label: __address__
      - action: replace
        regex: (.+)
        replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
        source_labels:
          - __meta_kubernetes_node_name
        target_label: __metrics_path__
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/production_ca_crt
  - bearer_token_file: /var/run/kube_secrets/production_bearer_token
    job_name: production-kubernetes-service-endpoints
    kubernetes_sd_configs:
      - api_server: api.internal.production.example.com
        bearer_token_file: /var/run/kube_secrets/production_bearer_token
        role: endpoints
        tls_config:
          ca_file: /var/run/kube_secrets/production_ca_crt
    metric_relabel_configs: []
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_scrape
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        source_labels:
          - __address__
          - __meta_kubernetes_service_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_service_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.production.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_service_name
        target_label: kubernetes_service_name
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/production_ca_crt
  - bearer_token_file: /var/run/kube_secrets/production_bearer_token
    job_name: production-kubernetes-services
    kubernetes_sd_configs:
      - api_server: api.internal.production.example.com
        bearer_token_file: /var/run/kube_secrets/production_bearer_token
        role: service
        tls_config:
          ca_file: /var/run/kube_secrets/production_ca_crt
    metric_relabel_configs: []
    metrics_path: /api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe
    params:
      module:
        - http_2xx
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_probe
      - action: replace
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_module
        target_label: __param_module
      - action: replace
        source_labels:
          - __address__
        target_label: __param_target
      - action: replace
        regex: (.+);(.+)
        replacement: $1$2
        separator: ;
        source_labels:
          - __param_target
          - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __param_target
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.production.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_service_name
        target_label: kubernetes_service_name
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/production_ca_crt
  - bearer_token_file: /var/run/kube_secrets/production_bearer_token
    job_name: production-kubernetes-pods-default
    kubernetes_sd_configs:
      - api_server: api.internal.production.example.com
        bearer_token_file: /var/run/kube_secrets/production_bearer_token
        role: pod
        tls_config:
          ca_file: /var/run/kube_secrets/production_ca_crt
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_scrape
      - action: drop
        regex: .+
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_interval
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        separator: ;
        source_labels:
          - __address__
          - __meta_kubernetes_pod_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_pod_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: api.internal.production.example.com:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_name
        target_label: kubernetes_pod_name
      - action: replace
        replacement: ''
        target_label: pod_template_hash
      - action: replace
        replacement: ''
        target_label: controller_revision_hash
      - action: replace
        replacement: ''
        target_label: pod_template_generation
    scheme: https
    tls_config:
      ca_file: /var/run/kube_secrets/production_ca_crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-nodes
    kubernetes_sd_configs:
      - role: node
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_node
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_master
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: replace
        regex: (.+)
        replacement: /api/v1/nodes/${1}/proxy/metrics
        source_labels:
          - __meta_kubernetes_node_name
        target_label: __metrics_path__
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-ingresses
    kubernetes_sd_configs:
      - role: ingress
    metric_relabel_configs: []
    metrics_path: /api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe
    params:
      module:
        - http_2xx
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_ingress_annotation_prometheus_io_probe
      - action: replace
        regex: (.+);(.+)
        replacement: ${1}${2}
        source_labels:
          - __address__
          - __meta_kubernetes_ingress_path
        target_label: __address__
      - action: replace
        source_labels:
          - __address__
        target_label: __param_target
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_ingress_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_ingress_name
        target_label: kubernetes_ingress_name
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-cadvisor
    kubernetes_sd_configs:
      - role: node
    metric_relabel_configs:
      - action: replace
        regex: ^/machine\\.slice/machine-rkt\\\\x2d([^\\\\]+)\\\\.+/([^/]+)\\.service$
        replacement: ${2}-${1}
        source_labels:
          - id
        target_label: rkt_container_name
      - action: replace
        regex: ^/system\\.slice/(.+)\\.service$
        replacement: ${1}
        source_labels:
          - id
        target_label: systemd_service_name
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_node
      - action: replace
        replacement: ''
        target_label: __meta_kubernetes_node_label_node_role_kubernetes_io_master
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: replace
        regex: (.+)
        replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
        source_labels:
          - __meta_kubernetes_node_name
        target_label: __metrics_path__
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-service-endpoints
    kubernetes_sd_configs:
      - role: endpoints
    metric_relabel_configs: []
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_scrape
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        source_labels:
          - __address__
          - __meta_kubernetes_service_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_service_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_service_name
        target_label: kubernetes_service_name
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-services
    kubernetes_sd_configs:
      - role: service
    metric_relabel_configs: []
    metrics_path: /api/v1/namespaces/monitoring/services/blackbox-exporter/proxy/probe
    params:
      module:
        - http_2xx
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_probe
      - action: replace
        source_labels:
          - __meta_kubernetes_service_annotation_prometheus_io_module
        target_label: __param_module
      - action: replace
        source_labels:
          - __address__
        target_label: __param_target
      - action: replace
        regex: (.+);(.+)
        replacement: $1$2
        separator: ;
        source_labels:
          - __param_target
          - __meta_kubernetes_service_annotation_prometheus_io_path
        target_label: __param_target
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_service_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_service_name
        target_label: kubernetes_service_name
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-pods-default
    kubernetes_sd_configs:
      - role: pod
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_scrape
      - action: drop
        regex: .+
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_interval
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        separator: ;
        source_labels:
          - __address__
          - __meta_kubernetes_pod_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_pod_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_name
        target_label: kubernetes_pod_name
      - action: replace
        replacement: ''
        target_label: pod_template_hash
      - action: replace
        replacement: ''
        target_label: controller_revision_hash
      - action: replace
        replacement: ''
        target_label: pod_template_generation
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
  - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    job_name: operations-kubernetes-pods-long
    kubernetes_sd_configs:
      - role: pod
    metric_relabel_configs:
      - action: drop
        regex: go_.*
        source_labels:
          - __name__
    relabel_configs:
      - action: keep
        regex: true
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_scrape
      - action: keep
        regex: long
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_interval
      - action: replace
        regex: (.+)
        source_labels:
          - __meta_kubernetes_pod_annotation_prometheus_io_path
        target_label: __metrics_path__
      - action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        separator: ;
        source_labels:
          - __address__
          - __meta_kubernetes_pod_annotation_prometheus_io_port
        target_label: __address__
      - action: replace
        regex: (.+);(.+);(.+);(.+)
        replacement: /api/v1/namespaces/$1/pods/$2:$3/proxy$4
        separator: ;
        source_labels:
          - __meta_kubernetes_namespace
          - __meta_kubernetes_pod_name
          - __meta_kubernetes_pod_annotation_prometheus_io_port
          - __metrics_path__
        target_label: __metrics_path__
      - action: replace
        source_labels:
          - __address__
        target_label: instance
      - action: replace
        replacement: kubernetes.default.svc:443
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: kubernetes_namespace
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_name
        target_label: kubernetes_pod_name
      - action: replace
        replacement: ''
        target_label: pod_template_hash
      - action: replace
        replacement: ''
        target_label: controller_revision_hash
      - action: replace
        replacement: ''
        target_label: pod_template_generation
    scheme: https
    scrape_interval: 1h
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
'''
