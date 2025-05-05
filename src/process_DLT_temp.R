setwd('z:/ewm_sha/')
library(stringr)

dlt_temp = read.table('./data/DLT_hrly_temp.txt',sep=',',header = T)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#streamflow temps
#extract date/time data
dlt_temp_yrs = as.numeric(str_sub(dlt_temp$DATE.TIME,1,4))-1900
dlt_temp_mos = as.numeric(str_sub(dlt_temp$DATE.TIME,5,6))-1
dlt_temp_dys = as.numeric(str_sub(dlt_temp$DATE.TIME,7,8))
n = length(dlt_temp_yrs)

#convert to a start and end date
st = paste(dlt_temp_yrs[1]+1900,dlt_temp_mos[1],dlt_temp_dys[1],sep='-')
ed = paste(dlt_temp_yrs[n]+1900,dlt_temp_mos[n],dlt_temp_dys[n],sep='-')

#convert from F to C for temps and setup DTG
dlt_temps_c = (as.numeric(dlt_temp$VALUE) - 32) / (9/5)
dlt_dates = seq(as.Date(st),as.Date(ed),'day')
dlt_idx = as.POSIXlt(dlt_dates)

new_start = '1990-02-01'  #temps appear to be corrupt before this date

#compile temperatures to mean daily values
temp_vec = rep(NA,length(dlt_dates))
for(i in 1:length(dlt_dates)){
  temp_vec[i] = mean(dlt_temps_c[which(dlt_temp_yrs==dlt_idx$year[i] & dlt_temp_mos==dlt_idx$mo[i] & dlt_temp_dys==dlt_idx$mday[i])],na.rm=T)
}

#update temp vector by removing corrupt days at beginning
idx_update = which(dlt_dates==new_start):length(dlt_dates)
temp_vec = temp_vec[idx_update]

#identify any other erroneous data that will throw errors in W2
t = which(temp_vec<(-5) | temp_vec>50 | is.na(temp_vec)==T)
tvc = temp_vec

#replace bad values with a persistence estimate from last good value
for(i in 1:length(t)){
  if(t[i]!=1){
    tvc[t[i]] <- tvc[t[i]-1]}
  if(t[i]==1){tvc[t[i]]<-mean(tvc,na.rm=T)}
}

if(length(which(tvc<(-5)|tvc>50|is.na(tvc)==T)) > 0){print('data cleaning did not work')}

#save to csv
dlt_mat = data.frame(as.character(dlt_dates[idx_update]),tvc)
colnames(dlt_mat)<-c('date','temp_C')
write.table(dlt_mat,'./data/DLT_90-24_temp_C.csv',sep=',',row.names = F,)

rm(list=ls());gc()

#############################################END###########################################