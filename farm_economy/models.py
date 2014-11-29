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
            pylab.subplot(i+1, 1, len(plots))
            for line in plot:
                pylab.plot(line.x, line.y, color=line.color, label=line.label,
                           linewidth=3)
            pylab.legend(loc='best')
        pylab.show()
    def run(self, seed, **params):
        p = ParamSet(self.params, params)
        r = self.generate_data(seed, p)

        return r



class ExampleButton(InterventionButton):
    desc = '''Here is some <em>html</em> that describes the model.
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


if __name__ == '__main__':
    b = ExampleButton()
    plots = b.run(seed=1, cert=100, org=7)
    b.multiplot_pylab(plots)
