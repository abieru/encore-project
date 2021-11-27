from . import ifcopenshell
def FIXe_Floor_Height(XgFloor,Floor):
    Geometry=XgFloor[Floor]
    Location=Geometry['Location']
    Location=list(Location)
    Height=Location[2]
    return Height
