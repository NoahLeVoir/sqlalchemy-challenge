# Import based on previous climate analysis
import numpy as np
import datetime as dt

# Import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup (Same as before)
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect = True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Route creation
# Home Route
@app.route("/")
def welcome():
    return """<html>
    <h1>Hawaii Climate App (Flask API)</h1>
        <p>Precipitation Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
            </ul>
        <p>Station Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
            </ul>
        <p>Temperature Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
            </ul>
        <p>Start Day Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
            </ul>
        <p>Start & End Day Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
            </ul>
    </html>
    """

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        precip_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
        
        # Convert into a Dictionary
        precip_data_list = dict(precip_data)
        
        # Return JSON Representation of Dictionary
        return jsonify(precip_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON List of Stations From the Dataset
        all_stations = session.query(Station.station, Station.name).all()
        
        # Convert List
        station_list = list(all_stations)
        
        # Return JSON List
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point for the most active station
        # I know the previous year date from the climate analysis section done beforehand
        previous_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
       
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        # I know that "USC00519281" is the most active station ID from the climate anylsis done beforehand
        tobs_data = session.query(Measurement.date, Measurement.tobs, Measurement.station == "USC00519281").\
                filter(Measurement.date >= previous_year).\
                order_by(Measurement.date).all()
        
        # Convert List
        tobs_data_list = list(tobs_data)
        
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        # Find the start days min, max, and average
        starting_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        
        # Convert List
        start_day_list = list(starting_day)
        
        # Return JSON List of min temp, avg temp and max temp
        return jsonify(start_day_list)

# Start to End Route
@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start, end):
        # Find the start days min, max, and average
        starting_to_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        
        # Convert List
        start_to_end_list = list(starting_to_end)
        
        # Return JSON List of min temp, avg temp and max temp
        return jsonify(start_to_end_list)



# Must have at end of flask
if __name__ == '__main__':
    app.run(debug = True)