[![Build Status](https://github.com/uw-it-aca/scout-manager/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=master)](https://github.com/uw-it-aca/scout-manager/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/scout-manager/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/scout-manager?branch=main)

# Scout Manager

## Installing the application

### Prerequisites
To run the app, you must have the following installed:
* Docker
* Docker-compose

### Steps to run
First, clone the app:

```bash
git clone https://github.com/uw-it-aca/scout-manager.git
```

If you wish to change the default settings, navigate to the develop branch and copy the sample environment variables into your own `.env` file:

```bash
cd scout-manager
git checkout develop
cp sample.env .env
```

Then, run the following command to build your docker container:

```bash
docker-compose up --build
```

You should see the server running at http://localhost:8000 (or at the port set in your `.env` file)

## Development

### Running the app with Docker

To rebuild the docker container from scratch, run:

```bash
docker-compose up --build
```

Otherwise, just run:

```bash
docker-compose up
```

### Running Unit Tests with Docker

```bash
docker exec -ti scout-manager bin/python manage.py test
```

### Running the app against a Live Spotseeker Server

### Setting up the correct environment variables

Settings `RESTCLIENTS_SPOTSEEKER_DAO_CLASS` to `Mock` will allow you to run the app without connecting to a live Spotseeker server. This is useful for testing and development. However, if you want to properly test the app against a live Spotseeker server, you will need to set up the following environment variables:

```bash
RESTCLIENTS_SPOTSEEKER_DAO_CLASS=Live
RESTCLIENTS_SPOTSEEKER_HOST=[your spotseeker server url]

SPOTSEEKER_OAUTH_CREDENTIAL=[your spotseeker server oauth credential]
```

You must go to your live spotseeker server instance to get the oauth credential. In spotseeker server, run the following command:

```bash
docker exec -ti spotseeker-server bin/python manage.py register_application [-s/--show-credential]
```

You will be prompted for an app name. The default name for this app is `scout-manager`. You can change this name by setting the `APP_NAME` environment variable. The command will give you a credential. Copy and paste this credential into the `SPOTSEEKER_OAUTH_CREDENTIAL` environment variable and you should be good to go.

It is recommended that you keep the scope to "read write" as that is what scout manager is designed for.

## Built With

* [Django](http://djangoproject.com/)

## List of settings

GOOGLE_MAPS_API

OAUTH_USER

DEBUG_CACHING
- If set to True, will use a real cache even while in DEBUG=True. This is useful for testing.

RESTCLIENTS_SPOTSEEKER_DAO_CLASS

RESTCLIENTS_SPOTSEEKER_HOST

SPOTSEEKER_OAUTH_CREDENTIAL

SPOTSEEKER_OAUTH_SCOPE

APP_NAME
