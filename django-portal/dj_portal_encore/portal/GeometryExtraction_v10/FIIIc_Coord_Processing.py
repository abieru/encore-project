from . import ifcopenshell
import numpy as np
def FIIIc_Coord_Processing(Loc,Dir,IdWall):
    Xgrel=None
    IdWall
    Xlrel=list((Loc))
    RotXAxis=list(Dir)
    if Xlrel[0]!=None and Xlrel[1]!=None and Xlrel[2]!=None:
        DirMatrix=([RotXAxis,[-RotXAxis[1],RotXAxis[0],RotXAxis[2]],[0,0,1]])
        Xgrel=np.dot(np.linalg.inv(DirMatrix),Xlrel)
    return (Xgrel)