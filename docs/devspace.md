---
layout: default
title: DevSpace
nav_exclude: true
---

## DevSpace

DevSpace is a developer tool that simplifies the development and deployment processes for Kubernetes. It is designed to streamline the workflow of building, testing, and deploying applications in Kubernetes environments. By providing an efficient and straightforward interface, DevSpace allows developers to focus more on writing code and less on the complexities of Kubernetes configuration and management.

*[Install link](https://www.devspace.sh/docs/getting-started/installation)*.

### DevSpace Configuration

`devspace.yaml` is a file that is used to customize and configure the development environment.

### Configure Kube Context

Set the context with the new namespace

```
kubectl config use-context your-context
kubectl create namespace webinar
kubectl config set-context your-context --namespace=webinar
```

We are adding global parameters to each command to make sure we are using the correct kube cluster and namespace.

```zsh
--kube-context=your-context --namespace=webinar
```

For Dev

```zsh
devspace dev --your-context --namespace=webinar
```

For Build

```zsh
devspace build --your-context 
```

For Deployment

```zsh
devspace build -b slack-bot-server --kube-context=your-context --namespace=webinar && devspace deploy --kube-context=your-context --namespace=webinar
```
