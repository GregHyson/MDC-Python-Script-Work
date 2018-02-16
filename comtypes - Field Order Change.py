import os
from comtypes.client import GetModule, CreateObject
from snippets105 import GetStandaloneModules, InitStandalone, GetDesktopModules
import snippets105

GetStandaloneModules()
InitStandalone()
GetDesktopModules()
esriCarto = GetModule(r"C:\Program Files (x86)\ArcGIS\Desktop10.5\com\esriCarto.olb")
arcMapUI = GetModule(r"C:\Program Files (x86)\ArcGIS\Desktop10.5\com\esriArcMapUI.olb")
geoDBUI = GetModule(r"C:\Program Files (x86)\ArcGIS\Desktop10.5\com\esriGeoDatabaseUI.olb")
esriSystem = GetModule(r"C:\Program Files (x86)\ArcGIS\Desktop10.5\com\esriSystem.olb")
# Layers, in order of importance
layer_order = [ 'Address', 'Location', 'Pipe_Nom_Dia', 'Pipe_Material',
                'Depth', 'Plan_Number', 'AMIS_ID','Asset_RID',
                'Asset_Stage','Install_Date','OBJECTID']


#-------------------------------------------------------------------------------
# Setting the current application mx document so you can get access to the table window
pApp = snippets105.GetCurrentApp()
pDoc = pApp.Document
print type(pDoc)
pMxDoc = snippets105.CType(pDoc, arcMapUI.IMxDocument)
pMap = pMxDoc.FocusMap
print type(pMxDoc)
print type(pMap)
pEnumLayer = pMap.Layers(None,True)
pLayer = pEnumLayer.Next()
print type(pLayer)

while pLayer:
    field_names = []
    pGeoFeatureLayer = snippets105.CType(pLayer,esriCarto.IGeoFeatureLayer)
    print type(pGeoFeatureLayer)
    if pGeoFeatureLayer:
        fields = pGeoFeatureLayer.QueryInterface(interface = esriCarto.ILayerFields)
        for i in xrange(fields.FieldCount):
            field_names.append(fields.Field(i).Name)
            
#-------------------------------------------------------------------------------
            
        ordered_fields = []
        for lo in layer_order:
            for fn in field_names:
                if fn.endswith(lo):
                    ordered_fields.append(fn)
                    field_names.remove(fn)
                    break
                
        while len(field_names) > 0:
            tbc = field_names.pop(0)
            ordered_fields.append(tbc)
        str_conversion = ','.join(ordered_fields)
        new_order = '"' + str_conversion + '"'
        
#-------------------------------------------------------------------------------      
        pTableWindow = arcMapUI.TableWindow()
        print type(pTableWindow)
        pTableWindow.blah = pGeoFeatureLayer
        print type(pTableWindow.blah)
        pTableWindow.FeatureLayer = pGeoFeatureLayer
        print type(pTableWindow.FeatureLayer)
        pTableWindow.Application = pApp
        print type(pTableWindow.Application)
        pTableWindow.ShowAliasNamesInColoumnHeadings = True
        if pTableWindow.ShowAliasNamesInColoumnHeadings:
            print "pTableWindow is using Alias Names for Headers."
        pTableWindow.Show = True
        if pTableWindow.Show:
            print "pTableWindow is Showing."
        
#--------------------------------------------------------------------------------
        
        pTableProperty = arcMapUI.ITableProperty()
        print type(pTableProperty)
        
        pTableProperties = pMxDoc.TableProperties
        print type(pTableProperties)
        pEnumTableProperties = pTableProperties.IEnumTableProperties
        print type(pEnumTableProperties)
        pEnumTableProperties.Reset        
        print type(pEnumTableProperties)
        pTableProperty = pEnumTableProperties
        print type(pTableProperty)
        
        pTableProperty.FieldOrder = new_order
        print "New Field Order : " + pTableProperty.FieldOrder                
        
#--------------------------------------------------------------------------------
# This seciton of the code is broken and requires more work.
# I have a sneaking suspiscion there has been a change to the implementation of TableWindow
# or Table Control that I have not been able to find record of.
        pTableWindow.Show = True
        if pTableWindow.Show:
            print "pTableWindow is still Showing."
        
        pConvTable = snippets105.CType(pTableWindow,arcMapUI.ITableWindow3)
        pTableWindows = pConvTable.IsVisible()
        if pTableWindows:
            print type(pTableWindows)
        #if pConvTable.Show:
            #print "pConvTable is also"
        pTableControl = geoDBUI.ITableControl3()
        print type(pTableControl)
        print type(pConvTable.TableControl)
        break
#--------------------------------------------------------------------------------
    print "\n"
    pLayer = pEnumLayer.Next()
