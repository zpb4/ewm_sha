# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 10:14:45 2025

@author: zpb4
"""

import pandas as pd
import numpy as np
import xarray as xr
import sys

short_names = ['u10','v10','d2m','t2m','tp','tcc']
yrs = 1940 + np.arange(2024-1940+1)
nth = 41
sth = 40.5
wst = -122.5
est = -122

var_names = [
     "10m_u_component_of_wind",
     "10m_v_component_of_wind",
     "2m_dewpoint_temperature",
     "2m_temperature",
     "total_precipitation",
     "total_cloud_cover"
 ]

for k in range(len(var_names)):
    output_folder = './raw_data/%s_%s.nc' %(var_names[k],yrs[0])
    da = xr.open_dataset(output_folder, engine="netcdf4")

    dat = da[short_names[k]].values
    out = np.mean(dat,axis=(1,2))

    for i in range(1,len(yrs)):
        output_folder = './raw_data/%s_%s.nc' %(var_names[k],yrs[i])
        da = xr.open_dataset(output_folder, engine="netcdf4")

        dat_add = da[short_names[k]].values
        out_add = np.mean(dat_add,axis=(1,2))
        dat = np.concat((dat,dat_add),axis=0)
        out = np.concat((out,out_add),axis=0)
    
    np.savez('./data/%s_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[k],nth,sth,wst,est,yrs[0],yrs[-1]),arr=dat)
    np.savez('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[k],nth,sth,wst,est,yrs[0],yrs[-1]),arr=out)

sd_null = '1995-10-01'
ed_null = '2016-12-31'

sd_era5 = '1940-01-01'
ed_era5 = '2024-12-31'

sd_hist = '1950-10-01'
ed_hist = '2023-09-30'

sd_all = '1990-02-01'
ed_all = '2024-08-29'

jday_ref = '1950-01-01'

era5_dtg = pd.date_range(sd_era5,ed_era5,freq='D')
null_dtg = pd.date_range(sd_null,ed_null,freq='D')
hist_dtg = pd.date_range(sd_hist,ed_hist,freq='D')
all_dtg = pd.date_range(sd_all,ed_all,freq='D')

jday_hist = len(pd.date_range(jday_ref,sd_hist,freq='D'))
jday_null = len(pd.date_range(jday_ref,sd_null,freq='D'))
jday_all = len(pd.date_range(jday_ref,sd_all,freq='D'))

tdew = np.load('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[2],nth,sth,wst,est,yrs[0],yrs[-1]))['arr']
tdew_df = pd.Series(tdew,index=era5_dtg)
tdew_null = tdew_df.loc[pd.date_range(sd_null,ed_null,freq='D')] - 273.15
tdew_hist = tdew_df.loc[pd.date_range(sd_hist,ed_hist,freq='D')] - 273.15
tdew_all = tdew_df.loc[pd.date_range(sd_all,ed_all,freq='D')] - 273.15

tair = np.load('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[3],nth,sth,wst,est,yrs[0],yrs[-1]))['arr']
tair_df = pd.Series(tair,index=era5_dtg)
tair_null = tair_df.loc[pd.date_range(sd_null,ed_null,freq='D')] - 273.15
tair_hist = tair_df.loc[pd.date_range(sd_hist,ed_hist,freq='D')] - 273.15
tair_all = tair_df.loc[pd.date_range(sd_all,ed_all,freq='D')] - 273.15

precip = np.load('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[4],nth,sth,wst,est,yrs[0],yrs[-1]))['arr']
precip_df = pd.Series(precip,index=era5_dtg)
precip_null = precip_df.loc[pd.date_range(sd_null,ed_null,freq='D')] 
precip_hist = precip_df.loc[pd.date_range(sd_hist,ed_hist,freq='D')] 
precip_all = precip_df.loc[pd.date_range(sd_all,ed_all,freq='D')] 

uwnd = np.load('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[0],nth,sth,wst,est,yrs[0],yrs[-1]))['arr']
uwnd_df = pd.Series(uwnd,index=era5_dtg)
uwnd_null = uwnd_df.loc[pd.date_range(sd_null,ed_null,freq='D')]
uwnd_hist = uwnd_df.loc[pd.date_range(sd_hist,ed_hist,freq='D')]
uwnd_all = uwnd_df.loc[pd.date_range(sd_all,ed_all,freq='D')]

vwnd = np.load('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[1],nth,sth,wst,est,yrs[0],yrs[-1]))['arr']
vwnd_df = pd.Series(vwnd,index=era5_dtg)
vwnd_null = vwnd_df.loc[pd.date_range(sd_null,ed_null,freq='D')]
vwnd_hist = vwnd_df.loc[pd.date_range(sd_hist,ed_hist,freq='D')]
vwnd_all = vwnd_df.loc[pd.date_range(sd_all,ed_all,freq='D')]

clcov = np.load('./data/%s_area-mean_N%s-%s_E%s-%s_%s-%s.npz' %(var_names[5],nth,sth,wst,est,yrs[0],yrs[-1]))['arr']
clcov_df = pd.Series(clcov,index=era5_dtg)
clcov_null = clcov_df.loc[pd.date_range(sd_null,ed_null,freq='D')] * 10
clcov_hist = clcov_df.loc[pd.date_range(sd_hist,ed_hist,freq='D')] * 10
clcov_all = clcov_df.loc[pd.date_range(sd_all,ed_all,freq='D')] * 10

#wind speed & direction calcs
wind_spd_null = np.sqrt(uwnd_null**2 + vwnd_null**2)
wind_spd_hist = np.sqrt(uwnd_hist**2 + vwnd_hist**2)
wind_spd_all = np.sqrt(uwnd_all**2 + vwnd_all**2)
#meteorological wind direction in rads (phi)
phi_null = np.atan2(uwnd_null/wind_spd_null, vwnd_null/wind_spd_null) + np.pi
phi_hist = np.atan2(uwnd_hist/wind_spd_hist, vwnd_hist/wind_spd_hist) + np.pi
phi_all = np.atan2(uwnd_all/wind_spd_all, vwnd_all/wind_spd_all) + np.pi
#phi_degrees_null = phi_null * 180/np.pi

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#output era5 to length of original Null data (1995-2016)
w2_met_out = pd.read_csv('h:/Projects/SITES-EDF/CE-QUAL-W2/SHA_model_pilot/met/met_sha_null.csv')
w2_met = pd.read_csv('h:/Projects/SITES-EDF/CE-QUAL-W2/SHA_model_pilot/met/met_sha_null.csv',header=2)
#w2_met['JDAY'] = np.arange(len(w2_met['JDAY'])) - 1918

w2_met_out.iloc[2:,0] = np.arange(len(w2_met_out.iloc[2:,0])) + jday_null
w2_met_out.iloc[2:,1] = round(tair_null,1) 
w2_met_out.iloc[2:,2] = round(tdew_null,1)
w2_met_out.iloc[2:,3] = round(wind_spd_null,2)
w2_met_out.iloc[2:,4] = round(phi_null,2)
w2_met_out.iloc[2:,5] = round(clcov_null,1)

w2_met_out.to_csv('h:/Projects/SITES-EDF/CE-QUAL-W2/SHA_model_pilot/met/met_sha_null2.csv',index=False,header=['$1995-2016 ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])
w2_met_out.to_csv('./met/met_sha-era5_null.csv',index=False,header=['$1995-2016 ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])

w2_met_out.iloc[2:,0] = np.arange(len(w2_met_out.iloc[2:,0])) + 1
w2_met_out.to_csv('h:/Projects/SITES-EDF/CE-QUAL-W2/SHA_model_pilot/met/met_sha_null-trial.csv',index=False,header=['$1995-2016 ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#output to full length of potential historical data (10/1/1950 - 9/30/2023)
data = {'JDAY':np.arange(len(hist_dtg)) + jday_hist,'TAIR':round(tair_hist,1),'TDEW':round(tdew_hist,1),'WIND':round(wind_spd_hist,2),'PHI':round(phi_hist,2),'CLOUD':round(clcov_hist,1)}
df = pd.DataFrame(data)

data2 = {'JDAY':hist_dtg,'TAIR':round(tair_hist,1),'TDEW':round(tdew_hist,1),'WIND':round(wind_spd_hist,2),'PHI':round(phi_hist,2),'CLOUD':round(clcov_hist,1)}
df2 = pd.DataFrame(data2)

df_new = w2_met_out.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])

df_out = pd.concat([df_new,df])

df_out.to_csv('h:/Projects/SITES-EDF/CE-QUAL-W2/SHA_model_pilot/met/met_sha_hist.csv',index=False,header=['$10/1/1950-9/30/2023 ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])
df_out.to_csv('./met/met_sha-era5_hist.csv',index=False,header=['$10/1/1950-9/30/2023  ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])

df_out2 = pd.concat([df_new,df2])

df_out2.to_csv('./met/met_sha-era5_hist-dates.csv',index=False,header=['$10/1/1950-9/30/2023  ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#output to length where all observed data available (2/1/1990 - 8/30/2024)
data = {'JDAY':np.arange(len(all_dtg)) + jday_all,'TAIR':round(tair_all,1),'TDEW':round(tdew_all,1),'WIND':round(wind_spd_all,2),'PHI':round(phi_all,2),'CLOUD':round(clcov_all,1)}
df = pd.DataFrame(data)

data2 = {'JDAY':all_dtg,'TAIR':round(tair_all,1),'TDEW':round(tdew_all,1),'WIND':round(wind_spd_all,2),'PHI':round(phi_all,2),'CLOUD':round(clcov_all,1)}
df2 = pd.DataFrame(data2)

df_new = w2_met_out.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])

df_out = pd.concat([df_new,df])

df_out.to_csv('h:/Projects/SITES-EDF/CE-QUAL-W2/SHA_model_pilot/met/met_sha_90-24.csv',index=False,header=['$10/1/1950-9/30/2023 ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])
df_out.to_csv('./met/met_sha-era5_90-24.csv',index=False,header=['$2/1/1990-8/30/2024  ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])

df_out2 = pd.concat([df_new,df2])

df_out2.to_csv('./met/met_sha-era5_90-24-dates.csv',index=False,header=['$2/1/1990-8/30/2024  ERA5 daily-mean N40.5-41.0 W122.5-122.0','','','','',''])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#output precip data
data = {'JDAY':null_dtg ,'PRECIP':precip_null}
df = pd.DataFrame(data)
df.to_csv('./met/precip_null.csv',index=False)

data = {'JDAY':hist_dtg ,'PRECIP':precip_hist}
df = pd.DataFrame(data)
df.to_csv('./met/precip_hist.csv',index=False)

data = {'JDAY':all_dtg ,'PRECIP':precip_all}
df = pd.DataFrame(data)
df.to_csv('./met/precip_90-24.csv',index=False)


#------------------------------------------------END-----------------------------------------