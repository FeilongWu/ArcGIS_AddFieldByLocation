import arcpy
import pythonaddins


class ButtonClass1(object):
    """Implementation for RoadConvertsion_AddField_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        self.massenger=arcpy.env.workspace+'\\'+'AddField_variables.txt'
    def onClick(self):
        f=open(self.massenger,'r')
        for i in f:
            content=i
        f.close()
        path1,selectedAttr,Type,target=content.split('|')
        f_values=[]
        geometries=[]
        arcpy.env.workspace=path1
        cursor = arcpy.SearchCursor(path1)
        for item in cursor:
            geometries.append(item.getValue('Shape'))
            f_values.append(item.getValue(selectedAttr))
        arcpy.env.workspace=target
        arcpy.AddField_management(target,selectedAttr,Type)
        targetFeature=[]
        Tcursor=arcpy.SearchCursor(target)
        for item in Tcursor:
            targetFeature.append(item.getValue('Shape'))
        cursor=None
        Tcursor=None
        Id=-1
        if Type=='String':
            NaN='Null'
        else:
            NaN=0
        with arcpy.da.UpdateCursor(target,selectedAttr) as cursor:
            for entry in cursor:
                Id+=1
                index=0
                length=len(geometries)
                for geo in geometries:
                    if geo.within(targetFeature[Id]):
                        entry[0]=f_values[index]
                        cursor.updateRow(entry)
                        break
                    index+=1
                    if index==length:
                        entry[0]=NaN
                        cursor.updateRow(entry)
                if index!=length:
                    geometries.pop(index)
                    f_values.pop(index)
        
                    

class ComboBoxClass1(object):
    """Implementation for RoadConvertsion_AddField_addin.combobox (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.massanger=arcpy.env.workspace
    def onSelChange(self, selection):
        layer = arcpy.mapping.ListLayers(self.mxd, selection)[0]
        arcpy.env.workspace=layer.workspacePath+'\\'+layer.name
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        self.mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(self.mxd)
        self.items = []
        for layer in layers:
            self.items.append(layer.name)
        f=open(self.massanger+'\\'+'AddField_variables.txt','w')
        f.close()
        
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ComboBoxClass2(object):
    """Implementation for RoadConvertsion_AddField_addin.combobox_1 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.massenger=''
        self.massenger1=arcpy.env.workspace+'\\'+'AddField_variables.txt'
        self.attributes=[]
        self.attTypes=[]
    def onSelChange(self, selection):
        selectedAttr=selection
        Type=self.attTypes[self.attributes.index(selectedAttr)]
        self.massenger+='|'+selectedAttr+'|'+Type
        f=open(self.massenger1,'w')
        f.write(self.massenger)
        f.close()
        
        
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        input_fc=arcpy.env.workspace
        fc1=input_fc.split('\\')
        name1=fc1[-1]
        name=name1+'.shp'
        path=''
        for i in range(len(fc1[0:-1])):
            path+=fc1[i]
            if i != len(fc1[0:-1])-1:
                path+='\\'
        arcpy.env.workspace=path
        for attr in arcpy.ListFields(name):
            if attr.aliasName in ['FID','Shape','Shape@']:
                continue
            else:
                self.attributes.append(attr.aliasName)
                self.attTypes.append(attr.type)
        input_fc+='.shp'
        self.massenger=input_fc
        self.items=self.attributes
    def onEnter(self):
        pass
    def refresh(self):
        pass

class ComboBoxClass3(object):
    """Implementation for RoadConvertsion_AddField_addin.combobox_2 (ComboBox)"""
    def __init__(self):
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        self.massenger1=arcpy.env.workspace+'\\'+'AddField_variables.txt'
    def onSelChange(self, selection):
        layer = arcpy.mapping.ListLayers(self.mxd, selection)[0]
        path=layer.workspacePath+'\\'+layer.name
        file=open(self.massenger1,'r')
        for i in file:
            content=i
        file.close()
        content+='|'+path+'.shp'
        file=open(self.massenger1,'w')
        file.write(content)
        file.close()
        
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        self.mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(self.mxd)
        self.items = []
        for layer in layers:
            self.items.append(layer.name)
        
        
    def onEnter(self):
        pass
    def refresh(self):
        pass
