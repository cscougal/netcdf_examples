# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:33:20 2018

@author: CS08
"""


import time
import sys 
sys.path.append(r"C:\Users\cs08\OneDrive -CEFAS\python_scripts\clean examples")
import netcdf_functions as nc



input_data =r"W:\Environmental variables\Salinity_Copernicus.eu\Seasurface\\"+\
        "MetO-NWS-PHYS-dm-SAL_1528112337498.nc"

out_path = r"W:\Environmental variables\Salinity_Copernicus.eu\Seasurface\\"+\
            "cs_sst\\"


keys, dimensions = nc.netCDFVariables(input_data) 
#gets us variables and dimensions

cdf_data = nc.netCDFData(input_data,"lat","lon","time")
#returns data , coordiantes, pixel info etc.
 
data, lats, lons, dtime = cdf_data[0], cdf_data[1], cdf_data[2], cdf_data[3]
originX ,originY = cdf_data[4], cdf_data[5]
pixelX ,pixelY =  cdf_data[6],cdf_data[7]
meta = cdf_data[8]

cols = lons.shape[0]
rows = lats.shape[0]
my_variable = 'vosaline'
#this can be passed to any variable present within the netcdf file
name = "Surf_salin"
crs=4326

input_list=[(data,my_variable,rows,cols,out_path,name,i,idx,crs,
             originX,originY,pixelX,pixelY) for idx,i in enumerate(dtime)]

#This creates a list of lists containing the relevant arguments to pass to the
#multiprocessing function. Essentially it is copying all parameters for each
#time series data within the netcdf file

start = time.time()

nc.multi_proc(nc.netcdf2GTIFF,input_list)

end= time.time()

finish = end- start

#estimated 2 minutes to convert netcdf with 1508 days of data to geotiffs





