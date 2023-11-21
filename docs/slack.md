---
layout: default
title: Slack Configuration
nav_order: 5
---

Since we are using Slack to build the bot, we have to configure Slack App. To initiate the Slack app creation follow this link [create app](https://api.slack.com/apps?new_app=1)

You will be presented with:
![create app](assets/img/slack_create_app.png)

Let's create the app "From scratch", Next:

![app name](assets/img/slack_app_name.png)

Choose the Slack app name and the Slack workspace where you will access the app during development.

## Basic Information

Once the app has been created in the "Basic Information" section you will find the "App Credentials". We use these credentials with the Slack Bot and we defined them in `.env` file. More info [Here](start.md)

We also have the options to customize the look and feel of the Slack app in the "Display Information" section.

![app name](assets/img/slack_display.png)

## OAuth and Permissions

Here we configure the permissions for the Slack Bot. Under the "Scopes" in the "Bot Token Scopes" add the required scopes.

For this application we give the Bot "app_mentions:read" and "chat:write" permissions.

![app scopes](assets/img/slack_scopes.png)

Once the scopes have been added the "Bot User OAuth Token" will be available in this section, it does required reinstalling the app. The reinstalling the app will simply refresh the app in the Slack workspace. The Bot Token should be added to the `.env` file.

## Slack Events

The configuration of Slack events has be configured after the `.env` file has been update the application has been deployed with DevSpace. [Here](app_dev.html)

In the "Events Subscriptions" we want to enable the events, configure the request URL and bot events subscription.

The URL is the public URL that is configured in the Ingress YAML. [Here](start.md)

![app events](assets/img/slack_events.png)

## Slack Interactions

To allow for two-way communication, we enable Slack interactivity feature. Since we required the Slack Bot applicaiton to be running for the request URL, the application has to be deployed with DevSpace [Here](app_dev.html).

![app interactions](assets/img/slack_interactions.png)
