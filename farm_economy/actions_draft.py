
# I'm going to go through and work more on this. This is just where I am now, 
# and it has one example of each of the kidns of things we'd need

class Varieties(InterventionButton):
	# Curve for new variety
	# Slider for labour cost
	# Slider for other costs

	# Curve for new variety
	# Slider for labour cost
	# Slider for other costs


	super(Varieties, self).__init__(name='New Variety',
                                    ylabel='Price ($)',
                                    xlabel='Quantity (MM 18lb masters)')
    self.add(Parameter('p_max', 5, min=0, max=20,
                       desc='Maximum Price'))
    self.add(Parameter('p_min', 0, min=0, max=20,
                       desc='Minimum Price'))
    self.add(Parameter('slope', 0, min=0, max=100,
                       desc='Price reduction', decimals=2))
    self.add(Parameter('quantity', 50, min=0, max=100,
                       desc='Quantity'))




class Marketing(InterventionButton)
	# Premium paid for local fruit (%1-20, default 5%)
	# Cost farmers pay for marketing/education (% 1-20, default 3% of $18/master price)
	# Additional premium paid for local organic fruit (%0-100, default 30%)	
	# Change in labour price for organic production (-20%-+100%, 10%)
	# On/Off. Subsidy for certification period (get organic prices right away)	

...