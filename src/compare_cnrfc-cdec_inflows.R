setwd('z:/ewm_sha/')
library(stringr)

hist_dat <- read.csv('./data/cord-sim_realtime_ppic.csv')
cnrfc_dat <- read.csv('./data/SHDC1_daily.csv')

sha_hist_inf <- hist_dat$SHA_inf/1000
sha_hist_fnf <- hist_dat$SHA_fnf/1000
sha_hist_date <- hist_dat$X

sha_cnrfc_fnf <- cnrfc_dat$Flow..KCFS.
sha_cnrfc_date <- cnrfc_dat$Date..ending.12.UTC.

cnrfc_st_ch <- str_split(sha_cnrfc_date[1],'/')[[1]]
cnrfc_ed_ch <- str_split(sha_cnrfc_date[length(sha_cnrfc_date)],'/')[[1]]
cnrfc_st = paste(cnrfc_st_ch[3],str_pad(cnrfc_st_ch[1],2,'left','0'),str_pad(cnrfc_st_ch[2],2,'left','0'),sep='-')
cnrfc_ed = paste(cnrfc_ed_ch[3],str_pad(cnrfc_ed_ch[1],2,'left','0'),str_pad(cnrfc_ed_ch[2],2,'left','0'),sep='-')
ixx_cnrfc = as.POSIXlt(seq(as.Date(cnrfc_st),as.Date(cnrfc_ed),by='day'))

hist_st_ch <- str_split(sha_hist_date[1],'/')[[1]]
hist_ed_ch <- str_split(sha_hist_date[length(sha_hist_date)],'/')[[1]]
hist_st = paste(hist_st_ch[3],str_pad(hist_st_ch[1],2,'left','0'),str_pad(hist_st_ch[2],2,'left','0'),sep='-')
hist_ed = paste(hist_ed_ch[3],str_pad(hist_ed_ch[1],2,'left','0'),str_pad(hist_ed_ch[2],2,'left','0'),sep='-')
ixx_hist = as.POSIXlt(seq(as.Date(hist_st),as.Date(hist_ed),by='day'))

plot(ixx_hist,sha_hist_fnf,type='l',lwd=2)
lines(ixx_hist,sha_hist_inf,lwd=2,col='green')

plot(sha_hist_fnf,sha_hist_inf)

plot(sha_cnrfc_fnf[ixx_cnrfc%in%ixx_hist],sha_hist_inf)

plot(sha_cnrfc_fnf[ixx_cnrfc%in%ixx_hist],sha_hist_inf,xlab='SHDC1 inflow (kcfs) - CNRFC: 10/1/95 - 12/31/16',ylab='SHA inflow (kcfs) - CDEC: 10/1/95 - 12/31/16')
abline(0,1,col='red',lty=2)
legend('topleft',c('Inflows','1:1 line'),lty=c(1,2),col=c('black','red'))

########################################END#################################################