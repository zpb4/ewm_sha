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

outflows = pd.read_csv('./outflows/qot_sha-null-partitioned_br1.csv',header=2)
otflow_jday = outflows['JDAY'].values
otflow_arr = outflows.iloc[:,1:].values

jday_dtg = pd.date_range(jday_ref,'2024-12-31',freq='D')
hist_sd = jday_dtg[otflow_jday[0]-1]
hist_ed = jday_dtg[otflow_jday[0-1]-1]
hist_dtg = pd.date_range(hist_sd,hist_ed,freq='D')

obs_shd = pd.read_csv('./data/SHD_90-24_temp_C.csv',index_col=0,parse_dates=True)[hist_sd:hist_ed]
obs_shd_T = obs_shd.values

sm_obs_shd_T = sml.lowess(endog=obs_shd_T[:,0],exog=np.arange(len(hist_dtg)),frac=0.01,xvals=np.arange(len(hist_dtg)))

#load W2 results and combine
tsr_sdg = pd.read_csv('./tsr_output/tsr_1_seg21.csv')
T_sdg = tsr_sdg['T2(C)'].values
T_sdg_jday_idx = np.int64(tsr_sdg['JDAY'].values - otflow_jday[0])
T_sdg_out = np.full(len(hist_dtg),np.mean(T_sdg))
T_sdg_out[T_sdg_jday_idx] = T_sdg

tsr_low = pd.read_csv('./tsr_output/tsr_2_seg21.csv')
T_low = tsr_low['T2(C)'].values
T_low_jday_idx = np.int64(tsr_low['JDAY'].values - otflow_jday[0])
T_low_out = np.full(len(hist_dtg),np.mean(T_low))
T_low_out[T_low_jday_idx] = T_low

tsr_mid = pd.read_csv('./tsr_output/tsr_3_seg21.csv')
T_mid = tsr_mid['T2(C)'].values
T_mid_jday_idx = np.int64(tsr_mid['JDAY'].values - otflow_jday[0])
T_mid_out = np.full(len(hist_dtg),np.mean(T_mid))
T_mid_out[T_mid_jday_idx] = T_mid

tsr_upp = pd.read_csv('./tsr_output/tsr_4_seg21.csv')
T_upp = tsr_upp['T2(C)'].values
T_upp_jday_idx = np.int64(tsr_upp['JDAY'].values - otflow_jday[0])
T_upp_out = np.full(len(hist_dtg),np.mean(T_upp))
T_upp_out[T_upp_jday_idx] = T_upp

tsr_sp = pd.read_csv('./tsr_output/tsr_5_seg21.csv')
T_sp = tsr_sp['T2(C)'].values
T_sp_jday_idx = np.int64(tsr_sp['JDAY'].values - otflow_jday[0])
T_sp_out = np.full(len(hist_dtg),np.mean(T_sp))
T_sp_out[T_sp_jday_idx] = T_sp

W2_T_arr = np.reshape(np.concat((T_sdg_out,T_low_out,T_mid_out,T_upp_out,T_sp_out),axis=0),(len(hist_dtg),5),order='F')

#calculate outflow temps 
otflow_T = np.zeros(len(hist_dtg))

for i in range(len(hist_dtg)):
    otflow_T[i] = np.sum(otflow_arr[i,:] * W2_T_arr[i,:]) / np.sum(otflow_arr[i,:])


sm_otflow_T= sml.lowess(endog=otflow_T,exog=np.arange(len(hist_dtg)),frac=0.01,xvals=np.arange(len(hist_dtg)))

#plot elev timeseries and release
sns.set_theme()
sns.set_style('ticks')
sns.set_context('paper')

#dt_format=mdates.DateFormatter('%m-%d')
fig = plt.figure(layout='constrained',figsize=(8,4))
gs0 = fig.add_gridspec(1,1)
ax1 = fig.add_subplot(gs0[0])

#ax1.plot(hist_dtg,obs_shd_T,linewidth=0.5,c='gray',alpha=0.5)
ax1.plot(hist_dtg,sm_obs_shd_T,linewidth=1,c='black')
ax1.plot(hist_dtg,otflow_T,linewidth=0.5,color='cyan',alpha=0.5)
ax1.plot(hist_dtg,sm_otflow_T,linewidth=1,color='cyan')
ax1.set_ylim([0,20])
ax1.set_ylabel('temperature (C)')



###############################################END#############################################