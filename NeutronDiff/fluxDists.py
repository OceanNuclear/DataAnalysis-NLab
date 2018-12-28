#!/home/ocean/anaconda3/bin/python3
from numpy import sqrt,cos, arccos, sin, arctan, tan, pi; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
from HiddenSubprograms import *
from fluxFit import FastFlux,fastFErr, ThmFlux,ThmErr, τ,target_y	#reverse import to know what the data are

#print("fluxDist",__name__)
global expression
global A
A=0.0
def normalize(calculated,data):	#normalize the calculated values to the data
	#print("'normalize' used")
	global A, FastFlux, ThmFlux, fastFErr, ThmErr
	if data == "fast":
		data = FastFlux	#reusing the data variable
		σ = fastFErr
	elif data=="Thm":
		data = ThmFlux
		σ = ThmErr
	else:
		raise ValueError
	if np.shape(calculated)==np.shape(data):
		#A = np.sum(data)/np.sum(calculated)
		A = np.sum(data*calculated/(σ**2))/np.sum(calculated*calculated/(σ**2))
	elif len(calculated)>len(data)*10:#in the case of calculating for smooth value;
		pass #use pre-existing normalization constant(stored globally)
	else:
		print("returning ValueError!!!")
		return ValueError
	return A*(calculated) #don't worry a calculated value does not require the confidence interval
def readA():
	global A
	return A
'''
def sqrt(s):
	assert s>0, "Stop checking for τ= "+str(s)+" ≤0 man!\n need to set a better guess value"
	return np.sqrt(s)
'''
#list of models
#Fast neutron models,
#Square model
def normSquare(xz,L,α,fastThm,text):	#wrapper for one group spherical
	setExpression(text)
	return normalize(Square(xz, L,α),fastThm)
def FastSquare  (xzfast,b,α):	#b should, in theory, approach τ
	text = r"$cos(\frac{pi}{2} \frac{x}{b}) cos(\frac{pi}{2} \frac{y}{b}) exp(-z \sqrt{\frac{\pi^2}{2b^2}+\frac{1}{a}})$"	#a=b, b=α
	return normSquare(xzfast,sqrt(b),α,"fast", text)	#give extra args
def FastSquarex (xzfast,b):	#only care about tau, removing x dependance.
	text = r"$exp(-z \sqrt{(const)-1/a})$"	#a=b which is the neutron age tau
	return normSquare(xzfast,sqrt(b),77,"fast", text)
def FastSquare_τ(xzfast,α  ):	#fixing tau, reducing dependance on z
	text = r"$cos(\frac{pi}{2} \frac{x}{a}) cos(\frac{pi}{2} \frac{y}{a}) exp(-z \sqrt{\frac{\pi^2}{2a^2}+\frac{1}{\tau}}), \tau = 368 cm^2$"	#a=α
	return normSquare(xzfast,sqrt(τ),α,"fast", text)
#Thermal neutron models,

def OneGrp_Thm(xz,L,α) :
	text = r"$cos(\frac{\pi}{2}*x /b) cos(\frac{\pi}{2}*y/b) exp(-z \sqrt{\frac{\pi^2}{2b^2}+\frac{1}{a^2}})$"
	return normSquare(xz,L,α,"Thm",text)
def OneGrp_Thmx(xz,L):	#only care about L
	text = r"$cos(\frac{\pi}{2}*x /const) cos(\frac{\pi}{2}*y/const) exp(-z \sqrt{\frac{\pi^2}{const}+\frac{1}{a^2}})$"	#a=L
	return normSquare(xz,L,77,"Thm",text)
def OneGrp_Thmz(xz,α):	#only care about alpha
	text = r"$cos(\frac{\pi}{2}*x /a) cos(\frac{\pi}{2}*y/a) exp(-z*const)$"	#a=α
	return normSquare(xz,160,α,"Thm",text)
def OneGrp_Thm_Sph(xz,L):
	text = r"$exp(r/a)/r$"+" where "+r"$r=\sqrt{x^2+y^2+z^2}$"
	return normSphere(xz,L,"Thm",text)

def TwoGrp_Thm(xz, L,α):	#Assumes resonance escape probability =1
	flux_orig = Square(xz,L,α)
	#	#Force b = τ in the fast neutron diffusion model.
	Fast = Square(xz,sqrt(τ),α)
	Thermal = (L**2/(L**2-τ)) * (flux_orig-Fast)
	text = r"$\frac{a^2}{a^2-\tau}( cos(\frac{\pi}{2}*x /b) cos(\frac{\pi}{2}*y/b) exp(-z \sqrt{\frac{\pi^2}{2b^2}+\frac{1}{a^2}})$"+"\n"+r"$-cos(\frac{\pi}{2}*x /b) cos(\frac{\pi}{2}*y/b) exp(-z \sqrt{\frac{\pi^2}{2b^2}+\frac{1}{\tau}}) ), \tau = 368 cm^2$"#a=L,b=α
	setExpression(text)
	return normalize(Thermal,"Thm")

def TwoGrp_Thmx(xz, L):	#only care about L
	α=77
	flux_orig = Square(xz,L,α)
	#	#Force b = τ in the fast neutron diffusion model.
	Fast = Square(xz,sqrt(τ),α)
	text = r"$\frac{a^2}{a^2-\tau}( cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{\frac{\pi^2}{2c^2}+\frac{1}{a^2}})$"+"\n"+r"$-cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{\frac{\pi^2}{2c^2}+\frac{1}{\tau}}) ) where c=const, \tau = 368 cm^2$"#a=L
	Thermal = (L**2/(L**2-τ)) * (flux_orig-Fast)
	setExpression(text)	
	return normalize(Thermal,"Thm")
def TwoGrp_Thmz(xz, α):	#only care about α
	L=160
	flux_orig = Square(xz,L,α)
	#Force b = τ in the fast neutron diffusion model.
	Fast = Square(xz,sqrt(τ),α)
	Thermal = (L**2/(L**2-τ)) * (flux_orig-Fast)
	text = r"$\frac{L^2}{L^2-\tau}( cos(\frac{\pi}{2}*x /a) cos(\frac{\pi}{2}*y/a) exp(-z \sqrt{\frac{\pi^2}{2a^2}+\frac{1}{L^2}})$"+"\n"+r"$-cos(\frac{\pi}{2}*x /a) cos(\frac{\pi}{2}*y/a) exp(-z \sqrt{\frac{\pi^2}{2a^2}+\frac{1}{\tau}}) ) where c=const$"#a=α
	setExpression(text)	
	return normalize(Thermal,"Thm")

def OneGrp_ThmNoBD(xz,a,b):
	text = r'$cos(\frac{pi}{2} \frac{x}{a})cos(\frac{pi}{2} \frac{y}{a})exp((\frac{-z}{b}))$'
	setExpression(text)
	[x,z] = xz.T
	Thm = cos(x/a)*np.exp(-z/b)
	return normalize(Thm,"Thm")
def OneGrp_ThmNoBDx(xz,b):
	[x,z] = xz.T
	text = r"$exp(\frac{z}{a})$"
	setExpression(text)
	return normalize(np.exp(-z/b),"Thm")
def OneGrp_ThmNoBDz(xz,a):
	[x,z] = xz.T
	text = r"$cos(\frac{pi}{2} \frac{x}{a})$"
	setExpression(text)
	return normalize(cos(-x/a),"Thm")

def ThirdOrd_OneGrp_Thmz(xz,L,B,α):
	#L is diffusion length,
	#B is the ratio of third order term to 1st order term.
	#α is half the reactor's extended side length
	ord1 = Square(xz,L,α)
	ord3 = Square3(xz,L,α)#Reactor extended length reached at the second zero of cos(\frac{\pi}{2}*x /3)
	#print("wait, RN you're using a simple case of addition; haven't checked if the gamma value will be changed by it or not.")
	text = r"$cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{ 1/a^2+\frac{\pi^2}{2c^2} })$"
	text += '\n'+r"$+b \left( cos(\frac{\pi}{2}*x /3c)cos(\frac{\pi}{2}*y/c)exp(-z \sqrt{ 1/a^2+\frac{5\pi^2}{2c^2} })\right)$"
	text += '\n'+r"$+b \left( cos(\frac{\pi}{2}*x /c)cos(\frac{\pi}{2}*y/3c)exp(-z \sqrt{ 1/a^2+\frac{5\pi^2}{2c^2} })\right)$"
	setExpression(text)
	return normalize((ord1+B*ord3),"Thm")
	#both the 1st order and the 3rd order shares the thing
def ThirdOrd_TwoGrp_Thmz(xz,L,tau,B,α):
	#tau is the fast neutron diffusion length^2 i.e. neutron age
	#Use 3rd order approximation on fast neutron as well then,
	ord1 = Square(xz,L,α)
	ord3 = Square3(xz,L,α)#reactor side length reached.
	Orig = ord1+B*ord3
	ord1 = Square(xz,sqrt(tau),α)
	ord3 = Square3(xz,sqrt(tau),α)#reactor side length reached.
	Fast = ord1+B*ord3
	text = r"$\frac{a^2}{a^2-b} \phi_{corrected}(a,d)-c\phi_{corrected}(\sqrt{b},d)$"+'\n'
	text += "where "+r"$\phi_{corrected}(L,α)=cos(\frac{\pi}{2}*x /α) cos(\frac{\pi}{2}*y/α) exp(-z \sqrt{ 1/L^2+\frac{\pi^2}{2a^2} })$"
	text += '\n'+r"$+b \left( cos(\frac{\pi}{2}*x /3α)cos(\frac{\pi}{2}*y/α)exp(-z \sqrt{ 1/L^2+\frac{5\pi^2}{2a^2} })\right)$"
	text += '\n'+r"$+b \left( cos(\frac{\pi}{2}*x /α)cos(\frac{\pi}{2}*y/3α)exp(-z \sqrt{ 1/L^2+\frac{5\pi^2}{2a^2} })\right)$"
	setExpression(text)
	Thermal = (L*2/(L**2-tau))*(Orig-Fast)
	return normalize(Thermal,"Thm")

def TwoGrp_redefine_τ(xz, L,tau,α):	#Assumes resonance escape probability =1
	flux_orig = Square(xz,L,α)
	Fast = Square(xz,sqrt(tau),α)
	Thermal = (L**2/(L**2-tau)) * (flux_orig-Fast)
	text = r"$\frac{a^2}{a^2-b}( cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{\frac{\pi^2}{2c^2}+\frac{1}{a^2}})$"+"\n"+r"$-cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{\frac{\pi^2}{2c^2}+\frac{1}{b}}) )$"#a=L,b=tau,c=α
	setExpression(text)
	return normalize(Thermal,"Thm")
def TwoGrp_redefine_τx(xz, L,tau):	#ignore α
	α= 77
	flux_orig = Square(xz,L,α)
	Fast = Square(xz,sqrt(tau),α)
	Thermal = (L**2/(L**2-tau)) * (flux_orig-Fast)
	text = r"$\frac{a^2}{a^2-b}( cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{\frac{\pi^2}{2c^2}+\frac{1}{a^2}})$"+"\n"+r"$-cos(\frac{\pi}{2}*x /c) cos(\frac{\pi}{2}*y/c) exp(-z \sqrt{\frac{\pi^2}{2c^2}+\frac{1}{b}}) ) where c=const$"#a=L,b=tau
	setExpression(text)
	return normalize(Thermal,"Thm")
def TwoGrp_redefine_τz(xz, α): #only care about α
	#is just the same as the scaling x
	text = r"$\frac{L^2}{L^2-\tau} (exp(-z \sqrt{\frac{\pi^2}{2a^2}+\frac{1}{L^2}})-exp(-z \sqrt{\frac{\pi^2}{2a^2}+\frac{1}{\tau}}) ) cos(\frac{\pi}{2}*x /a) cos(\frac{\pi}{2}*y/a)$"#a=α
	return normSquare(xz,160,α,"Thm",text)	#can use a normalized square since we only care about a single slice of constant z.
def GreensFuncFast(xz,a,tau,c):
	text = r"$\sum_{m,n,p=1}^{16}\frac{cos(\frac{m \pi x} {2a}) sin(\frac{p \pi z} {2c})sin(\frac{p \pi \epsilon} {2c}) } {[\frac{m^2+n^2}{a^2}+\frac{p^2}{c^2}+\frac{1}{b \pi^2}]}$"
	setFixedyExpression(text)
	[x,z]=ary(xz).T
	maxm=40+1
	epsilon = 20.25
	z = z+epsilon
	Sum = 0
	for m in range (1,maxm,2):
		for n in range (1,maxm,2):
			for p in range (1,maxm):
				Sum+= cos(m*pi*x/a/2)*sin(p*pi*z/c/2)*sin(p*pi*epsilon/c/2)/( (m/a)**2+(n/a/.9210)**2+(p/c)**2+(1/tau)  )
				#Sum+= sin(m*pi*(x+a)/a/2)*sin(n*pi*(target_y+a)/a/2)*sin(p*pi*z/c/2)*sin(p*pi*epsilon/c/2)*sin(m*pi*a/2/a)*sin(n*pi*a/2/a)/( (m/a)**2+(n/a/.9210)**2+(p/c)**2+(1/tau)  )
	z +=-epsilon
	return normalize(Sum,"fast")

def GreensFunc(xz,a,tau,c,L):
	text = r"$\sum_{m,n,p=1}^{32}\frac{cos(\frac{m \pi x} {2a}) sin(\frac{p \pi z} {2c})sin(\frac{p \pi \epsilon} {2c}) } {[\frac{m^2+n^2}{a^2}+\frac{p^2}{c^2}+\frac{1}{b \pi^2}][\frac{m^2+n^2}{a^2}+\frac{p^2}{c^2}+\frac{1}{d^2 \pi^2}]}$"
	setFixedyExpression(text)
	[x,z]=ary(xz).T
	maxm=32+1
	epsilon = 20.25
	z = z+epsilon
	Sum = 0
	for m in range (1,maxm,2):
		for n in range (1,maxm,2):
			for p in range (1,maxm):
				Sum+= cos(m*pi*x/a/2)*sin(p*pi*z/c/2)*sin(p*pi*epsilon/c/2)/(( (m/a)**2+(n/a/.9210)**2+(p/c)**2+(1/tau) )*( (m/a)**2+(n/a/.9210)**2+(p/c)**2+(1/L**2)  ))
																							#b=.9210*a
	z +=-epsilon
	return normalize(Sum,"Thm")

def FixL(xz,B):#for investigating higher order correction
	L = sqrt(3500)
	α = 76.8
	text = r'$cos(\frac{\pi}{2}*x /α) cos(\frac{\pi}{2}*y/α) exp(-z \sqrt{ 1/L^2+\frac{\pi^2}{2a^2} })$'
	text += '\n'+r"$+a \left( cos(\frac{\pi}{2}*x /3α)cos(\frac{\pi}{2}*y/α)exp(-z \sqrt{ 1/L^2+\frac{5\pi^2}{2a^2} })\right)$"
	text += '\n'+r"$+a \left( cos(\frac{\pi}{2}*x /α)cos(\frac{\pi}{2}*y/3α)exp(-z \sqrt{ 1/L^2+\frac{5\pi^2}{2a^2} })\right)$"
	text += "\nwhere "+r'$L^2$'+"=3500, α=76.8"
	setExpression(text)
	return normalize(higherOrd(xz,L,α,B),"Thm")
def FixLtau(xz,B):
	L = sqrt(3500)
	τ = 368
	α = 76.8
	text = r'$\frac{L^2}{L^2-τ} \phi_{corrected}(L=\sqrt{3500},α,a)-\phi_{corrected}(\sqrt{τ}=\sqrt{368},α,a)$'+'\n'
	text += "where "+r"$\phi_{corrected}(L,α,a)=cos(\frac{\pi}{2}*x /α) cos(\frac{\pi}{2}*y/α) exp(-z \sqrt{ 1/L^2+\frac{\pi^2}{2a^2} })$"
	text += '\n'+r"$+a \left( cos(\frac{\pi}{2}*x /3α)cos(\frac{\pi}{2}*y/α)exp(-z \sqrt{ 1/L^2+\frac{5\pi^2}{2a^2} })\right)$"
	text += '\n'+r"$+a \left( cos(\frac{\pi}{2}*x /α)cos(\frac{\pi}{2}*y/3α)exp(-z \sqrt{ 1/L^2+\frac{5\pi^2}{2a^2} })\right)$, α=76.8"
	setExpression(text)
	return normalize((L**2/(L**2-τ) )*(higherOrd(xz,L,α,B)-higherOrd(xz,sqrt(τ),α,B)),"Thm" )
def higherOrd(xz,L,α,B):	#up to the first cos(3x) and cos(3y) terms.
	[x,z] = xz.T
	def expon(num):
		return np.exp(-z*sqrt(1/L**2 + pi**2/4*num/(α**2)) )
	return cos(pi/2*x/α)*( expon(2)+B*expon(10) ) + B*cos(pi/2*x/(3*α))*expon(10)
#Spherical models
def normSphere(xz,L,fastThm,text):	#wrapper for one group spherical
	setExpression(text)
	return normalize(Spherical(xz,L,target_y),fastThm)
def FastSph  (xzfast,b):	#b should, in theory, approach τ
	text = rShortHand()
	return normSphere(xzfast,sqrt(b),"fast",text)
def FastSph_τ(xzfast  ):	#fixing tau
	text = rShortHand(tau=True)
	return normSphere(xzfast,sqrt(τ),"fast",text)
#For setting and getting the expression
def setExpression(text):
	global expression
	expression = r"$\phi(x,y,z) \propto$"
	expression += text
	return
def setFixedyExpression(text):
	global expression
	expression = r"$\phi(x,y=0,z) \propto$"
	expression += text
	return
def get_expression():
	return expression

'''
#Dump this here:
if False:	#this makes the labels readable. the purpose of the "if" is to indent for readability only.
	labels = [ fs(item.get_text()) for item in ax.get_xticklabels()]
	ax.set_xticklabels(labels)
	labels = [ fs(item.get_text()) for item in ax.get_yticklabels()]
	ax.set_yticklabels(labels)
'''