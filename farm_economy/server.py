import os.path
import json
import pkgutil

import farm_economy
import farm_economy.swi as swi

pkg = 'farm_economy'

graph_script_template = '''
var chart_%(name)s;
nv.addGraph(function() {
    chart_%(name)s = nv.models.lineChart()
                   .useInteractiveGuideline(true)
                   .options({
                       margin: {left: 100, bottom: 40},
                       showXAxis: true,
                       showYAxis: true,
                       transitionDuration: 250
                   })

    chart_%(name)s.xAxis     //Chart x-axis settings
              .axisLabel('%(xlabel)s')
              .tickFormat(d3.format(',.2f'));
    chart_%(name)s.yAxis
              .axisLabel('%(ylabel)s')
              .tickFormat(d3.format(',.2f'));
    %(extra)s

    return chart_%(name)s;
});
'''

class Server(swi.SimpleWebInterface):
    def swi_static(self, *path):
        if self.user is None: return
        fn = os.path.join('static', *path)
        if fn.endswith('.js'):
            mimetype = 'text/javascript'
        elif fn.endswith('.css'):
            mimetype = 'text/css'
        elif fn.endswith('.png'):
            mimetype = 'image/png'
        elif fn.endswith('.jpg'):
            mimetype = 'image/jpg'
        elif fn.endswith('.gif'):
            mimetype = 'image/gif'
        elif fn.endswith('.otf'):
            mimetype = 'font/font'
        else:
            raise Exception('unknown extenstion for %s' % fn)

        data = pkgutil.get_data(pkg, fn)
        return (mimetype, data)

    def swi(self):
        return self.swi_run('ExampleButton')

    def swi_run(self, model):
        m = getattr(farm_economy.models, model)()

        html = pkgutil.get_data(pkg, 'templates/run.html')

        sliders = m.html_sliders()
        slider_keys = m.params.keys()

        buttons = [
            ('Varieties', 'VarietiesButton'),
            ('Marketing/Certification ExampleButton1', 'ExampleButton'),
            ('Example with demand', 'ExampleButton2'),
            ('Processing', 'ProcessingButton'),
            ('ExampleButton2', 'ExampleButton2'),
            ('ExampleButton3', 'ExampleButton3'),
            ]
        button_bar = []
        for text, cls in buttons:
            button_bar.append('<li%s><a href="/run?model=%s">%s</a></li>' %
                                (' class="active"' if cls == model else '',
                                 cls, text))

        if isinstance(m.title, list):
            titles = m.title[1:]
            title = m.title[0]
            xlabel = m.xlabel[0]
            ylabel = m.ylabel[0]
            xlabels = m.xlabel[1:]
            ylabels = m.ylabel[1:]
        else:
            titles = None
            title = m.title
            xlabel = m.xlabel
            ylabel = m.ylabel

        graph_area = '''<div class="row" id="main_area">
        <div class="col-md-6" id="large_chart_area"></div>
            <h3>%s</h3>
            <div id="chart_main" class='with-3d-shadow with-transitions'>
                <svg style="height: 300px;"></svg>
            </div>
        </div>''' % title

        graph_script = graph_script_template % dict(name='main',
                xlabel=xlabel,ylabel=ylabel, extra='')

        if titles is not None and len(titles) > 0:
            graph_area += '<div class="row">'
            graph_script += 'var chart_extra = [%s];' % ','.join(['%d' % i for i in range(len(titles))])
            for i,t in enumerate(titles):
                graph_area += '''<div class="col-md-6" id="scenario_area%d">
                    <h3>%s</h3>
                    <div id="extra-plt%d">
                        <svg style="height: 200px"></svg>
                    </div>
                </div>''' % (i, t, i)
                graph_script += graph_script_template % dict(name='extra%d' % i,
                    xlabel=xlabels[i],ylabel=ylabels[i],
                    extra='chart_extra[%d] = chart_extra%d;' % (i, i))
            graph_area += '</div>'





        return html % dict(sliders=sliders, model_name=m.name,
                           model_class=model,
                           xlabel=m.xlabel, ylabel=m.ylabel,
                           slider_keys=slider_keys,
                           desc=m.desc,
                           button_bar=''.join(button_bar),
                           graph_area=graph_area,
                           graph_script=graph_script)

    def swi_run_json(self, model, count=1, **params):
        if count == 'undefined':
            count = 1
        count = int(count)
        p = {}
        for k, v in params.items():
            if k.startswith('key_'):
                p[k[4:]] = float(v)

        model = getattr(farm_economy.models, model)()

        r = model.run(seed=1, **p)
        data = model.plot_nvd3(r[0])
        extra_plots = [model.plot_nvd3(rr) for rr in r[1:]]

        for i in range(count-1):
            r = model.run(seed=2 + i, **p)
            d = model.plot_nvd3(r[0])
            for line in d:
                line['key'] = 'dummy_%s_%s' % (line['key'], i)
                data.append(line)
            for j, rr in enumerate(r[1:]):
                e = model.plot_nvd3(rr)
                for line in e:
                    line['key'] = 'dummy_%s_%s' % (line['key'], i)
                    extra_plots[j].append(line)

        return json.dumps(dict(main=data, extra_plots=extra_plots, count=count))


