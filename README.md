[![Build Status](https://github.com/uw-it-aca/scout-manager/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=master)](https://github.com/uw-it-aca/scout-manager/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/scout-manager/badge.svg?branch=master)](https://coveralls.io/github/uw-it-aca/scout-manager?branch=master)

SCOUT MANAGER
=============

This README documents whatever steps are necessary to get your application up and running.

## Installing the application ##

### Prerequisites ###
To run the app, you must have the following installed:
* Docker
* Docker-compose

### Steps to run ###
First, clone the app:

```
git clone https://github.com/uw-it-aca/scout-manager.git
```

If you wish to change the default settings, navigate to the develop branch and copy the sample environment variables into your own `.env` file:

```
cd scout-manager
git checkout develop
cp sample.env .env
```

Then, run the following command to build your docker container:

```
docker-compose up --build
```

You should see the server running at http://localhost:8000 (or at the port set in your `.env` file)

## Development ##

### Running the app with Docker ###

To rebuild the docker container from scratch, run:

```
docker-compose up --build
```

Otherwise, just run:

```
docker-compose up
```

### Running Unit Tests with Docker

```
docker-compose run --rm app bin/python manage.py test
```


### Running the app against a Live Spotseeker Server ###

To find more information on how to run scout against a Live Spotseeker server using the 'all_ok' Auth Module, check [here](https://github.com/uw-it-aca/spotseeker_server/wiki/Using-'all_ok'-oauth-module)


To find more information on how to run scout against a Live Spotseeker server using the 'oauth' Auth Module, check [here](https://github.com/uw-it-aca/spotseeker_server/wiki/Using-OAuth)

## Built With

* [Django](http://djangoproject.com/)
