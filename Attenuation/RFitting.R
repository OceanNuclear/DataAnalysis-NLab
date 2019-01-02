#!/usr/bin/Rscript
library(ggplot2)
quadrature <- function(a,b){
	return (sqrt(a^2+b^2))
}

#Record background
bg = c(0.7,0.3,0.4)#changes these records
#print((sd(bg))^2)
#print(mean(bg))
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
toFormula<- function(coefs,srpcov,chi.squared){
	#You'd think for a language specialzing in plotting, I don't have to write my own code just to add numbers onto the graph...	
	text <-paste(     "m=", toString(signif(coefs[2],3)))
	text <-paste(text,"±" , toString(signif(srpcov[2,2],3)))
	text <-paste(text,",c=",toString(signif(coefs[1],3)))
	text <-paste(text,"±" , toString(signif(srpcov[1,1],3)))
	text <-paste(text,", chi squared per DoF = ",toString(signif(chi.squared,3)))
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
		m=coefs[2],c=coefs[1],
		dm = srpcov[2,2],dc = srpcov[1,1],
		chi.sq.per.DoF= summary(lmobj)$sigma,#chi-squared per DoF
		formula=toFormula(coefs,srpcov,summary(lmobj)$sigma),
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

DF = rbind(dfc,dfu)#combine the data frames
#create the caption
caption="fit equation = m*x + c, i.e. ignoring build-up factor"
caption=paste(caption, '\noptimized using the method of least squares.')
caption=paste(caption, '\ncollimated:')
caption=paste(caption, toString(unlist(opt.c['formula'])))
caption=paste(caption, '\nuncollimated:')
caption=paste(caption, toString(unlist(opt.u['formula'])))

#plotting...
gplotobj<-
	#plot and specify dot size
	ggplot(DF,aes(x=thickness,y=log.dose.rate,color=color))+ geom_point(size = 2)+
	geom_errorbar(aes(ymin = ymin, ymax = ymax))+
	#the names('ymin','ymax') inside the argemnet are shared with ggplot.
	#labelling
	labs(x="thickness(mm)",y='log( dose rate/(1 microSv/hr) )',
		title="Semi-log(y) plot of dose rate")+
	#change the name of colors on the legend into proper names
	scale_color_manual(labels = c.conv[,2], values = c.conv[,1]) 
gplotobj<-gplotobj+
	geom_abline(data=opt.c,aes(intercept=c,slope=m,color=color))+
	#stat_smooth_func(geom="text",method="lm",hjust=0,parse=TRUE) +
	geom_abline(data=opt.u,aes(intercept=c,slope=m,color=color))+
	labs(caption=caption)
gplotobj #The command for saving is incredibly simple:)
