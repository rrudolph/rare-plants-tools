import arcpy
import os

ws = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb"

domain_scratch = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\domain_scratch.gdb"

domains = arcpy.da.ListDomains(ws)

for domain in domains:
    domname = domain.name
    print(domname)
    arcpy.DomainToTable_management(domain_scratch, domname, domname , "code", "desc")
