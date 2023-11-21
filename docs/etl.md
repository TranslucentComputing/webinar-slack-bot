---
layout: default
title: Redis ETL Job
nav_order: 7
nav_exclude: false
---

Most of the systems and applications have a state. To demonstrate how we can manage the state in an application we added Redis database to store data that the Slack Bot can access during the user interactions.

## Redis Deployment

The Redis database is deployed with devspace. We customize and build the image with devspace and we deploy Bitnami Kubernetes assets from the Bitnami Redis <a href="https://artifacthub.io/packages/helm/bitnami/redis" target="_blank">Helm Chart</a>.

## ETL

The ETL, extract/transform/load or extract/load/transform, is part of the development process. There are many powerful and versatile tools designed to provided a full ETL process. Such, tools are amazing and might not be suitable for you day-to-day development needs.

We have added a basic ETL job that can be executed quickly within the Kubernetes cluster with DevSpace and provided the data need for you development.

In the `elt` folder we have a simple script that executes Python job. In the `etl/data` we have several CSV files. These files are from HubSpot and contain popular quotes.

Once the `devspace dev` command has been executed and you are within the dev container, you can cd to the `elt` folder and execute the make command

```zsh
make indexer_job 
```

The code for the job is in the `src/jobs/redis_job.py` folder.

## Application

The Redis database is used by the Slack Bot in response to user feedback. The interactions proxied to the web applications allow us to provide a response to them. As a simple example of business logic we query Redis search index and randomly select a quote.
