'''
Script for automating adding fields to a new featureclass for shared rare plant database for California Channel Islands.
Takes excel spreadsheet as input. 

R. Ruddolph
9/15/22


Add field syntax
# in_table
# field_name
# field_type
# {field_precision}
# {field_scale}
# {field_length}
# {field_alias}
# {field_is_nullable}
# {field_is_required}
# {field_domain}

'''

print("Importing modules")
import arcpy
import pandas as pd
from os.path import join
from icecream import ic

def convert_field_type(field_type):
    ''' Returns the field typed needed to properly generate the field. '''
    lookup = {
        "String": "TEXT",
        "Short integer": "SHORT",
        "Double": "DOUBLE",
        "Date" : "DATE",
        "Boolean": "TEXT",
        "GUID"  : "GUID"
    }
    return lookup.get(field_type, "Error") 

xlsx = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\RR_RarePlantFields_Agreed_Sept2022.xlsx"
sheet = "New Fields"

ws = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb"
fc = "RarePlants_Poly_ICBC"
out_fc_path = join(ws, fc)

## Convert sheets to domains
# df = pd.read_excel(xlsx, sheet_name=None, header=0)
# for sheet_name, data in df.items():
#     print(sheet_name)
#     print("-------")
#     print(data)
#     if sheet_name.startswith("dom_"):
#         print(f"Adding domain {sheet_name}")
#         arcpy.management.CreateDomain(ws, sheet_name, sheet_name, "TEXT", "CODED")
#         for index, row in data.iterrows():
#             val =  row['Value']
#             print(f"Adding value {val}")
#             arcpy.AddCodedValueToDomain_management(ws, sheet_name, val, val)

# Choose a coordinate system https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/pdf/projected_coordinate_systems.pdf
# sr = arcpy.SpatialReference(2229) # NAD_1983_StatePlane_California_V_FIPS_0405_Feet
sr = arcpy.SpatialReference(3857) # WGS 1984 Web Mercator (auxiliary sphere)

print("Making featureclass")
arcpy.management.CreateFeatureclass(ws, fc, "POLYGON", None, "DISABLED", "DISABLED", sr, '', 0, 0, 0, '')

df = pd.read_excel(xlsx, sheet_name=sheet, header=0)
df = df.where(pd.notnull(df), None)

for index, row in df.iterrows():
    field_name =  row['Field']
    field_type = convert_field_type(row['Type'])
    field_length =  row['Field_length'] 
    field_alias = row['Alias']
    required = True if row['Req?'] == "Yes" else False
    crosswalk_field = row['USGS_Crosswalk']
    domain_to_assign = row['Domain_name']


    ic(field_name,
        field_type,
        field_length,
        field_alias,
        required,
        crosswalk_field)

    print("Making field")
    arcpy.management.AddField(out_fc_path, 
        field_name,
        field_type,
        None,
        None,
        field_length,
        field_alias,
        True,
        required,
        domain_to_assign)

print("Adding GlobalIDs")
arcpy.management.AddGlobalIDs(out_fc_path)