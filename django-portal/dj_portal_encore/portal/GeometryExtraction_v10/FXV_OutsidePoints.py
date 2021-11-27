from . import ifcopenshell
def FXV_OutsidePoints(GeometryAbsWalls,WallsAbsSide):
	xac=0
	yac=0
	count=0
	WallExternalPoints={}
	XCentral=0
	Ycentral=0
	for Wall in GeometryAbsWalls:
		for Point in GeometryAbsWalls[Wall]:
			xac+=Point[0]
			yac+=Point[1]
			count+=1
	if count!=0:
		XCentral=xac/count
		Ycentral=yac/count
	for Wall in GeometryAbsWalls:
		DistanceList=[]
		ExternalsPoints=[]
		MediumPoints=WallsAbsSide[Wall]
		MediumPointSide1=MediumPoints[0]
		MediumPointSide2=MediumPoints[1]
		DistanceSide1=((MediumPointSide1[0]-XCentral)**2+(MediumPointSide1[1]-Ycentral)**2)**(1/2)
		DistanceSide2=((MediumPointSide2[0]-XCentral)**2+(MediumPointSide2[1]-Ycentral)**2)**(1/2)
		for Point in GeometryAbsWalls[Wall]:
			if DistanceSide1>DistanceSide2:
				DistanceList.append(((MediumPointSide1[0]-Point[0])**2+(MediumPointSide1[1]-Point[1])**2)**(1/2))
			else:
				DistanceList.append(((MediumPointSide2[0]-Point[0])**2+(MediumPointSide2[1]-Point[1])**2)**(1/2))
		WallsPoints=GeometryAbsWalls[Wall]
		for i in range (2):
			MinDistance=min(DistanceList)
			MinDistanceIndex=DistanceList.index(MinDistance)
			ExternalsPoints.append(WallsPoints[MinDistanceIndex])
			DistanceList.pop(MinDistanceIndex)
			WallsPoints.pop(MinDistanceIndex)
		WallExternalPoints[Wall]=ExternalsPoints
	return WallExternalPoints