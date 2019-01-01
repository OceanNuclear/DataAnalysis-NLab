#!/usr/bin/Rscript
library(ggplot2)
#library(dplyr, warn.conflicts = F)
#library(devtools)
library(reshape2)
quadrature <- function(a,b){
	return (sqrt(a^2+b^2))
}

#Record background
bg = c(0.9,0.3,0.6)/2#changes these records

#function to turn file into data frame
readVar <- function(fname,color){
	dat 	= read.table(fname, header=T, sep="\t",check.names=F)
	thickness = as.numeric(colnames(dat))
	#find mean
	dat.mu	= apply(dat,2,mean)
	dat.mu	= (dat.mu-mean(bg))
	#sigma
	dat.s	= apply(dat,2,sd)
	dat.s	= quadrature(dat.s,sd(bg))
	#error on mean
	dat.err	= dat.s/sqrt(dim(dat)[2])
	logerr	= dat.err/dat.mu

	#Create data frame
	df = data.frame(thickness=thickness,
		'log.dose.rate'	=log(dat.mu),
		error 			=logerr,
		ymax 			=(log(dat.mu)+logerr),
		ymin 			=(log(dat.mu)-logerr),
		color			=color
		)

	#remove the weird row name labels
	row.names(df)<-NULL
	return(df)
}
toFormula<- function(dat){#You'd think that given R is a plotting engine, I don't have to write my own code just to add numbers onto the graph...
	#stopifnot(length(coefs)==2)#assert that it has two coefficients
	m=1
	c=1
	dm=1
	dc=1
	text <-paste("m= ",toString(m))
	text <-paste("c= ",toString(c))
	text <-paste("%+-%",toString(dm))
	text <-paste("dc=",toString(dc))
	return (text)
}
lmize <- function(dat,resid=F,cov=F){
	lmobj	<- lm(log.dose.rate~thickness,weight=(1/error^2),data=dat)
	#can repurpose lmize by parsing resid=T to return  the list of residuals.
	if (resid)
		{return (summary(lmobj)$residuals)}
	coefs	<- lmobj$coef
	color	<- head(dat['color'],1)#take only the first datapoint's color
	pcov	<- vcov(lmobj)
	#repurpsoe lmize to return covariance matrix,
	if (cov)
		{return (pcov)}
	srpcov	<- sqrt(abs(pcov))#square root of covariance materix
	optimized=data.frame(
		m=coefs[1],c=coefs[2],
		dm = srpcov[1,1],dc = srpcov[2,2],
		chi.sq.per.DoF= summary(lmobj)$sigma,#chi-squared per DoF
		formula=toFormula(coefs),
		color=color
		)
	return (optimized)
}

c.conv=cbind(c('blue','red'),c('collimated','uncollimated'))#conversion between plot-colors and geometry
#x,2 are the geometry; x,1 are the color

#Generate the dataframes+their optimization results
dfc		=  readVar(  "Col.tsv",  c.conv[1,1])
opt.c	<- lmize(dfc)
dfu = readVar("Uncol.tsv",  c.conv[2,1])
opt.u	<- lmize(dfu)
print(opt.u)
#create the caption
caption = paste('collimated fit : m=',toString(opt.c['c'])," c=",toString(opt.c["m"]))
caption <- paste(caption,"\nuncollimated fit:m=")
caption <- paste(caption,toString(opt.u['c'])," c=",toString(opt.u["m"]))
text = "hello"
DF = rbind(dfc,dfu)
#combined the dataframes, plot
gplotobj<-
	#plot and specify dot size
	ggplot(DF,aes(x=thickness,y=log.dose.rate,color=color))+ geom_point(size = 2)+
	geom_errorbar(aes(ymin = ymin, ymax = ymax))+
	#the names('ymin','ymax') inside the argemnet are shared with ggplot.
	#labelling
	labs(x="thickness(mm)",y='log( dose rate/(1 microSv/hr) )',
		title="Semi-log(y) plot of dose rate")+
	#change the name of colors on the legedn into things
	scale_color_manual(labels = c.conv[,2], values = c.conv[,1]) 
print('reached this point')
gplotobj<-gplotobj+
	geom_abline(data=opt.c,aes(intercept=m,slope=c,color=color))+
	#stat_smooth_func(geom="text",method="lm",hjust=0,parse=TRUE) +
	geom_abline(data=opt.u,aes(intercept=m,slope=c,color=color))+
	labs(caption=toString(opt.c['formula']))
print(opt.c['formula'][1])
#The act of saving is quite simple:)
gplotobj
#gplotobj+geom_abline(data=opt.u,aes(intercept=m,slope=c,color=color))

#plot(dose.rate ~ thickness, data=dfr, ylab="Dose rate(microSv/hr)", xlab="thickness(mm)",col="blue")
	if(F){
		thickness= dat["thickness"]
		y 		 = dat["log.dose.rate"]
		yfit 	 = equation(thickness,coefs[1],coefs[2])
		dy		 = dat["error"]
		resid	<- y-yfit
	}
	if (F){
		equation <- function(x,c,m){
		answer = exp(c)*exp(m*x)
		return (log(answer))
	}
	}