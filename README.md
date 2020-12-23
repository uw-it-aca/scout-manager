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

    $ git clone https://github.com/uw-it-aca/scout-manager.git

Navigate to the develop branch and copy the sample environment variables into your own `.env` file:

    $ cd scout-manager
    $ git checkout develop
    $ cp sample.env .env

Then, run the following command to build your docker container:

    $ docker-compose up --build

You should see the server running at http://localhost:8000 (or at the port set in your `.env` file)

## Development ##

### Running the app with Docker ###

To rebuild the docker container from scratch, run:

    $ docker-compose up --build

Otherwise, just run:

    $ docker-compose up


### Running the app against a live spotseeker server ###

In your `.env` file, uncomment the following lines:

    RESTCLIENTS_SPOTSEEKER_HOST = ''
    SPOTSEEKER_OAUTH_KEY ''
    SPOTSEEKER_OAUTH_SECRET = ''
    RESTCLIENTS_SPOTSEEKER_DAO_CLASS = 'spotseeker_restclient.dao_implementation.spotseeker.Live'
    OAUTH_USER = 'javerage'

You will need to make sure you have a valid oauth secret/key in order to run scout agains a live api. Make sure Spotseeker is running and set the url to `RESTCLIENTS_SPOTSEEKER_HOST`.