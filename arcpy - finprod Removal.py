# This is my attempt at completing this using the base arcpy module. It needs to be noted that the functionality
# I was looking for does not currently exist within the base arcpy module and the 
# final implementation of this method is done using the comtype module.
# The reason behind this is that there are two versions of filed aliases stored seperate from each other,
# one in the mxd and one in the GDB. The arcpy module only gives functionality to change the version stored within the GDB
# which is considerably more permanent.

import arcpy

# Debugger txt file path for Grant or Gregs work PC
ghydebugger = open('S:\Ghy\Development\printhere.txt', 'a')
# gmudebugger = open('S:\Gmu\WorkingDrafts\Script Work\Debugging.txt','a')

# Workspace will never change for the layers within AMIS Services (Joins)
arcpy.env.workspace = "G:\ArcGIS\Desktop105\DataConnections\GISTM.sde"


mxd = arcpy.mapping.MapDocument ("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)
for layer in layers:
    if not layer.isGroupLayer:
        ghydebugger.write("Layer name = " + layer.name + "\n")

        fcList = arcpy.ListFeatureClasses() #get a list of feature classes
        for fc in fcList:  #loop through feature classes
            fieldList = arcpy.ListFields(fc)  #get a list of fields for each feature class
            for field in fieldList: #loop through each field
                                        
                ghydebugger.write("Field Name = " + field.aliasName + "\n")
                        
                #if field.aliasName.startswith('finprod.dbo.vusrGIS_ASSET_UF.'):
                 #   new_alias = field.aliasName[29:]
                  #  ghydebugger.write("New Alias = " + new_alias + "\n")
                   # arcpy.AlterField_management(fc, field.name, '', new_alias)

