# syntax=docker/dockerfile:1

# Dockerfile to add support for Redis Stack modules.
# Author: Patryk Golabek
# Copyright: Translucent Computing Inc. 2023

ARG REDISJSON_VERSION
ARG REDISEARCH_VERSION

FROM redisfab/rejson:${REDISJSON_VERSION}-x64-bullseye AS json
FROM redisfab/redisearch:${REDISEARCH_VERSION}-x64-bullseye AS search
FROM bitnami/redis:7.2.2

# Copy the RedisJSON and Redisearch libraries
COPY --from=json    /usr/lib/redis/modules/rejson.so* "/usr/lib/redis/modules/"
COPY --from=search  /usr/lib/redis/modules/redisearch.so* "/usr/lib/redis/modules/"
