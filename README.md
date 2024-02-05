# sqlalchemy-challenge
Repository for Module 10 Challenge
The purpose of this challenge is to practise using the SQLalchemy library and ORM's, using a provided database of various weather station records from Hawaii.

## Data
The data provided is weather information recorded from weather stations in Hawaii. This is provided across two SQL tables, 'Measurement' and 'Station', within 'hawaii.sqlite' which includes the below:
* station identifier
* station number
* date (of record)
* precipitation recorded
* temperature recorded
* station geographical information (latitude, longitude, elevation)

## Part 1 - Analyse and Explore Climate Data
This part is located within the Surfs Up directory, within the 'climate_starter.ipynb' file. In this file you will find the below analysis:
* date of the most recent record
* date a year previoous to most recent
* the precipitation values for the most recent 12 months of record with its associated date
* a plot of date vs precipitation using matplotlib
* statistical analysis of the precipitation data
* total number of stations
* count of records each station has recorded, and identifying the most sctive station
* the mean, max and min temperature of the most active station
* each temperature recorded at the most active station within the most recent year of data
* histograph representation of the temperature

## Part 2 - Design of Climate App
This section uses Python to create a Flask API, and the file is again located within the 'Surfs Up' directory, under the file name 'app.py'. This file contains the follwing code:
* Creation of a homepage, informing the user of the available routes
* Creation of a route containing a dictionary of the precipitation values and date, as a json
* Creation of a route that list all of the stations as a json
* Creation of a route to obtain temperature data for each date within the last year of recording of the most active station
* Creation of a route that displays the min, max and average temperature starting from a specified start date to current
* Similar to above, creation of a route with temperature stats with a specified start and end date
  
## Running
For this code to run successfully, python is required to be installed along with the pandas tool library and either Jupyter lab or Jupyter notebook. One method to install these programs is to download Anaconda - link below. To run this code, open the file within Jupyter, ensure that the input files are directed correctly and run! 
##
Anaconda install: https://docs.anaconda.com/free/anaconda/install/
