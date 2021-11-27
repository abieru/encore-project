from . import ifcopenshell
def FIXh_AdvanceBrep_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight):
	WallsPoints=[]
	XPoints=[]
	YPoints=[]
	IFcAdvanceBrep=IfcTypeRepresentation
	Width=0
	WidthFind=False
	IfcClosedShell=IFcAdvanceBrep[0]
	CfsFaces=IfcClosedShell[0]
	for IfcAdvanceFace in CfsFaces:
		IfcPlane=IfcAdvanceFace[1]
		IfcAxis2Placment3D=IfcPlane[0]
		IfcCartesianPoint=IfcAxis2Placment3D[0]
		LocationData=IfcCartesianPoint[0]
		if LocationData[0]>=-0.01:
			XPoints.append(LocationData[0])
			YPoints.append(LocationData[1])
	XAxisInitialPoint=min(XPoints)
	XAxisFinalPoint=max(XPoints)
	Width=max(YPoints)
	WallsPoints.append([XAxisInitialPoint,Width,0])
	WallsPoints.append([XAxisInitialPoint,-Width,0])
	WallsPoints.append([XAxisFinalPoint,Width,0])
	WallsPoints.append([XAxisFinalPoint,-Width,0])
	return WallsPoints