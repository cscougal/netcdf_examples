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
#multiprocessing function. Essential it is copying all aparameters for each
# time series data within the netcdf file

start = time.time()

nc.multi_proc(nc.netcdf2GTIFF,input_list)

end= time.time()

finish = end- start

#estimated 2 minutes to convert netcdf with 1508 days of data to geotiffs













































#xmin, ymin , xmax , ymax = [lons.min(),lats.min(),lons.max(),lats.max()]
#nrows, ncols = np.shape(vosaline)
#
#xres = (xmax-xmin)/float(ncols)
#yres = (ymax-ymin)/float(nrows)
#
#
#geotransform=(xmin,xres,0,ymax,0, -yres)
#
#output_raster = gdal.GetDriverByName('GTiff').Create(out_path + 'myraster.tif',
#                                    ncols, nrows, 1 ,gdal.GDT_Float32)
#
#output_raster.SetGeoTransform(geotransform)  
#srs = osr.SpatialReference()             
#srs.ImportFromEPSG(4326)   
#output_raster.GetRasterBand(1).SetNoDataValue(-9999) 
#output_raster.SetProjection( srs.ExportToWkt() )
#                                                 
#output_raster.GetRasterBand(1).WriteArray(vosaline)  
#
#output_raster.FlushCache()
#
#
#del output_raster




#
#vosaline.min()
##gets first time step
#
#llcrnrlat =lats.min()
#urcrnrlat =lats.max()
#llcrnrlon =lons.min()
#urcrnrlon =lons.max()
#
#
#data.close()
#
#m = Basemap(projection='cyl',lon_0=0, llcrnrlat= llcrnrlat,
#            urcrnrlat = urcrnrlat,llcrnrlon = llcrnrlon,
#            urcrnrlon = urcrnrlon)    
#
#m.drawcountries()
#m.drawmapboundary(fill_color='0')
#
#lon, lat = np.meshgrid(lons, lats)
#xi, yi = m(lon, lat)
#


#fig = mp.figure()
#fig.frameon="false"
#mp.axis('off')
#fig.set_size_inches(12,10) 
#mp.tight_layout(pad=0)
##generic matplotlib settings
#
#ax = fig.add_axes([0.05,0.05,0.9,0.9])
#
#
#im = m.pcolormesh(xi,yi,vosaline,shading='flat',cmap=mp.cm.jet,latlon=True,vmin=0, vmax=32)
#cb = m.colorbar(im,"bottom", size="5%", pad="2%")
#cb.ax.tick_params(labelsize=12) 
#mp.title('TESTING ')









