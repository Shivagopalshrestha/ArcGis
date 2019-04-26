
# ArcGIS automation through scripting with Python
![Banner Image](banner.png)

This has been prepared for the part of the course. If you want to dive in deep in ArcPy
here is a helpful [link](https://pro.arcgis.com/en/pro-app/)



| **`Documentation`** |
|-----------------|

There are 3 tools inside this toolbox. Each of these have specific functions in ArcGis.

## 1.Find Near Points
This tool can be used to find the near points between a list of two points with their locations in  csv files.
The first argument is for the input file for which we want to find the nearest point. The second argument is the near points to be searched. This is also applicable for a file and check the nearest points with in itself.
The output is a point shapefile with new fields showing the nearest points and the arial distance.

## 2. NDVI_Calculator
This tool can be used to prepare NDVI from landsat files stored in folders.
It can be used for multiple subfolders with the landsat data in the main folder.
The only argument the tool requires is the location of the main folder.

The output are the NDVI output per subfolder and is located in the mainfolder and outside folders.

## 3. Shape2Heatmap

This tools can be used to prepare a heatmap from the input as point shapefile.
The purpose of this tool is find the density or scatter of points in latitude and longitude domain.
The input required is a point file and the output is heatmap which contains the counts of points lying within the fishnet polygon shapefile.



