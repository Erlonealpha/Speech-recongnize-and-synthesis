from .aip import AipSpeechRecognition
from .dashscope import SpeechSynth
from components.globals import Globals


class SpeechRecognition:
    def __init__(self):
        ...
    
    @staticmethod
    def asr(file_path, api_name, callback):
        match api_name:
            case 'baidu-aip':
                return aip_asr(file_path, callback)
            case 'ali-dashscope':
                return ali_dashscope_asr(file_path, callback)
    @staticmethod
    def asr_stream(api_name, callback):
        match api_name:
            case 'ali-dashscope':
                return ali_dashscope_asr_stream(callback)

    @staticmethod
    def tts(text, api_name, model_name, callback, folder):
        match api_name:
            case 'ali-dashscope':
                return ali_dashscope_synth(text, callback, folder, model_name)
            
def aip_asr(file_path, callback):
    info = Globals.rec_models.get('baidu-aip')
    aip = AipSpeechRecognition(info.get('app_id'), info.get('api_key'), info.get('secret_key'))
    aip.asr(file_path, callback)
def ali_dashscope_asr(file_path, callback):
    ...

def ali_dashscope_asr_stream(callback):
    ...

def ali_dashscope_synth(text, callback, folder, model_name):
    SpeechSynth.call(text, callback, model = model_name, folder=folder)