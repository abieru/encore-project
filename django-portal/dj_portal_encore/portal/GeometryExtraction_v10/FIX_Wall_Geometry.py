from . import ifcopenshell
from .FIXc_Wall_Axis_Points import*
from .FIXe_Floor_Height import *
from .FIXg_Extruded_Geometry import *
from  .FIXf_Clipping_Geometry import*
from .FIXd_Faces_in_Geometry import *
from .FIXh_AdvanceBrep_Geometry import *
def FIX_Wall_Geometry(DicWalls_Floor,ifc,XgFloors,XgWalls):
    Floors=list(DicWalls_Floor.keys())
    GeometryWalls={}
    WallHeight={}
    Height=0
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
                            	(Points,Height)=FIXg_Extruded_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                            	GeometryWalls[IdWall]=Points
                            	WallHeight[IdWall]=Height
                            elif IfcTypeRepresentation.is_a('IFCBOOLEANRESULT'):
                            	(Points,Height)=FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                            	GeometryWalls[IdWall]=Points
                            	WallHeight[IdWall]=Height
                            elif IfcTypeRepresentation.is_a('IFCFACETEDBREP'):
                                IfcClosedShell=IfcTypeRepresentation[0]
                                IfcFaces=IfcClosedShell[0]
                                (Points,Height)=FIXd_Faces_in_Geometry(IfcFaces,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                                WallHeight[IdWall]=Height
                        else:	
                            IfcTypeRepresentation=IfcShapeRepresentation[len(IfcShapeRepresentation)-1]
                            IfcTypeRepresentation=IfcTypeRepresentation[3]
                            IfcTypeRepresentation=IfcTypeRepresentation[0]
                            if IfcTypeRepresentation.is_a('IFCFACETEDBREP'):
                                IfcClosedShell=IfcTypeRepresentation[0]
                                IfcFaces=IfcClosedShell[0]
                                (Points,Height)=FIXd_Faces_in_Geometry(IfcFaces,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                                WallHeight[IdWall]=Height
                            elif IfcTypeRepresentation.is_a('IFCBOOLEANCLIPPINGRESULT'):
                                (Points,Height)=FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                                WallHeight[IdWall]=Height
                            elif IfcTypeRepresentation.is_a('IFCEXTRUDEDAREASOLID'):
                                (Points,Height)=FIXg_Extruded_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                                WallHeight[IdWall]=Height
                            elif IfcTypeRepresentation.is_a('IFCADVANCEDBREP'):
                                Points=FIXh_AdvanceBrep_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                                WallHeight[IdWall]=Height
                            elif IfcTypeRepresentation.is_a('IFCBOOLEANRESULT'):
                                Points=FIXf_Clipping_Geometry(IfcTypeRepresentation,XAxisInitialPoint,XAxisFinalPoint,FloorHeight)
                                GeometryWalls[IdWall]=Points
                                WallHeight[IdWall]=Height
                            else:
                                GeometryWalls[IdWall]=None 
    return (GeometryWalls,WallHeight)