import csv
import os
import subprocess
import time

from win10toast import ToastNotifier
from subprocess import run, PIPE

toaster = ToastNotifier()
var_CSV = '\\\\ad.garmin.com\\DE\\Cartography\\DECARTFS01\\Sources\\OSM\\Tile_File\\Norway_200526\\ElevationMapper' \
          '\\CSV.csv '
var_source = 5146
var_pathBIL = '\\\\ad.garmin.com\\DE\\Cartography\\DECARTFS01\\Sources\\OSM\\DEM\\Bils'
var_path = var_CSV.rsplit('\\', 1)
var_pathOUT = var_CSV.rsplit('\\', 2)[0] + '\\GEM'
# var_name = row[0] var_west = row[1] var_east = row[2] var_north = row[3] var_south = row[4] var_BILs = row[5]
print("Path is: " + str(var_path[0]))

# alle .xml löschen
print("REMOVING OLD .xml files")
time.sleep(5)
i_xml = 0
for file2 in os.listdir(var_path[0]):
    if file2.endswith(".xml"):
        os.remove(str(var_path[0]) + "\\" + str(file2))
        i_xml = i_xml + 1
print(str(i_xml) + " old files removed")

i_new_xml = 0
with open(var_CSV, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[5]:
            var_fileName = str(var_path[0]) + "\\input_" + row[0] + ".xml"
            f = open(var_fileName, "w+")
            f.write("<config remove-dupes=\"false\">\n")
            f.write(
                "    <bounding-box north=\"" + row[3] + "\" east=\"" + row[2] + "\" south=\"" + row[4] + "\" west=\"" +
                row[1] + "\" />\n")
            f.write("\n")
            f.write("    <elevation-map etype=\"bare\" gtype=\"point\">\n")
            f.write("        <elevation source=\"gdal\">\n")
            f.write("            <cache-size size=\"250000000\" />\n")
            var_bil_temp = row[5].split(',')
            for i in var_bil_temp:
                # print(var_fileName)
                f.write("            <source path=\"" + str(var_pathBIL) + "\\" + i + ".BIL\" units=\"meters\" />\n")
            f.write("        </elevation>\n")
            f.write("        <geometry source=\"cartdb\">\n")
            f.write("            <db source=\"" + str(var_source) + "\" majent=\"1\" precision=\"1000000\" />\n")
            f.write("            <feature-code min=\"2010\" max=\"2029\" />\n")
            f.write("            <feature-code min=\"3231\" max=\"3237\" />\n")
            f.write("            <feature-code min=\"2080\" max=\"2082\" />\n")
            f.write("        </geometry>\n    </elevation-map>\n</config>")
            i_new_xml = i_new_xml + 1
        f.close()
print(str(i_new_xml - 1) + " new .xml files created")
os.remove(str(var_path[0]) + "\\input_ï»¿Name.xml")
var_fileName2 = str(var_path[0]) + "\\build-exec_RoadElevations.bf"

b = open(var_fileName2, "w+")
b.write("[BF_Exec]\n\"Build GEM Files\" ElevationMapper.bat 1 "
        "\\\\ad.garmin.com\\DE\\Cartography\\DECARTFS01\\Bin\\ElevationMapper\\")
b.write("\n \n")
b.write("[BF_ExecInstance]\n")
i = 1
for file in os.listdir(var_path[0]):
    # file.sort(key=int)
    if file.endswith(".xml"):
        b.write(str(i) + " " + str(os.path.join(var_path[0], file)) + " " + str(
            var_pathOUT + '\output_' + str(i) + ".gem\n"))
        i = i + 1
b.close()
print("Creating Executable build")
# subprocess.run("J:\\Bin\\BuildFarm-Executable-Requester\\buildfarm-executable-requester.exe -s "
#                "J:\\Sources\\OSM\\Tile_File\\Norway_200526\\ElevationMapper\\build-exec_RoadElevations.bf -o "
#                "J:\\Sources\\OSM\\Tile_File\\Norway_200526\\gem_output -p \"executable Norway GEM\"")
cmd = "J:\\Bin\\BuildFarm-Executable-Requester\\buildfarm-executable-requester.exe -s " \
      "J:\\Sources\\OSM\\Tile_File\\Norway_200526\\ElevationMapper\\build-exec_RoadElevations.bf -o " \
      "J:\\Sources\\OSM\\Tile_File\\Norway_200526\\gem_output -p \"executable Norway GEM\" "
# subprocess.run(cmd, stdout=PIPE, input="yes", encoding='ascii')

toaster.show_toast("Executable Build", "Passt scho'")
time.sleep(100)
