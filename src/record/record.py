from pyaudio import PyAudio, paInt16
import wave
import threading
from os.path import exists as _exists, join as _join, dirname as _dirname
from os import makedirs as _makedirs

class Record:
    def __init__(self, chunk=1024, format=paInt16, channels=1, rate=44100):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        
        self.is_recording = False

    def start(self, save_path):
        if self.is_recording:
            return
        self.save_path = save_path
        if not _exists(_dirname(self.save_path)):
            _makedirs(_dirname(self.save_path))
        self.audio = PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        self.record_thread = threading.Thread(target=self.record, daemon=True)
        self.record_thread.start()
        self.is_recording = True
    
    def stop(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.record_thread.join()
    
    def record(self):
        with wave.open(self.save_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            while self.is_recording:
                data = self.stream.read(self.chunk)
                wf.writeframes(data)

if __name__ == '__main__':
    record = Record()
    record.start('output.wav')
    input('Press Enter to stop recording...')
    record.stop()
    
    