
import numpy as np 
import matplotlib.pyplot as plt

'''
NOTATION
	ep is expected price, p price, qd quantity demanded, qs quantity supplied, t time
	a is the demand curve intercept, b is the demand curve slope, 
	mu is the curvature multiplier in the supply curve,
	la (lambda) is the speed at which price adjusts.
'''

# DEFINE FUNCTIONS
def quantity_demanded(price_t, params):
	a = params['a']
	b = params['b']
	return a - b * price_t

def quantity_supplied(price_t, params):	
	mu = params['mu']
	return np.arctan(mu*price_t)

def expected_price(expected_price_t0, price_t0, params):
	la = params['la']
	return expected_price_t0 + la*(price_t0 - expected_price_t0)

def price(expected_price_t, params):
	a = params['a']
	b = params['b']
	mu = params['mu']
	return (a - np.arctan(mu*expected_price_t))/b


# SET PARAMETERS, INTITIALIZE VARIABLES
params1 = {'a': 1.00, 'b': 0.25, 'mu': 3.0, 'la': 0.3} 	# 1 Solution
params2 = {'a': 0.60, 'b': 0.25, 'mu': 3.0, 'la': 0.3} 	# 2 Solutions (look at bifurcation)
params3 = {'a': 1.00, 'b': 0.25, 'mu': 4.5, 'la': 0.3} 	# 2 Solutions
params4 = {'a': 0.50, 'b': 0.25, 'mu': 4.5, 'la': 0.3} 	# 4 Solutions
params5 = {'a': 0.76, 'b': 0.25, 'mu': 4.5, 'la': 0.3} 	# Chaotic regime

ep_init 		= 500
p_init 			= 80
samples 		= 4 
time 			= np.linspace(1,100,50) # start, end, samples

paramArray 		= []
paramStr 		= []
price_data		= []
quantity_data 	= []

paramArray.append(params1)
paramArray.append(params2)
# paramArray.append(params3)
# paramArray.append(params4)
# paramArray.append(params5)

# Supply and demand curves for reference
qd_line = [[]]
qs_line = [[]]
pe_line = [1.0*x/100.0 for x in range(-300,300) ]

for i in range(len(paramArray)):
	paramStr.append('a = %s, mu = %s, $\lambda$ = %s' %(str(paramArray[i]['a']), str(paramArray[i]['mu']), str(paramArray[i]['la'])))
	price_data.append(np.zeros((samples, len(time))))
	quantity_data.append(np.zeros((samples, len(time))))

	qd_line.append([])
	qd_line.append([])

	# for p in pe_line:
	# 	qs_line[i].append(quantity_supplied(p, paramArray[i]))
	# 	qd_line[i].append(quantity_demanded(p, paramArray[i]))



# RUN MODEL
# Run for each parameter setting
for i in range(len(paramArray)):
	# Run for each sample
	for s in range(samples):
		ep 	= ep_init
		p 	= p_init
		# Run for each time step
		for t in range(len(time)):	
			ep 	= expected_price(ep, p, paramArray[i])
			p 	= price(ep, paramArray[i]) + np.random.randn(1)*0.1
			qs 	= quantity_supplied(p, paramArray[i])
			price_data[i][s][t] = p  + 2*s
			quantity_data[i][s][t] = qs + 2*s 







# PLOT
f, axarr = plt.subplots(len(paramArray), 3)
for i in range(len(paramArray)):
	for s in range(samples):
		axarr[i, 0].plot(time, price_data[i][s]) #,pe_line,qd_line[i],pe_line,qs_line[i])
		axarr[i, 1].plot(time, quantity_data[i][s])	
		axarr[i, 2].plot()
	axarr[i, 0].set_title('Price and Quantity Agaisnt Time, %s' %(str(paramStr[i])))
	axarr[i, 1].set_title('Price Against Quantity, %s' %(str(paramStr[i])))

plt.show()	

