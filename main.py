import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtMultimedia as qtm

from data.globals import NOTES_INDEX, INDEX_NOTES, NOTES, CHORDS
from widgets.led import ledIndicator
from widgets.keyslide import keySlide
from modules.sound_mod import soundObject
from modules.arp_mod import arpObject

import sys
import json


class MainWindow(qtw.QWidget):

    shared_LED = {}
    shared_PITCH = {}
    shared_GATES = {}
    shared_COMMON = {}
    shared_PLAYING = {}

    dict_keyboard = {}

    soundscape = soundObject()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arp Toy")

        self.setMinimumSize(1000, 750)

        self.setup_panel_ui()

        self.octave = 2
        self.setup_key_btns()
        self.setup_keyboard()
        self.soundscape.setup_sounds("piano")

        self.change_steps(8)

        self.connect_panel()

        self.lst_n_type.setCurrentIndex(2)

        self.arpstepper = arpObject(
            self.shared_LED,
            self.shared_PITCH,
            self.shared_GATES,
            self.shared_COMMON,
            self.shared_PLAYING
        )

    def setup_panel_ui(self):
        lo_master = qtw.QVBoxLayout()
        struct_frame = qtw.QFrame()
        struct_north_holder = qtw.QWidget()
        struct_north = qtw.QWidget()
        struct_keyboard = qtw.QWidget()
        struct_northwest_panel = qtw.QWidget()
        struct_arp_holder = qtw.QFrame()
        struct_arp_steps = qtw.QWidget()
        struct_step_controls = qtw.QWidget()
        struct_panel_holder = qtw.QWidget()

        struct_frame.setObjectName("LShapeFrame")
        struct_arp_holder.setObjectName("LeftI")

        lo_frame = qtw.QHBoxLayout()
        lo_north = qtw.QHBoxLayout()
        lo_panel_holder = qtw.QVBoxLayout()
        lo_north_holder = qtw.QVBoxLayout()
        self.lo_keyboard = qtw.QGridLayout()
        lo_panel = qtw.QVBoxLayout()
        lo_arp_holder = qtw.QVBoxLayout()
        lo_arp_steps = qtw.QGridLayout()
        lo_arp_controls = qtw.QHBoxLayout()

        self.setLayout(lo_master)
        struct_north.setLayout(lo_north)
        struct_north_holder.setLayout(lo_north_holder)
        struct_keyboard.setLayout(self.lo_keyboard)
        struct_frame.setLayout(lo_frame)
        struct_northwest_panel.setLayout(lo_panel)
        struct_panel_holder.setLayout(lo_panel_holder)
        struct_arp_holder.setLayout(lo_arp_holder)
        struct_step_controls.setLayout(lo_arp_controls)
        struct_arp_steps.setLayout(lo_arp_steps)

        north_spacer = qtw.QSpacerItem(
            20, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding
        )

        lo_north_holder.addSpacerItem(north_spacer)
        lo_frame.addWidget(struct_north_holder)
        lo_master.addWidget(struct_frame)
        lo_master.addWidget(struct_keyboard)
        lo_arp_holder.addWidget(struct_step_controls)
        lo_arp_holder.addWidget(struct_arp_steps)
        lo_north.addWidget(struct_panel_holder, stretch=2)
        lo_north.addWidget(struct_arp_holder, stretch=4)
        lo_north_holder.addWidget(struct_north)

        # Top left - Panel

        struct_bpm_frame = qtw.QFrame()
        struct_bpm_frame.setObjectName("FullFrame")
        lo_bpm_frame = qtw.QVBoxLayout()
        struct_bpm_frame.setLayout(lo_bpm_frame)

        lbl_bpm = qtw.QLabel("BPM")
        lo_bpm_frame.addWidget(lbl_bpm)
        self.spn_bpm = qtw.QSpinBox(maximum=260, minimum=40, value=110)
        lo_bpm_frame.addWidget(self.spn_bpm)
        self.spn_bpm.valueChanged.connect(self.change_bpm)
        self.btn_tap = qtw.QPushButton("Tap Tempo")
        lo_bpm_frame.addWidget(self.btn_tap)

        lo_panel_holder.addWidget(struct_bpm_frame)

        self.lst_instrument = qtw.QComboBox()
        lo_panel.addWidget(self.lst_instrument)
        self.lst_chord = qtw.QComboBox()
        lo_panel.addWidget(self.lst_chord)
        self.lst_control_type = qtw.QComboBox()
        lo_panel.addWidget(self.lst_control_type)
        self.lst_control_type.currentTextChanged.connect(self.change_key_control)

        struct_oct_btns = qtw.QWidget()
        lo_oct_btns = qtw.QHBoxLayout()
        struct_oct_btns.setLayout(lo_oct_btns)
        self.btn_oct_down = qtw.QPushButton("Octave -")
        lo_oct_btns.addWidget(self.btn_oct_down)
        self.btn_oct_up = qtw.QPushButton("Octave +")
        lo_oct_btns.addWidget(self.btn_oct_up)
        lo_panel.addWidget(struct_oct_btns)

        lo_panel_holder.addWidget(struct_northwest_panel)

        # Top right - ARP

        for i in range(16):
            self.shared_LED[i] = ledIndicator()
            lo_arp_steps.addWidget(self.shared_LED[i], 2, i, 1, 1)
            self.shared_LED[i].clicked.connect(
                lambda _, led=self.shared_LED[i]: self.temp_toggleState(led)
            )

        for i in range(16):
            self.shared_PITCH[i] = qtw.QSlider(maximum=6, minimum=-6, value=0)
            self.shared_PITCH[i].setObjectName("CustomSlider")
            self.shared_PITCH[i].setOrientation(qtc.Qt.Horizontal)
            lo_arp_steps.addWidget(self.shared_PITCH[i], 3, i, 1, 1)
            self.shared_PITCH[i].sliderReleased.connect(
                lambda pitch=self.shared_PITCH[i]: print(pitch.value())
            )

        for i in range(16):
            self.shared_GATES[i] = qtw.QSlider(maximum=100, minimum=0, value=100)
            self.shared_GATES[i].setObjectName("CustomSlider")
            lo_arp_steps.addWidget(
                self.shared_GATES[i], 4, i, 1, 1, alignment=qtc.Qt.AlignCenter
            )

        self.btn_arp_enable = qtw.QPushButton("Arp Off", checkable=True)
        lo_arp_controls.addWidget(self.btn_arp_enable)
        self.btn_arp_enable.clicked.connect(self.toggle_arp)

        self.btn_latch = qtw.QPushButton("Latch", checkable=True)
        lo_arp_controls.addWidget(self.btn_latch)

        self.lst_presets = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_presets)

        self.lst_pattern = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_pattern)

        self.lst_n_type = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_n_type)
        self.lst_n_type.currentIndexChanged.connect(self.change_note_speed)

        self.lst_n_mod = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_n_mod)
        self.lst_n_mod.currentIndexChanged.connect(self.change_note_modifier)

        self.spn_steps = qtw.QSpinBox(prefix="Steps: ", maximum=16, minimum=4, value=8)
        lo_arp_controls.addWidget(self.spn_steps)
        self.spn_steps.valueChanged.connect(self.change_steps)

    def setup_key_btns(self):
        self.dict_keyboard.clear()

        for i in range(1, 6):
            for n in NOTES:
                note = f"{n}{i}"
                self.dict_keyboard[note] = keySlide(note.replace("s", "#")[:-1])
                self.dict_keyboard[note].setSizePolicy(
                    qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Expanding
                )
                if "s" in note:
                    self.dict_keyboard[note].setObjectName("PianoSharp")
                else:
                    self.dict_keyboard[note].setObjectName("PianoKey")

                self.dict_keyboard[note].pressed.connect(
                    lambda note=note: self.press_key(note)
                )

                self.dict_keyboard[note].released.connect(
                    lambda note=note: self.release_key(note)
                )

                self.dict_keyboard[note].setCheckable(True)

    def setup_keyboard(self):
        oct = self.octave
        self.lo_keyboard.addWidget(self.dict_keyboard[f"C{oct}"], 1, 0, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Cs{oct}"], 0, 1, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"D{oct}"], 1, 2, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Ds{oct}"], 0, 3, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"E{oct}"], 1, 4, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"F{oct}"], 1, 6, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Fs{oct}"], 0, 7, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"G{oct}"], 1, 8, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Gs{oct}"], 0, 9, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"A{oct}"], 1, 10, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"As{oct}"], 0, 11, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"B{oct}"], 1, 12, 1, 2)

        self.lo_keyboard.addWidget(self.dict_keyboard[f"C{oct+1}"], 1, 14, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Cs{oct+1}"], 0, 15, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"D{oct+1}"], 1, 16, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Ds{oct+1}"], 0, 17, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"E{oct+1}"], 1, 18, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"F{oct+1}"], 1, 20, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Fs{oct+1}"], 0, 21, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"G{oct+1}"], 1, 22, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"Gs{oct+1}"], 0, 23, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"A{oct+1}"], 1, 24, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"As{oct+1}"], 0, 25, 1, 2)
        self.lo_keyboard.addWidget(self.dict_keyboard[f"B{oct+1}"], 1, 26, 1, 2)

        # We'll just fill out the extra spots with invisible buttons
        # to make sure it all aligns.
        empty_buttons = {}
        for i in range(3):
            empty_buttons[i] = qtw.QPushButton("Z#")
            empty_buttons[i].setObjectName("Invisible")

        self.lo_keyboard.addWidget(empty_buttons[0], 0, 5, 1, 2)
        self.lo_keyboard.addWidget(empty_buttons[1], 0, 13, 1, 2)
        self.lo_keyboard.addWidget(empty_buttons[2], 0, 19, 1, 2)

    def press_key(self, note):

        # If we're in latch mode...
        if self.btn_latch.isChecked() is True:
            # And we're already playing the key...
            if note in self.shared_PLAYING.keys():
                # Then turn off the key and break out.
                self.dict_keyboard[note].setChecked(False)
                del self.shared_PLAYING[note]
                return

        cascade = self.get_cascade_notes(note)
        self.shared_PLAYING[note] = cascade

        flattened_cascade = [
            element for sublist in self.shared_PLAYING.values() for element in sublist
        ]

        for cascade_key in flattened_cascade:
            self.dict_keyboard[cascade_key].setDown(True)

        self.dict_keyboard[note].setChecked(True)

        if self.btn_arp_enable.isChecked() is False:
            self.soundscape.play_notes(flattened_cascade)

    def release_key(self, note):

        flattened_cascade = [
            element for sublist in self.shared_PLAYING.values() for element in sublist
        ]

        if self.btn_latch.isChecked() is True:
            if note in self.shared_PLAYING.keys():
                self.dict_keyboard[note].setChecked(True)
            else:
                self.dict_keyboard[note].setChecked(False)

            # Clear keyboard
            for key in self.dict_keyboard.values():
                key.setDown(False)

            # And reinit with still pressed keys:
            for cascade_key in flattened_cascade:
                self.dict_keyboard[cascade_key].setDown(True)

        elif self.btn_latch.isChecked() is False:

            for cascade_key in flattened_cascade:
                self.dict_keyboard[cascade_key].setDown(False)

            del self.shared_PLAYING[note]

            self.dict_keyboard[note].setChecked(False)

    def connect_panel(self):
        self.lst_instrument.addItem("Piano", "piano")
        self.lst_instrument.addItem("Clavinet", "clav")
        self.lst_instrument.addItem("Wurlitzer", "wurl")
        for chord in CHORDS.keys():
            self.lst_chord.addItem(chord)

        self.lst_pattern.addItem("Up/Down")
        self.lst_presets.addItem("No Preset")
        self.lst_n_type.addItem("1/1", 4)
        self.lst_n_type.addItem("1/2", 2)
        self.lst_n_type.addItem("1/4", 1)
        self.lst_n_type.addItem("1/8", 0.5)
        self.lst_n_type.addItem("1/16", 0.25)
        self.lst_n_type.addItem("1/32", 0.125)
        self.lst_n_mod.addItem("Whole", 1)
        self.lst_n_mod.addItem("Dotted", 1.5)
        self.lst_n_mod.addItem("Triplet", 0.67)
        self.lst_control_type.addItem("Click")
        self.lst_control_type.addItem("Slide")
        self.lst_control_type.addItem("Keybind")

        self.lst_instrument.currentIndexChanged.connect(self.change_instrument)
        self.btn_oct_up.clicked.connect(lambda _: self.change_octave("up"))
        self.btn_oct_down.clicked.connect(lambda _: self.change_octave("down"))

    def change_instrument(self, x):
        instrument = self.lst_instrument.itemData(x)
        self.soundscape.setup_sounds(instrument)

    def change_octave(self, direction):
        if direction == "up":
            self.octave += 1
        elif direction == "down":
            self.octave -= 1

        match self.octave:
            case 1:
                self.btn_oct_down.setDisabled(True)
            case 2:
                self.btn_oct_up.setDisabled(False)
                self.btn_oct_down.setDisabled(False)
            case 3:
                self.btn_oct_up.setDisabled(True)

        # Empty out the layout first:
        self.clear_keyboard()
        self.setup_key_btns()
        self.setup_keyboard()

        # Change the key control type
        self.change_key_control(self.lst_control_type.currentText())

        self.shared_PLAYING.clear()

    def clear_keyboard(self):
        while self.lo_keyboard.count():
            item = self.lo_keyboard.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.lo_keyboard.removeItem(item)

        self.dict_keyboard.clear()

    def change_steps(self, num_of_steps):
        for i in range(16):
            self.shared_LED[i].show()
            self.shared_PITCH[i].show()
            self.shared_GATES[i].show()

        for i in range(15, num_of_steps - 1, -1):
            self.shared_LED[i].hide()
            self.shared_PITCH[i].hide()
            self.shared_GATES[i].hide()

        self.shared_COMMON["steps"] = num_of_steps

    def change_key_control(self, value):
        for key in self.dict_keyboard.keys():
            self.dict_keyboard[key].type = value

    def change_bpm(self, value):
        self.shared_COMMON["bpm"] = value

    def toggle_arp(self, value):
        if value:
            self.btn_arp_enable.setText("Arp On")
            self.shared_COMMON["bpm"] = self.spn_bpm.value()
            self.shared_COMMON["steps"] = self.spn_steps.value()
            self.shared_COMMON["n_type"] = self.lst_n_type.currentData()
            self.shared_COMMON["n_mod"] = self.lst_n_mod.currentData()
            self.arpstepper.power_on()
        else:
            self.btn_arp_enable.setText("Arp Off")
            self.arpstepper.power_off()

    def change_note_speed(self):
        self.shared_COMMON["n_type"] = self.lst_n_type.currentData()

    def change_note_modifier(self):
        self.shared_COMMON["n_mod"] = self.lst_n_mod.currentData()

    def get_cascade_notes(self, note):
        chord = self.lst_chord.currentText()
        new_indexes = CHORDS[chord]
        current_index = NOTES_INDEX[note]

        cascade = []
        for index_mod in new_indexes:
            try:
                cascade.append(INDEX_NOTES[current_index + index_mod])
            except KeyError:
                pass

        return cascade


if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()

    fonts = [
        "ghostmood/AlteHaasGroteskRegular.ttf",
        "ghostmood/AlteHaasGroteskBold.ttf",
        "ghostmood/Nexa-ExtraLight.ttf",
        "ghostmood/Nexa-Heavy.ttf",
    ]

    for font in fonts:
        font_id = qtg.QFontDatabase.addApplicationFont(font)

        if font_id == -1:  # Font not loaded correctly
            print(f"{font} not added successfully!")

    style_file = qtc.QFile("ghostmood/stylesheet.css")
    style_file.open(qtc.QFile.ReadOnly | qtc.QFile.Text)
    stream = qtc.QTextStream(style_file)
    app.setStyleSheet(stream.readAll())

    mw.show()

    sys.exit(app.exec())
