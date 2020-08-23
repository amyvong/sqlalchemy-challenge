import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import Session
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station=Base.classes.station
session=Session(i8,engine)

app=Flask(__name__)

@app.route("/")
def welcome():
    """Available API Routes for Surfs Up"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/stations")
def stations():
session = Session(engine)
session.query(station.station,station.id)).all()
session.close()

stations=[]
for name, id in stations:
    stationdict = {}
    station['name'] = station[0]
    station['id'] = station[1]
    stations.append(stationdict)

return jsonify(stations)




@app.route("/api/v1.0/precipitation")
def precipitation():
session = Session(engine)
sel = [measurement.date,measurement.prcp]
prcpquery = session.query(*sel).filter(measurement.date >= querydate).all()

session.close()

precipitation = []
for date, amount in prcpquery:
    raindict = {}
    raindict['date'] = rain[0]
    raindict['amount'] = rain[1]
    precipitation.append(raindict)

return jsonify(precipitation)

@app.route("/api/v1.0/tobs")
def tobs():
session = Session(engine)
session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))
session.close()

tobs=[]
for minimum, maximum, average in tobs:
    tobsdict = {}
    tobsdict['min'] = tobsdict[0]
    tobsdict['max'] = tobsdict[1]
    tobsdict['avg'] = tobsdict[2]
    tobs.append(tobsdict)

return jsonify(tobs)



if __name__=='__main__':
    app.run()