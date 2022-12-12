'''

NOT WORKING, 

'''

print("Importing modules")
import arcpy
import pandas as pd
from os.path import join
from icecream import ic

def trunc_field(field):
    if len(field) > 31:
        return field[:31]
    else:
        return field

source = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_1"
dest = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_ICBC"

source_fields = [f for f in arcpy.ListFields(source)]
dest_fields = [f for f in arcpy.ListFields(dest)]

fm = arcpy.FieldMappings()

for dest_field in dest_fields:
    if dest_field.name not in ['OBJECTID', 'Shape', 'Shape_Length', "Shape_Area"]:
        print(f"\t...Creating a field map object for {dest_field.name}")
        fMap = arcpy.FieldMap()
        for source_field in source_fields:
            if trunc_field(dest_field.name) == source_field.name:
                ic(trunc_field(dest_field.name),source_field.name)
                fMap.addInputField(source, source_field.name)

        # set the output name
        print("\t...Setting the output name.")
        outputFieldName = fMap.outputField
        outputFieldName.name = dest_field.name
        fMap.outputField = outputFieldName
        
        # add the field map to the field mappings object
        print("\t...Adding the field map to the field mappings object.")
        fm.addFieldMap(fMap)

# perform the append
print("\nAppending!")
arcpy.Append_management(source, dest, "NO_TEST", fm)