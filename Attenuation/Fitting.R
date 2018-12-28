library("lattice")
fileName = "Ionization_Collimated.tsv"
df <- read.table(fileName, header=TRUE, sep="\t")
#File read.

Dose = sigma = thickness = c()
#created empty array for the 
for (dfn in df)
	{Dose <- c(Dose,mean(unlist(dfn)))
	sigma<- c(sigma, sd(unlist(dfn)))}#already takes into account Bessel's correction
for (nth in colnames(df)) {thickness = c(thickness,substring(nth,2))}	#cut the col name short so that they don't have the x in front.
thickness = as.numeric(thickness)
#Data handling finished

log.err = sigma/Dose
obj <- lm(log(Dose)~thickness,weights=1/(log.err)**2)
print(summary(obj))
