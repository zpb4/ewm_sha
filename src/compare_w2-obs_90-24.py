# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 12:30:15 2025

@author: zpb4
"""
import sys
import os
sys.path.insert(0, os.path.abspath('./src'))
import pandas as pd
import numpy as np
import xarray as xr
from util import water_day
import calendar
import matplotlib as matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import statsmodels.nonparametric.smoothers_lowess as sml

jday_ref = '1950-01-01'

sd = '1990-11-16'
ed = '2024-08-29'

jday_dtg = pd.date_range(jday_ref,'2024-12-31',freq='D')

jday_st = len(pd.date_range(jday_ref,sd,freq='D'))
jday_ed = len(pd.date_range(jday_ref,ed,freq='D'))

outflows = pd.read_csv('./outflows/qot_sha-90-24-partitioned_br1.csv',header=2,index_col=0)
otflow_jday = outflows.index
idx_st = np.where(otflow_jday==jday_st)[0][0]
idx_ed = (np.where(otflow_jday==jday_ed)[0][0]+1)
otflow_arr = outflows.iloc[idx_st:idx_ed,:].values
hist_sd = sd
hist_ed = ed
hist_dtg = pd.date_range(hist_sd,hist_ed,freq='D')

obs_shd = pd.read_csv('./data/SHD_90-24_temp_C.csv',index_col=0,parse_dates=True)[hist_sd:hist_ed]
obs_shd_T = obs_shd.values

sm_obs_shd_T = sml.lowess(endog=obs_shd_T[:,0],exog=np.arange(len(hist_dtg)),frac=0.005,xvals=np.arange(len(hist_dtg)))

#load W2 results and combine
tsr_sdg = pd.read_csv('./tsr_output/tsr-90-24_1_seg21.csv')
T_sdg = tsr_sdg['T2(C)'].values
T_sdg_jday = np.int64(tsr_sdg['JDAY'].values - otflow_jday[idx_st])
rmv_idx = np.where(T_sdg_jday<0)
T_sdg_idx = np.delete(T_sdg,rmv_idx)
T_sdg_jday_idx = np.delete(T_sdg_jday,rmv_idx)
T_sdg_out = np.full(len(hist_dtg),np.mean(T_sdg))
T_sdg_out[T_sdg_jday_idx] = T_sdg_idx

tsr_low = pd.read_csv('./tsr_output/tsr-90-24_2_seg21.csv')
T_low = tsr_low['T2(C)'].values
T_low_jday = np.int64(tsr_low['JDAY'].values - otflow_jday[idx_st])
rmv_idx = np.where(T_low_jday<0)
T_low_idx = np.delete(T_low,rmv_idx)
T_low_jday_idx = np.delete(T_low_jday,rmv_idx)
T_low_out = np.full(len(hist_dtg),np.mean(T_low))
T_low_out[T_low_jday_idx] = T_low_idx

tsr_mid = pd.read_csv('./tsr_output/tsr-90-24_3_seg21.csv')
T_mid = tsr_mid['T2(C)'].values
T_mid_jday = np.int64(tsr_mid['JDAY'].values - otflow_jday[idx_st])
rmv_idx = np.where(T_mid_jday<0)
T_mid_idx = np.delete(T_mid,rmv_idx)
T_mid_jday_idx = np.delete(T_mid_jday,rmv_idx)
T_mid_out = np.full(len(hist_dtg),np.mean(T_mid))
T_mid_out[T_mid_jday_idx] = T_mid_idx

tsr_upp = pd.read_csv('./tsr_output/tsr-90-24_4_seg21.csv')
T_upp = tsr_upp['T2(C)'].values
T_upp_jday = np.int64(tsr_upp['JDAY'].values - otflow_jday[idx_st])
rmv_idx = np.where(T_upp_jday<0)
T_upp_idx = np.delete(T_upp,rmv_idx)
T_upp_jday_idx = np.delete(T_upp_jday,rmv_idx)
T_upp_out = np.full(len(hist_dtg),np.mean(T_upp))
T_upp_out[T_upp_jday_idx] = T_upp_idx

tsr_sp = pd.read_csv('./tsr_output/tsr-90-24_5_seg21.csv')
T_sp = tsr_sp['T2(C)'].values
T_sp_jday = np.int64(tsr_sp['JDAY'].values - otflow_jday[idx_st])
rmv_idx = np.where(T_sp_jday<0)
T_sp_idx = np.delete(T_sp,rmv_idx)
T_sp_jday_idx = np.delete(T_sp_jday,rmv_idx)
T_sp_out = np.full(len(hist_dtg),np.mean(T_sp))
T_sp_out[T_sp_jday_idx] = T_sp_idx

W2_T_arr = np.reshape(np.concat((T_sdg_out,T_low_out,T_mid_out,T_upp_out,T_sp_out),axis=0),(len(hist_dtg),5),order='F')

#calculate outflow temps 
otflow_T = np.zeros(len(hist_dtg))

for i in range(len(hist_dtg)):
    otflow_T[i] = np.sum(otflow_arr[i,:] * W2_T_arr[i,:]) / np.sum(otflow_arr[i,:])


sm_otflow_T= sml.lowess(endog=otflow_T,exog=np.arange(len(hist_dtg)),frac=0.005,xvals=np.arange(len(hist_dtg)))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#plots
#compare W2 and obs timeseries
sns.set_theme()
sns.set_style('ticks')
sns.set_context('paper')

fig = plt.figure(layout='constrained',figsize=(8,10))
gs0 = fig.add_gridspec(3,1)
ax1 = fig.add_subplot(gs0[0])

ax1.plot(hist_dtg,obs_shd_T,linewidth=0.5,c='gray',alpha=0.5)
ax1.plot(hist_dtg,sm_obs_shd_T,linewidth=1,c='black')
ax1.legend(['Obs','Obs-smooth'],loc='upper left',fontsize='large',frameon=False)
ax1.set_ylabel('temperature (C)')
ax1.set_ylim((5,20))

ax2 = fig.add_subplot(gs0[1])
ax2.plot(hist_dtg,otflow_T,linewidth=0.5,color='cyan',alpha=0.5)
ax2.plot(hist_dtg,sm_otflow_T,linewidth=1,color='cyan')
ax2.legend(['W2','W2-smooth'],loc='upper left',fontsize='large',frameon=False)
ax2.set_ylim([5,20])
ax2.set_ylabel('temperature (C)')

ax3 = fig.add_subplot(gs0[2])
ax3.plot(hist_dtg,sm_obs_shd_T,linewidth=1,c='black')
ax3.plot(hist_dtg,sm_otflow_T,linewidth=1,color='cyan')
ax3.legend(['Obs-smooth','W2-smooth'],loc='upper left',fontsize='large',frameon=False)
ax3.set_ylim([5,20])
ax3.set_ylabel('temperature (C)')

#-------------------------------------------------
#error histograms
#all days
fig = plt.figure(layout='constrained',figsize=(8,6))
gs0 = fig.add_gridspec(1,1)
ax1 = fig.add_subplot(gs0[0])

ax1.hist(sm_obs_shd_T-sm_otflow_T)

#only summer days (jun-sep)
dowy = np.array([water_day(d,calendar.isleap(d.year)) for d in hist_dtg])

summer_idx = np.where(dowy>(365-122))

fig = plt.figure(layout='constrained',figsize=(8,6))
gs0 = fig.add_gridspec(1,1)
ax1 = fig.add_subplot(gs0[0])

ax1.hist(sm_obs_shd_T[summer_idx]-sm_otflow_T[summer_idx])

#only days with high obs temps (over optimum threshold)
high_idx = np.where(sm_obs_shd_T>11.5)

fig = plt.figure(layout='constrained',figsize=(8,6))
gs0 = fig.add_gridspec(1,1)
ax1 = fig.add_subplot(gs0[0])

ax1.hist(sm_obs_shd_T[high_idx]-sm_otflow_T[high_idx])

###############################################END#############################################