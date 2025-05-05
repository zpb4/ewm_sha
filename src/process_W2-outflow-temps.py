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

sd = '1990-02-01'
ed = '2024-08-29'

hist_dtg = pd.date_range(sd,ed,freq='D')
jday_dtg = pd.date_range(jday_ref,'2024-12-31',freq='D')

jday_st = len(pd.date_range(jday_ref,sd,freq='D'))

outflows = pd.read_csv('./outflows/qot_sha-90-24-partitioned_br1.csv',header=2,index_col=0)
otflow_jday = outflows.index
otflow_arr = outflows.iloc[:,:].values

#load W2 results and combine
tsr_sdg = pd.read_csv('./tsr_output/tsr-90-24_1_seg21.csv')
T_sdg = tsr_sdg['T2(C)'].values
T_sdg_jday = np.int64(tsr_sdg['JDAY'].values - jday_st)
rmv_idx = np.where(T_sdg_jday<0)
T_sdg_idx = np.delete(T_sdg,rmv_idx)
T_sdg_jday_idx = np.delete(T_sdg_jday,rmv_idx)
T_sdg_out = np.full(len(hist_dtg),np.mean(T_sdg))
T_sdg_out[T_sdg_jday_idx] = T_sdg_idx

tsr_low = pd.read_csv('./tsr_output/tsr-90-24_2_seg21.csv')
T_low = tsr_low['T2(C)'].values
T_low_jday = np.int64(tsr_low['JDAY'].values - jday_st)
rmv_idx = np.where(T_low_jday<0)
T_low_idx = np.delete(T_low,rmv_idx)
T_low_jday_idx = np.delete(T_low_jday,rmv_idx)
T_low_out = np.full(len(hist_dtg),np.mean(T_low))
T_low_out[T_low_jday_idx] = T_low_idx

tsr_mid = pd.read_csv('./tsr_output/tsr-90-24_3_seg21.csv')
T_mid = tsr_mid['T2(C)'].values
T_mid_jday = np.int64(tsr_mid['JDAY'].values - jday_st)
rmv_idx = np.where(T_mid_jday<0)
T_mid_idx = np.delete(T_mid,rmv_idx)
T_mid_jday_idx = np.delete(T_mid_jday,rmv_idx)
T_mid_out = np.full(len(hist_dtg),np.mean(T_mid))
T_mid_out[T_mid_jday_idx] = T_mid_idx

tsr_upp = pd.read_csv('./tsr_output/tsr-90-24_4_seg21.csv')
T_upp = tsr_upp['T2(C)'].values
T_upp_jday = np.int64(tsr_upp['JDAY'].values - jday_st)
rmv_idx = np.where(T_upp_jday<0)
T_upp_idx = np.delete(T_upp,rmv_idx)
T_upp_jday_idx = np.delete(T_upp_jday,rmv_idx)
T_upp_out = np.full(len(hist_dtg),np.mean(T_upp))
T_upp_out[T_upp_jday_idx] = T_upp_idx

tsr_sp = pd.read_csv('./tsr_output/tsr-90-24_5_seg21.csv')
T_sp = tsr_sp['T2(C)'].values
T_sp_jday = np.int64(tsr_sp['JDAY'].values - jday_st)
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

data = {'Date':hist_dtg,'T_outflow':np.round(otflow_T,2)}
df = pd.DataFrame(data)
df.to_csv('./data/W2_T-outflow_90-24.csv',index=False)

data1 = {'Date':hist_dtg,'T_outflow':np.round(sm_otflow_T,2)}
df1 = pd.DataFrame(data1)
df1.to_csv('./data/W2_T-outflow-smoothed_90-24.csv',index=False)


###############################################END#############################################