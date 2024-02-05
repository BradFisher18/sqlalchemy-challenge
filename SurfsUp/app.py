# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
#I have decided to open and close each session within each route

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#1. Welcome page route with a description of routes, including the format for the date input
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available routes:<br/>"
        f"<br/>"
        f"Precipitation data: /api/v1.0/precipitation<br/>"
        f"Station data: /api/v1.0/stations<br/>"
        f"Temperature data: api/v1.0/tobs<br/>"
        f"<br/>"
        f"For the below date inputs, please structure the date as YYYY-MM-DD:<br/>"
        f"To find the temperature data from a specified start date to present: <br/>/api/v1.0/start_date_temp_data/date<date><br/>"
        f"To find the temperature data for a specified date range: <br/> /api/v1.0/start_end_date_temp_data/start_date<start_date>/end_date<end_date><br/>"
    )

#############################################
#2. precipitation analysis
#############################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    #open session
    session = Session(engine)

    #query recent date
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #find out date of a year ago
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    #query prcp data from the last year using date queried above
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date.desc()).all()

    #close session
    session.close()

    #create list to store dictionary
    all_prcp = []
    
    for date, prcp in prcp_data:
        #store looped date and prcp into a dictionary
        precip_dict = {date:prcp}
        #append the dictionary into the list
        all_prcp.append(precip_dict)
    
    #jsonify the list
    return jsonify(all_prcp)

#############################################
#3. Stations list
#############################################
@app.route("/api/v1.0/stations")
def stations():
    #open session
    session = Session(engine)
    
    #query stations in Station table
    stn = session.query(Station.station).all()
    
    #close session
    session.close()
    
    #convert query to list
    stn_list = list(np.ravel(stn))
    
    #show station list as json
    return jsonify(stn_list)

#############################################
#4. Temperature observations
#############################################
@app.route("/api/v1.0/tobs")
def tobs():
    #open session
    session = Session(engine)

    #query date year ago
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    #define count variable for ease in queries below
    count = func.count(Measurement.station)

    #query count of each station
    station_count = session.query(Measurement.station, count).\
    group_by(Measurement.station).\
    order_by((count).desc()).\
    all()

    #select most active station i.e. first value in above query
    most_active_station = station_count[0][0]
    
    #define temperature column for ease of use below
    temp_column = func.round(Measurement.tobs,0)

    #query the date and related temperature for most active station in the last year, ordered by date
    temp_data = session.query(Measurement.date, temp_column).\
    filter(Measurement.date >= year_ago, Measurement.station == most_active_station).\
    order_by(Measurement.date).all()

    #close session
    session.close()

    #create list to store date and temperature
    all_tobs = []
    #loop through query
    for date, temp_column in temp_data:
       #create dictionary to store data
       tobs_dict = {date:temp_column}
        #tobs_dict["date"] = date
        #tobs_dict['tobs'] = temp_column
        #append the list with the dict
       all_tobs.append(tobs_dict)

    #show result as json
    return jsonify(all_tobs)

#############################################
#5.1 Temperatuire stats with dynamic start date
#############################################
@app.route("/api/v1.0/start_date_temp_data/<date>")
def temp_data_by_date(date):
    #start session
    session = Session(engine)
       
    #lowest temp
    lowest_temp = \
    session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= date).all()

    #highest temp
    highest_temp = \
    session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= date).all()

    #average temp
    ave_temp = \
    session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= date).all()

    #close session
    session.close()

    #convert queries to lists
    min_list = list(np.ravel(lowest_temp))
    max_list = list(np.ravel(highest_temp))
    ave_list = list(np.ravel(ave_temp))
    
    #print results as json
    return jsonify(f"Min: {min_list}, Max: {max_list}, Average: {ave_list}")

#############################################
#5.2 Temperature stats with dynamis start and end date
#############################################
@app.route("/api/v1.0/start_end_date_temp_data/<start_date>/<end_date>")
def start_end_date_temp_data(start_date, end_date):
    #start session
    session = Session(engine)
       
    #lowest temp
    lowest_temp = \
    session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    #highest temp
    highest_temp = \
    session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    #average temp
    ave_temp = \
    session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    #close session
    session.close()

    #store stats in list
    min_list = list(np.ravel(lowest_temp))
    max_list = list(np.ravel(highest_temp))
    ave_list = list(np.ravel(ave_temp))
    
    #print results as json
    return jsonify(f"Min: {min_list}, Max: {max_list}, Average: {ave_list}")




if __name__ == '__main__':
    app.run(debug=True)