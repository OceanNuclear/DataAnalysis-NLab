#!/usr/bin/Rscript
library(ggplot2)
quadrature <- function(a,b){
	return (sqrt(a^2+b^2))
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
dat = read.table("Calib.txt")
names(dat)<- c('Energy','Channel','Error')
lmobj = lm(Channel~Energy,data = dat,weights = (1/Error^2))