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


def convert_field_type(field_type):
    ''' Returns the field typed needed to properly generate the field. '''
    lookup = {
        "String": "TEXT",
        "Short integer": "SHORT",
        "Double": "DOUBLE",
        "Date" : "DATE",
        "Boolean": "TEXT"
    }
    return lookup.get(field_type, "Error") 


xlsx = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\RR_RarePlantFields_Agreed_Sept2022.xlsx"
sheet = "New Fields"

fc = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_1"

df = pd.read_excel(xlsx, sheet_name=sheet, header=0)
df = df.where(pd.notnull(df), None)

truncated_fields = []

for index, row in df.iterrows():
    field_name =  row['Field']
    field_type = convert_field_type(row['Type'])
    field_length =  row['Field_length'] 
    field_alias = row['Alias']
    required = True if row['Req?'] == "Yes" else False
    crosswalk_field = row['USGS_Crosswalk']

    if crosswalk_field:
        print("Altering field...")
        if len(field_name) > 31:
            truncated_fields.append(f"{field_name} - {trunc_field(field_name)}")

        ic(fc, crosswalk_field, field_name, field_alias, len(crosswalk_field), len(field_name), trunc_field(field_name), len(trunc_field(field_name)))
        arcpy.management.AlterField(fc, crosswalk_field, trunc_field(field_name), field_alias)


count_dict = {
    "Minimum": ['Min_count_int', "Min_count", "Minimum Count"],
    "Maximum": ['Max_count_int', "Max_count", "Maximum Count"],
}
print("Converting mix max count fields to int")
for key, vals in count_dict.items():
    int_name = vals[0]
    keep_name = vals[1]
    alias = vals[2]
    arcpy.management.AddField(fc, int_name, "SHORT", None, None, None, alias, "NULLABLE", "NON_REQUIRED", '')
    arcpy.management.CalculateField(fc, int_name, f"!{keep_name}!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.DeleteField(fc, keep_name, "DELETE_FIELDS")
    arcpy.management.AlterField(fc, int_name, keep_name, alias)

ic(truncated_fields)

# ic| truncated_fields: ['Representative_soil_texture_note - Representative_soil_texture_not',
#                        'Representative_surface_cover_note - Representative_surface_cover_no',
#                        'Herbarium_voucher_collector_number - Herbarium_voucher_collector_num',
#                        'Herbarium_voucher_catalog_number - Herbarium_voucher_catalog_numbe']

