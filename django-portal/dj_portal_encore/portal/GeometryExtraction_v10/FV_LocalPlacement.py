from . import ifcopenshell
def FV_LocalPlacement(ifcobject):
	breakage=False
	Direction=[1,0,0]
	for i in range(len(ifcobject)):
		if breakage:
			break
		if type(ifcobject[i])==ifcopenshell.entity_instance:
			if ifcobject[i].is_a('IFCLOCALPLACEMENT'):
				LocalPlacement=ifcobject[i]
				Placement3D=LocalPlacement[1]
				IfcLocation=Placement3D[0]
				Location=IfcLocation[0]
				if Placement3D[2]!=None:
					IfcDirection=Placement3D[2]
					Direction=IfcDirection[0]
				breakage=True

	return (Location,Direction)