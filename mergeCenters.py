"""
This module merges all the cluster centers 
and creates final cluster centers for the 
training database.
"""
import numpy as np
import cv2
from cv2 import __version__
import os
import pickle
import sys

def mergeCenters(nCenters):
	"""
	This function loads the cluster centers from ./Centers/ 
	directory and stores final centers in centerFinal.p file 
	in current directory. The centers are clubed together in 
	single numpy array and then kmeans is applied over the 
	clubed centers.
	"""
	path = os.getcwd()
	os.chdir('Centers/')
	center = np.zeros((0,128))		#: Populator for centers

	for i in os.listdir(os.getcwd()):
	    Center = open(i,"rb")		#: File pointer for centers file
	    center = np.vstack((center, pickle.load(Center)))	#Populate centers
	    Center.close()

	center = np.float32(center)
	criteria = (cv2.TERM_CRITERIA_MAX_ITER, 10,0.0001)
	#Checking version of opencv..
	if __verison__[0] == '3':
		ret,label,center=cv2.kmeans(center,int(nCenters),None,criteria,50,cv2.KMEANS_PP_CENTERS)
	else:
		ret,label,center=cv2.kmeans(center,int(nCenters),criteria,50,cv2.KMEANS_PP_CENTERS)

	CenterFinal = open(path+'/centerFinal.p',"wb")#: File pointer for final centers file
	pickle.dump(center, CenterFinal)	#Dump centers to file
	CenterFinal.close()

if __name__ == '__main__':
	if(len(sys.argv)!=2):
		print('Error. Usage: python mergeCenters.py numCenters')
	else:
		mergeCenters(sys.argv[1])
