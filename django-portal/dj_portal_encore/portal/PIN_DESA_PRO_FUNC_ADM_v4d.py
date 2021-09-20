import ifcopenshell
import numpy as np
import pyproj
import json
from pathlib import Path
BASE_DIR2 = Path(__file__).resolve().parent.parent
def FIa_Open(Archive):
	ifc=ifcopenshell.open(Archive)
	return ifc

def FIb_ParsIfc(ifc,lis,typeObject):
	lis=ifc.by_type(typeObject)
	return(lis)

def FIIIa_Coord_Project (ifc):
	Project=ifc.by_type('IFCPROJECT')[0]
	LisRepContext=Project[len(Project)-2]
	RepContext=LisRepContext[0]
	Lis3DPlacement=RepContext[len(RepContext)-2]
	Placement=Lis3DPlacement[0]
	XProject=Placement[0]
	return XProject

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

def FIIIb_Coord_Object(ifc,typeObject):
	LisIfc=[]
	LisIfc=FIb_ParsIfc(ifc,LisIfc,typeObject)
	(Location,Direction)=FV_LocalPlacement(LisIfc[0])
	return (Location,Direction)

def FIIIc_Coord_Processing(Loc,Dir,IdWall):
    Xgrel=None
    IdWall
    Xlrel=list((Loc))
    RotXAxis=list(Dir)
    if Xlrel[0]!=None and Xlrel[1]!=None and Xlrel[2]!=None:
        DirMatrix=([RotXAxis,[-RotXAxis[1],RotXAxis[0],RotXAxis[2]],[0,0,1]])
        Xgrel=np.dot(np.linalg.inv(DirMatrix),Xlrel)
    return (Xgrel)

def FIIId_Coord_Some_Objects(ifc,typeObject):
	Objects=[]
	Objects=FIb_ParsIfc(ifc,Objects,typeObject)
	XlrelObjects={}
	for Object in Objects:
		XlrelObject={}
		(Location,Direction)=FV_LocalPlacement(Object)
		XlrelObject['Xlrel']=Location
		XlrelObject['XlAxisDirection']=Direction
		XlrelObjects[Object.id()]=XlrelObject
	return XlrelObjects

def FIV_Walls_in_floor(ifc):
	DicWalls_Floor={}
	Floors=[]
	Rels=[]
	Walls=[]
	Floors=FIb_ParsIfc(ifc,Floors,'IFCBUILDINGSTOREY')
	Rels=FIb_ParsIfc(ifc,Rels,'IFCRELCONTAINEDINSPATIALSTRUCTURE')
	Walls=FIb_ParsIfc(ifc,Walls,'IFCWALL')
	for Rel in Rels:
		ClassId=[]
		if Rel[len(Rel)-1] in Floors:
			Floor=Rel[len(Rel)-1]
			ContainsElements=Rel[len(Rel)-2]
			for Element in ContainsElements:
				if Element in Walls:
					ClassId.append(Element.id())
			DicWalls_Floor[Floor.id()]=ClassId
	return(DicWalls_Floor)

def FVI_Absolute_Coord(XgSType,CSSType,Xlrel,CSType,IdWall):
    Xgrel=FIIIc_Coord_Processing(Xlrel,CSSType,IdWall)
    Xg=None
    Xg=XgSType+Xgrel
    XaxisSType=list(CSSType)
    XaxisType=list(CSType)
    MCSSType=([XaxisSType,[-XaxisSType[1],XaxisSType[0],XaxisSType[2]],[0,0,1]])
    MCSType=([XaxisType,[-XaxisType[1],XaxisType[0],XaxisType[2]],[0,0,1]])
    CSType=np.dot(MCSType,MCSSType)[0]
    return(Xg,CSType)

def FVII_Some_Object_Absolute_Coord(XlrelObjects,XgSType,CSSType):
	ObjectsId=list(XlrelObjects.keys())
	XgObjects={}
	IdWall=None
	for Id in ObjectsId:
		XgObject={}
		RelXandCS=XlrelObjects[Id]
		RelativeLocation=list(RelXandCS['Xlrel'])
		XgObject['Location']=list(FVI_Absolute_Coord(XgSType,CSSType,RelativeLocation,RelXandCS['XlAxisDirection'],IdWall))[0] #aquí
		XgObject['XlAxisDirection']=list(FVI_Absolute_Coord(XgSType,CSSType,RelativeLocation,RelXandCS['XlAxisDirection'],IdWall))[1] #aquí
		XgObjects[Id]=XgObject
	return(XgObjects)

def FVIII_Abs_Walls_by_Floor(DicWalls_Floor,XgObjects,XlrelObjects):
	FloorsId=list(DicWalls_Floor.keys())
	XgWalls={}
	IdWall=None
	for Id in FloorsId:
		Floor=XgObjects[Id]
		XgFloor=Floor['Location']
		Walls=DicWalls_Floor[Id]
		for Wall in Walls:
			XgWall={}
			XlrelWall=XlrelObjects[Wall]
			RelativeLocation=XlrelWall['Xlrel']
			CSystem=XlrelWall['XlAxisDirection']
			(Xg,XlAxisDirection)=list(FVI_Absolute_Coord(list(Floor['Location']),list(Floor['XlAxisDirection']),RelativeLocation,CSystem,IdWall)) #aquí
			XgWall['Xg']=list(Xg)
			XgWall['XlAxisDirection']=list(XlAxisDirection)
			XgWalls[Wall]=XgWall
	return(XgWalls)

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

def FIXd_Faces_in_Geometry(IfcFaces,XAxisInitial,XAxisFinal,FloorHeight):
	Points=[]
	BasePoints=[]
	Find=False
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
	return Points

def FIXe_Floor_Height(XgFloor,Floor):
    Geometry=XgFloor[Floor]
    Location=Geometry['Location']
    Location=list(Location)
    Height=Location[2]
    return Height

def FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitial,XAxisFinal,FloorHeight):
	WallsPoints=[]
	XPoint=[]
	YPoint=[]
	Firstoperand=IfcTypeRepresentation[1]
	IfcExtrudedAreaSolid=None
	while Firstoperand.is_a()=='IfcBooleanClippingResult' or Firstoperand.is_a('IfcBooleanResult'):
		Firstoperand=Firstoperand[1]
		IfcExtrudedAreaSolid=Firstoperand
	if IfcExtrudedAreaSolid==None:
		IfcExtrudedAreaSolid=Firstoperand
	if IfcExtrudedAreaSolid[0].is_a('IFCARBITRARYCLOSEDPROFILEDEF'):
		IfcArbitraryClosedProfileDef=IfcExtrudedAreaSolid[0]
		IfcPolyline=IfcArbitraryClosedProfileDef[2]
		IfcCartesianPoint=IfcPolyline[0]
		for Point in IfcCartesianPoint:
			Coordinates=Point[0]
			if Coordinates[0]>=-0.01:
				XPoint.append(Coordinates[0])
			YPoint.append(Coordinates[1])
		XAxisInitial=min(XPoint)
		XAxisFinal=max(XPoint)
		MaxWidth=max(YPoint)
		MinWidth=min(YPoint)
	elif IfcExtrudedAreaSolid[0].is_a('IFCRECTANGLEPROFILEDEF'):
		IfcRectangleProfileDef=IfcExtrudedAreaSolid[0]
		MaxWidth=IfcRectangleProfileDef[4]/2
		MinWidth=-MaxWidth
		XAxisFinal=IfcRectangleProfileDef[3]
		XAxisInitial=0
	else:
		Width=0
	WallsPoints.append([XAxisInitial,MaxWidth,0])
	WallsPoints.append([XAxisInitial,MinWidth,0])
	WallsPoints.append([XAxisFinal,MaxWidth,0])
	WallsPoints.append([XAxisFinal,MinWidth,0])		
	return WallsPoints

def FIXg_Extruded_Geometry(IfcTypeRepresentation,XAxisInitial,XAxisFinal,FloorHeight):
	WallsPoints=[]
	IfcRectangleProfileDef=IfcTypeRepresentation[0]
	if IfcRectangleProfileDef.is_a('IFCARBITRARYCLOSEDPROFILEDEF'):
		XAreaPoints=[]
		YAreaPoints=[]
		IfcPolyline=IfcRectangleProfileDef[2]
		IfcPolyline=IfcPolyline[0]
		for Point in IfcPolyline:
			if len(Point)!=1:
				XAreaPoints.append(Point[0])
				YAreaPoints.append(Point[1])
			else:
				Point=Point[0]
				XAreaPoints.append(Point[0])
				YAreaPoints.append(Point[1])				
		XAxisInitial=min(XAreaPoints)
		XAxisFinal=max(XAreaPoints)
		MaxWidth=max(YAreaPoints)
		MinWidth=min(YAreaPoints)

	else:
		MaxWidth=IfcRectangleProfileDef[4]/2
		MinWidth=-MaxWidth
		XAxisFinal=IfcRectangleProfileDef[3]
		XAxisInitial=0
	WallsPoints.append([XAxisInitial,MaxWidth,0])
	WallsPoints.append([XAxisInitial,MinWidth,0])
	WallsPoints.append([XAxisFinal,MaxWidth,0])
	WallsPoints.append([XAxisFinal,MinWidth,0])
	return WallsPoints

def FIXh_AdvanceBrep_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight):
	WallsPoints=[]
	XPoints=[]
	YPoints=[]
	IFcAdvanceBrep=IfcTypeRepresentation
	Width=0
	WidthFind=False
	IfcClosedShell=IFcAdvanceBrep[0]
	CfsFaces=IfcClosedShell[0]
	for IfcAdvanceFace in CfsFaces:
		IfcPlane=IfcAdvanceFace[1]
		IfcAxis2Placment3D=IfcPlane[0]
		IfcCartesianPoint=IfcAxis2Placment3D[0]
		LocationData=IfcCartesianPoint[0]
		if LocationData[0]>=-0.01:
			XPoints.append(LocationData[0])
			YPoints.append(LocationData[1])
	XAxisInitialPoint=min(XPoints)
	XAxisFinalPoint=max(XPoints)
	Width=max(YPoints)
	WallsPoints.append([XAxisInitialPoint,Width,0])
	WallsPoints.append([XAxisInitialPoint,-Width,0])
	WallsPoints.append([XAxisFinalPoint,Width,0])
	WallsPoints.append([XAxisFinalPoint,-Width,0])
	return WallsPoints

def FIX_Wall_Geometry(DicWalls_Floor,ifc,XgFloors,XgWalls):
    Floors=list(DicWalls_Floor.keys())
    GeometryWalls={}
    for Floor in Floors:
        IdWalls=DicWalls_Floor[Floor]
        FloorHeight=FIXe_Floor_Height(XgFloors,Floor)
        for IdWall in IdWalls:
            Wall=ifc.by_id(IdWall)
            for Atributes in Wall:
                if type(Atributes)==ifcopenshell.entity_instance:
                    if Atributes.is_a('IFCPRODUCTDEFINITIONSHAPE'):
                        (XAxisInitialPoint,XAxisFinalPoint)=FIXc_Wall_Axis_Points(Atributes)
                        IfcShapeRepresentation=Atributes[2]
                        if len(IfcShapeRepresentation)>2:
                            IfcShapeRepresentation=IfcShapeRepresentation[0]
                            IfcTypeRepresentation=IfcShapeRepresentation[len(IfcShapeRepresentation)-1]
                            IfcTypeRepresentation=IfcTypeRepresentation[0]
                            if IfcTypeRepresentation.is_a('IFCEXTRUDEDAREASOLID'):
                            	Points=FIXg_Extruded_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                            	GeometryWalls[IdWall]=Points
                            elif IfcTypeRepresentation.is_a('IFCBOOLEANRESULT'):
                            	Points=FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                            	GeometryWalls[IdWall]=Points
                            elif IfcTypeRepresentation.is_a('IFCFACETEDBREP'):
                                IfcClosedShell=IfcTypeRepresentation[0]
                                IfcFaces=IfcClosedShell[0]
                                Points=FIXd_Faces_in_Geometry(IfcFaces,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                        else:	
                            IfcTypeRepresentation=IfcShapeRepresentation[len(IfcShapeRepresentation)-1]
                            IfcTypeRepresentation=IfcTypeRepresentation[3]
                            IfcTypeRepresentation=IfcTypeRepresentation[0]
                            if IfcTypeRepresentation.is_a('IFCFACETEDBREP'):
                                IfcClosedShell=IfcTypeRepresentation[0]
                                IfcFaces=IfcClosedShell[0]
                                Points=FIXd_Faces_in_Geometry(IfcFaces,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                            elif IfcTypeRepresentation.is_a('IFCBOOLEANCLIPPINGRESULT'):
                                Points=FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                            elif IfcTypeRepresentation.is_a('IFCEXTRUDEDAREASOLID'):
                                Points=FIXg_Extruded_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                            elif IfcTypeRepresentation.is_a('IFCADVANCEDBREP'):
                                Points=FIXh_AdvanceBrep_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                            elif IfcTypeRepresentation.is_a('IFCBOOLEANRESULT'):
                                Points=FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                            else:
                                GeometryWalls[IdWall]=None 
    return (GeometryWalls)

def FX_Wall_Abs_Geometry(XgWalls,GeometryWalls):
	GeometryAbsWalls={}
	IdWalls=list(XgWalls.keys())
	for IdWall in IdWalls:
		ListGeometryPoints=[]
		BasePointData=XgWalls[IdWall]
		XgWall=BasePointData['Xg']
		CSWall=BasePointData['XlAxisDirection']
		WallPointsData=GeometryWalls[IdWall]
		if WallPointsData!=None:
			for WallPointData in WallPointsData:
				(Xg,CSType)=FVI_Absolute_Coord(XgWall,CSWall,WallPointData,[1,0,0],IdWall)
				ListGeometryPoints.append(list(Xg))
			GeometryAbsWalls[IdWall]=ListGeometryPoints
	return GeometryAbsWalls

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
								a=type(IfcBoolean[0])
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

def FXII_Coordinates_Convert(GeometryAbsWalls,ifc):

	_projections = {}
	
	def zone(coordinates):
		if 56 <= coordinates[1] < 64 and 3 <= coordinates[0] < 12:
			return 32
		if 72 <= coordinates[1] < 84 and 0 <= coordinates[0] < 42:
			if coordinates[0] < 9:
				return 31
			elif coordinates[0] < 21:
				return 33
			elif coordinates[0] < 33:
				return 35
			return 37
		return int((coordinates[0] + 180) / 6) + 1

	def letter(coordinates):
		return 'CDEFGHJKLMNPQRSTUVWXX'[int((coordinates[1] + 80) / 8)]

	def project(coordinates):
		z = zone(coordinates)
		l = letter(coordinates)
		if z not in _projections:
			_projections[z] = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
		x, y = _projections[z](coordinates[0], coordinates[1])
		if y < 0:
			y += 10000000
		return z, l, x, y

	def unproject(z, l, x, y):
		if z not in _projections:
			_projections[z] = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
		if l < 'N':
			y -= 10000000
		lng, lat = _projections[z](x, y, inverse=True)
		return (lng, lat)

	UTMZone=None
	WallsGeographicCoordinates={}
	IfcSite=ifc.by_type('IfcSite')
	IfcSite=IfcSite[0]
	GeographicalLocation=IfcSite[10]
	East=GeographicalLocation[0]+GeographicalLocation[1]*0.01
	for i in range(28,38):
		WestLimit=-18+((i-28)*6)
		EastLimit=-18+((i+1-28)*6)
		if East>WestLimit and East<EastLimit:
			UTMZone=i
			break
	for Wall in GeometryAbsWalls:
		Points=[]
		for Point in GeometryAbsWalls[Wall]:
			x=Point[0]
			y=Point[1]
			(Lon,Lat)=unproject(UTMZone,'N',x,y)
			Points.append([Lon,Lat,Point[2]])
		WallsGeographicCoordinates[Wall]=Points
	return(WallsGeographicCoordinates)

def FXIIIb_Json_Export(WallsGeographicCoordinates,DicWalls, filename):
	Dicexport={}
	for Floor in DicWalls:
		Walls=DicWalls[Floor]
		OutsideWallList=[]
		if len(Walls)!=0:
			for NumWall in range(len(Walls)):
				Wall=Walls[NumWall]
				if not Wall in WallsGeographicCoordinates:
					OutsideWallList.append(Wall)
			for Wall in OutsideWallList:
				Walls.remove(Wall)
			DicWalls[Floor]=Walls
	FloorList=list(DicWalls.keys())
	ListPlantas=[]
	DicEdificio={}
	ListEdificio=[]
	for Floor in DicWalls:
		if len(DicWalls[Floor])==0:
			break
		else:
			WallsinFloor=DicWalls[Floor]
			Wall=WallsinFloor[0]
			Geometry=WallsGeographicCoordinates[Wall]
			Geometry=Geometry[0]
			FloorHeight=Geometry[2]
			PointList=[]
			for Wall in DicWalls[Floor]:
				Points=WallsGeographicCoordinates[Wall]
				for Point in Points:
					DicCoordinates={}
					DicCoordinates["X"]=Point[0]
					DicCoordinates["Y"]=Point[1]
					PointList.append(DicCoordinates)
			DicPuntos={}
			DicPuntos["puntos"]=PointList
			ListEnvolventes=[]
			ListEnvolventes.append(DicPuntos)
			DicPlantas={}
			DicPlantas["alturaPlanta"]=FloorHeight
			DicPlantas["envolventes"]=ListEnvolventes
			ListPlantas.append(DicPlantas)
	DicEdificio["numEdificio"]=1
	DicEdificio["plantas"]=ListPlantas
	ListEdificio.append(DicEdificio)
	DicJson={}
	DicJson["edificios"]=ListEdificio
	with open(f'{BASE_DIR2}/portal/json_results/{filename}.json', 'w') as file:
		json.dump(DicJson, file, indent=4)



def FXIV_Medium_Points(GeometryWalls):
	WallSide={}
	for Wall in GeometryWalls:
		Side=[]
		y1=None
		y2=None
		x1acc=0
		x2acc=0
		for Point in GeometryWalls[Wall]:
			Height=Point[2]
			if y1==None:
				y1=Point[1]
				x1acc=Point[0]
			elif y1==Point[1]:
				x1acc+=Point[0]
			elif y2==None:
				y2=Point[1]
				x2acc=Point[0]
			else:
				x2acc+=Point[0]
		x1av=x1acc/2
		x2av=x2acc/2
		Side.append([x1av,y1,Height])
		Side.append([x2av,y2,Height])
		WallSide[Wall]=Side
	return WallSide

def FXV_OutsidePoints(GeometryAbsWalls,WallsAbsSide):
	xac=0
	yac=0
	count=0
	WallExternalPoints={}
	for Wall in GeometryAbsWalls:
		for Point in GeometryAbsWalls[Wall]:
			xac+=Point[0]
			yac+=Point[1]
			count+=1
	XCentral=xac/count
	Ycentral=yac/count
	for Wall in GeometryAbsWalls:
		DistanceList=[]
		ExternalsPoints=[]
		MediumPoints=WallsAbsSide[Wall]
		MediumPointSide1=MediumPoints[0]
		MediumPointSide2=MediumPoints[1]
		DistanceSide1=((MediumPointSide1[0]-XCentral)**2+(MediumPointSide1[1]-Ycentral)**2)**(1/2)
		DistanceSide2=((MediumPointSide2[0]-XCentral)**2+(MediumPointSide2[1]-Ycentral)**2)**(1/2)
		for Point in GeometryAbsWalls[Wall]:
			if DistanceSide1>DistanceSide2:
				DistanceList.append(((MediumPointSide1[0]-Point[0])**2+(MediumPointSide1[1]-Point[1])**2)**(1/2))
			else:
				DistanceList.append(((MediumPointSide2[0]-Point[0])**2+(MediumPointSide2[1]-Point[1])**2)**(1/2))
		WallsPoints=GeometryAbsWalls[Wall]
		for i in range (2):
			MinDistance=min(DistanceList)
			MinDistanceIndex=DistanceList.index(MinDistance)
			ExternalsPoints.append(WallsPoints[MinDistanceIndex])
			DistanceList.pop(MinDistanceIndex)
			WallsPoints.pop(MinDistanceIndex)
		WallExternalPoints[Wall]=ExternalsPoints
	return WallExternalPoints


		

