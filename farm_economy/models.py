from gbm.models.core import GraphBasedModel, Parameter, Line, ParamSet

import farm_game.model
# control how many farms there are
farm_game.model.Model.farm_width = 3
farm_game.model.Model.farm_height = 3
farm_game.model.Model.farm_count = (farm_game.model.Model.farm_width *
                                    farm_game.model.Model.farm_height)


import numpy as np

class InterventionButton(GraphBasedModel):
    def __init__(self, name, xlabel, ylabel, desc, title):
        super(InterventionButton, self).__init__(name=name, xlabel=xlabel,
            ylabel=ylabel)
        self.desc = desc
        self.title = title
    def multiplot_pylab(self, plots):
        import pylab
        for i, plot in enumerate(plots):
            pylab.subplot(len(plots), 1, i + 1)
            for line in plot:
                pylab.plot(line.x, line.y, color=line.color, label=line.label,
                           linewidth=3)
            pylab.legend(loc='best')
        pylab.show()
    def run(self, seed, **params):
        p = ParamSet(self.params, params)
        r = self.generate_data(seed, p)

        return r


class MarketingButton(InterventionButton):
    desc = '''<h3>Farm Economy</h3>

            What is the effect of changing sliders? What in this graph could each intervention change? What would be the effect?
            <br> <br>
            <ul>
            <li> <strong>Cold storage: </strong> 
            quality (bruising, ripeness), 
            waste, 
            managing supply. 

            <li> <strong> Value-Added Processing: </strong> 
            managing supply,  
            new products,  
            new markets. </li>

            <li> <strong>Approvals process: </strong>
            new products, 
            managing supply
            marketing ON Fruit 
            food knowledge 
            competition from imports

            <li> <strong> Educating Youth on Fruit </strong>: 
            food knowledge.  
            
            <li> <strong> Post-harvest handling: </strong> </li>
            costs of production (labour, scale of industry), 
            managing supply. 

            <li> <strong> Tax incentives for innovation: </strong></li>
            production costs (labor),
            new products, 
            quality (bruising, ripeness), 
            waste. </li>
            </ul>


    '''

    def __init__(self):
        super(MarketingButton, self).__init__(name='Economy',
                xlabel=['Quantity', 'Time', 'Time'], #, 'amount produced'],
                ylabel=['Price', '$', 'Quantity'], # 'price ($)'],
                desc=self.desc, title=['Supply and Demand','Revenue','Market Share'])
        self.add(Parameter('d', 0.33, min=0.01, max=1.5,
                           desc='Market power of local (d)'))
        self.add(Parameter('pe', 15, min=0.01, max=30,
                           desc='Mean expected import price ($/18lb unit)'))
        self.add(Parameter('plocal', 17, min=0.01, max=30,
                           desc='Price chosen by the marketing board ($/18lb unit'))
        self.add(Parameter('a', 30, min=20, max=50,
                           desc='Choke price, $/18lb unit (a)'))
        self.add(Parameter('b', 8, min=15, max=1000,
                           desc='Steepness of demand curve (b)'))        
        self.add(Parameter('ga', 1, min=0.01, max=5,
                           desc='Curve  '))        

    def generate_data(self, seed, p):
        # # TODO: Fix so it is the right slope the actually use..
        # # demand curve was calibrated for 49 farms, so we need to adjust it
        # # to fit the number of farms in this simulation
        # slope = p.b * 49 / farm_game.model.Model.farm_count

        # # turn the sliders into interventions of the same form
        # # as in farm_game/actions.py
        # interventions = [
        #     'subsidy:certification,%f' % p.cert,
        #     'sd:peachesOrganicRedhaven,%f,%f,%f' % (p.p_max, p.p_min, slope),
        #     'sd:peachesOrganicBabyGold,%f,%f,%f' % (p.p_max, p.p_min, slope),
        #     ]

        # code = 'init;' + ';'.join(interventions)

        # steps = 9   # number of steps to run the simulation for

        # # run the simulation
        # data = farm_game.model.run(seed, code, *(['none'] * steps))

        # # extract plot information from all the data returned from the model
        # plot1 = [
        #     Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
        #          color='red', label='Redhaven'),
        #     Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
        #          color='pink', label='Redhaven Organic'),
        #     Line(x=range(steps+2), y=data['prod_peachesBabyGold'],
        #          color='yellow', label='BabyGold'),
        #     Line(x=range(steps+2), y=data['prod_peachesOrganicBabyGold'],
        #          color='gold', label='BabyGold Organic'),
        #     ]

        # now generate the plot data for the supply/demand curve
        steps = 200
        qq = np.linspace(0, 2.0, steps)

        pe_line = [p.pe for i in range(0,steps)]


        pe_plt = p.pe*np.ones(steps)

        demand_basic = p.a - p.b * qq
        
        demand_local = p.pe + p.d * (p.a-p.pe)*qq

        d_intercept = p.pe + p.d*(p.a - p.pe)


        # Main Quantities:



        # p_imports = p.pe 
        # q_imports = (p.a - p.pe)/p.b
        # import_market_size = p_imports * q_imports

        # a_local = p.d*(p.a - p.pe) + p.pe       # ok
        # b_local = p.d*(p.a - p.pe)/q_imports    # ok
        
        # p_local = p.plocal
        # q_local = (a_local + p.plocal)/p.b # (p.a - p.plocal)/p.b

        # local_pq_intercept = np.abs((p.pe - a_local)/(b_local)) # NOPE!
        #local_pq_intercept = np.abs((d_intercept - p.plocal)/b_local)


        # plot1 = [
        #     Line([0, p.a/p.b], [p.a,0], color='gray', label='Overall Demand Curve for Peaches'),
        #     Line([0,(p.a - p.pe)/p.b], [p.pe, p.pe], color='blue', label='Import Price'),
        #     Line([q_imports,q_imports], [0, p.pe], color='blue',label=''),
        #     Line([0,(p.a - p.pe)/p.b], [d_intercept, p.pe], color='red', label='Local Demand'),
        #     #Line([0,local_pq_intercept], [p.plocal, p.plocal], color='green', label='Marketing Board\'s Price'),
        #     Line([(p.a - p.plocal)/p.b,(p.a - p.plocal)/p.b], [0, p.plocal], color='gray', label=''),
        #     # Line([0,0], [0, 35], color='gray', label=''),
        #     # Line([0,5], [0, 0], color='gray', label=''),
        #     ]

        # Backup sliders
        plot1 = [
            Line([0, p.a/p.b], [p.a,0], color='gray', label='Overall Demand Curve for Peaches'),
            Line([0,(p.a - p.pe)/p.b], [p.pe, p.pe], color='blue', label='Expected California Price'),
            Line([(p.a - p.pe)/p.b,(p.a - p.pe)/p.b], [0, p.pe], color='blue',label=''),
            Line([0,(p.a - p.pe)/p.b], [d_intercept, p.pe], color='red', label='Conditional Local Demand'),
            Line([0,(p.a - p.plocal)/p.b], [p.plocal, p.plocal], color='green', label='Marketing Board\'s Price'),
            Line([(p.a - p.plocal)/p.b,(p.a - p.plocal)/p.b], [0, p.plocal], color='gray', label=''),
        ]    

        # Local volume, local quantity, local revenue
        # Import volume, import revenue, 

        # TODO FIX
        # plot1 = plot2

        plot_revenue = [
            Line([0, p.a/p.b], [p.a,0], color='gray', label='Overall Demand Curve'),
        ]

        # Plot quantities as a share/%
        plot_quantities = [
            Line([0, p.a/p.b], [p.a,0], color='gray', label='Overall Demand Curve'),
        ]

        return [plot1, plot_revenue, plot_quantities] #, plot2]


class CertificationButton(InterventionButton):
    desc = '''What is the market for Ontario peaches? What is the effect of changing sliders?'''

    def __init__(self):
        super(CertificationButton, self).__init__(name='Economy',
                xlabel=['Time', 'amount produced'],
                ylabel=['Quantity', 'price ($)'],
                desc=self.desc, title=['A Supply Demand Curve'])
        self.add(Parameter('a', 30, min=0.01, max=50,
                           desc='Choke price, $/18lb unit (a)'))
        self.add(Parameter('b', 8, min=0.01, max=1000,
                           desc='Slope of demand curve (b)'))
        self.add(Parameter('d', 0.33, min=0.01, max=1.5,
                           desc='Market power of local (d)'))
        self.add(Parameter('ga', 1, min=0.01, max=5,
                           desc='Competition (gamma)'))
        self.add(Parameter('pe', 15, min=0.01, max=30,
                           desc='Mean expected import price, $/18lb unit (pe)'))
        self.add(Parameter('plocal', 17, min=0.01, max=30,
                           desc='Price chosen by the marketing board, $/18lb unit (pe)'))

    def generate_data(self, seed, p):
        # # TODO: Fix so it is the right slope the actually use..
        # # demand curve was calibrated for 49 farms, so we need to adjust it
        # # to fit the number of farms in this simulation
        # slope = p.b * 49 / farm_game.model.Model.farm_count

        # # turn the sliders into interventions of the same form
        # # as in farm_game/actions.py
        # interventions = [
        #     'subsidy:certification,%f' % p.cert,
        #     'sd:peachesOrganicRedhaven,%f,%f,%f' % (p.p_max, p.p_min, slope),
        #     'sd:peachesOrganicBabyGold,%f,%f,%f' % (p.p_max, p.p_min, slope),
        #     ]

        # code = 'init;' + ';'.join(interventions)

        # steps = 9   # number of steps to run the simulation for

        # # run the simulation
        # data = farm_game.model.run(seed, code, *(['none'] * steps))

        # # extract plot information from all the data returned from the model
        # plot1 = [
        #     Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
        #          color='red', label='Redhaven'),
        #     Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
        #          color='pink', label='Redhaven Organic'),
        #     Line(x=range(steps+2), y=data['prod_peachesBabyGold'],
        #          color='yellow', label='BabyGold'),
        #     Line(x=range(steps+2), y=data['prod_peachesOrganicBabyGold'],
        #          color='gold', label='BabyGold Organic'),
        #     ]

        # now generate the plot data for the supply/demand curve
        steps = 200
        qq = np.linspace(0, 2.0, steps)

        pe_line = [p.pe for i in range(0,steps)]


        pe_plt = p.pe*np.ones(steps)

        demand_basic = p.a - p.b * qq
        
        demand_local = p.pe + p.d * (p.a-p.pe)*qq

        d_intercept = p.pe + p.d*(p.a - p.pe)

        plot1 = [
            Line([0, p.a/p.b], [p.a,0], color='gray', label='Overall Demand Curve'),
            Line([0,(p.a - p.pe)/p.b], [p.pe, p.pe], color='blue', label='Expected California Price'),
            Line([(p.a - p.pe)/p.b,(p.a - p.pe)/p.b], [0, p.pe], color='blue',label=''),
            Line([0,(p.a - p.pe)/p.b], [d_intercept, p.pe], color='red', label='Local Demand Curve'),
            Line([0,(p.a - p.plocal)/p.b], [p.plocal, p.plocal], color='green', label='Marketing Board\'s Price'),
            Line([(p.a - p.plocal)/p.b,(p.a - p.plocal)/p.b], [0, p.plocal], color='gray', label=''),
            ]

        # TODO FIX
        # plot1 = plot2





        return [plot1] #, plot2]


class VarietiesButton(InterventionButton):
    desc = '''Revising. Here is a more complex example with a controllable supply/
    demeand curve.'''

    def __init__(self):
        super(VarietiesButton, self).__init__(name='Example',
                xlabel=['time', 'amount produced'],
                ylabel=['amount produced', 'price ($)'],
                desc=self.desc, title=['Example graph','Supply / Demand curve for organics'])
        self.add(Parameter('a', 30, min=0.01, max=50,
                           desc='Choke price, $/18lb unit (a)'))
        self.add(Parameter('b', 8, min=0.01, max=1000,
                           desc='Slope of demand curve (b)'))
        self.add(Parameter('d', 0.33, min=0.01, max=1.5,
                           desc='Market power of local (d)'))
        self.add(Parameter('ga', 1, min=0.01, max=5,
                           desc='Competition (gamma)'))
        self.add(Parameter('pe', 15, min=0.01, max=30,
                           desc='Mean expected import price, $/18lb unit (pe)'))
        self.add(Parameter('plocal', 17, min=0.01, max=30,
                           desc='Price chosen by the marketing board, $/18lb unit (pe)'))

    def generate_data(self, seed, p):
        # # TODO: Fix so it is the right slope the actually use..
        # # demand curve was calibrated for 49 farms, so we need to adjust it
        # # to fit the number of farms in this simulation
        # slope = p.b * 49 / farm_game.model.Model.farm_count

        # # turn the sliders into interventions of the same form
        # # as in farm_game/actions.py
        # interventions = [
        #     'subsidy:certification,%f' % p.cert,
        #     'sd:peachesOrganicRedhaven,%f,%f,%f' % (p.p_max, p.p_min, slope),
        #     'sd:peachesOrganicBabyGold,%f,%f,%f' % (p.p_max, p.p_min, slope),
        #     ]

        # code = 'init;' + ';'.join(interventions)

        # steps = 9   # number of steps to run the simulation for

        # # run the simulation
        # data = farm_game.model.run(seed, code, *(['none'] * steps))

        # # extract plot information from all the data returned from the model
        # plot1 = [
        #     Line(x=range(steps+2), y=data['prod_peachesRedhaven'],
        #          color='red', label='Redhaven'),
        #     Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'],
        #          color='pink', label='Redhaven Organic'),
        #     Line(x=range(steps+2), y=data['prod_peachesBabyGold'],
        #          color='yellow', label='BabyGold'),
        #     Line(x=range(steps+2), y=data['prod_peachesOrganicBabyGold'],
        #          color='gold', label='BabyGold Organic'),
        #     ]

        # now generate the plot data for the supply/demand curve
        steps = 200
        qq = np.linspace(0, 2.0, steps)

        pe_line = [p.pe for i in range(0,steps)]


        pe_plt = p.pe*np.ones(steps)

        demand_basic = p.a - p.b * qq
        
        demand_local = p.pe + p.d * (p.a-p.pe)*qq

        d_intercept = p.pe + p.d*(p.a - p.pe)

        plot2 = [
            Line([0, p.a/p.b], [p.a,0], color='gray', label='Demand'),
            Line([0,(p.a - p.pe)/p.b], [p.pe, p.pe], color='blue', label='Expected California Price'),
            Line([(p.a - p.pe)/p.b,(p.a - p.pe)/p.b], [0, p.pe], color='blue',label='Q Just California'),
            Line([0,(p.a - p.pe)/p.b], [d_intercept, p.pe], color='red', label='Local Demand'),
            Line([0,(p.a - p.plocal)/p.b], [p.plocal, p.plocal], color='red', label='Marketing Board Chooses'),
            Line([(p.a - p.plocal)/p.b,(p.a - p.plocal)/p.b], [0, p.plocal], color='gray', label='Q Local'),
            ]

        # TODO FIX
        plot1 = plot2





        return [plot1, plot2]

class CertificationButton2(InterventionButton):
    desc = '''Revising. Here is a more complex example with a controllable supply/
    demeand curve.'''

    def __init__(self):
        super(CertificationButton2, self).__init__(name='Example',
                xlabel=['time', 'amount produced'],
                ylabel=['amount produced', 'price ($)'],
                desc=self.desc, title=['Example graph',
                                       'Supply / Demand curve for organics'])
        self.add(Parameter('cert', 0, min=0, max=100,
                           desc='Certification subsidy (%)'))
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

class OtherButton(InterventionButton):
    desc = ''' ''' # VarietiesButton text. Here is some <em>html</em> that describes the model.
    #This will be displayed on the web page. When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
    #$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$'''

    def __init__(self):
        super(OtherButton, self).__init__(name='Varieties',
                xlabel=['time', 'time', 'time'], ylabel=['amount produced', 'test_data', 'test2'],
                desc=self.desc, title=['Varieties graph', 'Inputs', 'Nitrogen'])
        self.add(Parameter('cert', 0, min=0, max=100,
                           desc='Var. certification subsidy (%)'))
        self.add(Parameter('org', 6.5, min=0, max=20,
                           desc='Var.price of organics'))
        self.add(Parameter('qua', 5.5, min=0, max=20,
                           desc='Quality intervention' ))
        self.add(Parameter('pri', 4.5, min=0, max=20,
                           desc='Price slider' ))
        self.add(Parameter('loc', 3.5, min=0, max=20,
                           desc='Local slider' ))

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

        return [plotVar1, plotVar2, plotVar4]




if __name__ == '__main__':
    b = ExampleButton2()
    plots = b.run(seed=1, cert=100)
    b.multiplot_pylab(plots)
