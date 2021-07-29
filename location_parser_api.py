import logging
from flask import Flask, abort
from flask import request
from shapely.geometry import Point

from location_parser import LocationParser

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
parser = LocationParser("zip+s3://taihu-resource/gadm/shps", 2)
parser.load()


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


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)