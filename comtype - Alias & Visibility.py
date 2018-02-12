import os
from comtypes.client import GetModule, CreateObject
from snippets105 import GetStandaloneModules, InitStandalone, GetDesktopModules
import snippets105

GetStandaloneModules()
InitStandalone()
GetDesktopModules()
esriCarto = GetModule(r"C:\Program Files (x86)\ArcGIS\Desktop10.5\com\esriCarto.olb")
arcMapUI = GetModule(r"C:\Program Files (x86)\ArcGIS\Desktop10.5\com\esriArcMapUI.olb")

# Layers, in order of importance
layer_order = ['Address', 'Location', 'Pipe_Nom_Dia', 'Pipe_Material',
                   'Depth', 'Plan_Number', 'AMIS_ID','Asset_RID',
                   'Asset_Stage','Install_Date']

#----------------------------------------------------------------------
def fix_packages_alias_visibility(mxd_path,output_mxd_path=None):
    
    # Create a new map document and extract out the layers into an acceessible format    
    pMapDocument = CreateObject(esriCarto.MapDocument, interface=esriCarto.IMapDocument)
    pMapDocument.Open(mxd_path)
    pMap = pMapDocument.Map(0)
    pEnumLayer = pMap.Layers(None,True)
    pLayer = pEnumLayer.Next()



    # Fields to be made not to be visible
    unwanted_visible = ['AssetID','Site','Pressure_Zone','Service_Area',
                        'Supply_Area','AMIS_ID','Search_Description',
                        'Short_Description','ASSET_RID','Condition',
                        'Owner','Maint_Responsibility','GIS_LINK','Street',
                        'Locality','Criticality_Rating',
                        'Maintenance_Start_Date','Maintenance_End_Date',
                        'Useful_Service_Life','Base_Service_Life','aquisition_method',
                        'Year_Planned_Replace','Remaining_Life','ASSNBRI',
                        'Peak_Structural_Condition','Mean_Structural_Condition',
                        'Peak_Service_Condition','Mean_Service_Condition',
                        'ASSET_RID','ASSID','GIS_ID','GIS_LAYER', 'SHAPE',
                        'SHAPE.len', 'Catchment', 'Sub-Catchment', 'Risk_Rating'
                        'Install_Date_Reliability','Plan_Reliability',
                        'Material_Reliability', 'Diameter_Reliability']
    
    # Fields that defaultly have the finprod added to the front
    change_me = ['AMIS_Edited_Date', 'AMIS_Edited_User']

    while pLayer:
        
        # Checks wether the layer has features on it or is a Group Layer
        pGeoFeatureLayer = snippets105.CType(pLayer,esriCarto.IGeoFeatureLayer)
        if pGeoFeatureLayer:     
            # If it does have features then we want to open the interface that allows us to get access to the fields
            fields = pGeoFeatureLayer.QueryInterface(interface = esriCarto.ILayerFields)
            
            # Looping through the fields in the GeoFeatureLayer
            for i in xrange(fields.FieldCount):

                # Print out the current field alias
                current_alias = fields.Field(i).AliasName
                print "Current Alias : " + current_alias

                # Checks to see if the Alias is in need of fixing and if so, fixes it
                if current_alias.startswith('finprod.dbo.vusrGIS_ASSET_UF'):
                    fields.FieldInfo(i).Alias = current_alias[29:]
                    print "Changed Alias : " + fields.FieldInfo(i).Alias
                    current_alias = fields.FieldInfo(i).Alias
                for cm in change_me:
                    if current_alias.endswith(cm):
                        print "Changed Alias to : " + cm
                        fields.FieldInfo(i).Alias = cm
                # Checks to see if the field should be visible or not, and if not, hides it
                for uv in unwanted_visible:
                    if current_alias.endswith(uv):
                        fields.FieldInfo(i).Visible = False
                        print "Set : " + current_alias + " to being : Hidden."
                print "\n"
        pLayer = pEnumLayer.Next()

    # Creation of the new file path for the mxd
    if not output_mxd_path:
        output_mxd_path = os.path.join(os.path.dirname(mxd_path),os.path.splitext(os.path.basename(mxd_path))[0] + '_AV_CT' +
                                       os.path.splitext(os.path.basename(mxd_path))[1])

    # Saving as the new mxd
    pMapDocument.SaveAs(output_mxd_path)
    print "Finished!"
    return output_mxd_path


# CHANGE ME
mxd_path = r"S:\Ghy\Development\ComtypeInstallation\Test Map.mxd"


print fix_packages_alias_visibility(mxd_path)

