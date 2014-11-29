import os.path
import json
import pkgutil

import farm_economy
import farm_economy.swi as swi

pkg = 'farm_economy'

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

        return html % dict(sliders=sliders, model_name=m.name,
                           model_class=model,
                           xlabel=m.xlabel, ylabel=m.ylabel,
                           slider_keys=slider_keys,
                           desc=m.desc)

    def swi_run_json(self, model, **params):
        p = {}
        for k, v in params.items():
            if k.startswith('key_'):
                p[k[4:]] = float(v)

        model = getattr(farm_economy.models, model)()

        r = model.run(seed=1, **p)
        data = model.plot_nvd3(r[0])

        return json.dumps(dict(main=data))


