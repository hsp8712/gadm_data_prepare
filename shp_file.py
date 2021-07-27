import geopandas
import pandas

pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', 1000)

zipfile = "zip://C:/Users/spiro.huang/workspace/gadm/shps/gadm36_CHN_shp.zip!gadm36_CHN_0.shp"
level0_df = geopandas.read_file(zipfile)

print(type(level0_df['GID_0']))
print(type(level0_df['geometry']))

for index, row in level0_df.iterrows():
    print(type(row))

#
# zipfile = "zip://C:/Users/spiro.huang/workspace/gadm/shps/gadm36_CHN_shp.zip!gadm36_CHN_1.shp"
# level1_df = geopandas.read_file(zipfile)
# print(level1_df.head())