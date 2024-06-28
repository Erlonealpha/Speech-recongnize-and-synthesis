from json import load


class Globals_:
    def __init__(self):
        with open('config/config.json', 'r', encoding='utf-8') as f:
            self.config = load(f)
        
        self.rec_models = self.config.get('recongnizer', {}) \
            .get('models', {})
        self.synth_models = self.config.get('synthesizer', {}) \
            .get('models', {})
        
        self.rec_module_dic = {
            "ali-dashscope": "ali_dashscope",
            "baidu-aip": "aip"
        }
        self.synth_module_dic = {
            
        }

Globals = Globals_()