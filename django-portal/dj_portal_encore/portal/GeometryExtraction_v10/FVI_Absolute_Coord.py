from . import ifcopenshell
from .FIIIc_Coord_Processing import *
import numpy as np
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