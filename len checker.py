print("Importing modules")
import pandas as pd
from icecream import ic

xlsx = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\RR_RarePlantFields_Agreed_Sept2022.xlsx"
sheet = "New Fields"



df = pd.read_excel(xlsx, sheet_name=sheet, header=0)
df = df.where(pd.notnull(df), None)


for index, row in df.iterrows():
    field_name =  row['Field']
    field_length =  row['Field_length'] 
    field_alias = row['Alias']
    required = True if row['Req?'] == "Yes" else False
    crosswalk_field = row['USGS_Crosswalk']

    if len(field_name) > 31:
    	print(f'{field_name} too big {len(field_name)}')


