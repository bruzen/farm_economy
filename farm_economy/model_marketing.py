import farm_game.model

# control how many farms there are
farm_game.model.Model.farm_width = 3
farm_game.model.Model.farm_height = 3
farm_game.model.Model.farm_count = (farm_game.model.Model.farm_width *
                                    farm_game.model.Model.farm_height)

from gbm.models.core import Line


# make a function that will run the model and return graphs
#  the seed parameter sets the seed for the model
#  the other parameters will eventually be sliders
#  the output is plots to show
def model_marketing(seed, certification_percent, organic_price):

    # turn the sliders into interventions of the same form as in farm_game/actions.py
    interventions = [
        'subsidy:certification,%f' % certification_percent,
        'sd:peachesOrganicRedhaven,%f,0,0' % organic_price,
        'sd:peachesOrganicBabyGold,%f,0,0' % organic_price,
        ]

    code = 'init;' + ';'.join(interventions)

    steps = 10   # number of steps to run the simulation for

    # run the simulation
    data = farm_game.model.run(seed, code, *(['none'] * steps))

    # extract plot information from all the data returned from the model
    plot1 = [
        Line(x=range(steps+2), y=data['prod_peachesRedhaven'], color='red', label='Redhaven'),
        Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'], color='pink', label='Redhaven Organic'),
        ]

    return [plot1]


# just for testing purposes, plot the results
def show_plot(plots):
    import pylab
    for i, plot in enumerate(plots):
        pylab.subplot(i+1, 1, len(plots))
        for line in plot:
            pylab.plot(line.x, line.y, color=line.color, label=line.label,
                       linewidth=3)
        pylab.legend(loc='best')
    pylab.show()


if __name__ == '__main__':
    # run the simulation with a particular slider value and seed
    plots = model_marketing(seed=1, certification_percent=0, organic_price=10)
    show_plot(plots)






