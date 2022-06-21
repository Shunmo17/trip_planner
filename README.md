# Trip Planner
## Description
Optimize route for your trip with Google Map API

## Preparation
You need additional two files. We show examples of them.

### config.yaml
```
google_map:
  api_key: YOUR_API_KEY
  api_url:
    distance_matrix: https://maps.googleapis.com/maps/api/distancematrix/json
    geocodeing: https://maps.googleapis.com/maps/api/geocode/json

```
`YOUR_API_KEY`is your api key for google map api. Please get it from [HERE](https://developers.google.com/maps/documentation/javascript/).

### location.csv
```
name,day,address,latitude,longitude
LOCATION_NAME,DAY_NUMBER,LOCATION_ADDRESS,,
```
Both latitude and longitude are automatically set with geocode api.
What you have to set are only location name, address, and day.
The day is when you visit the location.

## Parameters
You can set some parameters on `modules/params.py`. Please set the number of trip days here.

## Output
The planning result will be shown in your terminal. In addition, the data got with Google Map API, such as distance between locations, are saved as pkl file. 

## Maintainer
[Shunmo17](https://github.com/Shunmo17)
