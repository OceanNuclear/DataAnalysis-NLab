#!/usr/bin/Rscript
library(ggplot2)
library(dplyr)
quadrature <- function(a,b){
	return (sqrt(a^2+b^2))
}
#Record background
bg = c(0.9,0.3,0.6)
bg=bg/1000
bg.mean=mean(bg)
bg.sd=sd(bg)
readVar <- function(fname){
	dat = read.table(fname, header=T, sep="\t",check.names=F)
	thickness = as.numeric(colnames(dat))
	#find mean
	dat.mu = apply(dat,2,mean)
	dat.mu = (dat.mu-bg.mean)
	#sigma
	dat.s  = apply(dat,2,sd)
	dat.s  = quadrature(dat.s,bg.sd)
	#error on mean
	dat.err= dat.s/sqrt(dim(dat)[2])
	return(c(thickness,dat.mu, dat.err, length(dat.mu)))
}
output1 = readVar("Col.tsv")
len=tail(output1,1)
#This is the most efficient way...?
c.th = output1[c(     1 :  len)]
c.mu = output1[c((  len+1):(2*len))]
c.s  = output1[c((2*len+1):(3*len))]
output2 = readVar("Uncol.tsv")
u.th = output2[c(      1:  len)]
u.mu = output2[c((  len+1):(2*len))]
u.s  = output2[c((2*len+1):(3*len))]

lmobj<-lm(log(c.mu)~c.th)
coef<-(lmobj$coefficients)
plot(c.th,log(c.mu))
abline(coef[1],coef[2])
#plot(u.th,log(u.mu))
