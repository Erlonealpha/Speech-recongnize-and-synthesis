import dashscope
from json import load
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
from dashscope.audio.tts import ResultCallback, SpeechSynthesizer, SpeechSynthesisResult

from os.path import join as _join
from datetime import datetime

api_key = load(open('env.json', 'r')).get('dashscope-api-key')
dashscope.api_key = api_key

class Callback(ResultCallback):
    def __init__(self, callback, path=None, folder=None):
        super().__init__()
        if folder is None: folder = ""
        self._callback = callback
        self.data = b''
        self.p = _join(folder, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav") if path is None else path
        self.time_stamps = []
        
    def on_open(self):
        print('Speech synthesizer is opened.')

    def on_complete(self):
        with open(self.p, 'wb') as f:
            f.write(self.data)
        print(f'Audio file is saved at {self.p}')
        self._callback(self.p, self.time_stamps)

    def on_error(self, response: SpeechSynthesisResponse):
        print('Speech synthesizer failed, response is %s' % (str(response)))

    def on_close(self):
        print('Speech synthesizer is closed.')

    def on_event(self, result: SpeechSynthesisResult):
        if result.get_audio_frame() is not None:
            self.data += result.get_audio_frame()

        if result.get_timestamp() is not None:
            time_stamp = result.get_timestamp()
            self.time_stamps.append(time_stamp)


class SpeechSynth:
    @staticmethod
    def call(text, callback, sample_rate=48000, model='sambert-zhiwei-v1'):
        '''
        callback parame: path:str, time_stamps:list'''
        callback = Callback(callback)
        SpeechSynthesizer.call(model=model,
                               text=text,
                               sample_rate=sample_rate,
                               callback=callback,
                               word_timestamp_enabled=True,
                               phoneme_timestamp_enabled=True)