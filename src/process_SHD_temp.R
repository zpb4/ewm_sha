setwd('z:/ewm_sha/')
library(stringr)

shd_temp = read.table('./data/SHD_hrly_temp.txt',sep=',',header = T)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#streamflow temps
#extract date/time data
shd_temp_yrs = as.numeric(str_sub(shd_temp$DATE.TIME,1,4))-1900
shd_temp_mos = as.numeric(str_sub(shd_temp$DATE.TIME,5,6))-1
shd_temp_dys = as.numeric(str_sub(shd_temp$DATE.TIME,7,8))
n = length(shd_temp_yrs)

#convert to a start and end date
st = paste(shd_temp_yrs[1]+1900,shd_temp_mos[1],shd_temp_dys[1],sep='-')
ed = paste(shd_temp_yrs[n]+1900,shd_temp_mos[n],shd_temp_dys[n],sep='-')

#convert from F to C for temps and setup DTG
shd_temps_c = (as.numeric(shd_temp$VALUE) - 32) / (9/5)
shd_dates = seq(as.Date(st),as.Date(ed),'day')
shd_idx = as.POSIXlt(shd_dates)

new_start = '1990-11-16'  #temps appear to be corrupt before this date

#compile temperatures to mean daily values
temp_vec = rep(NA,length(shd_dates))
for(i in 1:length(shd_dates)){
  temp_vec[i] = mean(shd_temps_c[which(shd_temp_yrs==shd_idx$year[i] & shd_temp_mos==shd_idx$mo[i] & shd_temp_dys==shd_idx$mday[i])],na.rm=T)
}

#update temp vector by removing corrupt days at beginning
idx_update = which(shd_dates==new_start):length(shd_dates)
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
shd_mat = data.frame(as.character(shd_dates[idx_update]),tvc)
colnames(shd_mat)<-c('date','temp_C')
write.table(shd_mat,'./data/SHD_90-24_temp_C.csv',sep=',',row.names = F,)

rm(list=ls());gc()

###############################################END#############################################################