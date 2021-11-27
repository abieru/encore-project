from . import ifcopenshell
def FIIIa_Coord_Project (ifc):
	Project=ifc.by_type('IFCPROJECT')[0]
	LisRepContext=Project[len(Project)-2]
	RepContext=LisRepContext[0]
	Lis3DPlacement=RepContext[len(RepContext)-2]
	Placement=Lis3DPlacement[0]
	XProject=Placement[0]
	return XProject