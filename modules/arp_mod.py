import PyQt5.QtCore as qtc


class arpObject(qtc.QThread):

    update_signal = qtc.pyqtSignal(bool)

    def __init__(self, led, pitch, gates, common, playing):
        self.led = led
        self.pitch = pitch
        self.gates = gates
        self.common = common
        self.playing = playing
        self.step_current = 0
        self.step_last = 0
        self.arpeggiate = False
        super().__init__()

    def run(self):
        while self.arpeggiate:
            start_time = qtc.QTime.currentTime()
            beats = self.common["bpm"]
            max_steps = self.common["steps"] - 1
            n_type = self.common["n_type"]
            n_mod = self.common["n_mod"]

            self.led[self.step_last].setChecked(False)
            self.led[self.step_current].setChecked(True)

            self.step_last = self.step_current

            if self.step_current < max_steps:
                self.step_current += 1
            else:
                self.step_current = 0

            print(self.get_sorted_cascade())

            elapsed = start_time.msecsTo(qtc.QTime.currentTime())
            qtc.QThread.msleep(
                max(0, int((((60000 / beats) * n_type) * n_mod) - elapsed))
            )

    def toggle(self):
        self.go = not self.go

    def power_off(self):
        self.arpeggiate = False
        for index in self.led.keys():
            self.led[index].setChecked(False)

    def power_on(self):
        self.step_current = 0
        self.step_last = 0
        self.arpeggiate = True
        self.start()

    def get_sorted_cascade(self):
        flattened_cascade = set([
            element for sublist in self.playing.values() for element in sublist
        ])
        return flattened_cascade
