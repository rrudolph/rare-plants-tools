import arcpy
import pandas as pd
from tabulate import tabulate

def get_sorted_fields(fc):
	fieldNames = [f for f in arcpy.ListFields(fc) if f]
	return sorted(fieldNames)

source = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_1"
dest = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_ICBC"

source_fields = get_sorted_fields(source)
for field in source_fields:
	print(field)

# dest_fields = get_sorted_fields(dest)

# data_dict = {}
# data_dict['Source']		= map(lambda f: f, source_fields)
# data_dict['Dest']		= map(lambda f: f, dest_fields)

# print(tabulate(data_dict, headers="keys")) #  tablefmt="grid"
