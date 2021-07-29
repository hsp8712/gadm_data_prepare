import geopandas
import pandas

pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 1000)

zipfile = "zip://C:/Users/hsp87/Desktop/gadm36_IDN_0.zip!gadm36_IDN_0.shp"
level0_df = geopandas.read_file(zipfile)
level0_df.insert(0, 'GID_0', ['IDN'], True)

for index, row in level0_df.iterrows():
    print(row)

level0_df.to_file("C:/Users/hsp87/Desktop/gadm36_IDN_0")

#
# zipfile = "zip://C:/Users/spiro.huang/workspace/gadm/shps/gadm36_CHN_shp.zip!gadm36_CHN_1.shp"
# level1_df = geopandas.read_file(zipfile)
# print(level1_df.head())