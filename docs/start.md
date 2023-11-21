---
layout: default
title: Quick Start
nav_order: 1
---

## Update Kubernetes Manifest

### Service Monitor

In Prometheus, an open-source monitoring and alerting toolkit, used in Kubernetes environments, a "Service Monitor" is a specific resource type in the Prometheus Operator. The Prometheus Operator simplifies the deployment and configuration of Prometheus monitoring instances.

A Service Monitor is used to define how Prometheus should discover and scrape metrics from a set of services within a Kubernetes cluster. The service monitor is deployed with project to get feedback from the FastAPI web application. For the service monitor to be able to connect to the Prometheus deployment in Kubernetes we have to update the ```devspace-deployment/manifest/service_monitor.yaml``` file with the correct label that is defined by Prometheus deployment.

To find the label, query for the prometheus resource.

```zsh
kubectl get prometheus -A
```

If prometheus is install the command will return the name of the deployment and namespace. We would use both to get the description of the deployment.

```
kubectl describe prometheus -n monitoring 
```

or

```
kubectl get prometheus -n monitoring -o yaml
```

Checking the result we can see in our case under the serviceMonitorSelector we have

```yaml
serviceMonitorSelector:
      matchLabels:
        release: dev-tekstack-monitoring-kube-prom-stack
```

Update the service_monitor.yaml and to the labels add

```yaml
release: dev-tekstack-monitoring-kube-prom-stack
```
