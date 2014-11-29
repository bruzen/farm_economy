import farm_game.model

farm_game.model.Model.farm_width = 3
farm_game.model.Model.farm_height = 3
farm_game.model.Model.farm_count = (farm_game.model.Model.farm_width *
                                    farm_game.model.Model.farm_height)

from gbm.models.core import Line


def model_marketing(seed, certification_percent, organic_price):
    interventions = [
        'subsidy:certification,%f' % certification_percent,
        'sd:peachesOrganicRedhaven,%f,0,0' % organic_price,
        'sd:peachesOrganicBabyGold,%f,0,0' % organic_price,
        ]

    code = 'init;' + ';'.join(interventions)

    steps = 10

    data = farm_game.model.run(seed, code, *(['none'] * steps))

    plot1 = [
        Line(x=range(steps+2), y=data['prod_peachesRedhaven'], color='red', label='Redhaven'),
        Line(x=range(steps+2), y=data['prod_peachesOrganicRedhaven'], color='pink', label='Redhaven Organic'),
        ]

    return [plot1]



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
    plots = model_marketing(seed=1, certification_percent=0, organic_price=10)

    show_plot(plots)






