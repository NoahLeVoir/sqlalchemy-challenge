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






# Must have at end of flask
if __name__ == '__main__':
    app.run(debug = True)