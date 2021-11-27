from . import ifcopenshell
from .FIb_ParsIfc import *
from .FV_LocalPlacement import *
def FIIIb_Coord_Object(ifc,typeObject):
	LisIfc=[]
	LisIfc=FIb_ParsIfc(ifc,LisIfc,typeObject)
	(Location,Direction)=FV_LocalPlacement(LisIfc[0])
	return (Location,Direction)






    