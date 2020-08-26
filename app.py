import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station=Base.classes.station


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
    results = session.query(station.station).all()
    session.close()
    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/temp/start/end")
def startend():
    session = Session(engine)
    sel = [measurement.date,measurement.prcp]
    lastdate=session.query(measurement.date).order_by(measurement.date.desc()).first()
    querydate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    lastdate = dt.datetime.strptime(lastdate[0], '%Y-%m-%d')
    querydate = dt.date(lastdate.year -1, lastdate.month, lastdate.day)
    prcpquery = session.query(*sel).filter(measurement.date >= querydate).all()
    session.close()

    startend = []
    for rain in prcpquery:
        raindict = {}
        raindict['date'] = rain[0]
        raindict['amount'] = rain[1]
        startend.append(raindict)

    return jsonify(startend)


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    date_str = "12"
    prcpresults=session.query(measurement.prcp).\
        filter(func.strftime("%m", measurement.prcp) == date_str).all() 
    session.close()
    precipitation = list(np.ravel(prcpresults))

    return jsonify(precipitation)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobsresults = session.query(measurement.tobs).all()
    session.close()

    tobslist = list(np.ravel(tobsresults))

    return jsonify(tobslist)



if __name__=='__main__':
    app.run()