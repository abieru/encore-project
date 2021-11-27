from . import ifcopenshell
def FXVIII_WallArea(DicWalls_Floor,GeometryWalls,GeometryAbsWalls,ifc,WallHeight):
    Floors=ifc.by_type('IfcBuildingStorey')
    HeightList=[]
    WallArea={}
    for Floor in Floors:
        HeightList.append(Floor.Elevation)
    Counter=1
    for Floor in Floors:
        WallList=DicWalls_Floor[Floor.id()]
        if Counter<len(Floors):
            Height=abs(HeightList[Counter]-HeightList[Counter-1])
            Counter+=1
        for Wall in WallList:
            Area=0
            if Wall in GeometryAbsWalls:
                BasePoints=GeometryWalls[Wall]
                if BasePoints[0][1]==BasePoints[1][1]:
                    Xfinal=BasePoints[0][0]
                    Xinitial=BasePoints[1][0]
                elif BasePoints[0][1]==BasePoints[2][1]:
                    Xfinal=BasePoints[0][0]
                    Xinitial=BasePoints[2][0]
                elif BasePoints[0][1]==BasePoints[3][1]:
                    Xfinal=BasePoints[0][0]
                    Xinitial=BasePoints[3][0]
                Base=abs(Xfinal-Xinitial)
                Area=Base*WallHeight[Wall]
                WallArea[Wall]=Area
    return WallArea


        