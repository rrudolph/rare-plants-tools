print("Importing modules")
# import arcpy
import yaml, pathlib, arcpy
from os.path import join

yaml_file = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\build rare plants fields.yaml"

def get_config():
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
        return data


ws = r"C:\GIS\Projects\CHIS_RarePlants\Data Entry Tools\scratch.gdb"
fc = "brand_new2"
print("Making featureclass")
arcpy.management.CreateFeatureclass(ws, fc, "POLYGON", None, "DISABLED", "DISABLED", 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision', '', 0, 0, 0, '')

dict_list = get_config()
# print(dict_list)

for field_dict in dict_list:
    for field_name, field_data in field_dict.items():
        print("Processing ", field_name, field_data)
        new_name = field_data[0]
        field_type = field_data[1]
        field_precision = field_data[2]
        field_scale = field_data[3]
        field_length = field_data[4]
        field_alias = field_data[5]
        field_is_nullable = field_data[6]
        field_is_required = field_data[7]
        field_domain = field_data[8]

        arcpy.management.AddField(join(ws, fc), 
            new_name,
            field_type,
            field_precision,
            field_scale,
            field_length,
            field_alias,
            field_is_nullable,
            field_is_required,
            field_domain)
        