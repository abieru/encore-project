from . import ifcopenshell
def FXIX_OpeninginWall(WindowArea,WallArea,WindowbyWall):
    OpeningPercentage={}
    for Wall in list(WindowbyWall.keys()):
        WindowAreaInWall=0
        WindowsInWall=WindowbyWall[Wall]
        for Window in WindowsInWall:
            WindowAreaInWall+=WindowArea[Window]
        OpeningPercentage[Wall]=((WindowAreaInWall)/(WallArea[Wall]))*100
    return OpeningPercentage

