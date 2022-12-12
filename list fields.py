import arcpy
import pandas as pd
from tabulate import tabulate

def get_new_field(df, in_val):
	try:
		out_val = df.loc[df['USGS_Crosswalk'] == in_val, 'Field'].iloc[0]
	except:
		out_val = None

	return(out_val)

fc = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly"


xlsx = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\RR_RarePlantFields_Agreed_Sept2022.xlsx"
sheet = "New Fields"

df = pd.read_excel(xlsx, sheet_name=sheet, header=0)
df = df.where(pd.notnull(df), None)



fieldNames = [f for f in arcpy.ListFields(fc)]

data_dict = {}
data_dict['Old Name']	= map(lambda f: f.name, fieldNames)
data_dict['New Name']	= map(lambda f: get_new_field(df, f.name), fieldNames)
data_dict['Type']		= map(lambda f: f.type, fieldNames)
data_dict['Length']		= map(lambda f: f.length, fieldNames)
data_dict['Domain']		= map(lambda f: f.domain, fieldNames)

print(tabulate(data_dict, headers="keys")) #  tablefmt="grid"

