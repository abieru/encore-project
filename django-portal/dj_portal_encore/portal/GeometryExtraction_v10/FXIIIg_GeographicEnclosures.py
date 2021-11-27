from . import ifcopenshell
from .FXII_Coordinates_Convert import *
def FXIIIg_GeographicEnclosures(EnclosuresOrderByFloor,UtmZone):
	EnclosuresOrderGeographic={}
	for Floor in EnclosuresOrderByFloor:
		GeographicPointList=[]
		for Keys in EnclosuresOrderByFloor[Floor]:
			(Lengh,Latitude)=FXII_Coordinates_Convert(UtmZone,'N',EnclosuresOrderByFloor[Floor][Keys][0],EnclosuresOrderByFloor[Floor][Keys][1])
			GeographicPointList.append([Lengh,Latitude])
		EnclosuresOrderGeographic[Floor]=GeographicPointList
	return EnclosuresOrderGeographic