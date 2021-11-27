from . import ifcopenshell
def FIXc_Wall_Axis_Points(IfcProductDefinitionShape):
    IfcShapeRepresentation1=IfcProductDefinitionShape[2]
    IfcShapeRepresentation1=IfcShapeRepresentation1[0]
    IfcPolyline=IfcShapeRepresentation1[len(IfcShapeRepresentation1)-1]
    IfcPolyline=IfcPolyline[0]
    if len(IfcPolyline)==2:
	    IfcPolyline=IfcPolyline[0]
	    IfcCartesianPoint=IfcPolyline[1]
	    XaxisFinalPoint=IfcCartesianPoint[0]
	    XaxisFinalPoint=XaxisFinalPoint[0]
	    IfcCartesianPoint=IfcPolyline
	    XaxisInitialPoint=IfcCartesianPoint[0]
	    XaxisInitialPoint=XaxisInitialPoint[0]
	    XaxisInitialPoint=XaxisInitialPoint[0]
    else:
        XaxisInitialPoint=None
        XaxisFinalPoint=None
    return(XaxisInitialPoint,XaxisFinalPoint)