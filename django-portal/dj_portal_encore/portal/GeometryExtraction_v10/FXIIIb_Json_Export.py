from . import ifcopenshell
import json
from .FIb_ParsIfc import *
from .FXIIIc_Order_Enclosures import *
from .FXIIIg_GeographicEnclosures import *
from .FXIIIe_SlabsinFloor import *
from .FXIIIf_Calculate_Floor_Area import *
from pathlib import Path
BASE_DIR2 = Path(__file__).resolve().parent.parent

def FXIIIb_Json_Export(WallsGeographicCoordinates,DicWalls,ifc,GeometryAbsWalls,UTMZONE,OpeningPercentage, filename):
	Dicexport={}
	Floors=[]
	jump=False
	PositiveHeightFloor=[]
	NegativeHeightFloor=[]
	Floors=FIb_ParsIfc(ifc,Floors,'IFCBUILDINGSTOREY')
	for Floor in Floors:
		Floor=Floor.id()
		Walls=DicWalls[Floor]
		jump=False
		if len(Walls)!=0:
			Wall=Walls[0]
			i=0
			while Wall not in WallsGeographicCoordinates and i<len(Walls):
				Wall=Walls[i]
				i+=1
				if i==len(Walls):
					jump=True
			if jump==True:
				continue
			Points=WallsGeographicCoordinates[Wall]
			Point=Points[0]
			Height=Point[2]
			if float(Height)>=0:
				PositiveHeightFloor.append(Height)
			else:
				NegativeHeightFloor.append(Height)
	PositiveHeightFloor.sort()
	NegativeHeightFloor.sort(reverse=True)
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
	EnclosuresOrderbyFloor=FXIIIc_Order_Enclosures(ifc=ifc,DicWalls=DicWalls,GeometryAbsWalls=GeometryAbsWalls)
	EnclosuresOrderGeographic=FXIIIg_GeographicEnclosures(EnclosuresOrderbyFloor,UTMZONE)
	DicSlabs_Floor=FXIIIe_SlabsinFloor(ifc)
	FloorArea=FXIIIf_Calculate_Floor_Area(ifc,DicSlabs_Floor)
	for Floor in DicWalls:
		if len(DicWalls[Floor])==0:
			continue
		else:
			WallsinFloor=DicWalls[Floor]
			Wall=WallsinFloor[0]
			Geometry=WallsGeographicCoordinates[Wall]
			Geometry=Geometry[0]
			FloorHeight=Geometry[2]
			PointList=[]
			PartyWallList=[]
			FachadaWallList=[]
			EnvolventeList=[]
			for Wall in DicWalls[Floor]:
				Points=WallsGeographicCoordinates[Wall]
				IfcWall=ifc.by_id(Wall)
				IfcWallType=IfcWall[4]
				if IfcWallType=="PARTY_WALL":
					DicPartyWall={}
					DicFachadaWall={}
					for Point in Points:
						DicPartyWallCoordinates={}
						DicPartyWallCoordinates["X"]=Point[0]
						DicPartyWallCoordinates["Y"]=Point[1]
						if Points.index(Point)==0:
							WallGuid=ifc.by_id(Wall).GlobalId
							DicPartyWall["id"]=WallGuid
							DicPartyWall["inicio"]=DicPartyWallCoordinates
						elif Points.index(Point)==1:
							DicPartyWall["fin"]=DicPartyWallCoordinates
					PartyWallList.append(DicPartyWall)
				else:
					DicPartyWall={}
					DicFachadaWall={}
					for Point in Points:
						DicFachadaWallCoordinates={}
						DicFachadaWallCoordinates["X"]=Point[0]
						DicFachadaWallCoordinates["Y"]=Point[1]
						if Points.index(Point)==0:
							WallGuid=ifc.by_id(Wall).GlobalId
							DicFachadaWall["id"]=WallGuid
							DicFachadaWall['porcentaje huecos']=OpeningPercentage[Wall]
							DicFachadaWall["inicio"]=DicFachadaWallCoordinates
						elif Points.index(Point)==1:
							DicFachadaWall["fin"]=DicFachadaWallCoordinates
					FachadaWallList.append(DicFachadaWall)
			DicEnvolvente={}
			EnvolventePointList=[]
			for Points in EnclosuresOrderGeographic[Floor]:
				DicEnvolventeCoordinates={}
				DicEnvolventeCoordinates["X"]=Points[0]
				DicEnvolventeCoordinates["Y"]=Points[1]
				EnvolventePointList.append(DicEnvolventeCoordinates)
			DicEnvolvente['puntos']=EnvolventePointList
			EnvolventeList.append(DicEnvolvente)
			DicPlantas={}
			if FloorHeight>=0:
				FloorLevel=PositiveHeightFloor.index(FloorHeight)
			else:
				FloorLevel=NegativeHeightFloor.index(FloorHeight)
				FloorLevel=(FloorLevel+1)*(-1)
			DicPlantas["alturaPlanta"]=FloorLevel
			DicPlantas['envolvente']=EnvolventeList
			DicPlantas["fachadas"]=FachadaWallList			
			if len(PartyWallList)!=0:
				DicPlantas["medianeras"]=PartyWallList
			DicPlantas['area']=FloorArea[Floor]
			ListPlantas.append(DicPlantas)
	DicEdificio["numEdificio"]=1
	DicEdificio["plantas"]=ListPlantas
	ListEdificio.append(DicEdificio)
	DicJson={}
	DicJson["edificios"]=ListEdificio
	with open(f'{BASE_DIR2}/json_results/{filename}.json', 'w') as file:
		json.dump(DicJson, file, indent=4)