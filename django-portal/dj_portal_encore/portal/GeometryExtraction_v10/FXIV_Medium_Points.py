from . import ifcopenshell
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