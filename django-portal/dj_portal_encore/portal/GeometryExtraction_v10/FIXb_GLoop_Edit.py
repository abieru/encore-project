from . import ifcopenshell
def FIXb_GLoop_Edit(IfcPolyLoop):
	LoopPoints=[]
	HorizontalFace=[]
	FilteredPoints=[]
	for IfcCartesian in IfcPolyLoop:
		IfcCartesian=IfcCartesian[0]
		LoopPoints.append(IfcCartesian)
		HorizontalFace.append(IfcCartesian[2])
	EqualPoints=set(HorizontalFace)
	if len(EqualPoints)==1:
		FilteredPoints=LoopPoints
	return FilteredPoints