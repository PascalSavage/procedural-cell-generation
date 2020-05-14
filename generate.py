import pickle
from pdm import PointDistributionModel
import numpy as np
import matplotlib.pyplot as plt
import struct
import alphashape
from descartes import PolygonPatch
from shapely.geometry import Polygon, Point, LineString
import os
import time

with open("shapes.dat", "rb+") as f:
    shapes = pickle.load(f)

shapes_list = []
for i in range(0, len(shapes)):
    shape = []
    for j in range(0, len(shapes[i])):
        shape += [shapes[i][j][0], shapes[i][j][1]]# shapes[0][j][2]]
    shapes_list.append(shape)

model = None
if not os.path.exists(f"model_cache.dat"):
    model = PointDistributionModel(shapes_list)
    with open("model_cache.dat", "wb+") as model_file:
        pickle.dump(model, model_file)
else:
    with open("model_cache.dat", "rb") as model_file:
        model = pickle.load(model_file)


seed = 800*5
new_shape = model.randomShape(seed)
xdata = []
ydata = []
zdata = []
by_nivo = {}
nivo_resolution = 1
for i in [n*nivo_resolution for n in range(0, 15)]:
    by_nivo[i] = []

i = 0
while i < len(new_shape):
    xdata.append(int(new_shape[i]))
    i += 2

i = 1
while i < len(new_shape):
    ydata.append(int(new_shape[i]))
    i += 2

i = 0
nivo = 0
counter = 0
while i < len(new_shape):
    zdata.append(nivo * nivo_resolution)
    i += 2
    counter += 1
    if counter % 100 == 0:
        nivo += 1

for i in range(0, len(zdata)):
    by_nivo[zdata[i]].append((xdata[i], ydata[i]))

min_z = min(zdata)
max_z = max(zdata)


polni_nivo = {}
outer_nivo =  {}

for _nivo in by_nivo:
    points = by_nivo[_nivo]
    alpha = 0.25 * alphashape.optimizealpha(points)
    hull = alphashape.alphashape(points, alpha)
    hull_pts = hull.exterior.coords.xy

    hull_points = []
    for i in range(0, len(hull_pts[0])):
        hull_points.append((hull_pts[0][i], hull_pts[1][i]))

    polyg = Polygon(hull_points)
    line_polygon = LineString(polyg.exterior.coords)
    # (minx, miny, maxx, maxy)
    bounds = list(map(int, list(polyg.bounds)))
    polni_nivo[_nivo] = []
    outer_nivo[_nivo] = []

    for i in range(bounds[0], bounds[2]+1):
        for j in range(bounds[1], bounds[3]+1):
            if line_polygon.contains(Point(i,j)):
                outer_nivo[_nivo].append((i,j))
            elif polyg.contains(Point(i,j)):
                polni_nivo[_nivo].append((i,j))
                if _nivo == min_z or _nivo == max_z:
                    outer_nivo[_nivo].append((i, j))


with open(f"polninivo{time.time()}.dat", "wb+") as f:
    pickle.dump(polni_nivo, f)

with open(f"outernivo{time.time()}.dat", "wb+") as f:
    pickle.dump(outer_nivo, f)

xdata_final = []
ydata_final = []
zdata_final = []
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter3D(xdata, ydata, zdata)
# plt.show()

