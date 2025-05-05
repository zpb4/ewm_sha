# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 21:08:43 2025

@author: zpb4
"""
import pandas as pd
import numpy as np
import xarray as xr
import sys

cfs_to_m3s = 0.028316847
jday_ref = '1950-01-01'

hist_flows = pd.read_csv('./data/cord-sim_realtime_ppic.csv',index_col=0)
cnrfc_inflows = pd.read_csv('./data/SHDC1_daily.csv',index_col=0)

#load original W2 inflow files
qin1_file = pd.read_csv('./inflows/qin_sha_br1.csv',header=2)
qin2_file = pd.read_csv('./inflows/qin_sha_br2.csv',header=2)
qin3_file = pd.read_csv('./inflows/qin_sha_br3.csv',header=2)
qin4_file = pd.read_csv('./inflows/qin_sha_br4.csv',header=2)
qin5_file = pd.read_csv('./inflows/qin_sha_br5.csv',header=2)

#load header data for inflows
qin1_file_hdr = pd.read_csv('./inflows/qin_sha_br1.csv') #Pit River
qin2_file_hdr = pd.read_csv('./inflows/qin_sha_br2.csv') #Squaw Creek   
qin3_file_hdr = pd.read_csv('./inflows/qin_sha_br3.csv') #McCloud River
qin4_file_hdr = pd.read_csv('./inflows/qin_sha_br4.csv') #Sacramento River
qin5_file_hdr = pd.read_csv('./inflows/qin_sha_br5.csv') #Branch 5 (0 flow)

#calculate mean flow for each inflow location
qin1_mn = np.mean(qin1_file['QIN'])
qin2_mn = np.mean(qin2_file['QIN'])
qin3_mn = np.mean(qin3_file['QIN'])
qin4_mn = np.mean(qin4_file['QIN'])
qin5_mn = np.mean(qin5_file['QIN'])

#calculate proportion of total inflow for each location
qin1_pro = qin1_mn / np.sum(([qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn]))
qin2_pro = qin2_mn / np.sum(([qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn]))
qin3_pro = qin3_mn / np.sum(([qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn]))
qin4_pro = qin4_mn / np.sum(([qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn]))
qin5_pro = qin5_mn / np.sum(([qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn]))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Null historical data process
#arrange date/time indices
date = hist_flows.index
sha_inf = hist_flows['SHA_inf'] * cfs_to_m3s
sha_otf = hist_flows['SHA_otf'] * cfs_to_m3s
sha_store = hist_flows['SHA_storage']

inf_dtg = pd.date_range(date[0],date[-1],freq='D')
jday = len(pd.date_range(jday_ref,inf_dtg[0],freq='D'))

#setup dataframes
data1 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin1_pro,2)}
data2 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin2_pro,2)}
data3 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin3_pro,2)}
data4 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin4_pro,2)}
data5 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':np.zeros(len(inf_dtg))}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)
df5 = pd.DataFrame(data5)

#concatenate dataframe elements to ensure output matches W2 specifications
#Branch 1
df_new = qin1_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./inflows/qin_sha-null_br1.csv',index=False,header=['$10/1/1995-12/31/2016 Pit River (proportional estimate)',''])

#Branch 2
df_new = qin2_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df2])
df_out.to_csv('./inflows/qin_sha-null_br2.csv',index=False,header=['$10/1/1995-12/31/2016 Squaw Creek (proportional estimate)',''])

#Branch 3
df_new = qin3_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df3])
df_out.to_csv('./inflows/qin_sha-null_br3.csv',index=False,header=['$10/1/1995-12/31/2016 McCloud River (proportional estimate)',''])

#Branch 4
df_new = qin4_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df4])
df_out.to_csv('./inflows/qin_sha-null_br4.csv',index=False,header=['$10/1/1995-12/31/2016 Sacramento River (proportional estimate)',''])

#Branch 5
df_new = qin5_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df5])
df_out.to_csv('./inflows/qin_sha-null_br5.csv',index=False,header=['$10/1/1995-12/31/2016 Branch 5 (no inflow)',''])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#CNRFC historical inflows data process
#arrange date/time indices
date = cnrfc_inflows.index
sha_inf = cnrfc_inflows['Flow (KCFS)'] * 1000 * cfs_to_m3s

inf_dtg = pd.date_range(date[0],date[-1],freq='D')
jday = -len(pd.date_range(inf_dtg[0],jday_ref,freq='D'))+1

#setup dataframes
data1 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin1_pro,2)}
data2 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin2_pro,2)}
data3 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin3_pro,2)}
data4 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin4_pro,2)}
data5 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':np.zeros(len(inf_dtg))}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)
df5 = pd.DataFrame(data5)

#concatenate dataframe elements to ensure output matches W2 specifications
#Branch 1
df_new = qin1_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./inflows/qin_sha-cnrfc_br1.csv',index=False,header=['$10/1/1950-8/29/2024 Pit River (proportional estimate)',''])

#Branch 2
df_new = qin2_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df2])
df_out.to_csv('./inflows/qin_sha-cnrfc_br2.csv',index=False,header=['$10/1/1950-8/29/2024 Squaw Creek (proportional estimate)',''])

#Branch 3
df_new = qin3_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df3])
df_out.to_csv('./inflows/qin_sha-cnrfc_br3.csv',index=False,header=['$10/1/1950-8/29/2024 McCloud River (proportional estimate)',''])

#Branch 4
df_new = qin4_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df4])
df_out.to_csv('./inflows/qin_sha-cnrfc_br4.csv',index=False,header=['$10/1/1950-8/29/2024 Sacramento River (proportional estimate)',''])

#Branch 5
df_new = qin5_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df5])
df_out.to_csv('./inflows/qin_sha-cnrfc_br5.csv',index=False,header=['$10/1/1950-8/29/2024 Branch 5 (no inflow)',''])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#CNRFC historical inflows data process --> historical length for all data
#arrange date/time indices
all_st = '1990-02-01'
all_ed = '2024-08-30'

cnrfc_inflows = pd.read_csv('./data/SHDC1_daily.csv',index_col=0,parse_dates=True)[all_st:all_ed]
date = cnrfc_inflows.index
sha_inf = cnrfc_inflows['Flow (KCFS)'] * 1000 * cfs_to_m3s
sha_inf[sha_inf<0] = 0

inf_dtg = pd.date_range(date[0],date[-1],freq='D')
jday = len(pd.date_range(jday_ref,inf_dtg[0],freq='D'))

#setup dataframes
data1 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin1_pro,2)}
data2 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin2_pro,2)}
data3 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin3_pro,2)}
data4 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':round(sha_inf * qin4_pro,2)}
data5 = {'JDAY':np.arange(len(inf_dtg)) + jday,'QIN':np.zeros(len(inf_dtg))}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)
df5 = pd.DataFrame(data5)

#concatenate dataframe elements to ensure output matches W2 specifications
#Branch 1
df_new = qin1_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./inflows/qin_sha-cnrfc-90-24_br1.csv',index=False,header=['$2/1/1990-8/29/2024 Pit River (proportional estimate)',''])

#Branch 2
df_new = qin2_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df2])
df_out.to_csv('./inflows/qin_sha-cnrfc-90-24_br2.csv',index=False,header=['$2/1/1990-8/29/2024 Squaw Creek (proportional estimate)',''])

#Branch 3
df_new = qin3_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df3])
df_out.to_csv('./inflows/qin_sha-cnrfc-90-24_br3.csv',index=False,header=['$2/1/1990-8/29/2024 McCloud River (proportional estimate)',''])

#Branch 4
df_new = qin4_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df4])
df_out.to_csv('./inflows/qin_sha-cnrfc-90-24_br4.csv',index=False,header=['$2/1/1990-8/29/2024 Sacramento River (proportional estimate)',''])

#Branch 5
df_new = qin5_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df5])
df_out.to_csv('./inflows/qin_sha-cnrfc-90-24_br5.csv',index=False,header=['$2/1/1990-8/29/2024 Branch 5 (no inflow)',''])


#############################################################END########################################