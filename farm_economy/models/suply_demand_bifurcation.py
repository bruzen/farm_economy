import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import odeint

# INTERVENTIONS
# New varieties
# Storage and shipping
# Value added processing
# Marketing/education
# Organics
# Trade

# POSSIBLE INSIGHTS
# Some don't have much impact (marketing and education?)
# Need a few (e.g. marketing at the right time to support processing)
# Local market loyalty helps
# Insight into when the system is vunerable to labour or fuel price changes, or public good pricing changes.
# Understand the nature of overshoot.

# Weather variability
# Waste %
# Shelf life
# Delay For New Growth


# INTERVENTIONS
# New varieties
# Price of new variety (parameterize curve)
# Yeild of new variety (parameterize curve)

# Storage and shipping
# Value added processing
# Marketing/education
# Organics
# Trade







# DEFINE PARAMETERS
# la = 0.3  # Curvature/multiplier of supply curve
# b  = 0.25 # Slope of demand curve
# mu = 4.5#3.0  # Mutlipier for response time?
# a = #[-1,1,0.01] # Demand intercept - vary for bifurcation

#params = {'la': 0.3, 'b': 0.25, 'mu': 3.0}
params = {'la': 0.3, 'b': 0.25, 'mu': 3.0}

# DEFINE FUNCTIONS
def expected_price(p_e0, a, params):
	la = params["la"]
	b  = params["b"]
	mu = params["mu"]
	return (1-la)*p_e0 + la*a/b - la * np.arctan(mu * p_e0) / b

# MAIN CODE
x0 = 0.01
samplingStartTime = 1000
sampleNumber = 100

resultA = []
resultX = []

a = 0.0 #00.5 #-1
da = 0.005

while a <= 1:
    x = x0
    for t in xrange(samplingStartTime):
        x = expected_price(x, a, params)
    for t in xrange(sampleNumber):
        x = expected_price(x, a, params)
        resultA.append(a)
        resultX.append(x)
    a += da

plt.plot(resultA, resultX, '.')
plt.title("Bifurcation Diagram for Supply Demand Model")
plt.xlabel("a")
plt.ylabel("$x^*$ equlibrium solutions")	
plt.show()
