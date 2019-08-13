# OpenTopoMap Tile Downloader
# (c) 2019 Kurt Höblinger aka NitricWare

import math
import subprocess
import urllib.request
import os.path
import os
import shutil

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

if not os.path.isdir("./tiles"):
  os.mkdir("./tiles")

print("Welcome to OpenTopoMaps Tile Downloader")
print("(c) Kurt Höblinger aka Nitricware")

print("")

print("Coordinates consist of Latitude, Longitude.")
print("example: 47.405950, 13.558321")
print("Latitude: 47.405950")
print("Longitude: 13.558321")

print("")

print("You will be asked two coordinates. Imagine a rectangular map.")
print("Chose a coordinate in the upper left and the lower right of the map.")

topY = float(input("Upper Left Latitude: "))
leftX = float(input("Upper Left Longitude: "))

bottomY = float(input("Lower Left Latitude: "))
rightX = float(input("Lower Right Longitude: "))

zoom = int(input("Zoomlevel: "))

print("Generating map from: " + str(leftX) + "|" + str(topY) + " to " + str(rightX) + "|" + str(bottomY))

topLeft = deg2num(topY, leftX, zoom)
bottomRight = deg2num(bottomY, rightX, zoom)

for x in range(topLeft[0], bottomRight[0]+1):
  for y in range(topLeft[1], bottomRight[1]+1):
    u = "https://a.tile.opentopomap.org/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".png"
    f = "./tiles/" + str(zoom) + "_" + str(y) + "_" + str(x) + ".png"
    if os.path.isfile(f):
      print("Keeping ", x, ",", y, "from", u, "to", f)
    else:
      print("Getting ", x, ",", y, "from", u, "to", f)
      urllib.request.urlretrieve(u,f)

print("")

print("Okay, let's stitch it all together...")
o = "out_z" + str(zoom) + "_" + str(topLeft[0]) + "_" + str(bottomRight[0]) + "-" + str(topLeft[0]) + "_" + str(bottomRight[0]) + ".png"
args = "montage -limit thread 8 -limit memory 30000MB -mode concatenate -tile " + str((bottomRight[0] - topLeft[0]) + 1) + "x ./tiles/" + str(zoom) + "_*.png " + o
subprocess.call(args, shell=True)
print("Done! If no error is displayed there should now be a file, called " + o + ", which containes your map.")

print("")

print("Would you like to delete the downloaded tiles? Creating a map containing the same tiles takes longer ina future run.")

if input("Delete? (y/n) ") == "y":
  print("Deleting...")
  shutil.rmtree("./tiles")
else:
  print("No 'y' was typed in, assuming 'n'. Not deleting.")

print("")

print("Thank's for using. Good Bye.")
