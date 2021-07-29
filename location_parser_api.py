import logging
from flask import Flask
from shapely.geometry import Point

from location_parser import LocationParser

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
parser = LocationParser("C:/Users/hsp87/Desktop", 2)
parser.load_country("CHN", 4)


@app.route("/location/<float:lng>/<float:lat>")
def location(lng, lat):
    result = parser.parse(Point(lng, lat))
    resp = {}
    if result is None:
        return resp
    for div in result:
        resp['level_' + str(div.level)] = div.to_dict()
    return resp
