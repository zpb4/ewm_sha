# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 21:08:43 2025

@author: zpb4
"""
import pandas as pd
import numpy as np
import xarray as xr
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import statsmodels.nonparametric.smoothers_lowess as sml

cfs_to_m3s = 0.028316847
jday_ref = '1950-01-01'

all_st = '1990-02-01'
all_ed = '2024-08-29'

null_st = '1995-10-01'
null_ed = '2016-12-31'

dlt_inf_temps = pd.read_csv('./data/DLT_90-24_temp_C.csv',index_col=0,parse_dates=True)[all_st:all_ed]

#load original W2 inflow files
tin1_file = pd.read_csv('./inflows/tin_sha_br1.csv',header=2)
tin2_file = pd.read_csv('./inflows/tin_sha_br2.csv',header=2)
tin3_file = pd.read_csv('./inflows/tin_sha_br3.csv',header=2)
tin4_file = pd.read_csv('./inflows/tin_sha_br4.csv',header=2)
tin5_file = pd.read_csv('./inflows/tin_sha_br5.csv',header=2)

#load header data for inflows
tin1_file_hdr = pd.read_csv('./inflows/tin_sha_br1.csv') #Pit River
tin2_file_hdr = pd.read_csv('./inflows/tin_sha_br2.csv') #Squaw Creek   
tin3_file_hdr = pd.read_csv('./inflows/tin_sha_br3.csv') #McCloud River
tin4_file_hdr = pd.read_csv('./inflows/tin_sha_br4.csv') #Sacramento River
tin5_file_hdr = pd.read_csv('./inflows/tin_sha_br5.csv') #Branch 5 (0 flow)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Null historical data process
#arrange date/time indices
date = pd.date_range(dlt_inf_temps.index[0],dlt_inf_temps.index[-1],freq='D')
jday_all = len(pd.date_range(jday_ref,date[0],freq='D'))

dlt_temps = dlt_inf_temps['temp_C'].values
sm_dlt_all = sml.lowess(endog=dlt_temps,exog=np.arange(len(dlt_temps)),frac=0.005,xvals=np.arange(len(dlt_temps)))

dlt_df = pd.Series(dlt_temps,index=date)
dlt_null = dlt_df.loc[pd.date_range(null_st,null_ed,freq='D')]

inf_dtg = pd.date_range(null_st,null_ed,freq='D')
jday = len(pd.date_range(jday_ref,inf_dtg[0],freq='D'))

sm_dlt_null = sml.lowess(endog=dlt_null,exog=np.arange(len(inf_dtg)),frac=0.005,xvals=np.arange(len(inf_dtg)))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Null data process and save
#setup dataframes
"""
#non-smoothed data
data1 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(dlt_null.values,2)}
data2 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(dlt_null.values,2)}
data3 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(dlt_null.values,2)}
data4 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(dlt_null.values,2)}
data5 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(dlt_null.values,2)}
"""
data1 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(sm_dlt_null,2)}
data2 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(sm_dlt_null,2)}
data3 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(sm_dlt_null,2)}
data4 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(sm_dlt_null,2)}
data5 = {'JDAY':np.arange(len(inf_dtg)) + jday,'TIN':np.round(sm_dlt_null,2)}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)
df5 = pd.DataFrame(data5)

#concatenate dataframe elements to ensure output matches W2 specifications
#Branch 1
df_new = tin1_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./inflows/tin_sha-null_br1.csv',index=False,header=['$10/1/1995-12/31/2016 Pit River temp-C (DLT temp)',''])

#Branch 2
df_new = tin2_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df2])
df_out.to_csv('./inflows/tin_sha-null_br2.csv',index=False,header=['$10/1/1995-12/31/2016 Squaw Creek temp-C (DLT temp)',''])

#Branch 3
df_new = tin3_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df3])
df_out.to_csv('./inflows/tin_sha-null_br3.csv',index=False,header=['$10/1/1995-12/31/2016 McCloud River temp-C (DLT temp)',''])

#Branch 4
df_new = tin4_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df4])
df_out.to_csv('./inflows/tin_sha-null_br4.csv',index=False,header=['$10/1/1995-12/31/2016 Sacramento River temp-C (DLT temp)',''])

#Branch 5
df_new = tin5_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df5])
df_out.to_csv('./inflows/tin_sha-null_br5.csv',index=False,header=['$10/1/1995-12/31/2016 Branch 5 temp-C (DLT temp)',''])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#All data process and save
#setup dataframes
data1 = {'JDAY':np.arange(len(date)) + jday_all,'TIN':np.round(sm_dlt_all,2)}
data2 = {'JDAY':np.arange(len(date)) + jday_all,'TIN':np.round(sm_dlt_all,2)}
data3 = {'JDAY':np.arange(len(date)) + jday_all,'TIN':np.round(sm_dlt_all,2)}
data4 = {'JDAY':np.arange(len(date)) + jday_all,'TIN':np.round(sm_dlt_all,2)}
data5 = {'JDAY':np.arange(len(date)) + jday_all,'TIN':np.round(sm_dlt_all,2)}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)
df5 = pd.DataFrame(data5)

#concatenate dataframe elements to ensure output matches W2 specifications
#Branch 1
df_new = tin1_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./inflows/tin_sha-90-24_br1.csv',index=False,header=['$2/1/1990-8/30/2024 Pit River temp-C (DLT temp)',''])

#Branch 2
df_new = tin2_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df2])
df_out.to_csv('./inflows/tin_sha-90-24_br2.csv',index=False,header=['$2/1/1990-8/30/2024 Squaw Creek temp-C (DLT temp)',''])

#Branch 3
df_new = tin3_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df3])
df_out.to_csv('./inflows/tin_sha-90-24_br3.csv',index=False,header=['$2/1/1990-8/30/2024 McCloud River temp-C (DLT temp)',''])

#Branch 4
df_new = tin4_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df4])
df_out.to_csv('./inflows/tin_sha-90-24_br4.csv',index=False,header=['$2/1/1990-8/30/2024 Sacramento River temp-C (DLT temp)',''])

#Branch 5
df_new = tin5_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df5])
df_out.to_csv('./inflows/tin_sha-90-24_br5.csv',index=False,header=['$2/1/1990-8/30/2024 Branch 5 temp-C (DLT temp)',''])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Plots

#plot temp timeseries for All dataa
sns.set_theme()
sns.set_style('ticks')
sns.set_context('paper')

fig = plt.figure(layout='constrained',figsize=(8,8))
gs0 = fig.add_gridspec(2,1)
ax1 = fig.add_subplot(gs0[0])

ax1.plot(date,dlt_temps,c='black')
ax1.set_ylabel('Temp (C)')
ax1.legend(['Raw DLT Temp'],loc='upper right',fontsize='large',frameon=False)

ax2 = fig.add_subplot(gs0[1])
ax2.plot(date,dlt_temps,c='gray',alpha=0.2)
ax2.plot(date,sm_dlt_all,c='black')
ax2.legend(['Raw DLT Temp','Smooth DLT Temp'],loc='upper right',fontsize='large',frameon=False)


#plot temp timeseries for Null dataa
sns.set_theme()
sns.set_style('ticks')
sns.set_context('paper')

fig = plt.figure(layout='constrained',figsize=(8,8))
gs0 = fig.add_gridspec(2,1)
ax1 = fig.add_subplot(gs0[0])

ax1.plot(inf_dtg,dlt_null,c='black')
ax1.set_ylabel('Temp (C)')
ax1.legend(['Raw DLT Temp'],loc='upper right',fontsize='large',frameon=False)

ax2 = fig.add_subplot(gs0[1])
ax2.plot(inf_dtg,dlt_null,c='gray',alpha=0.2)
ax2.plot(inf_dtg,sm_dlt_null,c='black')
ax2.legend(['Raw DLT Temp','Smooth DLT Temp'],loc='upper right',fontsize='large',frameon=False)
#############################################################END########################################