from . import ifcopenshell
from  .FVI_Absolute_Coord import *
def FVII_Some_Object_Absolute_Coord(XlrelObjects,XgSType,CSSType):
	ObjectsId=list(XlrelObjects.keys())
	XgObjects={}
	IdWall=None
	for Id in ObjectsId:
		XgObject={}
		RelXandCS=XlrelObjects[Id]
		RelativeLocation=list(RelXandCS['Xlrel'])
		XgObject['Location']=list(FVI_Absolute_Coord(XgSType,CSSType,RelativeLocation,RelXandCS['XlAxisDirection'],IdWall))[0] #aquí
		XgObject['XlAxisDirection']=list(FVI_Absolute_Coord(XgSType,CSSType,RelativeLocation,RelXandCS['XlAxisDirection'],IdWall))[1] #aquí
		XgObjects[Id]=XgObject
	return(XgObjects)