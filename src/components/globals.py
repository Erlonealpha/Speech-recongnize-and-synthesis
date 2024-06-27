from json import load


class Globals_:
    def __init__(self):
        with open('config/config.json', 'r') as f:
            self.config = load(f)
        
        self.rec_models = self.config.get('recongnizer', {}) \
            .get('models', {})
        self.synth_models = self.config.get('synthesizer', {}) \
            .get('models', {})

Globals = Globals_()