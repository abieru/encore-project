import math
from . import ifcopenshell
def FXIIId_Angle_Calculation(CenterPointX,CenterPointY,Point):
	def Angle(x,y):
		if x>0 and y>0:
			theta=math.degrees(math.atan2(y,x)) +270 
		elif x<0 and y>0:
			theta=math.degrees(math.atan2(y,x)) -90
		elif x<0 and y<0:
				theta=270 + math.degrees(math.atan2(y,x))
		elif x>0 and y<0:
			theta=270 + math.degrees(math.atan2(y,x))  
		return theta
	Ax=Point[0]-CenterPointX
	Ay=Point[1]-CenterPointY
	AngletoCenter=Angle(x=Ax,y=Ay)
	return AngletoCenter
