# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2020-06-16 18:31:14
"""
import arcpy

def Model():  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    Historical_Airtraffic_Data_may = "May\\airtraff_may2020_a"
    aircraft_db_csv = "aircraft_db.csv"
    Mean_NoiseMay2020_hexagon_2_ = "May\\Mean_NoiseMay2020_hexagon"

    # Process: Add Join (Add Join) 
    Joined_airtraffic_data = arcpy.AddJoin_management(in_layer_or_view=Historical_Airtraffic_Data_may, in_field="icao24", join_table=aircraft_db_csv, join_field="icao", join_type="KEEP_ALL")[0]

    # Process: Select Layer By Attribute (Select Layer By Attribute) 
    Eliminated_null_rows, Count = arcpy.SelectLayerByAttribute_management(in_layer_or_view=Joined_airtraffic_data, selection_type="NEW_SELECTION", where_clause="mdl IS NULL", invert_where_clause="")

    # Process: Generate Tessellation (Generate Tessellation) 
    Hexagonal_grid_per_1_km2 = "C:\\Users\\Dell\\Documents\\ArcGIS\\Projects\\mar apr may\\mar apr may.gdb\\GenerateTessellation"
    GenerateTessellation(Output_Feature_Class=Hexagonal_grid_per_1_km2, Extent="12.200035679703 47.3000064103676 13.700035679703 48.2000064103675", Shape_Type="HEXAGON", Size="0.0225 Unknown", Spatial_Reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Add Fields (multiple) (Add Fields (multiple)) 
    Added_new_fields = arcpy.AddFields_management(in_table=Eliminated_null_rows, field_description=[["size_class", "TEXT", "", "255", "", ""], ["noiselevel", "LONG", "", "", "", ""]])[0]

    # Process: Classify size based on aircraft model (Calculate Field) 
    Classified_size_class = arcpy.CalculateField_management(in_table=Added_new_fields, field="size_class", expression="Reclass(!mdl!)", expression_type="PYTHON3", code_block="# Reclassify values to another value
# More calculator examples at esriurl.com/CalculatorExamples
def Reclass(mdl):
    if mdl == \"a400\":
        return \"large\"
    elif mdl == \"b757\":
        return \"large\"
    elif mdl == \"a319\":
        return \"medium\"
    elif mdl == \"a320\":
        return \"medium\"
    elif mdl == \"a321\":
        return \"medium\"
    elif mdl == \"b733\":
        return \"medium\"
    elif mdl == \"b737\":
        return \"medium\"
    elif mdl == \"b738\":
        return \"medium\"
    elif mdl == \"b739\":
        return \"medium\"
    elif mdl == \"b752\":
        return \"medium\"
    elif mdl == \"bcs3\":
        return \"medium\"
    elif mdl == \"crj2\":
        return \"medium\"
    elif mdl == \"rj1h\":
        return \"medium\"
    elif mdl == \"dh8d\":
        return \"medium\"
    elif mdl == \"fa8x\":
        return \"medium\"
    else:
        return \"small\"", field_type="TEXT")[0]

    # Process: Classify noise based on size (Calculate Field) 
    Classified_noiselevel = arcpy.CalculateField_management(in_table=Classified_size_class, field="noiselevel", expression="Reclass(!size_class!,!altitude!", expression_type="PYTHON3", code_block="# Reclassify values to another value
# More calculator examples at esriurl.com/CalculatorExamples
def Reclass(size_class, altitude):
    if size_class is \"large\" and altitude <=11000:
        return 60
    elif size_class == \"large\" and (altitude > 11000 and altitude <= 15000):
        return 52
    elif size_class == \"large\" and (altitude > 11000 and altitude <= 15000):
        return 52
    elif size_class == \"large\" and (altitude > 15000 and altitude <= 16000):
        return 43
    elif size_class == \"large\" and (altitude > 16000):
        return 42
    elif size_class == \"medium\" and altitude <=4000:
        return 71
    elif size_class == \"medium\" and (altitude > 4000 and altitude <= 6000):
        return 70
    elif size_class == \"medium\" and (altitude > 6000 and altitude <= 9000):
        return 60
    elif size_class == \"medium\" and (altitude > 9000 and altitude <= 15000):
        return 59
    elif size_class == \"medium\" and (altitude > 15000 and altitude <= 16000):
        return 46
    elif size_class == \"medium\" and (altitude > 16000):
        return 36
    elif size_class == \"small\" and altitude <=4000:
        return 67
    elif size_class == \"small\" and (altitude > 4000 and altitude <= 5000):
        return 54
    elif size_class == \"small\" and (altitude > 5000):
        return 43", field_type="TEXT")[0]

    # Process: Point to Raster (Mean aggregated) (Point to Raster) 
    Mean_Noise_may_2020 = "C:\\Users\\Dell\\Documents\\ArcGIS\\Projects\\mar apr may\\mar apr may.gdb\\airtraff_may2020_a_PointToRaster"
    arcpy.PointToRaster_conversion(in_features=Classified_noiselevel, value_field="noiselevel", out_rasterdataset=Mean_Noise_may_2020, cell_assignment="MEAN", priority_field="NONE", cellsize="0.001")

    # Process: extract cell value (Raster to Point) 
    Points_represent_noiselevel = "C:\\Users\\Dell\\Documents\\ArcGIS\\Projects\\mar apr may\\mar apr may.gdb\\RasterT_airtraf1"
    arcpy.RasterToPoint_conversion(in_raster=Mean_Noise_may_2020, out_point_features=Points_represent_noiselevel, raster_field="VALUE")

    # Process: Feature To Polygon (Feature To Polygon) 
    Mean_NoiseMay2020_hexagon = "C:\\Users\\Dell\\Documents\\ArcGIS\\Projects\\mar apr may\\mar apr may.gdb\\GenerateTessellation_Feature"
    arcpy.FeatureToPolygon_management(in_features=[Hexagonal_grid_per_1_km2], out_feature_class=Mean_NoiseMay2020_hexagon, cluster_tolerance="", attributes="ATTRIBUTES", label_features=Points_represent_noiselevel)

    # Process: Polygon to Raster (Polygon to Raster) 
    Mean_NoiseZone_may2020 = "C:\\Users\\Dell\\Documents\\ArcGIS\\Projects\\mar apr may\\mar apr may.gdb\\GenerateTessellation_Feature_PolygonToRaster"
    if Mean_NoiseMay2020_hexagon:
        arcpy.PolygonToRaster_conversion(in_features=Mean_NoiseMay2020_hexagon_2_, value_field="grid_code", out_rasterdataset=Mean_NoiseZone_may2020, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="0.02")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\Dell\Documents\ArcGIS\Projects\mar apr may\mar apr may.gdb", workspace=r"C:\Users\Dell\Documents\ArcGIS\Projects\mar apr may\mar apr may.gdb"):
        Model()
