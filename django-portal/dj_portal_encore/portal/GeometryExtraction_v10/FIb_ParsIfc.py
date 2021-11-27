from . import ifcopenshell
def FIb_ParsIfc(ifc,lis,typeObject):
	lis=ifc.by_type(typeObject)
	return(lis)