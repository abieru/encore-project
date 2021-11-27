from . import ifcopenshell
def FIXg_Extruded_Geometry(IfcTypeRepresentation,XAxisInitial,XAxisFinal,FloorHeight):
	WallsPoints=[]
	Height=0
	IfcRectangleProfileDef=IfcTypeRepresentation[0]
	if IfcRectangleProfileDef.is_a('IFCARBITRARYCLOSEDPROFILEDEF'):
		XAreaPoints=[]
		YAreaPoints=[]
		IfcPolyline=IfcRectangleProfileDef[2]
		IfcPolyline=IfcPolyline[0]
		for Point in IfcPolyline:
			if len(Point)!=1:
				XAreaPoints.append(Point[0])
				YAreaPoints.append(Point[1])
			else:
				Point=Point[0]
				XAreaPoints.append(Point[0])
				YAreaPoints.append(Point[1])				
		XAxisInitial=min(XAreaPoints)
		XAxisFinal=max(XAreaPoints)
		MaxWidth=max(YAreaPoints)
		MinWidth=min(YAreaPoints)

	else:
		MaxWidth=IfcRectangleProfileDef[4]/2
		MinWidth=-MaxWidth
		XAxisFinal=IfcRectangleProfileDef[3]
		XAxisInitial=0
	WallsPoints.append([XAxisInitial,MaxWidth,0])
	WallsPoints.append([XAxisInitial,MinWidth,0])
	WallsPoints.append([XAxisFinal,MaxWidth,0])
	WallsPoints.append([XAxisFinal,MinWidth,0])
	if IfcTypeRepresentation.is_a('IFCEXTRUDEDAREASOLID'):
		Height=IfcTypeRepresentation.Depth
	return (WallsPoints,Height)