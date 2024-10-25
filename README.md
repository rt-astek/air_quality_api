# Air Quality API

## Description
This is a RESTful API for managing air quality data focused on PM2.5 levels.

## Prepare data

Download the data and upload inside the app/data directory and for all the files use the name air_quality_data with their corresponding extension.

## Docker Setup

docker build -t air_quality_api .
docker run -d -p 5000:5000 --name air_quality_api air_quality_api

## Initial run
Run the path with data/csv to create the CSV file that only will have the required data lat, lon, year and GWRPM25

## Swagger specs
http://localhost:5000/docs
