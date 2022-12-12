import arcpy


ws = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb"



domains = arcpy.da.ListDomains(ws)

for domain in domains:
	print(domain.name)