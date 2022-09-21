###   __This py is used to discretize tree crowns alonge the height__	###

#   Including functions (1)CrownDiscretization(dhresolution_in, type_in, hstem_in, htree_in, dcrown_in)

import numpy as np
import math

######	Tree crown discretization along the height	######
def CrownDiscretization(dhresolution_in, type_in, hstem_in, htree_in, dcrown_in):
	
	###	accept (1)discretization resolution of tree height /m
	###	accept (2)height of stem /m
	###	accept (3)maximum diameter of crwon /m
	
	###	return (1)discretized source heights of one specific height, list object
	###	return (2)discretized source area ratios of one specific height, list object
	
	HCROWN_in = htree_in - hstem_in
	VolCROWN = math.pi * dcrown_in * dcrown_in * HCROWN_in / 12
	#AREACROWN_in = HCROWN_in*dcrown_in / 2
	tritype_in = [1]#	Two types are considered, i.e., triangle and diamond
	
	if HCROWN_in % dhresolution_in == 0:
		NODH_in = int(HCROWN_in / dhresolution_in)
	else:
		NODH_in = int(HCROWN_in / dhresolution_in) + 1
	
	dharr_in = []#	discretized source heights of one specific height
	dvarr_in = []#	discretized source volume of one specific height
	
	if type_in in tritype_in:#	triangle
		DHREAL_in = HCROWN_in / NODH_in
		#	Note: an approximation is adopted
		DELTAZ_in = DHREAL_in / 2 + hstem_in
		dharr_in.append(DELTAZ_in)
		for i in range(1, NODH_in):
			DELTAZ_in = DELTAZ_in + DHREAL_in
			dharr_in.append(DELTAZ_in)
		#	Note: an approximation is adopted
		
		DOUBLECORNER_in = DHREAL_in*dcrown_in/HCROWN_in
		LENSOURCE_in = dcrown_in
		for i in range(NODH_in-1):
			DELTAVOL = math.pi/12 * DHREAL_in * \
				(math.pow(LENSOURCE_in,2) + math.pow(LENSOURCE_in-DOUBLECORNER_in,2) + \
				LENSOURCE_in * (LENSOURCE_in-DOUBLECORNER_in))
			dvarr_in.append(DELTAVOL)
			LENSOURCE_in = LENSOURCE_in - DOUBLECORNER_in
		dvarr_in.append(math.pi/12 * LENSOURCE_in * LENSOURCE_in * DHREAL_in)
	else:#	diamond
		#	Note: an approximation is adopted
		if NODH_in <= 2:
			NODH_upper_in = 1
			NODH_lower_in = 1
		else:
			if (NODH_in * 2) % 3 == 0:
				NODH_upper_in = int(NODH_in * 2/3)
			else:
				NODH_upper_in = int(NODH_in * 2/3) + 1
			NODH_lower_in = NODH_in - NODH_upper_in
		
		HCROWN_upper_in = HCROWN_in * 2/3
		HCROWN_lower_in= HCROWN_in - HCROWN_upper_in
		DHREAL_upper_in = HCROWN_upper_in / NODH_upper_in
		DHREAL_lower_in = HCROWN_lower_in / NODH_lower_in
			
			# lower part of crown
		DELTAZ_lower_in = DHREAL_lower_in / 2 + hstem_in
		dharr_in.append(DELTAZ_lower_in)
		if NODH_lower_in > 1:
			for i in range(1, NODH_lower_in):
				DELTAZ_lower_in = DELTAZ_lower_in + DHREAL_lower_in
				dharr_in.append(DELTAZ_lower_in)
			# lower part of crown
			
			# upper part of crown
		DELTAZ_upper_in = DHREAL_upper_in / 2 + HCROWN_lower_in + hstem_in
		dharr_in.append(DELTAZ_upper_in)
		if NODH_upper_in > 1:
			for i in range(1, NODH_upper_in):
				DELTAZ_upper_in = DELTAZ_upper_in + DHREAL_upper_in
				dharr_in.append(DELTAZ_upper_in)
			# upper part of crown
		#	Note: an approximation is adopted
		
			# lower part of crown
		DOUBLECORNER_lower_in = DHREAL_lower_in*dcrown_in/HCROWN_lower_in
		LENSOURCE_lower_in = dcrown_in
		dvarr_lower_in = []
		for i in range(NODH_lower_in-1):
			DELTAVOL = math.pi/12 * DHREAL_lower_in * \
				(math.pow(LENSOURCE_lower_in,2) + math.pow(LENSOURCE_lower_in-DOUBLECORNER_lower_in,2) + \
				LENSOURCE_lower_in * (LENSOURCE_lower_in-DOUBLECORNER_lower_in))
			dvarr_lower_in.append(DELTAVOL)
			LENSOURCE_lower_in = LENSOURCE_lower_in - DOUBLECORNER_lower_in
		dvarr_lower_in.append(math.pi/12 * LENSOURCE_lower_in * LENSOURCE_lower_in * DHREAL_lower_in)
		dvarr_lower_in.reverse()
		for item in dvarr_lower_in:
			dvarr_in.append(item)
			# lower part of crown
		
			# upper part of crown
		DOUBLECORNER_upper_in = DHREAL_upper_in*dcrown_in/HCROWN_upper_in
		LENSOURCE_upper_in = dcrown_in
		for i in range(NODH_upper_in-1):
			DELTAVOL = math.pi/12 * DHREAL_upper_in * \
				(math.pow(LENSOURCE_upper_in,2) + math.pow(LENSOURCE_upper_in-DOUBLECORNER_upper_in,2) + \
				LENSOURCE_upper_in * (LENSOURCE_upper_in-DOUBLECORNER_upper_in))
			dvarr_in.append(DELTAVOL)
			LENSOURCE_upper_in = LENSOURCE_upper_in - DOUBLECORNER_upper_in
		dvarr_in.append(math.pi/12 * LENSOURCE_upper_in * LENSOURCE_upper_in * DHREAL_upper_in)
			# upper part of crown
	
	return 	NODH_in, dharr_in, dvarr_in

# ##	CODE TEST	##
# dhresolution = 2
# typetree = 3
# hstem = 3
# htree = 10
# dcrown = 2
# nodh, dharr, dsararr = CrownDiscretization(dhresolution, typetree, hstem, htree, dcrown)
# print(nodh)
# print(dharr)
# print(dsararr)
# ##	CODE TEST	##
