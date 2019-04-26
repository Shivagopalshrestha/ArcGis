import arcpy
from arcpy import env
from arcpy.sa import *
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = 'Shiva_Toolbox'
        self.alias = 'ShapeToolBox'

        # List of tool classes associated with this toolbox
        self.tools = [NDVI_,Findnearest,Toheatmap]


class NDVI_(object):
    def __init__(self):
        self.label = 'Ndvi_Calculator'
        self.description = 'This tool will return NDVI from the landsat data provided. All you need to provide is the folder with subfolders which contains the landsat data'
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        parameters = []
        # Data  Folder
        wrok = arcpy.Parameter(
            displayName="Input Raster",
            name="inputDcsv",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")
        parameters.append(wrok)

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = True
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.workspace = parameters[0].valueAsText
        fold= arcpy.env.workspace
        arcpy.AddMessage(os.path.split((arcpy.env.workspace))[-1])
        asl = os.listdir(arcpy.env.workspace)
        asl = [x for x in asl if "WINT" not in x]


        arcpy.AddMessage(asl)
        for year in asl:
            arcpy.env.workspace = os.path.join(fold, year)
            arcpy.AddMessage(os.path.split(os.path.dirname(parameters[0].valueAsText))[-1])
            listRasters1 = arcpy.ListRasters("*_B4*", "")
            listRasters2 = arcpy.ListRasters("*_B5*", "")
            arcpy.AddMessage(listRasters1 + listRasters2)
            B5 = arcpy.ListRasters("*_B4*", "")
            B4 = arcpy.ListRasters("*_B5*", "")
            aa = (Raster(str(B5[0]))*1.0 - Raster(str(B4[0]))*1.0) / (Raster(str(B5[0]))*1.0 + Raster(str(B4[0]))*1.0)
            aa.save(os.path.join(os.path.dirname(env.workspace), "NDVI" + year + ".tif"))
        arcpy.CheckInExtension("Spatial")

        arcpy.AddMessage('NDVI computed succesfully')

        return

class Findnearest(object):
    def __init__(self):
        self.label = 'Find Near points'
        self.description = 'This tool creat shapefile  from csv. It will compute the nearest point for the input file with given near points '
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        parameters = []

        # Reference States layer

        # Data  CSV file
        inputData = arcpy.Parameter(
            displayName="Input csv File",
            name="inputDcsv",
            datatype="DETable",
            parameterType="Required",
            direction="Input")
        parameters.append(inputData)

        States = arcpy.Parameter(
            displayName="Input Shape",
            name="States",
            datatype="DEFeatureClass", #DEFeatureClassDEShapefile
            parameterType="Required",
            direction="Output")
        parameters.append(States)

        inputData1 = arcpy.Parameter(
            displayName="Near csv File",
            name="inputcsv2",
            datatype="DETable",
            parameterType="Required",
            direction="Input")
        parameters.append(inputData1)

        States1 = arcpy.Parameter(
            displayName="Near Shapefile",
            name="States2",
            datatype="DEFeatureClass",  # DEFeatureClassDEShapefile
            parameterType="Required",
            direction="Output")
        parameters.append(States1)

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = True

        # Create target names based on name of input table (assuming you want the CSV filename)
        # tempStr = os.path.splitext(os.path.basename(parameters[1].valueAsText))[0]
        in_Table = parameters[0].valueAsText
        # arcpy.AddMessage(tempStr+ " ok ")
        x_coords = "X"
        y_coords = "Y"
        z_coords = "Y"
        out_Layer = "firestations_layer"
        saved_Layer = parameters[1].valueAsText
        # arcpy.AddMessage(saved_Layer + " ok ")

        # Set the spatial reference
        spRef = arcpy.SpatialReference(4326)

        # Make the XY event layer...
        arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef,z_coords)
        arcpy.CopyFeatures_management(out_Layer, saved_Layer)
        out_Layer = "firestations_layer1"
        saved_Layer1 = parameters[3].valueAsText

        arcpy.MakeXYEventLayer_management(parameters[2].valueAsText, x_coords, y_coords, out_Layer, spRef,z_coords)
        arcpy.CopyFeatures_management(out_Layer,parameters[3].valueAsText)

        # find the nearest points to input files from nearpoints shapfile
        arcpy.Near_analysis(saved_Layer, saved_Layer1)
        if arcpy.Exists(saved_Layer):
            arcpy.AddMessage( "Created  shapefile with near distances successfully!")
            arcpy.Delete_management(saved_Layer1)

        return

class Toheatmap(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Shape2Heatmap"
        self.description = "This tool will create heatmap to find the density of point distribution.This is done by using fishnet tools and spatial join"
        self.canRunInBackground = False
            # Set environment settings


    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_line = arcpy.Parameter(name="input_line",
                                     displayName="Point Shape File",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(input_line)

        output = arcpy.Parameter(name="output",
                                 displayName="Fishnets",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(output)

        Aoutput1 = arcpy.Parameter(name="AoutputA",
                                 displayName="Heatmaps",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(Aoutput1)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.CheckOutExtension("Spatial")
        inPointFeatures = parameters[0].valueAsText
        outFeatureClass = parameters[1].valueAsText
        output = parameters[2].valueAsText


        desc = arcpy.Describe(inPointFeatures)
        XMin = desc.extent.XMin
        XMax = desc.extent.XMax
        YMin = desc.extent.YMin
        YMax = desc.extent.YMax
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)


        # Set the origin of the fishnet
        originCoordinate = str(XMin) + " " + str(YMin)  # Left bottom of our point data
        yAxisCoordinate = str(XMin) + " " + str(YMin + 0.1)  # This sets the orientation on the y-axis, so we head north
        cellSizeWidth = "0.1"
        cellSizeHeight = "0.1"
        numRows = ""  # Leave blank, as we have set cellSize
        numColumns = ""  # Leave blank, as we have set cellSize
        oppositeCorner = str(XMax) + " " + str(YMax)  # i.e. max x and max y coordinate
        labels = "NO_LABELS"
        templateExtent = "#"  # No need to use, as we have set yAxisCoordinate and oppositeCorner
        geometryType = "POLYGON"  # Create a polygon, could be POLYLINE

        arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                       cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                       oppositeCorner, labels, templateExtent, geometryType)




        target_features = outFeatureClass  # "Fishnet here"
        join_features = inPointFeatures
        out_feature_class = output  # "_HeatMap here"
        join_operation = "JOIN_ONE_TO_ONE"
        join_type = "KEEP_ALL"
        field_mapping = ""
        match_option = "INTERSECT"
        search_radius = ""
        distance_field_name = ""

        arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                                   join_operation, join_type, field_mapping, match_option,
                                   search_radius, distance_field_name)
        arcpy.CheckInExtension("Spatial")
        arcpy.AddMessage("Created  heatmap successfully!")


        return