from . import ifcopenshell
import numpy as np
from pathlib import Path
from .GeometryExtraction_v10 import *
import json
BASE_DIR2 = Path(__file__).resolve().parent.parent
def IfcGeometryConvertToJson(Archive, filename):
    ifc=FIa_Open(Archive)
    XgProject=FIIIa_Coord_Project(ifc)
    CSgProject=[1,0,0]
    (XlrelSite,CSlSite)=FIIIb_Coord_Object(ifc,'IFCSITE')
    (XgSite,CSlSite)=FVI_Absolute_Coord(XgProject,CSgProject,XlrelSite,CSlSite,None)
    (XlRelBuilding,CSlBuilding)=FIIIb_Coord_Object(ifc,'IFCBUILDING')
    (XgBuilding,CSlBuilding)=FVI_Absolute_Coord(XgSite,CSlSite,XlRelBuilding,CSlBuilding,None)
    DicWalls_Floor=FIV_Walls_in_floor(ifc)
    XlrelFloors=FIIId_Coord_Some_Objects(ifc,'IFCBUILDINGSTOREY')
    XgFloors=FVII_Some_Object_Absolute_Coord(XlrelFloors,XgBuilding,CSlBuilding)
    XlrelWalls=FIIId_Coord_Some_Objects(ifc,'IFCWALL')
    XgWalls=FVIII_Abs_Walls_by_Floor(DicWalls_Floor,XgFloors,XlrelWalls)
    (GeometryWalls,WallHeight)=FIX_Wall_Geometry(DicWalls_Floor,ifc,XgFloors,XgWalls)
    GeometryAbsWalls=FX_Wall_Abs_Geometry(XgWalls,GeometryWalls)
    GeometryAbsWalls=FXI_External_Walls(GeometryAbsWalls,ifc)
    WallSide=FXIV_Medium_Points(GeometryWalls)
    WallAbsSide=FX_Wall_Abs_Geometry(XgWalls,WallSide)
    GeometryOutsideAbsWalls=FXV_OutsidePoints(GeometryAbsWalls,WallAbsSide)
    (WallsGeographicCoordinates,UTMZone)=FXIIa_WallCoordinates_Convert(GeometryOutsideAbsWalls,ifc)
    WindowArea=FXVI_WindowArea(ifc)
    WindowbyWall=FXVII_WindowsinWall(ifc,GeometryAbsWalls)
    WallArea=FXVIII_WallArea(DicWalls_Floor,GeometryWalls,GeometryAbsWalls,ifc,WallHeight)
    OpeningPercentage=FXIX_OpeninginWall(WindowArea,WallArea,WindowbyWall)
    FXIIIb_Json_Export(WallsGeographicCoordinates,DicWalls_Floor,ifc,GeometryAbsWalls,UTMZone,OpeningPercentage, filename)
    return (DicWalls_Floor,GeometryAbsWalls,ifc)

def runscript(file):
    Archive=Path(rf'{BASE_DIR2}/portal/ifc_files/{file}')
    (DicWalls_Floor,GeometryAbsWalls,ifc)=IfcGeometryConvertToJson(Archive, file)


def runscript1(file):
    Archive=Path(rf'{BASE_DIR2}/media/files/IFCFile_model/{file}')
    filename = f'temp{file}'
    (DicWalls_Floor,GeometryAbsWalls,ifc)=IfcGeometryConvertToJson(Archive, filename)

