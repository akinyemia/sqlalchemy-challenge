import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify 

# Create connection to Hawaii.sqlite file
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# Base.prepare(autoload_with=engine)
Base.prepare(engine, reflect=True)
# print(Base.classes.keys())


# reflect the tables
Base.prepare(engine, reflect=True)

# # Save references to the measurement and station tables in the database
measurement = Base.classes.measurement
station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
#list all available routes
@app.route("/")
def home():
    return (
        f"Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# 4. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # start query session
    session = Session(engine)
    
    most_recent_date = session.query(func.max(measurement.date))[0][0]

    date_object = datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    year_prior = date_object+ relativedelta(months=-12)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_prior).all()

    # close query session
    session.close()

    precipitation_data = []
    for x in results:
        temp_dat = {}
        temp_dat[x[0]] = x[1]
        precipitation_data.append(temp_dat)
    
    

    return jsonify(precipitation_data)

# 5. Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(station.station).all()

    session.close()

    stations_list = []
    for x in results: 
        stations_list.append(x[0])

    return jsonify(stations_list)


# 6. Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    most_recent_date = session.query(func.max(measurement.date))[0][0]

    date_object = datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    year_prior = date_object+ relativedelta(months=-12)

    most_active_station = session.query(measurement.station).group_by(measurement.station).order_by(func.count().desc()).limit(1)[0][0]

    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active_station, measurement.date >= year_prior).all()

    # close query session
    session.close()

    temperature_data = []
    for x in results:
        temp_dat = {}
        temp_dat[x[0]] = x[1]
        temperature_data.append(temp_dat)
    
    return jsonify(temperature_data)


# 7. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    
    date_object = datetime.strptime(start, '%Y-%m-%d').date()
    start_date = date_object

    most_active_station = session.query(measurement.station).group_by(measurement.station).order_by(func.count().desc()).limit(1)[0][0]

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.station == most_active_station, measurement.date >= start_date).all()

    # close query session
    session.close()

    start_data = []
    for x in results:
        start_data.append(f"Lowest Temperature: {x[0]}")
        start_data.append(f"Highest Temperature: {x[1]}")
        start_data.append(f"Average Temperature: {x[2]}")
    
    return jsonify(start_data)


# 8. For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()

    most_active_station = session.query(measurement.station).group_by(measurement.station).order_by(func.count().desc()).limit(1)[0][0]

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.station == most_active_station, measurement.date >= start_date,measurement.date <= end_date).all()

    # close query session
    session.close()

    start_end_data = []
    for x in results:
        TMIN = x[0]
        TAVG = x[2]
        TMAX = x[1]
        start_end_data.append(f"Lowest Temperature: {TMIN}")
        start_end_data.append(f"Highest Temperature: {TMAX}")
        start_end_data.append(f"Average Temperature: {TAVG}")
    return jsonify(start_end_data)



if __name__ == "__main__":
    app.run(debug=True)