from aip import AipSpeech
from threading import Thread

class AipSpeechRecognition:
    def __init__(self, app_id, api_key, secret_key):
        self.client = AipSpeech(app_id, api_key, secret_key)
        self.is_running = False
        self.callback = None
    
    def asr(self, audio_file, callback):
        if self.is_running:
            return
        self.callback = callback
        self.thr = Thread(target=self.wait_for_result, args=(audio_file, ))
        self.thr.start()
        self.is_running = True
    
    def wait_for_result(self, audio_file):
        with open(audio_file, 'rb') as fp:
            audio_data = fp.read()
            result = self.client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
            if result['err_no']!= 0:
                self.callback("识别失败，请重新录制")
            else:
                text = result['result'][0]
                self.callback(text)
            self.is_running = False