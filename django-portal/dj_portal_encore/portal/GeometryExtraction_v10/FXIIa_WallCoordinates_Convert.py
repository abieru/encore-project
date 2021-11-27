from . import ifcopenshell
from .FXII_Coordinates_Convert import *
def FXIIa_WallCoordinates_Convert(GeometryAbsWalls,ifc):
	UTMZone=None
	WallsGeographicCoordinates={}
	IfcSite=ifc.by_type('IfcSite')
	IfcSite=IfcSite[0]
	GeographicalLocation=IfcSite[10]
	East=GeographicalLocation[0]+GeographicalLocation[1]*0.01
	for i in range(28,38):
		WestLimit=-18+((i-28)*6)
		EastLimit=-18+((i+1-28)*6)
		if East>WestLimit and East<EastLimit:
			UTMZone=i
			break
	for Wall in GeometryAbsWalls:
		Points=[]
		for Point in GeometryAbsWalls[Wall]:
			x=Point[0]
			y=Point[1]
			(Lon,Lat)=FXII_Coordinates_Convert(UTMZone,'N',x,y)
			Points.append([Lon,Lat,Point[2]])
		WallsGeographicCoordinates[Wall]=Points
	return(WallsGeographicCoordinates,UTMZone)