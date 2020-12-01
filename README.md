# CSVS ENSO Server

## Introduction

This application provides an user interface through a REST API to serve Multivariate ENSO Index Version 2 (MEI.v2) data 
in CSV format.

The values are provided from https://www.psl.noaa.gov/enso/mei/

It provides two simple entry points:

### Update ENSO values

Updates the database with the new values. The data in the mentioned site is updated automatically every 10th of each 
month.

The link to the data is given as an environment variable (see `docker-compose.yml`) in case this url is migrated in the
future.

### Get ENSO values

It returns a CSV file containing the Time and MEI.v2 values as columns.


## Deployment

Follow the Makefile file for instructions or:

Deploy the app using docker compose

```docker
docker-compose up -d app
```

Open http://localhost:8000/docs
