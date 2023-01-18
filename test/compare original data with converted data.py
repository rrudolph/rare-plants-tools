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


def get_all_values(fc, field):
   # Returns all values in a field as a list
    with arcpy.da.SearchCursor(fc, [field]) as cursor:
        return [row[0] for row in cursor]

xlsx = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\RR_RarePlantFields_Agreed_Sept2022.xlsx"
sheet = "New Fields"

source = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_1"
dest = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_ICBC"

# original_values = get_all_values(source, "UniqueID")
# new_values = get_all_values(dest, "UniqueID")

# error_vals = []

# for val in original_values:
# 	if val not in new_values:
# 		print(f"{val} Did not transfer")
# 		error_vals.append(val)

# print(", ".join(error_vals))


df = pd.read_excel(xlsx, sheet_name=sheet, header=0)
df = df.where(pd.notnull(df), None)



for index, row in df.iterrows():
    field_name =  row['Field']
    crosswalk_field = row['USGS_Crosswalk']

    if crosswalk_field:
    	print(f"******* Processing {field_name}")
    	original_values = get_all_values(source, trunc_field(field_name))
    	new_values = get_all_values(dest, field_name)
    	ic(len(original_values))
    	ic(len(new_values))

    	not_same = []
    	for orig, new in zip(original_values, new_values):
    		if orig != new:
    			if field_name == 'Representative_surface_cover_note':
    				print(f"NOT THE SAME {orig} : {new}")
    			not_same.append([orig, new])
    	if len(not_same) > 0:
    		ic(len(not_same), "<---------- PROBLEM")
    	print()
