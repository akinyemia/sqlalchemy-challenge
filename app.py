import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 

# Create connection to Hawaii.sqlite file
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

Base.prepare(autoload_with=engine)
Base.classes.keys()

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0//api/v1.0/<start>/<end>"
    )

# 4. Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
# to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(func.max(measurement.date))[0][0]

    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    date_object = datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    year_prior = date_object+ relativedelta(months=-12)

    precipitation_data = {}
    for x in session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_prior).all():
        precipitation_data[x[0]] = x[1]
    
    session.close()

    return jsonify(precipitation_data)

# 5. Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


# 6. Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


# 7. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start
@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


# 8. For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"



if __name__ == "__main__":
    app.run(debug=True)