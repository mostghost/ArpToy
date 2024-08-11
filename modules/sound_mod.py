import PyQt5.QtCore as qtc
import PyQt5.QtMultimedia as qtm
import random as rand
from data.globals import NOTES


class soundObject:

    dict_sounds = {}

    def setup_sounds(self, instrument):
        self.dict_sounds.clear()
        for i in range(1, 5):
            for n in NOTES:
                note = f"{n}{i}"
                self.dict_sounds[note] = qtm.QSoundEffect()
                self.dict_sounds[note].setSource(
                    qtc.QUrl.fromLocalFile(f"sound/{instrument}/{note}.wav")
                )

    def play_notes(self, note_cascade):
        print(note_cascade)

        for nc in note_cascade:
            qtc.QTimer.singleShot(
                rand.randint(10, 30), lambda note=nc: self.dict_sounds[note].play()
            )

    def play_note_arp(self, note, gate):
        self.dict_sounds[note].play()
        print(gate)
        qtc.QTimer.singleShot(gate, lambda g=gate, n=note: print(f'stopping {n} after {g}'))
        # qtc.QTimer.singleShot(gate, lambda n=note: self.dict_sounds[n].stop())
