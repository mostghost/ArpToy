import PyQt5.QtCore as qtc

class MutexDict:
    def __init__(self):
        self.dict = {}
        self.mutex = qtc.QMutex()

    def __setitem__(self, key, value):
        self.mutex.lock()
        self.dict[key] = value
        self.mutex.unlock()

    def __getitem__(self, key):
        self.mutex.lock()
        value = self.dict.get(key)
        self.mutex.unlock()
        return value
