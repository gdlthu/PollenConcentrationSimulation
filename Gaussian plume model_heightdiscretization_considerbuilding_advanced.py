###   __This py is used to perform GAUSSIAN PLUME MODEL (considering discretization along height and building shading)__	###

import Collectinfo
import Meshgeneration
import Parametercalculator
import Heightdiscretization

import os
import time
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.geometry import Polygon
from multiprocessing import Pool


start=time.time()

######	Input file	######
treeinfofile = './input/TreeKeyInfo_revise.txt'
bldginfofile = './input/BuildingPolygons.txt'
bldgheightfile = './input/BuildingHeight.txt'
plotfigure = True# whether plot the figure of pollen concentration

weatherinfo = [0, -1, 1]# isolation 1: daytime strong; isolation 2: daytime moderate; isolation 3: daytime slight

gridresolution = 50
dhresolution = 1
heightofinterset = 1.5
agents = 4

limitvalue = 20
normlimit = 10
interval = 1
t2_level=np.arange(0,normlimit+interval,interval)

distancelimit = 200
######	Input file	######

print('######	Version: Considering building shading	######')
print('######	Grid resolution: ' + str(gridresolution) + ' m	######')
print('######	Height resolution: ' + str(dhresolution) + ' m	######')

######	Output file	######
def create_dir_exist_or_not(path):#	Check directory exist or not	#
    if not os.path.exists(path):
        os.mkdir(path)
create_dir_exist_or_not('./output')
outputfile = './output/HDis_Bldg_Pollen Concentration_{}_{}_{}-{}-{}.txt'.\
	format(gridresolution, dhresolution, weatherinfo[0], weatherinfo[1], weatherinfo[2])
outputfile2 = './output/HDis_Bldg_Time Consumed_{}_{}_{}-{}-{}.txt'.\
	format(gridresolution, dhresolution, weatherinfo[0], weatherinfo[1], weatherinfo[2])
figname = './output/HDis_Bldg_Figure_{}_{}_{}-{}-{}.png'.\
	format(gridresolution, dhresolution, weatherinfo[0], weatherinfo[1], weatherinfo[2])
######	Output file	######

print('######	Collect Tree Data	######')
NOTREE, treeinfoarr = Collectinfo.CollectTreeInfo(treeinfofile)
print('######	Collect Bldg Data	######')
NOBLDG, bldgno, bldgx, bldgy, polyallbldg, bldgheight = Collectinfo.CollectBldgInfo(bldginfofile, bldgheightfile)

print('######	Generate Grid	######')
nogridx, nogridy, gridgenarr = Meshgeneration.PlaneGridGen(gridresolution, treeinfoarr, bldgx, bldgy, heightofinterset)


######	Determine whether gird point is WITHIN bldg polygons	######
def GridInorOutBldg(gridpoint_in):
	
	###	accept (1)grid point = [x, y, z]
	
	###	return (1)determine whether gird point is within bldg polygons, True or False
	
	global NOBLDG, bldgno, bldgx, bldgy, polyallbldg, bldgheight
	
	J_in = 0
	for p in range(NOBLDG):
		if Point(gridpoint_in[0], gridpoint_in[1]).intersects(polyallbldg[p]):
			J_in = J_in + 1
	
	return (J_in > 0)
######	Determine whether gird point is WITHIN bldg polygons	######


######	Determine whether gird point is BEHIND one bldg	######
def GridNOTBehindBldg(gridpoint_in, sourcepoint_in):
	
	###	accept (1)grid point = [x, y, z]
	###	accept (2)source point = [x, y, z]
	
	###	return (1)determine whether gird point is NOT behind one specific bldg, True or False
	
	global NOBLDG, bldgno, bldgx, bldgy, polyallbldg, bldgheight
	
	# horizational plane
	sourceorigin_in = (sourcepoint_in[0], sourcepoint_in[1])
	gridorigin_in = (gridpoint_in[0],gridpoint_in[1])
	
	targetline_in = LineString([sourceorigin_in, gridorigin_in])
	# horizontal plane
	
	J_in = 0
	for p in range(NOBLDG):
		bldgpolygon_in = polyallbldg[p]
		bldgh = bldgheight[p]
		
		if bldgpolygon_in.intersects(targetline_in):# intersection in the horizontal plane
			intersectionpoint_in = bldgpolygon_in.intersection(targetline_in)
			#	check for object type to retrieve all intersection coordinates
			if intersectionpoint_in.type == "LineString":
				coords = np.asarray([intersectionpoint_in.coords.xy])
			elif intersectionpoint_in.type == "MultiLineString":
				coords = np.asarray([l.coords.xy for l in intersectionpoint_in.geoms])
			#	check for object type to retrieve all intersection coordinates
			
			#	reshape array point coordinates into a form that does not make my head hurt
			coords = coords.transpose(1, 0, 2).reshape(2, -1)
			intersectionnumber = len(coords[0])
			intersectionlist_in = []
			for i in range(intersectionnumber):
				intersectionlist_in.append((coords[0][i], coords[1][i]))
			#	reshape array point coordinates into a form that does not make my head hurt
			
			intersectionlen_in = []
			for isp in intersectionlist_in:
				ispdistance_in = Point(sourceorigin_in).distance(Point(isp))
				intersectionlen_in.append(ispdistance_in)
			
			# vertical plane
			source_vertical_in = (0, sourcepoint_in[2])
			gird_vertical_in = (Point(sourceorigin_in).distance(Point(gridorigin_in)), gridpoint_in[2])
			tergetline_vertical_in = LineString([source_vertical_in, gird_vertical_in])
			
			if len(intersectionlen_in) == 1:# only one instersection point
				ispx_in = intersectionlen_in[0]
				ispy_in = bldgh
				bldgline_vertical_in = LineString([(ispx_in, 0), (ispx_in, ispy_in)])
				if tergetline_vertical_in.intersects(bldgline_vertical_in):# intersection in the vertical plane
					J_in = J_in + 1
			else:# more than one instersection point
				ispx1_in = min(intersectionlen_in)
				ispx2_in = max(intersectionlen_in)
				ispy_in = bldgh
				bldgpolygon_vertical_in = Polygon([(ispx1_in, 0),(ispx1_in, ispy_in), (ispx2_in, ispy_in), (ispx2_in, 0)])
				if tergetline_vertical_in.intersects(bldgpolygon_vertical_in):# intersection in the vertical plane
					J_in = J_in + 1
			# vertical plane
	
	return (J_in == 0)
######	Determine whether gird point is BEHIND one bldg	######


######	Simple Gaussian plume model (one grid)	######
def GaussianPlumeModel_simple(targetinfo_in):
	
	###	accept (1)grid information, targetinfo_in=[x, y, z]
	
	###	return (1)realitive value of pollen concentration
	
	global NOTREE, treeinfoarr
	global weatherinfo
	global dhresolution
	
	if GridInorOutBldg(targetinfo_in):
		targetpollen_in = 0
	else:
		targetpollen_in = 0
		for sourceinfo_in in treeinfoarr:
			XSOURCE_in = sourceinfo_in[0]
			YSOURCE_in = sourceinfo_in[1]
			TYPESOURCE_in = sourceinfo_in[2]
			HEIGHTSTEM_in = sourceinfo_in[3]
			HEIGHTTREE_in = sourceinfo_in[4]
			DIACROWN_in = sourceinfo_in[5]
			HEIGHTCROEN_in = HEIGHTTREE_in-HEIGHTSTEM_in
			
			if HEIGHTCROEN_in == 0:
				pollenconcentration_in = 0
			else:
				NOSOURCE_in, ZSOURCELIST_in, VSOURCELIST_in = \
					Heightdiscretization.CrownDiscretization(dhresolution, TYPESOURCE_in, HEIGHTSTEM_in, HEIGHTTREE_in, DIACROWN_in)
				
				XTARGET_in = targetinfo_in[0]
				YTARGET_in = targetinfo_in[1]
				ZTARGET_in = targetinfo_in[2]
				
				UX_in = weatherinfo[0]
				UY_in = weatherinfo[1]
				ISLT_in = weatherinfo[2]
				
				XTARGET_ROTATE_in, YTARGET_ROTATE_in, UWIND_in = \
				Parametercalculator.SourceBasedCoordinateTransformation(XSOURCE_in, YSOURCE_in, XTARGET_in, YTARGET_in, UX_in, UY_in)
				
				QVALUE_in = Parametercalculator.QCalculation(TYPESOURCE_in)
				SIGMAY_in, SIGMAZ_in = Parametercalculator.SDofConcentrationDistribution(ISLT_in, UWIND_in, XTARGET_ROTATE_in)
				
				if QVALUE_in * XTARGET_ROTATE_in <= 0:#	target grid is in upwind direction of source
					pollenconcentration_in = 0
				elif XTARGET_ROTATE_in >= distancelimit:#	target grid is far engough from source
					pollenconcentration_in = 0
				elif not GridNOTBehindBldg(targetinfo_in, [XSOURCE_in, YSOURCE_in, ZSOURCELIST_in[-1]]):
					#	target grid is totally affected by building shading
					pollenconcentration_in = 0
				else:
					#	generate the shading factor, shading innersource = 0, free innersource = 1
						#	e.g., shadinglist_in = [0, 0, 0, 0, 1]
					shadinglist_in = np.zeros(NOSOURCE_in)
					for i in range(NOSOURCE_in):
						if np.sum(shadinglist_in) == 0:
							ZSOURCE_in = ZSOURCELIST_in[i]
							sourcepoint_in = [XSOURCE_in, YSOURCE_in, ZSOURCE_in]
							if GridNOTBehindBldg(targetinfo_in, sourcepoint_in):
								shadinglist_in[i] = 1
						else:
							shadinglist_in[i] = 1
					#	generate the shading factor, shading innersource = 0, free innersource = 1	
					
					pollenconcentration_in = 0
					for i in range(NOSOURCE_in):
						if shadinglist_in[i] == 1:
							ZSOURCE_in = ZSOURCELIST_in[i]
							VSOURCE_in = VSOURCELIST_in[i]
							CONCENTRATION1_in = QVALUE_in*VSOURCE_in/2/math.pi/UWIND_in/SIGMAY_in/SIGMAZ_in
							CONCENTRATION2_in = math.exp((-1)*YTARGET_ROTATE_in*YTARGET_ROTATE_in/2/SIGMAY_in/SIGMAY_in)
							CONCENTRATION3_in = math.exp((-1)*(ZTARGET_in-ZSOURCE_in)*(ZTARGET_in-ZSOURCE_in)/2/SIGMAZ_in/SIGMAZ_in) + \
								math.exp((-1)*(ZTARGET_in+ZSOURCE_in)*(ZTARGET_in+ZSOURCE_in)/2/SIGMAZ_in/SIGMAZ_in)
							pollenconcentration_in = pollenconcentration_in + CONCENTRATION1_in * CONCENTRATION2_in * CONCENTRATION3_in
					
			targetpollen_in = targetpollen_in + pollenconcentration_in
		
	return targetpollen_in
######	Simple Gaussian plume model (one grid)	######


######	Simple Gaussian plume model (grids in a row, designed for parallel computing)	######
def GaussianPlumeModel_simple_row(rowinfo_in):
	
	###	accept (1)grid information in a row, rowinfo_in=[[x1, y1, z1], [x2, y2, z2], ...]
	
	###	return (1)realitive values of pollen concentration in a row, list object
	
	gridpollen_in = []
	for grid_in in rowinfo_in:
		gridpollen_in.append(GaussianPlumeModel_simple(grid_in))
	
	return gridpollen_in
######	Simple Gaussian plume model (grids in a row, designed for parallel computing)	######


######	MAIN	MAIN	MAIN	######
if __name__ == '__main__':
	print('######	Compute Pollen Concentration using Parallel Cores: ' + str(agents) + '	######')
	with Pool(processes=agents) as pool:
		pollenlist = pool.map(GaussianPlumeModel_simple_row, gridgenarr)# 2D list object
	
	print('######	Write pollen concenstration results	######')
	with open(outputfile, 'w') as f_out:
		f_out.write('ID   X   Y   Z    Concentration\n')
		
		m = 0
		for j in range(nogridy):
			for i in range(nogridx):
				f_out.write(str(m+1) + '  ' + \
					str(gridgenarr[j][i][0]) + '  ' + str(gridgenarr[j][i][1]) + '  ' +\
					str(heightofinterset) + '  ' + str(pollenlist[j][i]) + '\n')
				m = m + 1	
	end=time.time()
	
	print('######	Plot the Figure   ######')
	###	plot the figure of pollen concentration	###
	if plotfigure:
		start2=time.time()
		
		gridgenarr_X = []
		for i in range(nogridx):
			gridgenarr_X.append(gridgenarr[0][i][0])	
		gridgenarr_Y = []
		for j in range(nogridy):
			gridgenarr_Y.append(gridgenarr[j][0][1])
		
		#	values higher than the limitvalue is set as the limit, then values are normalized between 0-10
		for j in range(nogridy):
			for i in range(nogridx):
				pollenlist[j][i] = min(pollenlist[j][i], limitvalue)/limitvalue*10
		#	values higher than the limitvalue is set as the limit, then values are normalized between 0-10
		
		fig = plt.figure(figsize=(7.5,7))
		im = fig.add_subplot(111)
		plt.xlim(-1000,1000)
		plt.ylim(-1200,1200)
		plt.tick_params(axis='both',which='major',labelsize=16)
		x_major_locator = MultipleLocator(500)
		y_major_locator = MultipleLocator(500)
		ax = plt.gca()
		ax.xaxis.set_major_locator(x_major_locator)
		ax.yaxis.set_major_locator(y_major_locator)
		labels=ax.get_xticklabels()+ax.get_yticklabels()
		[label.set_fontproperties(FontProperties(fname="./font/Arial.ttf",size=16)) for label in labels]
		
		pcf = plt.contourf(gridgenarr_X,gridgenarr_Y,pollenlist,levels=t2_level,alpha=1,cmap=plt.cm.jet)
		#plt.xlabel('x coordinate (m)', fontsize = 15)
		#plt.ylabel('y coordinate (m)', fontsize = 15)
		
		fig.subplots_adjust(right=0.8)
		rect = [0.83, 0.15, 0.018, 0.7] 
		cbar_ax = fig.add_axes(rect)
		cb = fig.colorbar(pcf, drawedges=False, ticks=t2_level, cax=cbar_ax, orientation='vertical',spacing='uniform')
		labels=cb.ax.get_xticklabels()+cb.ax.get_yticklabels()
		[label.set_fontproperties(FontProperties(fname="./font/Arial.ttf",size=16)) for label in labels]
		
		# plot bldgs
		k = 0
		for i in range(NOBLDG):
			polyarr = []
			No_vertics_i = bldgno.count(i)
			for p in range(No_vertics_i-1):
				polyarr_temp = []
				polyarr_temp.append(bldgx[k])
				polyarr_temp.append(bldgy[k])
				polyarr.append(polyarr_temp)
				k = k+1
			k = k+1
			pgon = plt.Polygon(polyarr, ec='black', fc='w', linewidth = 0.8)
			im.add_patch(pgon)
		# plot bldgs
	
		plt.savefig(figname,dpi=1000)
		end2=time.time()
		
		with open(outputfile2, 'w') as f_out2:
			f_out2.write('Time for computation with ' + str(agents) + ' cores:' + ' ' + str(end-start) + '\n')
			f_out2.write('Time for figure:' + ' ' + str(end2-start2))
	else:
		with open(outputfile2, 'w') as f_out2:
			f_out2.write('Time for computation with ' + str(agents) + ' cores:' + ' ' + str(end-start) + '\n')
	###	plot the figure of pollen concentration	###
######	MAIN	MAIN	MAIN	######
