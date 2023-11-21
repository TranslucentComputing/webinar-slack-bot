---
layout: default
title: DevSpace
nav_order: 4
---

## DevSpace

DevSpace is a developer tool that simplifies the development and deployment processes for Kubernetes. It is designed to streamline the workflow of building, testing, and deploying applications in Kubernetes environments. By providing an efficient and straightforward interface, DevSpace allows developers to focus more on writing code and less on the complexities of Kubernetes configuration and management.

*[Install link](https://www.devspace.sh/docs/getting-started/installation)*.

### DevSpace Configuration

`devspace.yaml` is a file that is used to customize and configure the development environment.

In our Slack Bot DevSpace we have five major section where we define DevSpace configuration for this project. Which are:

- Variables (vars): This section declares environment variables for image names, sourcing them from the environment variables that are read from the `.env.devspace` file.

- Pipelines: It defines two pipelines - dev and deploy. We customize the deployment by patching the images in the Kubernetes deployment YAMLs. This is mostly done for this public deployment since we do not want to hardcode image names in the YAMLs.

- Images: This section details how different images will be built. We customize the build engine and the build strategy. We only want to build when we execute the build command explicitly. Additionally we use BuildKit as the container build engine. BuildKit provides optimization features that allows to build all the images concurrently much faster. Additionally, we do have a specific image for devspace dev. Having different images for dev and build allows us to customize the container for either engagement.

- Deployments: Outlines the deployment configuration for Kubernetes. It includes Kubernetes manifest files and patches to modify the deployment, particularly concerning the images used for the Slack bot server and Redis master. Both of these images when build locally generate a tag. By patching both images we can use the lates tag with the image name.

- Development (dev) Section: Defines the development environment for the slack-bot-server. It includes settings for selecting the pod, replacing the container image with a development-optimized image, syncing files between the local system and the development container, terminal setup, SSH server injection, proxy commands, and port forwarding.

### DevSpace Commands

Before you start using DevSpace you have to configure you Kubernetes context. A Kubernetes context is a set of access parameters for a Kubernetes cluster. It's a part of the Kubernetes configuration file (`kubeconfig`) and serves as a way to quickly switch between different clusters and namespaces within those clusters.

For cloud cluster you will have to configure the secure access to the cluster. Update the kubeconfig with cloud cluster credentials. Example for GKE

```zsh
gcloud container clusters get-credentials <cluster_name> --zone northamerica-northeast1-a --project <project_name>
```

Once the access to the cluster has been configure, view the config.

```zsh
kubectl config view
```

Choose the context name for you specific cluster and set the context with the new namespace.

```zsh
kubectl config use-context your-context
kubectl create namespace webinar
kubectl config set-context your-context --namespace=webinar
```

We are adding global parameters to each command to make sure we are using the correct (a bit paranoid) Kubernetes cluster and namespace.

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
