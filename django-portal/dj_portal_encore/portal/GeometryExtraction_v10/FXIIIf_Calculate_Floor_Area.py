from . import ifcopenshell
def FXIIIf_Calculate_Floor_Area(ifc,DicSlabs_Floor):
	FloorArea={}
	for Floor in DicSlabs_Floor:
		Area=0
		if len(DicSlabs_Floor[Floor])!=0:
			for Slab in DicSlabs_Floor[Floor]:
				SlabObject=ifc.by_id(Slab)
				DefinionShape=SlabObject.Representation
				RepresentationSlab=DefinionShape.Representations[0]
				if RepresentationSlab.RepresentationType=='SweptSolid':
					RepresentationSubContext=RepresentationSlab.Items[0]
					SweptArea=RepresentationSubContext.SweptArea
					if SweptArea.is_a('IFCRECTANGLEPROFILEDEF'):
						Area+=SweptArea.XDim*SweptArea.YDim
		FloorArea[Floor]=Area
	return FloorArea