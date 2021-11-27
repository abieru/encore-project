from . import ifcopenshell
def FXI_External_Walls(GeometryAbsWalls,ifc):
	Relations=ifc.by_type('IFCRELDEFINESBYPROPERTIES')
	OutsideWalls={}
	for Wall in GeometryAbsWalls:
		for Relation in Relations:
			Object=Relation[4]
			Object=Object[0]
			ObjectId=Object.id()
			if Wall==ObjectId:
				PSet=Relation[5]
				if PSet[2]=='Pset_WallCommon':
					Properties=PSet[4]
					if len(Properties)>1:
						for Property in Properties:
							if Property[0]=='IsExternal':
								IfcBoolean=Property[2]
								if IfcBoolean[0]==True:
									OutsideWalls[Wall]=GeometryAbsWalls[Wall]
									break
					else:
						Property=Properties
						if Property[0]=='IsExternal':
							IfcBoolean=Property[2]
							if IfcBoolean[0]==True:
								OutsideWalls[Wall]=GeometryAbsWalls[Wall]
								break
					
	return(OutsideWalls)