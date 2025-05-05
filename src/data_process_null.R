setwd('z:/ewm_sha/')
library(stringr)

cfs_to_m3s = 0.028316847

flows = read.csv('./raw_data/cord-sim_realtime_ppic.csv')
weath1 = read.csv('./raw_data/WEATH1.csv')
met_file = read.csv('./met/met_sha.csv',header = F)
dlt_temp = read.table('./raw_data/DLT_hrly_temp.txt',sep=',',header = T)

qin1_file = read.csv('./inflows/qin_sha_br1.csv',header=F)
qin2_file = read.csv('./inflows/qin_sha_br2.csv',header=F)
qin3_file = read.csv('./inflows/qin_sha_br3.csv',header=F)
qin4_file = read.csv('./inflows/qin_sha_br4.csv',header=F)
qin5_file = read.csv('./inflows/qin_sha_br5.csv',header=F)

qin1_mn = mean(as.numeric(qin1_file$V2[4:length(qin1_file$V2)]))
qin2_mn = mean(as.numeric(qin2_file$V2[4:length(qin2_file$V2)]))
qin3_mn = mean(as.numeric(qin3_file$V2[4:length(qin3_file$V2)]))
qin4_mn = mean(as.numeric(qin4_file$V2[4:length(qin4_file$V2)]))
qin5_mn = mean(as.numeric(qin5_file$V2[4:length(qin5_file$V2)]))

qin1_pro = qin1_mn / sum(qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn)
qin2_pro = qin2_mn / sum(qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn)
qin3_pro = qin3_mn / sum(qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn)
qin4_pro = qin4_mn / sum(qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn)
qin5_pro = qin5_mn / sum(qin1_mn,qin2_mn,qin3_mn,qin4_mn,qin5_mn)

date = flows$X
sha_inf = flows$SHA_inf * cfs_to_m3s
sha_otf = flows$SHA_otf * cfs_to_m3s
sha_store = flows$SHA_storage

hist_date = seq(as.Date('1995-10-01'),as.Date('2016-12-31'),'day')
hist_idx = as.POSIXlt(hist_date)

qin1_file_out = rbind(qin1_file[1:3,],array(NA,c(length(hist_date),dim(qin1_file)[2])))
qin1_file_out[4:length(qin1_file_out$V1),1] <- 1:(length(qin1_file_out$V1)-3)
qin1_file_out[4:length(qin1_file_out$V1),2] <- sha_inf * qin1_pro
qin1_file_out[1,1]<-'$1995-2016 Shasta Res Branch 1 (pit usgs) inflow w usbr comp infl - daily frac'
qin1_file_out <- apply(qin1_file_out,c(1,2),as.numeric)
write.table(qin1_file_out,'./inflows/qin_sha-null_br1.csv',sep=',',row.names = F,col.names = F)

qin1_file_out = rbind(qin1_file[1:3,],array(NA,c(length(hist_date),dim(qin1_file)[2])))
qin1_file_out[4:length(qin1_file_out$V1),1] <- 1:(length(qin1_file_out$V1)-3)
qin1_file_out[4:length(qin1_file_out$V1),2] <- sha_inf
qin1_file_out[1,1]<-'$1995-2016 Shasta Res Branch 1 (pit usgs) inflow w usbr comp infl - daily frac'
qin1_file_out <- apply(qin1_file_out,c(1,2),as.numeric)
write.table(qin1_file_out,'./inflows/qin_sha2-null_br1.csv',sep=',',row.names = F,col.names = F)

qin2_file_out = rbind(qin2_file[1:3,],array(NA,c(length(hist_date),dim(qin2_file)[2])))
qin2_file_out[4:length(qin2_file_out$V1),1] <- 1:(length(qin2_file_out$V1)-3)
qin2_file_out[4:length(qin2_file_out$V1),2] <- sha_inf * qin2_pro
qin2_file_out[1,1]<-'$1995-2016 Shasta Res Branch 2 (sqw usgs) inflow w usbr comp infl - daily frac'
qin2_file_out <- apply(qin2_file_out,c(1,2),as.numeric)
write.table(qin2_file_out,'./inflows/qin_sha-null_br2.csv',sep=',',row.names = F,col.names = F)

qin3_file_out = rbind(qin3_file[1:3,],array(NA,c(length(hist_date),dim(qin3_file)[2])))
qin3_file_out[4:length(qin3_file_out$V1),1] <- 1:(length(qin3_file_out$V1)-3)
qin3_file_out[4:length(qin3_file_out$V1),2] <- sha_inf * qin3_pro
qin3_file_out[1,1]<-'$1995-2016 Shasta Res Branch 3 (mccloud usgs) inflow w usbr comp infl - daily frac'
qin3_file_out <- apply(qin3_file_out,c(1,2),as.numeric)
write.table(qin3_file_out,'./inflows/qin_sha-null_br3.csv',sep=',',row.names = F,col.names = F)

qin4_file_out = rbind(qin4_file[1:3,],array(NA,c(length(hist_date),dim(qin4_file)[2])))
qin4_file_out[4:length(qin4_file_out$V1),1] <- 1:(length(qin4_file_out$V1)-3)
qin4_file_out[4:length(qin4_file_out$V1),2] <- sha_inf * qin4_pro
qin4_file_out[1,1]<-'$1995-2016 Shasta Res Branch 4 (sacto usgs) inflow w usbr comp infl - daily frac'
qin4_file_out <- apply(qin4_file_out,c(1,2),as.numeric)
write.table(qin4_file_out,'./inflows/qin_sha-null_br4.csv',sep=',',row.names = F,col.names = F)

qin5_file_out = rbind(qin5_file[1:3,],array(NA,c(length(hist_date),dim(qin5_file)[2])))
qin5_file_out[4:length(qin5_file_out$V1),1] <- 1:(length(qin5_file_out$V1)-3)
qin5_file_out[4:length(qin5_file_out$V1),2] <- sha_inf * qin5_pro
qin5_file_out[1,1]<-'$1995-2016 Shasta Res Branch 5 inflow'
qin5_file_out <- apply(qin5_file_out,c(1,2),as.numeric)
write.table(qin5_file_out,'./inflows/qin_sha-null_br5.csv',sep=',',row.names = F,col.names = F)


qot1_file = read.csv('./outflows/qot_br1.csv',header=F)

qot1_file_out = rbind(qot1_file[1:3,],array(0,c(length(hist_date),dim(qot1_file)[2])))
qot1_file_out[4:length(qot1_file_out$V1),1] <- 1:(length(qot1_file_out$V1)-3)
qot1_file_out[4:length(qot1_file_out$V1),3] <- sha_otf + diff_m3s
qot1_file_out[1,1]<-'$1995-2016 Shasta Reservoir branch 1 outflow'
qot1_file_out <- apply(qot1_file_out,c(1,2),as.numeric)
write.table(qot1_file_out,'./outflows/qot_sha-null_br1.csv',sep=',',row.names = F,col.names = F)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#meteorology
null_dtg = weath1$time.of.observation
null_tair = (weath1$dry.bulb.air.temperatin.in.F - 32) / (9/5)
null_tdew = (weath1$wet.bulb.or.dew.point.air.temp - 32) / (9/5)
null_windspd = weath1$wind.speed.in.mph / 2.23693629
null_cc = weath1$fraction.of.sky.that.is.cloud.covered * 10
wind_dir = mean(as.numeric(met_file[4:length(met_file$V1),5]))

null_yrs = as.numeric(str_sub(null_dtg,1,2))+80
null_mths = as.numeric(str_sub(null_dtg,3,4))

tair_vec = rep(NA,length(hist_date))
tdew_vec = rep(NA,length(hist_date))
windspd_vec = rep(NA,length(hist_date))

for(i in 1:length(null_yrs)){
  tair_vec[which(hist_idx$year==null_yrs[i] & hist_idx$mo==(null_mths[i]-1))] <- null_tair[i]
  tdew_vec[which(hist_idx$year==null_yrs[i] & hist_idx$mo==(null_mths[i]-1))] <- null_tdew[i]
  windspd_vec[which(hist_idx$year==null_yrs[i] & hist_idx$mo==(null_mths[i]-1))] <- null_windspd[i]
}

met_file_out = rbind(met_file[1:3,],array(NA,c(length(hist_date),dim(met_file)[2])))
met_file_out[4:length(met_file_out$V1),1] <- 1:(length(met_file_out$V1)-3)
met_file_out[4:length(met_file_out$V1),2] <- tair_vec
met_file_out[4:length(met_file_out$V1),3] <- tdew_vec
met_file_out[4:length(met_file_out$V1),4] <- windspd_vec
met_file_out[4:length(met_file_out$V1),5] <- wind_dir
met_file_out[4:length(met_file_out$V1),6] <- null_cc[1]

met_file_out[1,1] <- '$1995-2016 Shasta Reservoir meteorology'

#met_file_out[4:length(met_file_out$V1),1:6] <- apply(met_file_out[4:length(met_file_out$V1),1:6],c(1,2),as.numeric)
met_file_out <- apply(met_file_out,c(1,2),as.numeric)
#met_file_out[3,]<-c('JDAY','TAIR','TDEW','WIND','PHI','CLOUD')

write.table(met_file_out,'./met/met_sha_null.csv',sep=',',row.names = F,col.names = F)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#streamflow temps
dlt_temp_yrs = as.numeric(str_sub(dlt_temp$DATE.TIME,1,4))-1900
dlt_temp_mos = as.numeric(str_sub(dlt_temp$DATE.TIME,5,6))-1
dlt_temp_dys = as.numeric(str_sub(dlt_temp$DATE.TIME,7,8))
n = length(dlt_temp_yrs)

st = paste(dlt_temp_yrs[1]+1900,dlt_temp_mos[1],dlt_temp_dys[1],sep='-')
ed = paste(dlt_temp_yrs[n]+1900,dlt_temp_mos[n],dlt_temp_dys[n],sep='-')

dlt_temps_c = (as.numeric(dlt_temp$VALUE) - 32) / (9/5)
dlt_dates = seq(as.Date(st),as.Date(ed),'day')
dlt_idx = as.POSIXlt(dlt_dates)

#temp_vec = rep(NA,length(dlt_dates))
#for(i in 1:length(dlt_dates)){
  #temp_vec[i] = mean(dlt_temps_c[which(dlt_temp_yrs==dlt_idx$year[i] & dlt_temp_mos==dlt_idx$mo[i] & dlt_temp_dys==dlt_idx$mday[i])],na.rm=T)
#}

dlt_mat = cbind(as.character(dlt_dates),temp_vec)
tvec = dlt_mat[,2];tvec[tvec=='NaN']<-mean(as.numeric(tvec),na.rm=T)
dlt_mat[,2] <- as.numeric(tvec)
colnames(dlt_mat)<-c('date','temp_C')
write.table(dlt_mat,'./raw_data/DLT_89-24_temp_C.csv',sep=',',row.names = F,)

st_idx = which(dlt_dates==hist_date[1])
ed_idx = which(dlt_dates==hist_date[length(hist_date)])

dlt_null = dlt_mat[st_idx:ed_idx,]

dlt_null = apply(dlt_null,c(1,2),as.numeric)

t = which(dlt_null[,2]<(-5) | dlt_null[,2]>50)
tvc = dlt_null[,2]

for(i in 1:length(t)){
  tvc[t[i]] <- tvc[t[i]-1]
}

t = which(tvc<(-5)|tvc>50)

dlt_null_out <- data.frame(hist_date,tvc)
colnames(dlt_null_out) <- c('Date','Temp (C)')

write.table(dlt_null,'./raw_data/DLT_95-16_temp_C.csv',sep=',',row.names = F)

tin1_file = read.csv('./inflows/tin_sha_br1.csv',header=F)
tin2_file = read.csv('./inflows/tin_sha_br2.csv',header=F)
tin3_file = read.csv('./inflows/tin_sha_br3.csv',header=F)
tin4_file = read.csv('./inflows/tin_sha_br4.csv',header=F)
tin5_file = read.csv('./inflows/tin_sha_br5.csv',header=F)

tin1_file_out = rbind(tin1_file[1:3,],array(NA,c(length(hist_date),dim(tin1_file)[2])))
tin1_file_out[4:length(tin1_file_out$V1),1] <- 1:(length(tin1_file_out$V1)-3)
tin1_file_out[4:length(tin1_file_out$V1),2] <- dlt_null[,2]
tin1_file_out[1,1]<-'$1995-2016 Shasta Reservoir branch 1 inflow temperature'
tin1_file_out <- apply(tin1_file_out,c(1,2),as.numeric)
write.table(tin1_file_out,'./inflows/tin_sha-null_br1.csv',sep=',',row.names = F,col.names = F)
write.table(tin1_file_out,'./inflows/tin_sha2-null_br1.csv',sep=',',row.names = F,col.names = F)

tin2_file_out = rbind(tin2_file[1:3,],array(NA,c(length(hist_date),dim(tin2_file)[2])))
tin2_file_out[4:length(tin2_file_out$V1),1] <- 1:(length(tin2_file_out$V1)-3)
tin2_file_out[4:length(tin2_file_out$V1),2] <- dlt_null[,2]
tin2_file_out[1,1]<-'$1995-2016 Shasta Reservoir branch 2 inflow temperature'
tin2_file_out <- apply(tin2_file_out,c(1,2),as.numeric)
write.table(tin2_file_out,'./inflows/tin_sha-null_br2.csv',sep=',',row.names = F,col.names = F)

tin3_file_out = rbind(tin3_file[1:3,],array(NA,c(length(hist_date),dim(tin3_file)[2])))
tin3_file_out[4:length(tin3_file_out$V1),1] <- 1:(length(tin3_file_out$V1)-3)
tin3_file_out[4:length(tin3_file_out$V1),2] <- dlt_null[,2]
tin3_file_out[1,1]<-'$1995-2016 Shasta Reservoir branch 3 inflow temperature'
tin3_file_out <- apply(tin3_file_out,c(1,2),as.numeric)
write.table(tin3_file_out,'./inflows/tin_sha-null_br3.csv',sep=',',row.names = F,col.names = F)

tin4_file_out = rbind(tin4_file[1:3,],array(NA,c(length(hist_date),dim(tin4_file)[2])))
tin4_file_out[4:length(tin4_file_out$V1),1] <- 1:(length(tin4_file_out$V1)-3)
tin4_file_out[4:length(tin4_file_out$V1),2] <- dlt_null[,2]
tin4_file_out[1,1]<-'$1995-2016 Shasta Reservoir branch 4 inflow temperature'
tin4_file_out <- apply(tin4_file_out,c(1,2),as.numeric)
write.table(tin4_file_out,'./inflows/tin_sha-null_br4.csv',sep=',',row.names = F,col.names = F)

tin5_file_out = rbind(tin5_file[1:3,],array(NA,c(length(hist_date),dim(tin5_file)[2])))
tin5_file_out[4:length(tin5_file_out$V1),1] <- 1:(length(tin5_file_out$V1)-3)
tin5_file_out[4:length(tin5_file_out$V1),2] <- dlt_null[,2]
tin5_file_out[1,1]<-'$1995-2016 Shasta Reservoir branch 5 inflow temperature'
tin5_file_out <- apply(tin5_file_out,c(1,2),as.numeric)
write.table(tin5_file_out,'./inflows/tin_sha-null_br5.csv',sep=',',row.names = F,col.names = F)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#wind speed & direction calcs
u_ms = -0.1
v_ms = -10

wind_spd = sqrt(u_ms^2 + v_ms^2)
#meteorological wind
phi = atan2(u_ms/wind_spd, v_ms/wind_spd) + pi
phi_degrees = phi * 180/pi
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#outflow & storage comparisons
sha_hist_elev = read.csv('./raw_data/SHA_elev.csv')
elev_dtg = sha_hist_elev$DATE.TIME
elev_date = seq(as.Date(str_sub(elev_dtg,1,10)[1]),as.Date(str_sub(elev_dtg,1,10)[length(elev_dtg)]),'day')
sha_elev = sha_hist_elev$VALUE
na_idx = which(is.na(sha_elev)==T)
for(i in 1:length(na_idx)){
  sha_elev[na_idx[i]]<-sha_elev[na_idx[i]-1]
}

sha_hist_store = read.csv('./raw_data/SHA_store.csv')
store_dtg = sha_hist_store$DATE.TIME
store_date = seq(as.Date(str_sub(store_dtg,1,10)[1]),as.Date(str_sub(store_dtg,1,10)[length(store_dtg)]),'day')
sha_store = as.numeric(str_remove_all(sha_hist_store$VALUE,','))
na_idx = which(is.na(sha_store)==T)
for(i in 1:length(na_idx)){
  sha_store[na_idx[i]]<-sha_store[na_idx[i]-1]
}

hist_elev = sha_elev[which(elev_date==hist_date[1]):which(elev_date==hist_date[length(hist_date)])] * 0.3048
hist_store = sha_store[which(store_date==hist_date[1]):which(store_date==hist_date[length(hist_date)])] / 1e6

ls_fit<-loess(hist_store~hist_elev,span=0.75,degree=2,family='gaussian',control=loess.control(surface='direct',statistics = 'none',trace.hat = 'approximate'))
ls_pred<-predict(ls_fit,hist_elev)

#plot(hist_elev,hist_store)
#points(hist_elev,ls_pred,col='red')

w2_sha_elev = read.csv('./tsr_output/tsr_1_seg21.csv')
w2_elev = w2_sha_elev$ELWS.m.

w2_store = predict(ls_fit,w2_elev)
w2_mat = data.frame(hist_date[-c(length(hist_date))],w2_store)
colnames(w2_mat)<-c('date','storage (MAF)')
write.table(w2_mat,'./raw_data/W2_hist_95-16_store.csv',sep=',',row.names = F,)

lowwd_temp_w2 <- read.csv('./tsr_output/tsr_2_seg21_lowwd.csv')
w2_mat = data.frame(hist_date[-c(length(hist_date))],lowwd_temp_w2$T2.C.)
colnames(w2_mat)<-c('date','Temp (C)')
write.table(w2_mat,'./raw_data/W2_hist_95-16_outflow-temp.csv',sep=',',row.names = F,)

met_data <- read.csv('./met/met_sha_null.csv')
tair <- as.numeric(met_data$X[3:length(met_data$X)])
tdew <- as.numeric(met_data$X.1[3:length(met_data$X)])
wind <- as.numeric(met_data$X.2[3:length(met_data$X)])
phi <- as.numeric(met_data$X.3[3:length(met_data$X)])
cloud <- as.numeric(met_data$X.4[3:length(met_data$X)])

w2_mat = data.frame(hist_date,tair,tdew,wind,phi,cloud)
colnames(w2_mat)<-c('date','Tair (C)','Tdew (C)','Wind speed (m/s)','Wind dir (phi)','Cloud cover (1-10)')
write.table(w2_mat,'./raw_data/W2_hist_95-16_met.csv',sep=',',row.names = F,)

w2_rel <- read.csv('./outflows/qot_sha-null_br1.csv')
g1_rel <- as.numeric(w2_rel$X[3:length(met_data$X)])
g2_rel <- as.numeric(w2_rel$X.1[3:length(met_data$X)])
g3_rel <- as.numeric(w2_rel$X.2[3:length(met_data$X)])
g4_rel <- as.numeric(w2_rel$X.3[3:length(met_data$X)])
g5_rel <- as.numeric(w2_rel$X.4[3:length(met_data$X)])

w2_mat = data.frame(hist_date,g1_rel,g2_rel,g3_rel,g4_rel,g5_rel)
colnames(w2_mat)<-c('date','G1 rel (m3/s)','G2 rel (m3/s)','G3 rel (m3/s)','G4 rel (m3/s)','G5 rel (m3/s)')
write.table(w2_mat,'./raw_data/W2_hist_95-16_gate-releases.csv',sep=',',row.names = F,)

w2_inf <- read.csv('./inflows/qin_sha2-null_br1.csv')
inf <- as.numeric(w2_inf$X[3:length(met_data$X)])

w2_mat = data.frame(hist_date,inf)
colnames(w2_mat)<-c('date','inflow (m3/s)')
write.table(w2_mat,'./raw_data/W2_hist_95-16_inflow.csv',sep=',',row.names = F,)

#correct the 
yrs = unique(hist_idx$year)
yr_idx = c()
for(i in 1:length(yrs)){
  yr_idx[i] = which(hist_idx$year==yrs[i] & hist_idx$mo==9 & hist_idx$mday==1)
}

diff_maf = predict(ls_fit,w2_elev[length(w2_elev)]) - predict(ls_fit,hist_elev[length(w2_elev)]) +  predict(ls_fit,hist_elev[1]) - predict(ls_fit,w2_elev[1]) 

diff_m3 = diff_maf * 1e6 * 1233
diff_m3s = diff_m3 / (60*60*24) / length(w2_elev)

plot(1:length(hist_elev),hist_elev,type='l',xlab='',ylab='Elevation (m)',ylim=c(270,330),axes=F)
lines(1:length(w2_elev),w2_elev,col='green')
axis(1,at=yr_idx,labels=yrs+1900)
axis(2,at=seq(270,330,10),labels=seq(270,330,10))
legend('bottomleft',c('Obs','W2'),lwd=c(1,1),col=c('black','green'))

low_temp_ts <- read.csv('./tsr_output/tsr_3_seg21.csv')
tlow_c <- low_temp_ts$T2.C.

plot(1:length(w2_elev),tlow_c,type='l',xlab='',ylab='Temp (C)',ylim=c(0,25),axes=F)
abline(h=20,col='red',lty=2)
abline(h=15,col='blue',lty=2)
abline(h=11.5,col='green',lty=2)
axis(1,at=yr_idx,labels=yrs+1900)
axis(2,at=seq(0,25,5),labels=seq(0,25,5))
legend('bottomleft',c('W2','suitable','optimal hi','optimal lo'),lwd=c(1,1),col=c('black','red','blue','green'))


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#SHA dam temps
shd_temp = read.table('./raw_data/SHD_hrly_temp.txt',sep=',',header = T)
shd_temp_yrs = as.numeric(str_sub(shd_temp$DATE.TIME,1,4))-1900
shd_temp_mos = as.numeric(str_sub(shd_temp$DATE.TIME,5,6))-1
shd_temp_dys = as.numeric(str_sub(shd_temp$DATE.TIME,7,8))
n = length(shd_temp_yrs)

st = paste(shd_temp_yrs[1]+1900,shd_temp_mos[1],shd_temp_dys[1],sep='-')
ed = paste(shd_temp_yrs[n]+1900,shd_temp_mos[n],shd_temp_dys[n],sep='-')

shd_temps_c = (as.numeric(shd_temp$VALUE) - 32) / (9/5)
shd_dates = seq(as.Date(st),as.Date(ed),'day')
shd_idx = as.POSIXlt(shd_dates)

temp_vec = rep(NA,length(shd_dates))
for(i in 1:length(shd_dates)){
  temp_vec[i] = mean(shd_temps_c[which(shd_temp_yrs==shd_idx$year[i] & shd_temp_mos==shd_idx$mo[i] & shd_temp_dys==shd_idx$mday[i])],na.rm=T)
}

temp_vec[1]<-10
temp_vec[temp_vec<(-5)|temp_vec>50]<-NaN
t = which(is.na(temp_vec)==T)
for(i in 1:length(t)){
  temp_vec[t[i]] <- temp_vec[t[i]-1]
}
shd_mat = cbind(as.character(shd_dates),temp_vec)
shd_mat[,2] <- as.numeric(tvec)
colnames(shd_mat)<-c('date','temp_C')
write.table(shd_mat,'./raw_data/SHD_90-24_temp_C.csv',sep=',',row.names = F,)

st_idx = which(shd_dates==hist_date[1])
ed_idx = which(shd_dates==hist_date[length(hist_date)])

shd_null = shd_mat[st_idx:ed_idx,]
tvc = as.numeric(shd_null[,2])

plot(1:length(w2_elev),tlow_c,type='l',xlab='',ylab='Temp (C)',col='green',lwd=2,ylim=c(0,25),axes=F)
lines(1:length(w2_elev),tvc[1:length(w2_elev)],col='gray',lwd=2)
abline(h=20,col='red',lty=2)
abline(h=15,col='blue',lty=2)
axis(1,at=yr_idx,labels=yrs+1900)
axis(2,at=seq(0,25,5),labels=seq(0,25,5))
legend('topright',c('W2','Obs','suitable','optimal'),lwd=c(2,2,1,1),col=c('green','gray','blue','red'))

#-------------------------------------------------------------------------------------
#data correlations
library(ranger)

pred_mat <- data.frame(inf[1:(length(inf)-1)],g2_rel[1:(length(inf)-1)],tair[1:(length(inf)-1)],tdew[1:(length(inf)-1)],wind[1:(length(inf)-1)],w2_store,tvc[1:(length(inf)-1)],lowwd_temp_w2$T2.C.)
#pred_mat <- data.frame(inf[1:(length(inf)-1)],g2_rel[1:(length(inf)-1)],tair[1:(length(inf)-1)],w2_store,tvc[1:(length(inf)-1)],lowwd_temp_w2$T2.C.)
cor_mat <- cor(pred_mat)

rf_fit <- ranger(pred_mat$lowwd_temp_w2.T2.C.~.,pred_mat)
rf_pred <- predict(rf_fit, data = pred_mat[,1:7])

plot(1:length(lowwd_temp_w2$T2.C.),lowwd_temp_w2$T2.C.,type='l')
lines(1:length(lowwd_temp_w2$T2.C.),rf_pred$predictions,col='green')

#cal/val
cal_idx = which(hist_date=='1997-10-01'):which(hist_date=='2012-09-30')
val_idx = which(hist_date=='2013-10-01'):length(hist_date)
rf_fit <- ranger(y=pred_mat$lowwd_temp_w2.T2.C.[cal_idx],x=pred_mat[cal_idx,1:7])
rf_pred <- predict(rf_fit, data = pred_mat[val_idx,1:7])

plot(1:length(val_idx),lowwd_temp_w2$T2.C.[val_idx],type='l')
lines(1:length(val_idx),rf_pred$predictions,col='green')

#cal/val2
cal_idx = which(hist_date=='2003-10-01'):(length(hist_date)-1)
val_idx = which(hist_date=='1997-10-01'):which(hist_date=='2003-09-30')
rf_fit <- ranger(y=pred_mat$lowwd_temp_w2.T2.C.[cal_idx],x=pred_mat[cal_idx,1:7])
rf_pred <- predict(rf_fit, data = pred_mat[val_idx,1:7])

plot(1:length(val_idx),lowwd_temp_w2$T2.C.[val_idx],type='l')
lines(1:length(val_idx),rf_pred$predictions,col='green')


#--------------------------------------------------------------------------------------
#experiment with outlet height selection decision variable

outlet_hts <- c(226.2,256.6,287.2,316.1)

prop_fun <- function(dec_var,pwr,outlet_hts){
  norm_span <- (outlet_hts - min(outlet_hts)) / (max(outlet_hts) - min(outlet_hts))
  inv_wt_dist <- 1 / abs(dec_var - norm_span)^pwr
  if(any(inv_wt_dist==Inf)==T){prop_out <- rep(0,length(outlet_hts));prop_out[which(inv_wt_dist==Inf)] <-1}
  else{prop_out <- inv_wt_dist / sum(inv_wt_dist)}
  return(prop_out)
}

dec_var = 0.2
pwr = 3

prop_fun(dec_var,pwr,outlet_hts)


####################################################END##################################