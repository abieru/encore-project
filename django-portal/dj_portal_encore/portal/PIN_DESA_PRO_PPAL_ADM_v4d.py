
#from portal import ifcopenshell
import numpy as np
from .PIN_DESA_PRO_FUNC_ADM_v4d import *
from pathlib import Path
import json
BASE_DIR2 = Path(__file__).resolve().parent.parent


def ifcjsonfunc(filename):
    Archive=Path(rf'{BASE_DIR2}/portal/ifc_files/{filename}')
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
    Output='OutputData_Test_PruebaNuevoGeom.csv'
    GeometryWalls=FIX_Wall_Geometry(DicWalls_Floor,ifc,XgFloors,XgWalls)
    GeometryAbsWalls=FX_Wall_Abs_Geometry(XgWalls,GeometryWalls)
    GeometryAbsWalls=FXI_External_Walls(GeometryAbsWalls,ifc)
    WallSide=FXIV_Medium_Points(GeometryWalls)
    WallAbsSide=FX_Wall_Abs_Geometry(XgWalls,WallSide)
    GeometryAbsWalls=FXV_OutsidePoints(GeometryAbsWalls,WallAbsSide)
    WallsGeographicCoordinates=FXII_Coordinates_Convert(GeometryAbsWalls,ifc)
    FXIIIb_Json_Export(WallsGeographicCoordinates,DicWalls_Floor, filename)

#ifcjsonfunc('EDEA_ifc2x3CV20_EXISTING.ifc')