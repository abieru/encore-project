from . import ifcopenshell
def FIa_Open(Archive):
	ifc=ifcopenshell.open(Archive)
	return ifc
