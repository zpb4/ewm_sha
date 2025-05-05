setwd('z:/ewm_sha/')
library(stringr)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#outflow & storage comparisons

#read in and process historical elevation data
sha_hist_elev = read.csv('./data/SHA_elev.csv')
elev_dtg = sha_hist_elev$DATE.TIME
elev_date = seq(as.Date(str_sub(elev_dtg,1,10)[1]),as.Date(str_sub(elev_dtg,1,10)[length(elev_dtg)]),'day')
left_out_day <- which(!elev_date%in%as.Date(str_sub(elev_dtg,1,10)))
sha_elev = sha_hist_elev$VALUE * 0.3048 #conversion to m
sha_elev = c(sha_elev[1:(left_out_day-1)],sha_elev[(left_out_day-1)],sha_elev[left_out_day:length(sha_elev)])
na_idx = which(is.na(sha_elev)==T)
if(na_idx[1]==1){sha_elev[1]<-sha_elev[!na_idx][1];na_idx <- na_idx[-c(1)]}
for(i in 1:length(na_idx)){
  sha_elev[na_idx[i]]<-sha_elev[na_idx[i]-1]
}

#read in and process historical storage data
sha_hist_store = read.csv('./data/SHA_store.csv')
store_dtg = sha_hist_store$DATE.TIME
store_date = seq(as.Date(str_sub(store_dtg,1,10)[1]),as.Date(str_sub(store_dtg,1,10)[length(store_dtg)]),'day')
sha_store = as.numeric(str_remove_all(sha_hist_store$VALUE,',')) / 1e6 #conversion to MAF
na_idx = which(is.na(sha_store)==T)
if(na_idx[1]==1){sha_store[1]<-sha_store[!na_idx][1];na_idx <- na_idx[-c(1)]}
for(i in 1:length(na_idx)){
  sha_store[na_idx[i]]<-sha_store[na_idx[i]-1]
}

#save SHA historical cleaned elevation data (full length)
elev_df = data.frame(elev_date,sha_elev)
colnames(elev_df)<-c('date','Elev (m)')
write.table(elev_df,'./data/hist_85-25_elev.csv',sep=',',row.names = F)

#save SHA historical cleaned storage data (full length)
store_df = data.frame(store_date,sha_store)
colnames(store_df)<-c('date','Storage (MAF)')
write.table(store_df,'./data/hist_85-25_store.csv',sep=',',row.names = F)

hist_sd = '1994-10-01'
hist_ed = '2024-09-30'

sha_elev_hist <- sha_elev[which(elev_date==hist_sd):which(elev_date==hist_ed)]
sha_store_hist <- sha_store[which(store_date==hist_sd):which(store_date==hist_ed)]

#fit a loess model between elevation and storage to predict new storages, given an elevation (W2 outputs elevation)
ls_fit<-loess(sha_store_hist~sha_elev_hist,span=0.75,degree=2,family='gaussian',control=loess.control(surface='direct',statistics = 'none',trace.hat = 'approximate'))
ls_pred<-predict(ls_fit,sha_elev_hist)

#quick plot to verify results
plot(sha_elev_hist,sha_store_hist)
points(sha_elev_hist,ls_pred,col='red')

#read in historical inflow/outflow
cnrfc_dat = read.table('./data/SHDC1_daily.csv',sep=',',header = T)
sha_cnrfc_fnf <- cnrfc_dat$Flow..KCFS. * 1000
sha_cnrfc_date <- cnrfc_dat$Date..ending.12.UTC.

cnrfc_st_ch <- str_split(sha_cnrfc_date[1],'/')[[1]]
cnrfc_ed_ch <- str_split(sha_cnrfc_date[length(sha_cnrfc_date)],'/')[[1]]
cnrfc_st = paste(cnrfc_st_ch[3],str_pad(cnrfc_st_ch[1],2,'left','0'),str_pad(cnrfc_st_ch[2],2,'left','0'),sep='-')
cnrfc_ed = paste(cnrfc_ed_ch[3],str_pad(cnrfc_ed_ch[1],2,'left','0'),str_pad(cnrfc_ed_ch[2],2,'left','0'),sep='-')
ixx_cnrfc = seq(as.Date(cnrfc_st),as.Date(cnrfc_ed),by='day')

sha_inflow = read.table('./data/SHA_dly_inflow.txt',sep=',',header = T)
inflow_dtg = sha_inflow$DATE.TIME
inflow_date = seq(as.Date(paste(str_sub(inflow_dtg,1,4)[1],str_sub(inflow_dtg,5,6)[1],str_sub(inflow_dtg,7,8)[1],sep='-')),
                  as.Date(paste(str_sub(inflow_dtg,1,4)[length(inflow_dtg)],str_sub(inflow_dtg,5,6)[length(inflow_dtg)],str_sub(inflow_dtg,7,8)[length(inflow_dtg)],sep='-')),'day')
act_inflow_date = as.Date(paste(str_sub(inflow_dtg,1,4),str_sub(inflow_dtg,5,6),str_sub(inflow_dtg,7,8),sep='-'))
missing_idx = which(!inflow_date%in%act_inflow_date)
sha_inf = as.numeric(sha_inflow$VALUE)
sha_in_cfs = rep(NA,length(inflow_date))
sha_in_cfs[inflow_date%in%act_inflow_date] <- sha_inf
sha_in_cfs[!inflow_date%in%act_inflow_date] <- sha_cnrfc_fnf[ixx_cnrfc%in%inflow_date[missing_idx]]
na_idx = which(is.na(sha_in_cfs)==T)
if(na_idx[1]==1){sha_in_cfs[1]<-sha_in_cfs[!na_idx][1];na_idx <- na_idx[-c(1)]}
for(i in 1:length(na_idx)){
  sha_in_cfs[na_idx[i]]<-sha_in_cfs[na_idx[i]-1]
}
if(anyNA(sha_in_cfs)==T){print('stop, NAs in inflow TS')}

sha_outflow = read.table('./data/SHA_dly_outflow.txt',sep=',',header = T)
otflow_dtg = sha_outflow$DATE.TIME
otflow_date = seq(as.Date(paste(str_sub(otflow_dtg,1,4)[1],str_sub(otflow_dtg,5,6)[1],str_sub(otflow_dtg,7,8)[1],sep='-')),
                  as.Date(paste(str_sub(otflow_dtg,1,4)[length(otflow_dtg)],str_sub(otflow_dtg,5,6)[length(otflow_dtg)],str_sub(otflow_dtg,7,8)[length(otflow_dtg)],sep='-')),'day')
act_otflow_date = as.Date(paste(str_sub(otflow_dtg,1,4),str_sub(otflow_dtg,5,6),str_sub(otflow_dtg,7,8),sep='-'))
missing_idx = which(!otflow_date%in%act_otflow_date)
sha_out = as.numeric(sha_outflow$VALUE)
sha_out_cfs = rep(NA,length(otflow_date))
sha_out_cfs[otflow_date%in%act_otflow_date] <- sha_out
na_idx = which(is.na(sha_out_cfs)==T)
if(na_idx[1]==1){sha_out_cfs[1]<-sha_out_cfs[!na_idx][1];na_idx <- na_idx[-c(1)]}
for(i in 1:length(na_idx)){
  sha_out_cfs[na_idx[i]]<-sha_out_cfs[na_idx[i]-1]
}
if(anyNA(sha_out_cfs)==T){print('stop, NAs in outflow TS')}

#save inflow timeseries - CDEC
inflow_df = data.frame(inflow_date,sha_in_cfs)
colnames(inflow_df)<-c('date','inflow (cfs)')
write.table(store_df,'./data/hist_90-24_inflow.csv',sep=',',row.names = F)

plot(inflow_date,sha_in_cfs,type='l')

#save outflow timeseries
otflow_df = data.frame(otflow_date,sha_out_cfs)
colnames(otflow_df)<-c('date','outflow (cfs)')
write.table(otflow_df,'./data/hist_87-24_outflow.csv',sep=',',row.names = F)

plot(otflow_date,sha_out_cfs,type='l')

#read in SHA elevation timeseries from W2 model run without mass-balance correction
w2_sha_elev = read.csv('./tsr_output/tsr-raw-90-24_1_seg21.csv')
w2_elev = w2_sha_elev$ELWS.m.
w2_store = predict(ls_fit,w2_elev)

all_st = '1990-02-01'
all_ed = '2024-08-29'

all_date = seq(as.Date(all_st),as.Date(all_ed),by='day')

all_store <- sha_store[which(store_date==all_st):which(store_date==all_ed)]
all_elev <- sha_elev[which(elev_date==all_st):which(elev_date==all_ed)]

#plot to show mass balance discrepancy
plot(all_date,all_store,type='l')
lines(all_date,w2_store,col='green')

#calculate required daily correction in m^3/s to be applied to outflows for mass balance
diff_maf = predict(ls_fit,w2_elev[length(w2_elev)]) - predict(ls_fit,all_elev[length(w2_elev)]) +  predict(ls_fit,all_elev[1]) - predict(ls_fit,w2_elev[1]) 
diff_m3 = diff_maf * 1e6 * 1233
diff_m3s = diff_m3 / (60*60*24) / length(w2_elev)

#apply correction to outflows and save for processing in Python
cfs_to_m3s = 0.028316847
all_otf <- sha_out_cfs[which(otflow_date==all_st):which(otflow_date==all_ed)]
raw_qotf <- all_otf * cfs_to_m3s
corrected_qotf <- raw_qotf + diff_m3s
corrected_qotf[corrected_qotf<0] <- 0
qotf_df = data.frame(all_date,corrected_qotf )
write.table(qotf_df,'./outflows/qot_sha-90-24-corrected_br1.csv',sep=',',row.names = F)

#read in SHA elevation timeseries from W2 model run with mass-balance correction
w2_sha_elev = read.csv('./tsr_output/tsr-mb-90-24_1_seg21.csv')
w2_elev = w2_sha_elev$ELWS.m.
w2_store = predict(ls_fit,w2_elev)

#plot to show mass balance is now corrected
plot(all_date,all_store,type='l')
lines(all_date,w2_store,col='green')

#save storage timeseries for Null length data
store_df = data.frame(all_date,w2_store)
colnames(store_df)<-c('date','storage (MAF)')
write.table(store_df,'./data/W2_hist_90-24_store.csv',sep=',',row.names = F)

#save elev timeseries for Null length data
elev_df = data.frame(all_date,w2_elev)
colnames(elev_df)<-c('date','elevation (m)')
write.table(elev_df,'./data/W2_hist_90-24_elev.csv',sep=',',row.names = F)

##################################################END############################################################
