setwd('z:/ewm_sha/')
library(stringr)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#outflow & storage comparisons

#Null DTG
hist_date = seq(as.Date('1995-10-01'),as.Date('2016-12-31'),'day')
hist_idx = as.POSIXlt(hist_date)

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

#convert to Null timing
hist_elev = sha_elev[which(elev_date==hist_date[1]):which(elev_date==hist_date[length(hist_date)])] 
hist_store = sha_store[which(store_date==hist_date[1]):which(store_date==hist_date[length(hist_date)])]

#save SHA historical cleaned elevation data
elev_df = data.frame(hist_date,hist_elev)
colnames(elev_df)<-c('date','Elev (m)')
write.table(elev_df,'./data/hist_95-16_elev.csv',sep=',',row.names = F)

#save SHA historical cleaned storage data
store_df = data.frame(hist_date,hist_store)
colnames(store_df)<-c('date','Storage (MAF)')
write.table(store_df,'./data/hist_95-16_store.csv',sep=',',row.names = F)

#fit a loess model between elevation and storage to predict new storages, given an elevation (W2 outputs elevation)
ls_fit<-loess(hist_store~hist_elev,span=0.75,degree=2,family='gaussian',control=loess.control(surface='direct',statistics = 'none',trace.hat = 'approximate'))
ls_pred<-predict(ls_fit,hist_elev)

#quick plot to verify results
plot(hist_elev,hist_store)
points(hist_elev,ls_pred,col='red')

#read in SHA elevation timeseries from W2 model run without mass-balance correction
w2_sha_elev = read.csv('./data/W2_mass-balance_run.csv')
w2_elev = w2_sha_elev$ELWS.m.
w2_store = predict(ls_fit,w2_elev)

#plot to show mass balance discrepancy
plot(hist_date,hist_store,type='l')
lines(hist_date,w2_store,col='green')

#calculate required daily correction in m^3/s to be applied to outflows for mass balance
diff_maf = predict(ls_fit,w2_elev[length(w2_elev)]) - predict(ls_fit,hist_elev[length(w2_elev)]) +  predict(ls_fit,hist_elev[1]) - predict(ls_fit,w2_elev[1]) 
diff_m3 = diff_maf * 1e6 * 1233
diff_m3s = diff_m3 / (60*60*24) / length(w2_elev)

#apply correction to outflows and save for processing in Python
qotf <- read.csv('./outflows/qot_sha-null-raw_br1.csv',skip=2)
raw_qotf <- qotf$QOUT
corrected_qotf <- raw_qotf + diff_m3s
corrected_qotf[corrected_qotf<0] <- 0
qotf[,'QOUT'] <- corrected_qotf
write.table(qotf,'./outflows/qot_sha-null-corrected_br1.csv',sep=',',row.names = F)


#read in SHA elevation timeseries from W2 model run with mass-balance correction
w2_sha_elev = read.csv('./data/W2_mb-correction_check.csv')
w2_elev = w2_sha_elev$ELWS.m.
w2_store = predict(ls_fit,w2_elev)

#plot to show mass balance is now corrected
plot(hist_date,hist_store,type='l')
lines(hist_date,w2_store,col='green')

#save storage timeseries for Null length data
store_df = data.frame(hist_date,w2_store)
colnames(store_df)<-c('date','storage (MAF)')
write.table(store_df,'./data/W2_hist_95-16_store.csv',sep=',',row.names = F)

#save elev timeseries for Null length data
elev_df = data.frame(hist_date,w2_elev)
colnames(elev_df)<-c('date','elevation (m)')
write.table(elev_df,'./data/W2_hist_95-16_elev.csv',sep=',',row.names = F)

##################################################END############################################################
