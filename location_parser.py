import geopandas
import pandas
from shapely.geometry.point import Point
from shapely.geometry.base import BaseGeometry

from countries import all_countries
import logging

pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 1000)

ALL_COUNTRIES = all_countries
SHP_FILE_DIR = "zip://C:/Users/spiro.huang/workspace/gadm/shps"
DATA_URL_TEMP = SHP_FILE_DIR + "/gadm36_{country_code}_shp.zip!gadm36_{country_code}_{level}.shp"


class Division:
    def __init__(self, level: int, geometry: BaseGeometry, gid: str, name: str, var_name: str = None,
                 nl_name: str = None,
                 hasc: str = None, local_type: str = None, eng_type: str = None):
        self.level = level
        self.gid = gid
        self.name = name
        self.var_name = var_name
        self.nl_name = nl_name
        self.hasc = hasc
        self.local_type = local_type
        self.eng_type = eng_type
        self.geometry = geometry
        self.subDivisions = {}

    def add_sub(self, d):
        self.subDivisions[d.gid] = d

    def contains(self, p: Point):
        return self.geometry.contains(p)

    def parse(self, p: Point):
        if not self.contains(p):
            return None

        result = [self]
        for gid, subDivision in self.subDivisions.items():
            sub_result = subDivision.parse_location(p)
            if sub_result is not None:
                result.extend(sub_result)
                break
        return result


class LocationParser:
    def __init__(self, shp_file_dir):
        self.country = {}  # key: country_code value: Division

    def load_country(self, country_code, nums_of_level):
        for level in range(nums_of_level):
            data_url = DATA_URL_TEMP.format(country_code=country_code, level=level)
            logging.info("country_code: %s, level: %d - reading", country_code, level)
            df = geopandas.read_file(data_url)
            logging.info("country_code: %s, level: %d - read done, loading", country_code, level)

            item_count = 0
            if level == 0:
                for index, row in df.iterrows():
                    gid = row['GID_0']
                    name = row['NAME_0']
                    geometry = row['geometry']
                    self.country[gid] = Division(0, geometry, gid, name)
                    item_count += 1
                continue
            else:
                for index, row in df.iterrows():
                    gid = row['GID_{}'.format(level)]
                    name = row['NAME_{}'.format(level)]
                    var_name = row['VARNAME_{}'.format(level)]
                    nl_name = row['NL_NAME_{}'.format(level)]
                    hasc = row['HASC_{}'.format(level)]
                    local_type = row['TYPE_{}'.format(level)]
                    eng_type = row['ENGTYPE_{}'.format(level)]

                    geometry = row['geometry']

                    division = Division(level, geometry, gid, name, var_name, nl_name, hasc, local_type, eng_type)

                    # TODO: add division

                    item_count += 1
                continue

            logging.info("country_code: %s, level: %d, item_count: %d - loaded", country_code, level, item_count)

    def load(self):
        for country in ALL_COUNTRIES:
            country_code = country[0]
            nums_of_level = country[2]
            self.load_country(country_code, nums_of_level)

    def parse(self, p: Point):
        for country_code, division in self.country.items():
            result = division.parse(p)
            if result is not None:
                return result
        return None
