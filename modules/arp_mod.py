import PyQt5.QtCore as qtc
from data.globals import INDEX_NOTES, NOTES_INDEX


class arpObject(qtc.QThread):

    signal_note = qtc.pyqtSignal(str, int)

    current_cascade = []
    last_note = None
    new_note = None
    toggle_repeat = False
    toggle_hat = False
    toggle_flip = False

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
            self.start_time = qtc.QTime.currentTime()

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

            self.last_note = self.new_note
            self.new_note = self.next_note()

            if self.new_note:
                self.mod_and_play_note(self.new_note, beats, n_type, n_mod)
            else:
                self.last_note = None

            elapsed = self.start_time.msecsTo(qtc.QTime.currentTime())
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

    def get_cascade(self):
        flattened_cascade = set(
            [element for sublist in self.playing.values() for element in sublist]
        )
        return list(flattened_cascade)

    def next_note(self):
        self.current_cascade = self.get_cascade()
        if len(self.current_cascade) == 0:
            return None

        pattern = self.common["pattern"]

        match pattern:
            case "Up":
                next_note = self.pattern_linear()
            case "Down":
                next_note = self.pattern_linear(reverse=True)
            case "Up/Down":
                next_note = self.pattern_updown()
            case "2x U/D":
                next_note = self.pattern_doubleud()

        return next_note

    def sort_linear(self, rev=False):
        self.current_cascade = sorted(
            self.current_cascade, key=lambda x: NOTES_INDEX[x], reverse=rev
        )

    def get_current(self):
        index = self.current_cascade.index(self.last_note) + 1
        if (index) >= len(self.current_cascade):
            return self.current_cascade[0]
        else:
            return self.current_cascade[index]

    def verify_last(self):
        if self.last_note is None:
            self.last_note = self.current_cascade[0]
        elif self.last_note not in self.current_cascade:
            # We'll take our best guess to sort out which note to use
            index_current = {NOTES_INDEX[note]: note for note in self.current_cascade}
            index_last = NOTES_INDEX[self.last_note]
            closest_index = min(index_current.keys(), key=lambda x: abs(x - index_last))
            self.last_note = INDEX_NOTES[closest_index]

    def pattern_linear(self, reverse=False):
        self.sort_linear(rev=reverse)
        self.verify_last()

        current = self.get_current()
        return current

    def pattern_updown(self):
        if self.toggle_flip:
            self.sort_linear(rev=True)
        else:
            self.sort_linear()

        self.verify_last()
        if self.last_note == self.current_cascade[-2]:
            # The last note was the note before the end, so this note is the last
            self.toggle_flip = not self.toggle_flip

        current = self.get_current()
        return current

    def pattern_doubleud(self):

        if self.toggle_repeat:
            self.toggle_repeat = False
            return self.last_note

        if self.toggle_flip:
            self.sort_linear(rev=True)
        else:
            self.sort_linear()

        self.verify_last()
        if self.last_note == self.current_cascade[-2]:
            # The last note was the note before the end, so this note is the last
            self.toggle_flip = not self.toggle_flip
            self.toggle_repeat = True

        current = self.get_current()
        return current

    def mod_and_play_note(self, note, beats, n_type, n_mod):
        gate_orig = self.gates[self.step_last].value()
        gate_percent = gate_orig * 0.01

        pitch_index = self.pitch[self.step_last].value()

        elapsed = self.start_time.msecsTo(qtc.QTime.currentTime())
        gate = int((((60000 / beats) * n_type) * n_mod) - elapsed)

        index = NOTES_INDEX[note]
        try:
            pitch = INDEX_NOTES[index + pitch_index]
        except KeyError:
            pitch = INDEX_NOTES[index]

        gate = int((gate * gate_percent) * 0.9)

        self.signal_note.emit(pitch, gate)
