---
layout: default
title: Before Dev or Deployment
nav_order: 2
nav_exclude: false
---

Several project resources must be customized for your development and deployment.

## Update Kubernetes Manifest

Kubernetes manifest refers to the YAML or JSON file that describes how an application or service should be deployed and managed within a Kubernetes cluster. These manifests are crucial for defining the desired state of your application in the Kubernetes environment.

### Ingress

In Kubernetes, an Ingress resource is a flexible tool that manages external access to services within a cluster. It provides HTTP and HTTPS routing to services based on defined rules.

Ingress is an entry point for your cluster's network, enabling external traffic to reach the correct services within your Kubernetes cluster. It allows you to expose multiple services under a single IP address, with traffic routing based on the request's host or path.

Since the Slack system requires a public domain, we are deploying an Ingress resource that must be customized before deployment. The file to update is `devspace-deployment/kube-proxy/ingress.yaml`

### Replace the Hostname

Locate the line under annotations:

```yaml
external-dns.alpha.kubernetes.io/hostname: <your-domain-name>
```

External DNS is used to manage the Cloud DNS entries. It creates a DNS record for the domain name.

Update Host in Rules and TLS:

```yaml
- host: <your-domain-name>
```

And in the TLS section:

```yaml
- hosts:
    - <your-domain-name>
```

### Adjust the Certificate Manager Annotation

```yaml
cert-manager.io/cluster-issuer: <your-cluster-issuer>
```

The cert-manager is used to provision the Lets Encrypt TLS certificates.

To find the name of the cluster issuer installed within your cluster, list all the cluster issuers:

```zsh
kubectl get clusterissuer
```

The result from the command is a list of the names of different cluster issuers available within your cluster. Choose one and update the ingress.yaml.

To get some more feedback about specific cluster issuer, execute:

```zsh
kubectl describe clusterissuer [name-of-clusterissuer]
```

### Service Monitor

In Prometheus, an open-source monitoring and alerting toolkit used in Kubernetes environments, a "Service Monitor" is a specific resource type in the Prometheus Operator. The Prometheus Operator simplifies the deployment and configuration of Prometheus monitoring instances.

A Service Monitor is used to define how Prometheus should discover and scrape metrics from a set of services within a Kubernetes cluster. The service monitor is deployed with project to get feedback from the FastAPI web application. For the service monitor to be able to connect to the Prometheus deployment in Kubernetes we have to update the ```devspace-deployment/manifest/service_monitor.yaml``` file with the correct label that is defined by Prometheus deployment.

To find the label, query for the Prometheus resource.

```zsh
kubectl get prometheus -A
```

If Prometheus is installed the command will return the deployment name and namespace. We would use both to get the description of the deployment.

```zsh
kubectl describe prometheus -n monitoring 
```

or

```zsh
kubectl get prometheus -n monitoring -o yaml
```

The result shows that in our case, under the serviceMonitorSelector we have:

```yaml
serviceMonitorSelector:
      matchLabels:
        release: dev-tekstack-monitoring-kube-prom-stack
```

Update the service_monitor.yaml and add to the labels:

```yaml
release: dev-tekstack-monitoring-kube-prom-stack
```

## Update DevSpace Images

DevSpace is used to build images for the required containers that are deployed. In DevSpace, an image typically refers to a Docker image. This lightweight, standalone, executable package includes everything needed to run a piece of software, including the code, a runtime, libraries, environment variables, and config files. By containerizing applications into images, DevSpace enables consistent, reliable, and portable software deployments.

To make it easier to update the image for your specific image repository the image names have to be externalized into the ```.env.devspace``` file. There is a template file ```.env.devspace_bak``` that has the variables that are expected be used in the devspace.yaml file.

Create the ```.env.devspace``` file with full image names.

`IMAGE=` This is the main Docker image for your application. It is used with `devspace deploy`.

`IMAGE_DEV=` This Docker image is specifically tailored for development purposes. It is used with `devspace dev`.

`IMAGE_REDIS_STACK=` This image is for a Redis deployment.

Since we are using the Google Container Registry(GCR), our file would look something like:

```zsh
IMAGE=gcr.io/<project_name>/webinar/slackbot/slack-bot-server
IMAGE_DEV=gcr.io/<project_name>/webinar/slackbot/slack-bot-server-devspace
IMAGE_REDIS_STACK=gcr.io/<project_name>/webinar/slackbot/redis-stack
```

We store all the images under the same folder `webinar`.

Since DevSpace will automatically build and push these images to your repository you should have and configure access to the repository.

## Update Slack credentials

To access the Slack server with the Slack Bot, we must provide the Slack credentials. The credentials are located in the `.env` file. We also provided a template `.env_bak` file as an example.

Create the `.env` file and update:

```zsh
# SLACK_BOT_TOKEN is used to authenticate your bot with the Slack API.
SLACK_BOT_TOKEN=add_me

# SLACK_SIGNING_SECRET is used to verify incoming requests from Slack.
SLACK_SIGNING_SECRET=add_me
```

Slack configuration can be found [here](slack.html).
