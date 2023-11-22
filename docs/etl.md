---
layout: default
title: Redis ETL Job
nav_order: 8
nav_exclude: false
---

# Redis ETL Job

Most of the systems and applications have a state. To demonstrate how we can manage the state in an application we added a Redis database to the project to store data that the Slack Bot can access during the user interactions.

## Redis Deployment

The Redis database is deployed with devspace. We customize and build the image with devspace, and we deploy Bitnami Kubernetes assets from the Bitnami Redis <a href="https://artifacthub.io/packages/helm/bitnami/redis" target="_blank">Helm Chart</a>.

## ETL

The ETL, extract/transform/load or extract/load/transform, is part of the development process. There are many powerful and versatile tools designed to provide a full ETL process. These tools are amazing, however might not always be suitable for your day-to-day development needs.

We have added a basic ETL job that can be executed quickly within the Kubernetes cluster using DevSpace and provided the data needed for your development.

In the `etl` folder we have a simple script that executes Python job. In the `etl/data` we have several CSV files. These files are from HubSpot and contain popular quotes.

Once the `devspace dev` command has been executed and you are within the dev container, you can cd to the `etl` folder and execute the make command.

```zsh
make indexer_job 
```

The code for the job is in the `src/jobs/redis_job.py` file.

## Application

The Redis database is used by the Slack Bot in response to user feedback. The interactions proxied to the web applications allow us to provide a response to them. As a simple example of business logic, we query the Redis search index and randomly select a quote.
