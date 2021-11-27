from . import ifcopenshell
def FXVI_WindowArea(ifc):
	def WindowAreaFace(IfcFace):
		IfcFaceOuterBound=IfcFace.Bounds[0]
		XCoordinatePoints=[]
		YCoordinatePoints=[]
		ZCoordinatePoints=[]
		Area=0
		IfcPolyLoop=IfcFaceOuterBound.Bound
		Polygon=IfcPolyLoop.Polygon
		for IfcCartesianPoint in Polygon:
			XCoordinatePoints.append(IfcCartesianPoint.Coordinates[0])
			YCoordinatePoints.append(IfcCartesianPoint.Coordinates[1])
			ZCoordinatePoints.append(IfcCartesianPoint.Coordinates[2])
		if len(set(YCoordinatePoints))==1 and len(set(XCoordinatePoints))==2 and len(set(ZCoordinatePoints))==2:
			Area=abs((list(set(XCoordinatePoints))[0]-list(set(XCoordinatePoints))[1])*(list(set(ZCoordinatePoints))[0]-list(set(ZCoordinatePoints))[1]))
		return Area
	Area={}
	Windows=ifc.by_type('IFCWINDOW')
	for Window in Windows:
		FaceArea=[]
		FillsVoids=Window.FillsVoids[0]
		IfcOpeningElement=FillsVoids.RelatingOpeningElement
		IfcProductDefinitionShape=IfcOpeningElement.Representation
		IfcShapeRepresentation=IfcProductDefinitionShape.Representations[0]
		if IfcShapeRepresentation.RepresentationType=='Brep':
			IfcFacetedBrep=IfcShapeRepresentation.Items[0]
			IfcClosedShell=IfcFacetedBrep.Outer
			IfcFaces=IfcClosedShell.CfsFaces
			for IfcFace in IfcFaces:
				FaceArea.append(WindowAreaFace(IfcFace))
			DiferentsAreas=list(set(FaceArea))
			DiferentsAreas.remove(0)
			if len(DiferentsAreas)==1:
				Area[Window.id()]=DiferentsAreas[0]
		elif IfcShapeRepresentation.RepresentationType=='SweptSolid':
			if IfcShapeRepresentation.Items[0].is_a('IfcExtrudedAreaSolid'):
				IfcExtrudedAreaSolid=IfcShapeRepresentation.Items[0]
				IfcRectangleProfileDef=IfcExtrudedAreaSolid.SweptArea
				Area[Window.id()]=IfcRectangleProfileDef.XDim*IfcRectangleProfileDef.YDim
	return Area