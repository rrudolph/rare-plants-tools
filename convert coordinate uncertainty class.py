'''
Convert the text-based description of the accuracy uncertainty to an actual number value.
'''

import arcpy
from tabulate import tabulate


def get_unique_values(fc, field):
    '''Returns unique values of a field into a list'''
    with arcpy.da.SearchCursor(fc, [field]) as cursor:
        return {row[0] for row in cursor if row[0] is not None}


def val_lookup(val):

   switcher = {
    '1 to 10m'              : 10, 
    'Greater than 10,000m'  : 99999, 
    '100 to 1,000m'         : 1000, 
    'Less than 1m'          : 1, 
    '1,000 to 10,000m'      : 10000, 
    '10 to 100m'            : 100
    }

   return switcher.get(val, False)

fc = r"C:\GIS\Projects\CHIS_RarePlants\ICBC Database Conversion\CHIS_Rare_Plants_20221208.gdb\RarePlants_Poly_ICBC"


#  Coordinate uncertainity
vals = get_unique_values(fc, "CoordUncertClass")
with arcpy.da.UpdateCursor(fc, ['CoordUncertClass', 'Accuracy_meters']) as cursor:
    for row in cursor:
        val = row[0]
        if val_lookup(val):
            print(f"Converting {val} to {val_lookup(val)}")
            row[1] = val_lookup(val)
            cursor.updateRow(row)
print("Done")

## Aspect field

# vals = get_unique_values(fc, "Aspect")
# val_dict = {} # Make a dictionary by mapping over the errors list and accessing each of the items in the tuples.
# val_dict["Aspect Values"]          = map(lambda d: d, vals)
# val_dict["Is Numeric Value?"]     = map(lambda d: d.isnumeric(), vals)
# print(tabulate(val_dict, headers="keys")) 