from . import ifcopenshell
def FIXb_Geometry_Loop(IfcPolyLoop,XAxisInitial,XAxisFinal,FloorHeight,Find,BaseFace):
	Xlrel=[]
	FilterPoints=[]
	FilteredPoints=[]
	if  XAxisInitial!=None:
		for IfcCartesian in IfcPolyLoop:
			IfcCartesian=IfcCartesian[0]
			Xlrel.append(IfcCartesian)
		for Point in Xlrel:
			if Point[0]==XAxisInitial or Point[0]== XAxisFinal:
				if Point[2]==FloorHeight:
					width=abs(Point[1])
					Find=True
		FilteredPoints.append([XAxisInitial,width,0])
		FilteredPoints.append([XAxisInitial,-width,0])
		FilteredPoints.append([XAxisFinal,width,0])
		FilteredPoints.append([XAxisFinal,-width,0])
	else:
		LoopPoints=[]
		BaseFacePoints=0
		for IfcCartesian in IfcPolyLoop:
			IfcCartesian=IfcCartesian[0]
			LoopPoints.append(IfcCartesian)
		for Point in LoopPoints:
			if Point[0]>=-0.01 and Point[2]>=(FloorHeight-0.1) and Point[2]<=(FloorHeight+0.1):
				BaseFacePoints+=1
		if BaseFacePoints==4 or BaseFacePoints==len(LoopPoints):
			BaseFace=True
			FilteredPoints=LoopPoints
	return (FilteredPoints,Find,BaseFace)