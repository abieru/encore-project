from . import ifcopenshell
from .FVI_Absolute_Coord import *
def FVIII_Abs_Walls_by_Floor(DicWalls_Floor,XgObjects,XlrelObjects):
	FloorsId=list(DicWalls_Floor.keys())
	XgWalls={}
	IdWall=None
	for Id in FloorsId:
		Floor=XgObjects[Id]
		XgFloor=Floor['Location']
		Walls=DicWalls_Floor[Id]
		for Wall in Walls:
			XgWall={}
			XlrelWall=XlrelObjects[Wall]
			RelativeLocation=XlrelWall['Xlrel']
			CSystem=XlrelWall['XlAxisDirection']
			(Xg,XlAxisDirection)=list(FVI_Absolute_Coord(list(Floor['Location']),list(Floor['XlAxisDirection']),RelativeLocation,CSystem,IdWall)) #aquí
			XgWall['Xg']=list(Xg)
			XgWall['XlAxisDirection']=list(XlAxisDirection)
			XgWalls[Wall]=XgWall
	return(XgWalls)