# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:33:20 2018

@author: CS08
"""

from netCDF4 import Dataset , num2date
import numpy as np
import gdal ,  osr
from multiprocessing.dummy import Pool as ThreadPool 
import multiprocessing


#This approach uses gdal bindings, alternative approaches using modules
#like xarray could be useful to explore


#This module holds a  variety of fucntions designed to handle, process, and
# visualise, netcdf data



def netCDFVariables(input_data):
    
    '''Simple function which returns the dimensions of a netCDF file and the
        variable keys within'''

    data = Dataset(input_data,'r')
    
    dimensions = list(data.dimensions.keys())
    variable_keys = list(data.variables.keys())
    #variable_items = list(data.variables.items())
    #print (data.variables["crs"])
    
    return variable_keys , dimensions
        
     
    
def netCDFData(input_data,lat,lon,my_time): 
    
    '''Gets geodata, time,pixel data etc. from a netcdf file'''
    
    data = Dataset(input_data,'r')    
    lats = data.variables[lat][:]
    lons = data.variables[lon][:]
 
    dtime = num2date(data.variables[my_time][:],data.variables[my_time].units)
    #converts netcdf time to python datetime
    dtime = [ i.strftime("%Y-%m-%d") for i in dtime]
    
    gtif = gdal.Open( input_data )
    
    gdal_info = gdal.Info(gtif, format='json')
    #very useful, returns meta data from raster data
    
    originX = gdal_info["geoTransform"][0]
    originY = gdal_info["geoTransform"][3]
    pixelX = gdal_info["geoTransform"][1]
    pixelY = gdal_info["geoTransform"][5]
    
    return data, lats, lons ,dtime ,originX, originY, pixelX ,pixelY,gdal_info



def multi_proc(func,input_list):
    
    '''This function allows use to use multi core processing on a given 
        function and allows multiple arguments'''

    pool = ThreadPool(multiprocessing.cpu_count()) 
    data= pool.starmap(func,input_list) 
    pool.close() 
    pool.join()
    
    return data



def netcdf2GTIFF(data,my_variable,rows,cols,outpath,name_prefix,my_date,step,
                 crs,originX,originY,pixelX,pixelY):
                     
    '''Function which takes netcdf as an array with  various metadata and 
        converts to a geotiff file using gdal bindings'''             
     
    my_variable = data.variables[my_variable][step].squeeze()
    #this gets the variable values at a given index
     
    my_variable = my_variable[::-1]
    #flips the array to correct orientation
    my_variable = np.ma.filled(my_variable,-9999)
    #fills masked vlaues with set num
           
    driver = gdal.GetDriverByName('GTiff')
    
    output_raster = driver.Create(outpath + name_prefix + my_date+".tif", 
                                  cols, rows,1,gdal.GDT_Float32)
    #creates empty output raster whith desired spec.
    
    output_raster.SetGeoTransform((originX, pixelX, 0, originY, 0, pixelY))
    #sets origin and pixel vals based on gdal info
    
    srs = osr.SpatialReference()             
    srs.ImportFromEPSG(crs)   
    output_raster.SetProjection( srs.ExportToWkt()) 
    output_raster.GetRasterBand(1).SetNoDataValue(-9999) 
    #sets CRS , no data values
    
    output_raster.GetRasterBand(1).WriteArray(my_variable)
    #writes data to raster
    output_raster.FlushCache()
    
    del output_raster
    del my_variable
    





