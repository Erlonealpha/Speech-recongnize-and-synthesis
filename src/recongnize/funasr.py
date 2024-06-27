import soundfile
import os
from numpy import frombuffer, int16
from pyaudio import PyAudio, paInt16
from threading import Thread
from queue import Queue

from funasr import AutoModel