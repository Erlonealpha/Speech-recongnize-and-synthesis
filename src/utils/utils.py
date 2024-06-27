from queue import Queue
from threading import Thread
from PySide6.QtCore import QThread, Signal
from time import sleep

def call_delay(delay, func, *args, **kwargs):
    """
    Call a function after a delay.
    if want get return value
    this fun may return a Queue to get result
    """
    def wrap(queue):
        sleep(delay)
        res = func(*args, **kwargs)
        queue.put(res)
    queue = Queue()
    thr = Thread(target=wrap, args=(queue,))
    thr.start()
    return queue

class TimerThread(QThread):
    def __init__(self, delay, callback, queue: Queue, *args, parent=None, **kwargs):
        super().__init__(parent)
        self.queue = queue
        self.delay = delay
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        QThread.sleep(self.delay)
        res = self.callback(*self.args, **self.kwargs)
        self.queue.put(res)

def qcall_delay(delay, callback, *args, **kwargs):
    queue = Queue()
    qthr = TimerThread(delay, callback, queue, *args, **kwargs)
    qthr.start()
    return queue
