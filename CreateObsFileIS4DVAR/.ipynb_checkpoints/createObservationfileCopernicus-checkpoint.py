'''The module is base on crateObservationFileAVHRR.py
   but here we will use the data downloaded from Copernicus 
   CopernicusSST.py'''

import xesmf as xe
import xarray as xr

import os, sys, datetime, string
import numpy as np
import CopernicusSST
import time
from datetime import timedelta, date


def getGrid():
    path_grind = '/home/lisapro/OneDrive/Documents/Projects/from Windows/norfjords_160m_grid_A04.nc'
    with xr.open_dataset(path_grind) as ds:

        #We get only 'rho' values
        grid_lon = ds.lon_rho.values
        grid_lat = ds.lat_rho.values      
        mask_rho = ds.mask_rho.values 

        grid_h = ds.h.values

        print ("Grid dimmensions: %s and %s"%(ds.lon_rho.shape,ds.lat_rho.shape))
        print (f"Grid domain longitude from {ds.lon_rho.min().values} to {ds.lon_rho.max().values}")
        print (f"Grid domain latitude from {ds.lat_rho.min().values} to {ds.lat_rho.max().values}")

        """Calculate the x,y grid coordinates"""
        #(Mp,Lp)= ds.lon_rho.shape
        #X=np.arange(0,Mp,1)
        #Y=np.arange(0,Lp,1)

        return mask_rho, grid_lon, grid_lat,grid_h,ds


def check_duplicates_output_file(outputFile):
    if os.path.exists(outputFile): 
        os.remove(outputFile)

def main():


    check_duplicates_output_file("NS8KM_Copernicus_obsSST.nc")

    """Read the grid info from the grid file"""
    mask_rho, lon_rho,lat_rho,grid_h,ds_grid = getGrid()

    ''' Read the file with SST data downloaded from Copernicus'''
    ds_copernicus = CopernicusSST.read_nc_sst()

    ds_out = ds_grid.rename({'lon_rho': 'lon', 'lat_rho': 'lat'})

    regridder = xe.Regridder(ds_copernicus.isel(time=0), ds_out, 'bilinear')
    #regridder.clean_weight_file()
    ds_out = regridder(ds_copernicus)
    print ('regridded, now saving netcdf ')
    try:
        ds_out.to_netcdf('Copernicus_regridded.nc')
    except Exception as e:
        print (e)
    
    """AVHRR time is days since 1978/1/1 00:00:00"""
    #refDate=datetime.datetime(1978,1,1,0,0,0)
    
    """Have to convert the day of observation to the relative time used by ROMS
    which is 1948/1/1:00:00:00"""
    #refDateROMS=datetime.datetime(1948,1,1,0,0,0)
    #delta=refDate-refDateROMS
    #daysSince1948to1978=delta.days

    '''                          
    survey_time=[]
    for currentDate in daterange(startDate, endDate):

        print ("\n-----\nCurrent date", currentDate)
        """Open the files and check that NOAA is online"""
        currentTime, sst,longitude = getAVHRR.openAVHRR(currentDate,indexes)
        currentDate=refDateROMS + datetime.timedelta(days=currentTime+daysSince1948to1978)
        
        """Interpolate the original values to the grid. This is the data that will be saved to file"""
        SSTi = mp.interp(sst,longitude,latitude,
                             lon_rho,lat_rho,checkbounds=False,masked=True,order=1)

        SSTi = np.where(SSTi < -0.5, -0.5, SSTi)
        print ("Mean SST %s"%(np.ma.mean(SSTi)))

        SSTi = SSTi*mask_rho

        igood=np.nonzero(SSTi)
        numberOfobs=len(SSTi[igood])

        obs_lon=lon_rho[igood]
        obs_lat=lat_rho[igood]
        obs_value=SSTi[igood]
        obs_Xgrid=roms_Xgrid[igood]
        obs_Ygrid=roms_Ygrid[igood]
        Nobs=numberOfobs
        survey_time.append(currentTime+daysSince1948to1978)
       
        obs_time=[]
        for ot in xrange(numberOfobs):
            obs_time.append(currentTime+daysSince1948to1978)
            if ot==0:
                print ("Date to file:", refDateROMS + datetime.timedelta(days=currentTime+daysSince1948to1978),currentTime+daysSince1948to1978)

        print ("Found %s observations for %s"%(numberOfobs, currentDate))

        """Create map where the colored data shows the interpolated values and the
            grey colored data are the original data"""
        """Define the max and minimim area to crate map for (not used to create obs file)"""
        lat_start=43; lat_end=71.5; lon_start=-20; lon_end=35



        """ Finished, now cleanup and make sure everything are arrays"""
        obs_time=np.asarray(obs_time)


        """Finally write the results to file"""

        """Temp variables not used until lastIteration is set to True, but required for function call"""
        obs_flag = 6; is3d = 1; survey =0; Nstate = 7
        if firstIteration is True:
            print( "Writing data of TYPE: %s to file (6=Temperature)"%(obs_flag))

        unos = np.ones(len(obs_value))
        obs_type = obs_flag*unos
        obs_error = unos   # error eqaul one scale later
        obs_Zgrid = 0*unos
        obs_depth = 35*unos #If positive has to be the sigma level, if negative depth in meters
        obs_variance=np.asarray(np.ones(Nstate))


        print ("Min and max of SST to file: %s - %s"%(obs_value.min(),obs_value.max()))


        writeObsfile.writeData(outputFile,obs_lat,obs_lon,obs_value,Nobs,survey_time,obs_time,obs_Xgrid,obs_Ygrid,
                                   firstIteration,lastIteration,
                                   obs_flag,obs_type,obs_error,obs_Zgrid,obs_depth,obs_variance,
                                   survey,is3d,Nstate,USENETCDF4)
        firstIteration=False
       

    """Cleanup and write final dimensions and variables"""
    lastIteration=True
    """ some extra variables """

    obs_flag = 6       # for temperature data
    is3d = 1
    survey=len(survey_time)
    survey_time=np.asarray(survey_time)
    survey_time=survey_time.flatten()
    Nstate = 7

    writeObsfile.writeData(outputFile,obs_lat,obs_lon,obs_value,Nobs,survey_time,obs_time,obs_Xgrid,obs_Ygrid,
                               firstIteration,lastIteration,
                               obs_flag,obs_type,obs_error,obs_Zgrid,obs_depth,obs_variance,
                               survey,is3d,Nstate,USENETCDF4)

    endTime=time.time()

    print ("Program ended successfully after %s seconds"%(endTime-startTime))
    '''

if __name__ == "__main__":

    #main()
    mask_rho, lon_rho,lat_rho,grid_h= getGrid()
    
