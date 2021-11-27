from . import ifcopenshell
from .FXIIId_Angle_Calculation import *
def FXIIIc_Order_Enclosures(ifc,DicWalls,GeometryAbsWalls):
	Floors=ifc.by_type('IFCBUILDINGSTOREY')
	EnclosuresOrder={}
	EnclosuresOrderbyFloor={}
	CenterPointX=0
	CenterPointY=0
	for Floor in Floors:
		Counter=0
		Walls=DicWalls[Floor.id()]
		for Wall in Walls:
			if Wall in GeometryAbsWalls:
				for Point in GeometryAbsWalls[Wall]:
					CenterPointX+=Point[0]
					CenterPointY+=Point[1]
					Counter+=1
		if Counter!=0:
			CenterPointX=CenterPointX/Counter
			CenterPointY=CenterPointY/Counter
		PointsList=[]
		AngleList=[]
		for Wall in Walls:
			if Wall in GeometryAbsWalls:
				for Point in GeometryAbsWalls[Wall]:
					AngletoCenter=FXIIId_Angle_Calculation(CenterPointX=CenterPointX,CenterPointY=CenterPointY,Point=Point)
					PointsList.append(Point)
					AngleList.append(AngletoCenter)
		AngleListOrder=sorted(AngleList)
		OrderPointDict={}
		Counter=1
		for Point in AngleListOrder:
			OrderPointDict[Counter]=PointsList[AngleList.index(Point)]
			Counter+=1
		EnclosuresOrderbyFloor[Floor.id()]=OrderPointDict
	return EnclosuresOrderbyFloor