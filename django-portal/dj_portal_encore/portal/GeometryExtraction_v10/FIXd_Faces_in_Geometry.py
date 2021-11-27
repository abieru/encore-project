from . import ifcopenshell
from .FIXb_Geometry_Loop import *
from .FIXb_GLoop_Edit import *
def FIXd_Faces_in_Geometry(IfcFaces,XAxisInitial,XAxisFinal,FloorHeight):
	Points=[]
	BasePoints=[]
	Find=False
	Height=0
	if XAxisInitial!=None:
		for Face in IfcFaces:
			Face=Face[0]
			IfcPolyLoop=Face[0]
			IfcPolyLoop=IfcPolyLoop[0]
			IfcPolyLoop=IfcPolyLoop[0]
			if Find==False:
				(Points,Find)=FIXb_Geometry_Loop(IfcPolyLoop,XAxisInitial,XAxisFinal,FloorHeight,Find)
	else:
		for Face in IfcFaces:
			BaseFace=False
			Face=Face[0]
			IfcPolyLoop=Face[0]
			IfcPolyLoop=IfcPolyLoop[0]
			IfcPolyLoop=IfcPolyLoop[0]
			(FilteredPoints,Find,BaseFace)=FIXb_Geometry_Loop(IfcPolyLoop,XAxisInitial,XAxisFinal,FloorHeight,Find,BaseFace)
			if BaseFace==True:
				BasePoints.append(FilteredPoints)
		if len(BasePoints)==0:
			for Face in IfcFaces:
				BaseFace=False
				Face=Face[0]
				IfcPolyLoop=Face[0]
				IfcPolyLoop=IfcPolyLoop[0]
				IfcPolyLoop=IfcPolyLoop[0]
				FilteredPoints=FIXb_GLoop_Edit(IfcPolyLoop)
				if len(FilteredPoints)!=0:
					BasePoints.append(FilteredPoints)
		Xpoints=[]
		Ypoints=[]	
		for BasePoint in BasePoints:
			for Point in BasePoint:
				Xpoints.append(Point[0])
				Ypoints.append(Point[1])
		if len(Xpoints)>0:
			Xmin=min(Xpoints)
			Xmax=max(Xpoints)
			MinWidth=min(Ypoints)	
			MaxWidth=max(Ypoints)
			Points.append([Xmin,MinWidth,FloorHeight])
			Points.append([Xmin,MaxWidth,FloorHeight])
			Points.append([Xmax,MinWidth,FloorHeight])
			Points.append([Xmax,MaxWidth,FloorHeight])
	for Face in IfcFaces:
		IfcFaceOuterBound=Face.Bounds[0]
		XCoordinatePoints=[]
		YCoordinatePoints=[]
		ZCoordinatePoints=[]
		IfcPolyLoop=IfcFaceOuterBound.Bound
		Polygon=IfcPolyLoop.Polygon
		for IfcCartesianPoint in Polygon:
			XCoordinatePoints.append(IfcCartesianPoint.Coordinates[0])
			YCoordinatePoints.append(IfcCartesianPoint.Coordinates[1])
			ZCoordinatePoints.append(IfcCartesianPoint.Coordinates[2])
			ZOrderPoints=list(set(ZCoordinatePoints))
		if len(set(YCoordinatePoints))==1 and len(set(XCoordinatePoints))==2 and len(set(ZCoordinatePoints))==2:
			Height=float(abs(ZOrderPoints[0]-ZOrderPoints[1]))
	return (Points,Height)