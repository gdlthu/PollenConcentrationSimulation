###   __This py is used to calculate basic parameters except for PDd of AIROT model__	###

#   Including functions (1)QCalculation(treetype_in, areacrown_in), for Gaussian Plume model
#   Including functions (2)SDofConcentrationDistribution(insolation_in, windspeed_in, downwinddistance_in), for Gaussian Plume model
#   Including functions (3)SourceBasedCoordinateTransformation(xs_in, ys_in, xt_in, yt_in, ux_in, uy_in), for Gaussian Plume model

import math

######	Determination of pollen emitting rate Q	######
def QCalculation(treetype_in):
	
	###	accept (1)tree type: 1-14
	
	###	return (1)Q value per m3 (unit: kg/s/m3)
	
	#unitsource_in = [2,3,0,3,0,0,0,0,0,3,0,1,0,3]
	unitsource_in = [2,3,0,3,1,1,0,1,0,3,1,2,1,3]# please see our paper
	pollenrate_in = unitsource_in[treetype_in-1]
	
	return pollenrate_in
######	Determination of pollen emitting rate Q	######


######	Sigma calculation at a specific downwind distance	######
def SDofConcentrationDistribution(insolation_in, windspeed_in, downwinddistance_in):
	
	###	accept (1)insolation type: 1, 2, 3
	###	accept (2)wind speed at 10 m (unit: m/s)
	###	accept (3)downwind distance (unit: m)
	
	###	return (1)sigma value (unit: m)
	
	stabilityconditions_y = {
		'A':[5.357, 0.8828],
		'B':[5.058, 0.9024],
		'C':[4.651, 0.9181],
		'D':[4.230, 0.9222],
		'E':[3.922, 0.9222],
		'F':[3.533, 0.9181]}
	
	stabilityconditions_z = {
		'A':[6.035, 2.1097],
		'B':[4.694, 1.0629],
		'C':[4.110, 0.9201],
		'D':[3.414, 0.7371],
		'E':[3.057, 0.6794],
		'F':[2.621, 0.6564]}
	
	if insolation_in == 1:# Daytime, strong insolation
		if windspeed_in < 2:
			STABILITY_in = 'A'
		elif windspeed_in <= 3:
			STABILITY_in = 'B'
		elif windspeed_in <= 5:
			STABILITY_in = 'B'
		elif windspeed_in <= 6:
			STABILITY_in = 'C'
		else:
			STABILITY_in = 'C'
	elif insolation_in == 2:# Daytime, moderate insolation
		if windspeed_in < 2:
			STABILITY_in = 'B'
		elif windspeed_in <= 3:
			STABILITY_in = 'B'
		elif windspeed_in <= 5:
			STABILITY_in = 'C'
		elif windspeed_in <= 6:
			STABILITY_in = 'D'
		else:
			STABILITY_in = 'D'
	else:# Daytime, slight insolation
		if windspeed_in < 2:
			STABILITY_in = 'B'
		elif windspeed_in <= 3:
			STABILITY_in = 'C'
		elif windspeed_in <= 5:
			STABILITY_in = 'C'
		elif windspeed_in <= 6:
			STABILITY_in = 'D'
		else:
			STABILITY_in = 'D'
	
	CONSTANTY_I_in = stabilityconditions_y[STABILITY_in][0]
	CONSTANTY_J_in = stabilityconditions_y[STABILITY_in][1]
	CONSTANTZ_I_in = stabilityconditions_z[STABILITY_in][0]
	CONSTANTZ_J_in = stabilityconditions_z[STABILITY_in][1]
	#	sigma = ax^b, x = downwinddistance_in(unit: m)/1000 with the unit of km
	#	a = e^I, b = J
	downwinddistance_in = max(downwinddistance_in, 0)
	sdy_in = math.exp(CONSTANTY_I_in) * math.pow(downwinddistance_in/1000, CONSTANTY_J_in)
	sdz_in = math.exp(CONSTANTZ_I_in) * math.pow(downwinddistance_in/1000, CONSTANTZ_J_in)
	
	return sdy_in, sdz_in
# ##	CODE TEST	##
# print(SDofConcentrationDistribution(2, 5.5, -2))
######	Sigma calculation at a specific downwind distance	######


######	Establishment of local coordinate system	######
def SourceBasedCoordinateTransformation(xs_in, ys_in, xt_in, yt_in, ux_in, uy_in):
	
	###	accept (1)x coordinate of source
	###	accept (2)y coordinate of source
	###	accept (3)x coordinate of target grid
	###	accept (4)y coordinate of target grid
	###	accept (5)wind speed in x direction (positive or negative)
	###	accept (6)wind speed in y direction (positive or negative)
	
	###	return (1)transformated x coordinate of target grid based on source location and wind direction
	###	return (2)transformated y coordinate of target grid based on source location and wind direction
	###	return (3)wind speed magnitude
	
	XT_TEMP_in = xt_in - xs_in
	YT_TEMP_in = yt_in - ys_in
	UWIND_in = math.pow((ux_in*ux_in + uy_in*uy_in), 0.5)
	COSSITA_in = ux_in / UWIND_in
	SINSITA_in = uy_in / UWIND_in
	xt_rotate_in = COSSITA_in * XT_TEMP_in + SINSITA_in * YT_TEMP_in
	yt_rotate_in = COSSITA_in * YT_TEMP_in - SINSITA_in * XT_TEMP_in
	
	return xt_rotate_in, yt_rotate_in, UWIND_in
# ##	CODE TEST	##
# print(SourceBasedCoordinateTransformation(1, 1, 5, 5, 1, 1))
######	Establishment of local coordinate system	######
