from . import ifcopenshell
from .FIb_ParsIfc import *
def FIV_Walls_in_floor(ifc):
	DicWalls_Floor={}
	Floors=[]
	Rels=[]
	Walls=[]
	Floors=FIb_ParsIfc(ifc,Floors,'IFCBUILDINGSTOREY')
	Rels=FIb_ParsIfc(ifc,Rels,'IFCRELCONTAINEDINSPATIALSTRUCTURE')
	Walls=FIb_ParsIfc(ifc,Walls,'IFCWALL')
	for Rel in Rels:
		ClassId=[]
		if Rel[len(Rel)-1] in Floors:
			Floor=Rel[len(Rel)-1]
			ContainsElements=Rel[len(Rel)-2]
			for Element in ContainsElements:
				if Element in Walls:
					ClassId.append(Element.id())
			DicWalls_Floor[Floor.id()]=ClassId
	return(DicWalls_Floor)