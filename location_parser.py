import geopandas
from shapely.geometry.point import Point
from shapely.geometry.base import BaseGeometry

from countries import all_countries
import logging

def hierarchy(string: str, delimiter: str):
    """
    Generate hierarchy list. For example string="CHN.1.2" then return list like ["CHN", "CHN.1", "CHN.1.2"]
    :param string:
    :param delimiter:
    :return:
    """
    result = []
    i = -1
    while True:
        i = string.find(delimiter, i + 1)
        if i == -1:
            result.append(string)
            break
        result.append(string[0:i])
    return result


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
        self.hierarchy_gids = hierarchy(gid, ".")

    def add_sub(self, d):
        self.subDivisions[d.gid] = d

    def contains(self, p: Point):
        return self.geometry.contains(p)

    def parse(self, p: Point):
        if not self.contains(p):
            return None

        result = [self]
        for gid, subDivision in self.subDivisions.items():
            sub_result = subDivision.parse(p)
            if sub_result is not None:
                result.extend(sub_result)
                break
        return result

    def to_dict(self):
        d = {
            "level": self.level,
            "gid": self.gid,
            "name": self.name
        }

        if self.level > 0:
            d['var_name'] = self.var_name
            d['nl_name'] = self.nl_name
            d['hasc'] = self.hasc
            d['local_type'] = self.local_type
            d['eng_type'] = self.eng_type
        return d

    def __str__(self):
        return "{{level: {}, gid: {}, hasc: {}, name: {}, var_name: {}, local_type: {}, eng_type: {}, nl_name: {}}}"\
            .format(self.level, self.gid, self.hasc, self.name, self.var_name, self.local_type, self.eng_type, self.nl_name)

    def __repr__(self):
        return self.__str__()


ALL_COUNTRIES = all_countries


class LocationParser:
    def __init__(self, data_dir: str, max_level: int):
        if not data_dir.endswith("/"):
            data_dir += "/"
        self.data_dir = data_dir
        self.data_url_temp = "zip://" + self.data_dir + "gadm36_{country_code}_shp.zip!gadm36_{country_code}_{level}.shp"
        self.country = {}  # key: country_code value: Division
        self.max_level = max_level

    def load_country(self, country_code, nums_of_level):
        for level in range(nums_of_level):
            if level > self.max_level:
                return

            data_url = self.data_url_temp.format(country_code=country_code, level=level)
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
            else:
                for index, row in df.iterrows():
                    gid = row['GID_{}'.format(level)]
                    underscore_idx = gid.rfind("_")
                    if underscore_idx != -1:
                        gid = gid[0:underscore_idx]
                    name = row['NAME_{}'.format(level)]
                    var_name = row['VARNAME_{}'.format(level)]
                    nl_name = row['NL_NAME_{}'.format(level)]
                    hasc = row['HASC_{}'.format(level)]
                    local_type = row['TYPE_{}'.format(level)]
                    eng_type = row['ENGTYPE_{}'.format(level)]
                    geometry = row['geometry']
                    division = Division(level, geometry, gid, name, var_name, nl_name, hasc, local_type, eng_type)
                    parent_div = self.find_parent(division)
                    if parent_div is None:
                        logging.warning("gid: %s, name: %s, parent not found", gid, name)
                    else:
                        parent_div.add_sub(division)
                    item_count += 1
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

    def find_parent(self, division: Division) -> Division:
        parent_hier_gids = division.hierarchy_gids[:-1]
        # find parent node
        next_level_divs = self.country
        div_p = None
        for gid in parent_hier_gids:
            div_p = next_level_divs.get(gid)
            if div_p is not None:
                next_level_divs = div_p.subDivisions
        return div_p


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    parser = LocationParser("C:/Users/hsp87/Desktop", 2)
    parser.load_country("CHN", 4)
    result = parser.parse(Point(121.546074, 31.090431))
    print(result)
