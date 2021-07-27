from matplotlib import pyplot
from shapely.geometry import Polygon, Point
from descartes.patch import PolygonPatch

ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0), (1, 0.3), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0.3)]
#int = [(1, 0), (0.5, 0.5), (1, 1), (1.5, 0.5), (1, 0)]



polygon = Polygon(ext)

print(polygon.exterior.coords.xy)
print(len(polygon.interiors))

print(polygon.contains(Point(1, 0.5)))


