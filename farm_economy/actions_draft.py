# THE BUTTONS

class VarietiesButton(InterventionButton):
    desc = '''VarietiesButton text. Here is some <em>html</em> that describes the model.
    This will be displayed on the web page. When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$'''

    def __init__(self):
        super(VarietiesButton, self).__init__(name='Varieties',
                xlabel=['time', 'time', 'time', 'something else'], ylabel=['amount produced', 'test_data', 'test2', 'test3'],
                desc=self.desc, title=['Varieties graph', 'test_data', 'another_test_graph', 'one_more'])
        self.add(Parameter('cert', 0, min=0, max=100,
                           desc='Var. certification subsidy (%)'))
        self.add(Parameter('org', 6.5, min=0, max=20,
                           desc='Var.price of organics'))
        self.add(Parameter('qua', 5.5, min=0, max=20,
                           desc='Try to add quality intervention' ))
        self.add(Parameter('pri', 4.5, min=0, max=20,
                           desc='Try to add price slider' ))
        self.add(Parameter('loc', 3.5, min=0, max=20,
                           desc='Try to add local slider' ))

    def generate_data(self, seed, p):
        # turn the sliders into interventions of the same form
        # as in farm_game/actions.py
        interventions = [
            'subsidy:certification,%f' % p.cert,
            'sd:peachesOrganicRedhaven,%f,0,0' % p.org,
            'sd:peachesOrganicBabyGold,%f,0,0' % p.org,
            'price:peachesOrganicRedhaven*%f' %p.pri,
            'quality: %f,1.0,3.0,2.0' %p.qua,
            'local: 5.0,%f,10.0' %p.qua,
            ]

        code = 'init;' + ';'.join(interventions)

        steps = 9   # number of steps to run the simulation for

        # run the simulation
        data = farm_game.model.run(seed, code, *(['none'] * steps))

        # extract plot information from all the data returned from the model
        plotVar1 = [
            Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
                 color='red', label='Redhaven'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
                 color='pink', label='Redhaven Organic'),
            ]

        plotVar2 = [
            Line(x=range(steps+2), y=-np.array(data['test_data']),
                 color='green', label='test data'),
            ]

        plotVar3 = [
            Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
                 color='red', label='Redhaven'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
                 color='pink', label='Redhaven Organic'),
            ]

        plotVar4 = [
            Line(x=range(steps+2), y=-np.array(data['prod_nitrogen']),
                 color='green', label='nitrogen'),
            ]            

        return [plotVar1, plotVar2, plotVar3, plotVar4]


class ExampleButton(InterventionButton):
    desc = '''Ex1 Text. Here is some <em>html</em> that describes the model.
    This will be displayed on the web page.'''

    def __init__(self):
        super(ExampleButton, self).__init__(name='Example',
                xlabel=['time', 'time'], ylabel=['amount produced', 'nitrogen'],
                desc=self.desc, title=['Example graph', 'Nitrogen'])
        self.add(Parameter('cert', 0, min=0, max=100,
                           desc='certification subsidy (%)'))
        self.add(Parameter('org', 6.5, min=0, max=20,
                           desc='price of organics'))

    def generate_data(self, seed, p):
        # turn the sliders into interventions of the same form
        # as in farm_game/actions.py
        interventions = [
            'subsidy:certification,%f' % p.cert,
            'sd:peachesOrganicRedhaven,%f,0,0' % p.org,
            'sd:peachesOrganicBabyGold,%f,0,0' % p.org,
            ]

        code = 'init;' + ';'.join(interventions)

        steps = 9   # number of steps to run the simulation for

        # run the simulation
        data = farm_game.model.run(seed, code, *(['none'] * steps))

        # extract plot information from all the data returned from the model
        plot1 = [
            Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
                 color='red', label='Redhaven'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
                 color='pink', label='Redhaven Organic'),
            ]

        plot2 = [
            Line(x=range(steps+2), y=-np.array(data['prod_nitrogen']),
                 color='green', label='nitrogen'),
            ]

        return [plot1, plot2]

class ExampleButton2(InterventionButton):
    desc = '''Here is a more complex example with a controllable supply/
    demeand curve.'''

    def __init__(self):
        super(ExampleButton2, self).__init__(name='Example',
                xlabel=['time', 'amount produced'],
                ylabel=['amount produced', 'price ($)'],
                desc=self.desc, title=['Example graph',
                                       'Supply / Demand curve for organics'])
        self.add(Parameter('cert', 0, min=0, max=100,
                           desc='certification subsidy (%)'))
        self.add(Parameter('p_max', 5, min=0, max=20,
                           desc='Maximum Price'))
        self.add(Parameter('p_min', 0, min=0, max=20,
                           desc='Minimum Price'))
        self.add(Parameter('slope', 0, min=0, max=100,
                           desc='Price reduction', decimals=2))
        self.add(Parameter('quantity', 50, min=0, max=100,
                           desc='Quantity'))

    def generate_data(self, seed, p):
        # demand curve was calibrated for 49 farms, so we need to adjust it
        # to fit the number of farms in this simulation
        slope = p.slope * 49 / farm_game.model.Model.farm_count

        # turn the sliders into interventions of the same form
        # as in farm_game/actions.py
        interventions = [
            'subsidy:certification,%f' % p.cert,
            'sd:peachesOrganicRedhaven,%f,%f,%f' % (p.p_max, p.p_min, slope),
            'sd:peachesOrganicBabyGold,%f,%f,%f' % (p.p_max, p.p_min, slope),
            ]

        code = 'init;' + ';'.join(interventions)

        steps = 9   # number of steps to run the simulation for

        # run the simulation
        data = farm_game.model.run(seed, code, *(['none'] * steps))

        # extract plot information from all the data returned from the model
        plot1 = [
            Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
                 color='red', label='Redhaven'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
                 color='pink', label='Redhaven Organic'),
            Line(x=range(steps+2), y=data['prod_peachesBabyGold'],
                 color='yellow', label='BabyGold'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicBabyGold'],
                 color='gold', label='BabyGold Organic'),
            ]

        # now generate the plot data for the supply/demand curve
        steps = 200
        qq = np.linspace(0, 100, steps)

        price = -slope * p.p_max * 0.001 * qq + p.p_max
        price = np.maximum(price, p.p_min)

        target_price = -slope * p.p_max * 0.001 * p.quantity + p.p_max
        target_price = np.maximum(target_price, p.p_min)

        plot2 = [
            Line(qq, price, color='green', label='demand'),
            Line([0, p.quantity], [target_price, target_price], color='blue', label='price'),
            Line([p.quantity, p.quantity], [0, target_price], color='red', label='quantity'),
            ]

        return [plot1, plot2]



#
# TO DO
#
# Maybe put caps in the text in the overbars
# Tell Terry just sending the line/time series is fine - I can just manage special cases by setting the max/min using parameters/no?
# Tell Terry how beautiful the code is
#
# ON WEB
# Get force layout d3 example (and still version)
# Get example where sliders give imediate input
# Get examples where hoving over a line shows the distribution in data..


# Interactive maps (satelite data)
# Dangerous because making making it pretty easier does not make the thnking or math easier.. easy to be wrong
# You can buy tools (mathematica) we have done it all from scratch using open source.. lots use the browser, some math is much better done on a server, then you have all the details around deployment..
# D3 examples online you can download and play with. The returns from learning code are higher than ever, and the barriers are lower.. an actual decline in the cheating tools as it becomes basic litteracy.. but the tools are still very good and getting better.


#
# TALK OUTLINE
#
# List interventions, what controls entry, what controls exit,..
# 


'''
Farme economy

Market power.. cert and marketing (and a cost)
Storage/shipping..
Processing - entering another market...
Varities (value added, each small, vs change the season..)
-- could be either..
Policy/trade (.. change the price of inputs.... change the quantity of imports), change the quantity of exports 
--- VALUE ADDED BUT WITH A LARGE QUANTITY....
'''
# SHOW THE BASIC MATH
# ADD EQUATIONS
# SHOW SCENARIOS 
# Choose which is main one from a set (tick box to set parameter - for which slider line to send )
# ADD TIME
# COMPETITION - OTHER FRUIT
# INTERVENTIONS
# What might each do (maybe with scenarios)






#
# DRAFT BUTTONS
#

class BasicEconomyButton(InterventionButton):
    desc = '''Here is a more complex example with a controllable supply/
    demeand curve.'''

    def __init__(self):
        super(BasicEconomyButton, self).__init__(name='Example',
                xlabel=['time', 'amount produced'],
                ylabel=['amount produced', 'price ($)'],
                desc=self.desc, title=['Example graph',
                                       'Supply / Demand curve for organics'])
        self.add(Parameter('cert', 0, min=0, max=100,
                           desc='certification subsidy (%)'))
        self.add(Parameter('p_max', 5, min=0, max=20,
                           desc='Maximum Price'))
        self.add(Parameter('p_min', 0, min=0, max=20,
                           desc='Minimum Price'))
        self.add(Parameter('slope', 0, min=0, max=100,
                           desc='Price reduction', decimals=2))
        self.add(Parameter('quantity', 50, min=0, max=100,
                           desc='Quantity'))

    def generate_data(self, seed, p):
        # demand curve was calibrated for 49 farms, so we need to adjust it
        # to fit the number of farms in this simulation
        slope = p.slope * 49 / farm_game.model.Model.farm_count

        # turn the sliders into interventions of the same form
        # as in farm_game/actions.py
        interventions = [
            'subsidy:certification,%f' % p.cert,
            'sd:peachesOrganicRedhaven,%f,%f,%f' % (p.p_max, p.p_min, slope),
            'sd:peachesOrganicBabyGold,%f,%f,%f' % (p.p_max, p.p_min, slope),
            ]

        code = 'init;' + ';'.join(interventions)

        steps = 9   # number of steps to run the simulation for

        # run the simulation
        data = farm_game.model.run(seed, code, *(['none'] * steps))

        # extract plot information from all the data returned from the model
        plot1 = [
            Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
                 color='red', label='Redhaven'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
                 color='pink', label='Redhaven Organic'),
            Line(x=range(steps+2), y=data['prod_peachesBabyGold'],
                 color='yellow', label='BabyGold'),
            Line(x=range(steps+2), y=data['prod_peachesOrganicBabyGold'],
                 color='gold', label='BabyGold Organic'),
            ]

        # now generate the plot data for the supply/demand curve
        steps = 200
        qq = np.linspace(0, 100, steps)

        price = -slope * p.p_max * 0.001 * qq + p.p_max
        price = np.maximum(price, p.p_min)

        target_price = -slope * p.p_max * 0.001 * p.quantity + p.p_max
        target_price = np.maximum(target_price, p.p_min)

        plot2 = [
            Line(qq, price, color='green', label='demand'),
            Line([0, p.quantity], [target_price, target_price], color='blue', label='price'),
            Line([p.quantity, p.quantity], [0, target_price], color='red', label='quantity'),
            ]

        return [plot1, plot2]
