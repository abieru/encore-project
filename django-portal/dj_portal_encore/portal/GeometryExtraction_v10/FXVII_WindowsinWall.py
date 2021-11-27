from . import ifcopenshell
def FXVII_WindowsinWall(ifc,GeometryAbsWalls):
	WallsId=list(GeometryAbsWalls.keys())
	WindowsbyWall={}
	for WallId in WallsId:
		Wall=ifc.by_id(WallId)
		WindowsList=[]
		IfcRelVoidsElements=Wall.HasOpenings
		for IfcRelVoidsElement in IfcRelVoidsElements:
			IfcOpeningElement=IfcRelVoidsElement.RelatedOpeningElement
			IfcRelFillsElement=IfcOpeningElement.HasFillings
			if len(IfcRelFillsElement)==1:
				IfcRelFillsElement=IfcRelFillsElement[0]
				IfcWindow=IfcRelFillsElement.RelatedBuildingElement
				if IfcWindow.is_a('IFCWINDOW'):
					WindowsList.append(IfcWindow.id())
		WindowsbyWall[Wall.id()]=WindowsList
	return WindowsbyWall
