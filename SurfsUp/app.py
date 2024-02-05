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
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date_temp_data/<date><br/>"
        f"/api/v1.0/start_end_date_temp_data/<start_date>/<end_date><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
    order_by(Measurement.date.desc()).all()

    session.close()

    all_prcp = []
    for date, prcp in prcp_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_prcp.append(precip_dict)
    

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stn = session.query(Station.station).all()

    stn_list = list(np.ravel(stn))

    return jsonify(stn_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    count = func.count(Measurement.station)
    station_count = session.query(Measurement.station, count).\
    group_by(Measurement.station).\
    order_by((count).desc()).\
    all()

    most_active_station = station_count[0][0]

    temp_column = func.round(Measurement.tobs,0)
    temp_data = session.query(Measurement.date, temp_column).\
    filter(Measurement.date >= year_ago, Measurement.station == most_active_station).\
    order_by(Measurement.date).all()

    session.close()

    all_tobs = []
    for date, temp_column in temp_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict['tobs'] = temp_column
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start_date_temp_data/<date>")
def temp_data_by_date(date):
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

    session.close()

    min_list = list(np.ravel(lowest_temp))
    max_list = list(np.ravel(highest_temp))
    ave_list = list(np.ravel(ave_temp))
    

    return jsonify(min_list, max_list, ave_list)

@app.route("/api/v1.0/start_end_date_temp_data/<start_date>/<end_date>")
def start_end_date_temp_data(start_date, end_date):
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

    session.close()

    min_list = list(np.ravel(lowest_temp))
    max_list = list(np.ravel(highest_temp))
    ave_list = list(np.ravel(ave_temp))
    

    return jsonify(min_list, max_list, ave_list)

if __name__ == '__main__':
    app.run(debug=True)