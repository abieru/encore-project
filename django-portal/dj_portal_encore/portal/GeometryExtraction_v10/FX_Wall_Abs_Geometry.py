from . import ifcopenshell
from .FVI_Absolute_Coord import *
def FX_Wall_Abs_Geometry(XgWalls,GeometryWalls):
	GeometryAbsWalls={}
	IdWalls=list(XgWalls.keys())
	for IdWall in IdWalls:
		ListGeometryPoints=[]
		BasePointData=XgWalls[IdWall]
		XgWall=BasePointData['Xg']
		CSWall=BasePointData['XlAxisDirection']
		WallPointsData=GeometryWalls[IdWall]
		if WallPointsData!=None:
			for WallPointData in WallPointsData:
				(Xg,CSType)=FVI_Absolute_Coord(XgWall,CSWall,WallPointData,[1,0,0],IdWall)
				ListGeometryPoints.append(list(Xg))
			GeometryAbsWalls[IdWall]=ListGeometryPoints
	return GeometryAbsWalls