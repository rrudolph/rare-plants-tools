print("Importing modules")
# import arcpy
import yaml, pathlib, arcpy

yaml_file = r"C:\GIS\Projects\CHIS_RarePlants\rare-plants-tools\build rare plants fields.yaml"

def get_config():
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
        return data

fc = r"C:\GIS\Projects\CHIS_RarePlants\Data Entry Tools\scratch.gdb\test_rare_plants_fc"

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

        arcpy.management.AddField(fc, 
            new_name,
            field_type,
            field_precision,
            field_scale,
            field_length,
            field_alias,
            field_is_nullable,
            field_is_required,
            field_domain)
        