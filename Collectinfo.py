###   __This py is used to READ tree and building polygon information__	###

#   Including functions (1)CollectTreeInfo(treeinfofile_in)
#   Including functions (2)CollectBldgInfo(bldginfofile_in)
#   Including functions (3)CollectPollenResult(resultfile_in)

from shapely.geometry import Polygon

######	Tree information collection through reading corresponding file	######
def CollectTreeInfo(treeinfofile_in):
	
	###	accept (1)a TXT file containing tree information
	
	###	return (1)number of trees
	###	return (2)tree information
	
	with open(treeinfofile_in) as f_in:
		contents = f_in.readlines()
	
	treeinfoarr_in = []
	for item in contents[1:]:
		item_single = item.split()
		treeinfoarr_in.append(item_single)
	
	#treeid_in = [ID for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]###	id starts from 0
	treex_in = [X for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	treey_in = [Y for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	treetype_in = [TYPE for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	treehstem_in = [HCB for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	treeh_in = [HCT for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	#treedstem_in = [DSTEM for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	treedcrown_in = [DCROWN for [ID,X,Y,PN,TYPE,HCB,HCT,DSTEM,DCROWN] in treeinfoarr_in]
	
	NOTREE_in = len(treex_in)
	treeinfoarr_in = []
	for i in range(NOTREE_in):
		#	0:X; 1:Y; 2:TYPE(1-14); 3:Hstem; 4:Htree; 5:Dstem; 6:Dcrowm	#
		treeinfoarr_in.append([])
		treeinfoarr_in[i].append(float(treex_in[i]))
		treeinfoarr_in[i].append(float(treey_in[i]))
		treeinfoarr_in[i].append(int(treetype_in[i]))
		treeinfoarr_in[i].append(float(treehstem_in[i]))
		treeinfoarr_in[i].append(float(treeh_in[i]))
		#treeinfoarr_in[i].append(float(treedstem_in[i]))
		treeinfoarr_in[i].append(float(treedcrown_in[i]))
	
	return NOTREE_in, treeinfoarr_in
######	Tree information collection through reading corresponding file	######


######	Building polygon and height information collection through reading corresponding file	######
def CollectBldgInfo(bldginfofile_in, bldgheightfile_in):
	
	###	accept (1)a TXT file containing building vertex information
	###	accept (2)a TXT file containing building height information
	
	###	return (1)no of bldgs
	###	return (2)ID of polygon vertices
	###	return (3)X coordinates
	###	return (4)Y coordinates
	###	return (5)building polygon list
	###	return (6)building height list
	
	with open(bldginfofile_in) as f_in:
		contents = f_in.readlines()
	
	bldginfoarr_in = []
	for item in contents[1:]:
		item_single = item.split()
		bldginfoarr_in.append(item_single)
	temp_bldgno_in = [ID for [ID,X,Y] in bldginfoarr_in]#	For one specific building, the last point is the same as the first one
	temp_bldgx_in = [X for [ID,X,Y] in bldginfoarr_in]
	temp_bldgy_in = [Y for [ID,X,Y] in bldginfoarr_in]
	
	bldgno_in=[]
	bldgx_in=[]
	bldgy_in=[]
	for item in temp_bldgno_in:
		bldgno_in.append(int(item))
	for item in temp_bldgx_in:
		bldgx_in.append(float(item))	
	for item in temp_bldgy_in:
		bldgy_in.append(float(item))
		
	NOBLDG_in = max(bldgno_in) + 1
	
	#	create bldg polygons based on Shapely	#
	#	in Shapely, polygon = shapely.geometry.Polygon([(0, 0), (1, 1), (1, 0)])
	polyallbldg_in = []# Store polygons of all bldgs using a list object
	K_in = 0
	for i in range(NOBLDG_in):
		NOVERTEX_in = bldgno_in.count(i)-1#For one specific building, the last point is the same as the first one
		vertex_in = []
		for j in range(NOVERTEX_in):
			vertex_in.append((bldgx_in[K_in], bldgy_in[K_in]))
			K_in = K_in + 1
		POLYBLDGi_in = Polygon(vertex_in)
		polyallbldg_in.append(POLYBLDGi_in)
		K_in = K_in + 1
	#	create bldg polygons based on Shapely	#
	
	with open(bldgheightfile_in) as f_in:
		contents = f_in.readlines()
	
	bldgheightarr_in = []
	for item in contents[1:]:
		item_single = item.split()
		bldgheightarr_in.append(item_single)
	temp_bldgheight_in = [H for [ID,H] in bldgheightarr_in]
	
	bldgheight_in=[]
	for item in temp_bldgheight_in:
		bldgheight_in.append(float(item))
	
	return NOBLDG_in, bldgno_in, bldgx_in, bldgy_in, polyallbldg_in, bldgheight_in
######	Building polygon and height information collection through reading corresponding file	######


######	Simulation result information collection through reading corresponding file	######
def CollectPollenResult(resultfile_in):
	
	###	accept (1)a TXT file containing pollen concentration results
	
	###	return (1)X coordinates of grids
	###	return (2)Y coordinates of grids
	###	return (3)simulated pollen concentration
	
	with open(resultfile_in) as f_in:
		contents = f_in.readlines()
	
	resultinfoarr_in = []
	for item in contents[1:]:
		item_single = item.split()
		resultinfoarr_in.append(item_single)
	temp_resultx_in = [X for [ID,X,Y,Z,PC] in resultinfoarr_in]
	temp_resulty_in = [Y for [ID,X,Y,Z,PC] in resultinfoarr_in]
	temp_resultvalue_in = [PC for [ID,X,Y,Z,PC] in resultinfoarr_in]
	
	resultx_in=[]
	resulty_in=[]
	resultvalue_in=[]
	for item in temp_resultx_in:
		resultx_in.append(float(item))
	for item in temp_resulty_in:
		resulty_in.append(float(item))
	for item in temp_resultvalue_in:
		resultvalue_in.append(float(item))
	
	NORESULT_in = len(resultx_in)
	
	return NORESULT_in, resultx_in, resulty_in, resultvalue_in
######	Simulation result information collection through reading corresponding file	######
