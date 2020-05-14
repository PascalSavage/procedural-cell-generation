import pickle
import time

with open("polninivo1589451606.8455255.dat", "rb") as f:
    polni_nivo = pickle.load(f)

with open("outernivo1589451607.027524.dat", "rb") as f:
    outer_nivo = pickle.load(f)


coordinates = {}
for nivo in polni_nivo:
    for point in polni_nivo[nivo]:
        coordinates[f"{point[0]},{point[1]},{nivo}"] = 255

coordinates2 = {}
for nivo in outer_nivo:
    for point in outer_nivo[nivo]:
        coordinates2[f"{point[0]},{point[1]},{nivo}"] = 128

with open(file=f"celica{time.time()}.raw", mode="wb+") as f:
    for z in range(0, 4*15):
        for y in range(0, 600):
            for x in range(0, 600):
                if f"{x},{y},{z}" in coordinates2:
                    a = 128
                    f.write(bytearray([a]))
                elif f"{x},{y},{z}" in coordinates:
                    a = 255
                    f.write(bytearray([a]))
                else:
                    a = 0
                    f.write(bytearray([a]))
