import logging
from flask import Flask, abort
from flask import request
from shapely.geometry import Point

from location_parser import LocationParser

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
parser = LocationParser("C:/Users/hsp87/Desktop", 2)
parser.load_country("CHN", 4)


@app.route("/location")
def location():
    try:
        lng = request.args.get('lng', type=float)
        lat = request.args.get('lat', type=float)
        logging.info("lng = %f, lat = %f", lng, lat)
        result = parser.parse(Point(lng, lat))
    except TypeError:
        logging.error("parameter lng or lat wrong")
        abort(400, "parameter lng or lat wrong")
        return

    resp = {}
    if result is None:
        return resp
    for div in result:
        resp['level_' + str(div.level)] = div.to_dict()
    return resp
