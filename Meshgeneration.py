###   __This py is used to generate MESH within the plane of interest__	###

#   Including functions (1)PlaneGridGen(gridresolution_in, treeinfofile_in, bldginfofile_in, redundancyborder_in=0)

import numpy as np

######	Mesh generation at the height of interest	######
def PlaneGridGen(gridresolution_in, treeinfoarr_in, bldgx_in, bldgy_in, heightofinterset_in, redundancyborder_in=0):
	
	###	accept (1)grid resolution /m
	###	accept (2)tree information list (from Collectinfo.py)
	###	accept (3)bldg's x cooridinate list (from Collectinfo.py)
	###	accept (4)bldg's y cooridinate list (from Collectinfo.py)
	###	accept (5)height of interset /m, generally taken as 1.5 m
	###	accept (6)a redundancy in boundary size (optional)
	
	###	return (1)grid coordinates that including X, Y, Z as a 3D list object
	
	###	define the boundary of generated mesh	###
	#	capture the boundary of tree clusters	#
	treex_temp = []
	treey_temp = []
	treeno_temp = len(treeinfoarr_in)
	for i in range(treeno_temp):
		treex_temp.append(treeinfoarr_in[i][0])
		treey_temp.append(treeinfoarr_in[i][1])
	maxtreex_in = max(treex_temp)
	mintreex_in = min(treex_temp)
	maxtreey_in = max(treey_temp)
	mintreey_in = min(treey_temp)
	#	capture the boundary of tree clusters	#
	
	#	capture the boundary of bldg clusters	#
	maxbldgx_in = max(bldgx_in)
	minbldgx_in = min(bldgx_in)
	maxbldgy_in = max(bldgy_in)
	minbldgy_in = min(bldgy_in)
	#	capture the boundary of bldg clusters	#
	
	maxgridx_in = max([maxtreex_in, maxbldgx_in]) + redundancyborder_in
	maxgridy_in = max([maxtreey_in, maxbldgy_in]) + redundancyborder_in
	mingridx_in = min([mintreex_in, minbldgx_in]) - redundancyborder_in
	mingridy_in = min([mintreey_in, minbldgy_in]) - redundancyborder_in
	###	define the boundary of generated mesh	###
	
	###	generate the X-Y-Z grid	###
	nogridx_in = int((maxgridx_in - mingridx_in) / gridresolution_in)+1# Generally, no of grid in one direction is not an integer
	nogridy_in = int((maxgridy_in - mingridy_in) / gridresolution_in)+1
	
	gridx_in = np.linspace(mingridx_in, maxgridx_in, nogridx_in)
	gridy_in = np.linspace(mingridy_in, maxgridy_in, nogridy_in)
	
	gridgenarr_in = []
	for j in gridy_in:
		rowgridarr_in = []
		for i in gridx_in:
			rowgridarr_in.append([i,j,heightofinterset_in])
		gridgenarr_in.append(rowgridarr_in)
	###	generate the X-Y-Z grid	###
	
	return nogridx_in, nogridy_in, gridgenarr_in
######	Mesh generation at the height of interest	######


##	CODE TEST	##
# import Collectinfo
# import os
# gridresolution = 50
# heightofinterset = 1.5
# treeinfofile = './input/TreeKeyInfo.txt'
# bldginfofile = './input/BuildingPolygons.txt'
# NOTREE, treeinfoarr = Collectinfo.CollectTreeInfo(treeinfofile)
# NOBLDG, bldgno, bldgx, bldgy = Collectinfo.CollectBldgInfo(bldginfofile)
# nogridx, nogridy, gridgenarr = PlaneGridGen(gridresolution, treeinfoarr, bldgx, bldgy, heightofinterset)
# print(nogridx, nogridy)

# def create_dir_exist_or_not(path):
    # if not os.path.exists(path):
        # os.mkdir(path)
# create_dir_exist_or_not('./codetest')
# outputfile = './codetest/gridtest3.txt'
# with open(outputfile, 'w') as f_out:
	# for rowitem in gridgenarr:
		# for griditem in rowitem:
			# f_out.write(str(griditem[0]) + '	' + str(griditem[1]) + '\n')
##	CODE TEST	##
