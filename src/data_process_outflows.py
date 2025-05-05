# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 22:15:02 2025

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
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

cfs_to_m3s = 0.028316847
jday_ref = '1950-01-01'

hist_flows = pd.read_csv('./data/cord-sim_realtime_ppic.csv',index_col=0)

#load original W2 inflow files
qot_file = pd.read_csv('./outflows/qot_br1.csv',header=2)

#load header data for inflows
qot_file_hdr = pd.read_csv('./outflows/qot_br1.csv') 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Null historical data process
#arrange date/time indices
date = hist_flows.index
sha_otf = hist_flows['SHA_otf'] * cfs_to_m3s
sha_store = hist_flows['SHA_storage']

otf_dtg = pd.date_range(date[0],date[-1],freq='D')
jday = len(pd.date_range(jday_ref,otf_dtg[0],freq='D'))

#setup dataframes
data1 = {'JDAY':np.arange(len(otf_dtg)) + jday,'QOUT1':round(sha_otf,2),'QOUT2':np.zeros(len(otf_dtg)),'QOUT3':np.zeros(len(otf_dtg)),'QOUT4':np.zeros(len(otf_dtg)),'QOUT5':np.zeros(len(otf_dtg))}

df1 = pd.DataFrame(data1)

#concatenate dataframe elements to ensure output matches W2 specifications
#Output raw outflow file
df_new = qot_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df1.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./outflows/qot_sha-null-raw_br1.csv',index=False,header=['$10/1/1995-12/31/2016 SHA outflow (historical)','','','','',''])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#All historical data process (all historical inputs available)
#arrange date/time indices
all_st = '1990-02-01'
all_ed = '2024-08-29'

hist_flows = pd.read_csv('./data/hist_87-24_outflow.csv',index_col=0,parse_dates=True)[all_st:all_ed]
date = hist_flows.index
sha_otf = hist_flows.values[:,0] * cfs_to_m3s
sha_otf[sha_otf<0] = 0

otf_dtg = pd.date_range(date[0],date[-1],freq='D')
jday = len(pd.date_range(jday_ref,otf_dtg[0],freq='D'))

#setup dataframes
data1 = {'JDAY':np.arange(len(otf_dtg)) + jday,'QOUT1':np.round(sha_otf,2),'QOUT2':np.zeros(len(otf_dtg)),'QOUT3':np.zeros(len(otf_dtg)),'QOUT4':np.zeros(len(otf_dtg)),'QOUT5':np.zeros(len(otf_dtg))}
df1 = pd.DataFrame(data1)

#concatenate dataframe elements to ensure output matches W2 specifications
#Output raw outflow file
df_new = qot_file_hdr.iloc[:2,:]
df_new.columns = (df_new.iloc[1,:])
df1.columns = (df_new.iloc[1,:])
df_out = pd.concat([df_new,df1])
df_out.to_csv('./outflows/qot_sha-90-24-raw_br1.csv',index=False,header=['$2/1/1990-8/29/2024 SHA outflow (historical)','','','','',''])


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#read in corrected outflow file after run through W2 and mass-balance correction applied in R
qot_corrected_file = pd.read_csv('./outflows/qot_sha-null-corrected_br1.csv') 
qotf_corrected = qot_corrected_file['QOUT']
df_out.iloc[2:,1] = np.round(qotf_corrected.values,1)
df_out.to_csv('./outflows/qot_sha-null_br1.csv',index=False,header=['$10/1/1995-12/31/2016 SHA outflow (historical)','','','','',''])

#allocate corrected flows to simulated TCD operations
dowy = np.array([water_day(d,calendar.isleap(d.year)) for d in otf_dtg])
#gate_elev = {'SDG':226.2,'LOW':248.4,'MID':281,'UPP':311.5,'SPILL':325.2}
gate_elev = {'SDG':226.2,'LOW':256.6,'MID':287.2,'UPP':316.1,'SPILL':325.2}

#setup standard gate strategy
#gates go from bottom to top in array dimensions
#0 = SDG, 1 = LOW, 2 = MID, 3 = UPP, 4 = SPILL
alloc_array = np.zeros((5,365))
#oct1 - dec31: 50% SDG, 50% LOW
alloc_array[0,0:92] = 0.5
alloc_array[1,0:92] = 0.5
#jan1 - jun1: 100% UPP
alloc_array[3,92:243] = 1
#jun1 - jul15: 50% UPP, 50% MID
alloc_array[3,243:288] = 0.5
alloc_array[2,243:288] = 0.5
#jul15 - aug15: 100% MID
alloc_array[2,288:319] = 1
#aug15 - sep30: 100% LOW
alloc_array[1,319:365] = 1

otf_prop_array = np.zeros((len(otf_dtg),5)) #store outflow proportion
otf_wd_array = np.zeros((len(otf_dtg),5))   #store outflow withdrawal for plotting
otf_wd_chg = np.zeros(len(otf_dtg))
sha_hist_elev = pd.read_csv('./data/W2_hist_95-16_elev.csv',index_col=0,parse_dates=True)
elev = sha_hist_elev['elevation (m)']
for i in range(len(otf_dtg)):
    otf_prop_array[i,:] = alloc_array[:,dowy[i]]
    #activate spillway if above spillway elevation
    ##if elev.iloc[i] > gate_elev['SPILL']:
        ##print('spillway usage',i)
        ##otf_prop_array[i,:] = ([0,0,0,0,1])
    if elev.iloc[i] < (gate_elev['UPP']+5) and dowy[i] >= 92 and dowy[i] < 243:
        print('below UPP and jan-jun, 100% MID',i)
        otf_prop_array[i,:] = ([0,0,1,0,0])
    if elev.iloc[i] < (gate_elev['MID']+5) and dowy[i] >= 92 and dowy[i] < 243:
        print('below MID and jan-jun, 100% LOW',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+5) and dowy[i] >= 92 and dowy[i] < 243:
        print('below LOW and jan-jun, 100% SDG',i)
        otf_prop_array[i,:] = ([1,0,0,0,0])
    if elev.iloc[i] < (gate_elev['UPP']+10) and dowy[i] >= 243 and dowy[i] < 288:
        print('below UPP and jun-jul, 100% MID',i)
        otf_prop_array[i,:] = ([0,0,1,0,0])
    if elev.iloc[i] < (gate_elev['MID']+10) and dowy[i] >= 243 and dowy[i] < 288:
        print('below MID and jun-jul, 100% LOW',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+10) and dowy[i] >= 243 and dowy[i] < 288:
        print('below MID and jun-jul, 100% SDG',i)
        otf_prop_array[i,:] = ([1,0,0,0,0])
    if elev.iloc[i] < (gate_elev['MID']+20) and dowy[i] >= 288 and dowy[i] < 319:
        print('below MID and jul-aug, 100% LOW',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+20) and dowy[i] >= 288 and dowy[i] < 319:
        print('below LOW and jul-aug, 100% SDG',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+25) and dowy[i] >= 319:
        print('below LOW and aug-sep, 100% SDG',i)
        otf_prop_array[i,:] = ([1,0,0,0,0])
    rel_gates = np.copy(otf_prop_array[i,:])
    rel_gates[rel_gates>0] = 1
    otf_wd_array[i,:] = list(gate_elev.values()) * rel_gates
    if np.sum(np.abs(alloc_array[:,dowy[i]] - otf_prop_array[i,:])) != 0:
        otf_wd_chg[i] = 1

#check data
otf_prop_chk = otf_prop_array.sum(axis=1)
if any(otf_prop_chk != 1):
    print('bad proportion array!')
 
#partition corrected outflow to gates to run through W2
qot_corrected_file = pd.read_csv('./outflows/qot_sha-null-corrected_br1.csv') 
qotf_corrected = qot_corrected_file['QOUT']
qotf_corrected_vec = np.reshape(np.repeat(qotf_corrected,5),(len(otf_dtg),5))

partitioned_otflow = qotf_corrected_vec * otf_prop_array
df_out.iloc[2:,1:] = np.round(partitioned_otflow,1)
df_out.to_csv('./outflows/qot_sha-null-partitioned_br1.csv',index=False,header=['$10/1/1995-12/31/2016 SHA outflow (historical)','','','','',''])
    

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Plots

#plot elev timeseries and release
sns.set_theme()
sns.set_style('ticks')
sns.set_context('paper')

dtg_index = sha_hist_elev.index
mod_areas = dtg_index[otf_wd_chg==1]

#dt_format=mdates.DateFormatter('%m-%d')
fig = plt.figure(layout='constrained',figsize=(8,12))
gs0 = fig.add_gridspec(6,1,height_ratios=[2,1,1,1,1,1])
ax1 = fig.add_subplot(gs0[0])

ax1.plot(dtg_index,elev,c='black')
ax1.scatter(dtg_index,otf_wd_array[:,0],s=0.25,color='blue')
ax1.scatter(dtg_index,otf_wd_array[:,1],s=0.25,color='cyan')
ax1.scatter(dtg_index,otf_wd_array[:,2],s=0.25,color='gray')
ax1.scatter(dtg_index,otf_wd_array[:,3],s=0.25,color='orange')
ax1.scatter(dtg_index,otf_wd_array[:,4],s=0.25,color='green')
for i in range(len(mod_areas)):
    ax1.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.1)
ax1.set_ylim([220,330])
ax1.set_ylabel('elevation (m)')

ax2 = fig.add_subplot(gs0[1])
ax2.plot(dtg_index,otf_prop_array[:,4],linewidth=0.5,color='green')
for i in range(len(mod_areas)):
    ax2.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax2.set_ylim([0,1.01])
ax2.set_ylabel('SPILL activation')

ax3 = fig.add_subplot(gs0[2])
ax3.plot(dtg_index,otf_prop_array[:,3],linewidth=0.5,color='orange')
for i in range(len(mod_areas)):
    ax3.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax3.set_ylim([0,1.01])
ax3.set_ylabel('UPP activation')

ax4 = fig.add_subplot(gs0[3])
ax4.plot(dtg_index,otf_prop_array[:,2],linewidth=0.5,color='gray')
for i in range(len(mod_areas)):
    ax4.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax4.set_ylim([0,1.01])
ax4.set_ylabel('MID activation')

ax5 = fig.add_subplot(gs0[4])
ax5.plot(dtg_index,otf_prop_array[:,1],linewidth=0.5,color='cyan')
for i in range(len(mod_areas)):
    ax5.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax5.set_ylim([0,1.01])
ax5.set_ylabel('LOW activation')

ax6 = fig.add_subplot(gs0[5])
ax6.plot(dtg_index,otf_prop_array[:,0],linewidth=0.5,color='blue')
for i in range(len(mod_areas)):
    ax6.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax6.set_ylim([0,1.01])
ax6.set_ylabel('SDG activation')
#ax1.xaxis.set_major_formatter(dt_format)
plt.show()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#outflows for All historical period
#read in corrected outflow file after run through W2 and mass-balance correction applied in R
qot_corrected_file = pd.read_csv('./outflows/qot_sha-90-24-corrected_br1.csv',index_col=0,parse_dates=True) 
qotf_corrected = qot_corrected_file.values
df_out.iloc[2:,1] = np.round(qotf_corrected,1)
df_out.to_csv('./outflows/qot_sha-90-24_br1.csv',index=False,header=['$2/1/1990-8/29/2024 SHA outflow (historical)','','','','',''])

#allocate corrected flows to simulated TCD operations
dowy = np.array([water_day(d,calendar.isleap(d.year)) for d in otf_dtg])
#gate_elev = {'SDG':226.2,'LOW':248.4,'MID':281,'UPP':311.5,'SPILL':325.2}
gate_elev = {'SDG':226.2,'LOW':256.6,'MID':287.2,'UPP':316.1,'SPILL':325.2}

#setup standard gate strategy
#gates go from bottom to top in array dimensions
#0 = SDG, 1 = LOW, 2 = MID, 3 = UPP, 4 = SPILL
alloc_array = np.zeros((5,365))
#oct1 - dec31: 50% SDG, 50% LOW
alloc_array[0,0:92] = 0.5
alloc_array[1,0:92] = 0.5
#jan1 - jun1: 100% UPP
alloc_array[3,92:243] = 1
#jun1 - jul15: 50% UPP, 50% MID
alloc_array[3,243:288] = 0.5
alloc_array[2,243:288] = 0.5
#jul15 - aug15: 100% MID
alloc_array[2,288:319] = 1
#aug15 - sep30: 100% LOW
alloc_array[1,319:365] = 1

otf_prop_array = np.zeros((len(otf_dtg),5)) #store outflow proportion
otf_wd_array = np.zeros((len(otf_dtg),5))   #store outflow withdrawal for plotting
otf_wd_chg = np.zeros(len(otf_dtg))
sha_hist_elev = pd.read_csv('./data/W2_hist_90-24_elev.csv',index_col=0,parse_dates=True)
elev = sha_hist_elev['elevation (m)']
for i in range(len(otf_dtg)):
    otf_prop_array[i,:] = alloc_array[:,dowy[i]]
    #activate spillway if above spillway elevation
    ##if elev.iloc[i] > gate_elev['SPILL']:
        ##print('spillway usage',i)
        ##otf_prop_array[i,:] = ([0,0,0,0,1])
    if elev.iloc[i] < (gate_elev['UPP']+5) and dowy[i] >= 92 and dowy[i] < 243:
        print('below UPP and jan-jun, 100% MID',i)
        otf_prop_array[i,:] = ([0,0,1,0,0])
    if elev.iloc[i] < (gate_elev['MID']+5) and dowy[i] >= 92 and dowy[i] < 243:
        print('below MID and jan-jun, 100% LOW',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+5) and dowy[i] >= 92 and dowy[i] < 243:
        print('below LOW and jan-jun, 100% SDG',i)
        otf_prop_array[i,:] = ([1,0,0,0,0])
    if elev.iloc[i] < (gate_elev['UPP']+10) and dowy[i] >= 243 and dowy[i] < 288:
        print('below UPP and jun-jul, 100% MID',i)
        otf_prop_array[i,:] = ([0,0,1,0,0])
    if elev.iloc[i] < (gate_elev['MID']+10) and dowy[i] >= 243 and dowy[i] < 288:
        print('below MID and jun-jul, 100% LOW',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+10) and dowy[i] >= 243 and dowy[i] < 288:
        print('below MID and jun-jul, 100% SDG',i)
        otf_prop_array[i,:] = ([1,0,0,0,0])
    if elev.iloc[i] < (gate_elev['MID']+20) and dowy[i] >= 288 and dowy[i] < 319:
        print('below MID and jul-aug, 100% LOW',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+20) and dowy[i] >= 288 and dowy[i] < 319:
        print('below LOW and jul-aug, 100% SDG',i)
        otf_prop_array[i,:] = ([0,1,0,0,0])
    if elev.iloc[i] < (gate_elev['LOW']+25) and dowy[i] >= 319:
        print('below LOW and aug-sep, 100% SDG',i)
        otf_prop_array[i,:] = ([1,0,0,0,0])
    rel_gates = np.copy(otf_prop_array[i,:])
    rel_gates[rel_gates>0] = 1
    otf_wd_array[i,:] = list(gate_elev.values()) * rel_gates
    if np.sum(np.abs(alloc_array[:,dowy[i]] - otf_prop_array[i,:])) != 0:
        otf_wd_chg[i] = 1

#check data
otf_prop_chk = otf_prop_array.sum(axis=1)
if any(otf_prop_chk != 1):
    print('bad proportion array!')
 
#partition corrected outflow to gates to run through W2
qotf_corrected_vec = np.reshape(np.repeat(qotf_corrected,5),(len(otf_dtg),5))

partitioned_otflow = qotf_corrected_vec * otf_prop_array
df_out.iloc[2:,1:] = np.round(partitioned_otflow,1)
df_out.to_csv('./outflows/qot_sha-90-24-partitioned_br1.csv',index=False,header=['$2/1/1990-8/29/2024 SHA outflow (historical)','','','','',''])
    

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Plots

#plot elev timeseries and release
sns.set_theme()
sns.set_style('ticks')
sns.set_context('paper')

dtg_index = sha_hist_elev.index
mod_areas = dtg_index[otf_wd_chg==1]

#dt_format=mdates.DateFormatter('%m-%d')
fig = plt.figure(layout='constrained',figsize=(8,12))
gs0 = fig.add_gridspec(6,1,height_ratios=[2,1,1,1,1,1])
ax1 = fig.add_subplot(gs0[0])

ax1.plot(dtg_index,elev,c='black')
ax1.scatter(dtg_index,otf_wd_array[:,0],s=0.25,color='blue')
ax1.scatter(dtg_index,otf_wd_array[:,1],s=0.25,color='cyan')
ax1.scatter(dtg_index,otf_wd_array[:,2],s=0.25,color='gray')
ax1.scatter(dtg_index,otf_wd_array[:,3],s=0.25,color='orange')
ax1.scatter(dtg_index,otf_wd_array[:,4],s=0.25,color='green')
for i in range(len(mod_areas)):
    ax1.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.1)
ax1.set_ylim([220,330])
ax1.set_ylabel('elevation (m)')

ax2 = fig.add_subplot(gs0[1])
ax2.plot(dtg_index,otf_prop_array[:,4],linewidth=0.5,color='green')
for i in range(len(mod_areas)):
    ax2.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax2.set_ylim([0,1.01])
ax2.set_ylabel('SPILL activation')

ax3 = fig.add_subplot(gs0[2])
ax3.plot(dtg_index,otf_prop_array[:,3],linewidth=0.5,color='orange')
for i in range(len(mod_areas)):
    ax3.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax3.set_ylim([0,1.01])
ax3.set_ylabel('UPP activation')

ax4 = fig.add_subplot(gs0[3])
ax4.plot(dtg_index,otf_prop_array[:,2],linewidth=0.5,color='gray')
for i in range(len(mod_areas)):
    ax4.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax4.set_ylim([0,1.01])
ax4.set_ylabel('MID activation')

ax5 = fig.add_subplot(gs0[4])
ax5.plot(dtg_index,otf_prop_array[:,1],linewidth=0.5,color='cyan')
for i in range(len(mod_areas)):
    ax5.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax5.set_ylim([0,1.01])
ax5.set_ylabel('LOW activation')

ax6 = fig.add_subplot(gs0[5])
ax6.plot(dtg_index,otf_prop_array[:,0],linewidth=0.5,color='blue')
for i in range(len(mod_areas)):
    ax6.axvline(x=mod_areas[i],c='pink',linewidth=0.1,alpha=0.05)
ax6.set_ylim([0,1.01])
ax6.set_ylabel('SDG activation')
#ax1.xaxis.set_major_formatter(dt_format)
plt.show()





################################EEND