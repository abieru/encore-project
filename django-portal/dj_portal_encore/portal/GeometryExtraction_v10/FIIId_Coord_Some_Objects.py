from . import ifcopenshell
from .FIb_ParsIfc import *
from .FV_LocalPlacement import *
def FIIId_Coord_Some_Objects(ifc,typeObject):
	Objects=[]
	Objects=FIb_ParsIfc(ifc,Objects,typeObject)
	XlrelObjects={}
	for Object in Objects:
		XlrelObject={}
		(Location,Direction)=FV_LocalPlacement(Object)
		XlrelObject['Xlrel']=Location
		XlrelObject['XlAxisDirection']=Direction
		XlrelObjects[Object.id()]=XlrelObject
	return XlrelObjects