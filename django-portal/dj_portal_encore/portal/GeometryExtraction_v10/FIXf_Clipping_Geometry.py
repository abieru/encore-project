from . import ifcopenshell
def FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitial,XAxisFinal,FloorHeight):
	WallsPoints=[]
	XPoint=[]
	YPoint=[]
	WallHeight=0
	Firstoperand=IfcTypeRepresentation[1]
	IfcExtrudedAreaSolid=None
	while Firstoperand.is_a()=='IfcBooleanClippingResult' or Firstoperand.is_a('IfcBooleanResult'):
		Firstoperand=Firstoperand[1]
		IfcExtrudedAreaSolid=Firstoperand
	if IfcExtrudedAreaSolid==None:
		IfcExtrudedAreaSolid=Firstoperand
	WallHeight=IfcExtrudedAreaSolid.Depth
	if IfcExtrudedAreaSolid[0].is_a('IFCARBITRARYCLOSEDPROFILEDEF'):
		IfcArbitraryClosedProfileDef=IfcExtrudedAreaSolid[0]
		IfcPolyline=IfcArbitraryClosedProfileDef[2]
		IfcCartesianPoint=IfcPolyline[0]
		for Point in IfcCartesianPoint:
			Coordinates=Point[0]
			if Coordinates[0]>=-0.01:
				XPoint.append(Coordinates[0])
			YPoint.append(Coordinates[1])
		XAxisInitial=min(XPoint)
		XAxisFinal=max(XPoint)
		MaxWidth=max(YPoint)
		MinWidth=min(YPoint)
	elif IfcExtrudedAreaSolid[0].is_a('IFCRECTANGLEPROFILEDEF'):
		
		IfcRectangleProfileDef=IfcExtrudedAreaSolid[0]
		MaxWidth=IfcRectangleProfileDef[4]/2
		MinWidth=-MaxWidth
		XAxisFinal=IfcRectangleProfileDef[3]
		XAxisInitial=0
	else:
		Width=0
	WallsPoints.append([XAxisInitial,MaxWidth,0])
	WallsPoints.append([XAxisInitial,MinWidth,0])
	WallsPoints.append([XAxisFinal,MaxWidth,0])
	WallsPoints.append([XAxisFinal,MinWidth,0])		
	return (WallsPoints, WallHeight)