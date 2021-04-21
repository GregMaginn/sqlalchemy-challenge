from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return( f"Welcome to the homepage"
           f"Routes Available are:"
           f"/api/v1.0/precipitation......"
           f"/api/v1.0/stations......"
           f"/api/v1.0/tobs......"
           f"/api/v1.0/start...... ENTER DATE IN YYYY-MM-DD FORM"
           f"/api/v1.0/start/end...... ENTER DATE IN YYYY-MM-DD FORM"
          )

@app.route("/api/v1.0/precipitation")
def prcp_web():
    print("Server received request for 'precipitation' page...")
    
    all_dates = session.query(Measurement.date).all()
    all_prcp = session.query(Measurement.prcp).all()

    prcp_dic = {str(all_dates[i]): str(all_prcp[i]) for i in range(len(all_dates))}
    
    return jsonify(prcp_dic)


@app.route("/api/v1.0/stations")
def station_web():
    print("Server recieved request for 'stations' list...")

    stations_lst = session.query(Measurement.station).distinct().all()

    return jsonify(str(stations_lst))

@app.route("/api/v1.0/tobs")
def tobs_web():
    print("Server recieved request for 'tobs' info")
    year_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.prcp != 'None').order_by(Measurement.date).all()

    return jsonify(str(year_tobs))
    
@app.route("/api/v1.0/<start>")
def just_start(start):
    
    sel = [func.avg(Measurement.tobs), 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs),
      ]

    results = session.query(*sel).filter(Measurement.date >= start).all()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    sel = [func.avg(Measurement.tobs), 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs),
      ]

    res = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
