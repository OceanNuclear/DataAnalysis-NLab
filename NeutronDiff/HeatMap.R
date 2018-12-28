library("lattice")

df <- read.csv("PulseHeight-V_app.csv", header=TRUE, sep="\t", col.names=(c("V_app","Min","Max","error")))
print(df)
