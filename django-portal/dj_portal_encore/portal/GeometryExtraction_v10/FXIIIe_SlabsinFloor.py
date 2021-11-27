from . import ifcopenshell
def FXIIIe_SlabsinFloor(ifc):
	Floors=ifc.by_type('IFCBUILDINGSTOREY')
	Rels=ifc.by_type('IFCRELCONTAINEDINSPATIALSTRUCTURE')
	Slabs=ifc.by_type('IFCSLAB')
	DicSlabs_Floor={}
	for Rel in Rels:
		ClassId=[]
		if Rel[len(Rel)-1] in Floors:
			Floor=Rel[len(Rel)-1]
			ContainsElements=Rel[len(Rel)-2]
			for Element in ContainsElements:
				if Element in Slabs:
					ClassId.append(Element.id())
			DicSlabs_Floor[Floor.id()]=ClassId
	return DicSlabs_Floor