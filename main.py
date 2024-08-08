import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtMultimedia as qtm
import sys
from src.led import LedIndicator
from src.globals import NOTES_INDEX, INDEX_NOTES, NOTES
from src.keyslide import KeySlide


class MainWindow(qtw.QWidget):

    shared_led = {}
    shared_pitch = {}
    shared_gates = {}
    shared_common = {}

    dict_keyboard = {}
    dict_sounds = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arp Toy")

        self.setMinimumSize(1000, 750)

        self.setupPanelUI()

        self.octave = 2
        self.setupKeyboardButtons()
        self.setupKeyboard()
        self.setupKeyboardSounds("piano")

        self.changeSteps(8)

        self.connectPanel()

        self.lst_n_type.setCurrentIndex(2)

        self.arp = ArpStepper(
            self.shared_led,
            self.shared_pitch,
            self.shared_gates,
            self.shared_common,
        )

    def setupPanelUI(self):
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
        self.spn_bpm.valueChanged.connect(self.changeBPM)
        self.btn_tap = qtw.QPushButton("Tap Tempo")
        lo_bpm_frame.addWidget(self.btn_tap)

        lo_panel_holder.addWidget(struct_bpm_frame)

        self.lst_instrument = qtw.QComboBox()
        lo_panel.addWidget(self.lst_instrument)
        self.lst_chord = qtw.QComboBox()
        lo_panel.addWidget(self.lst_chord)
        self.lst_control_type = qtw.QComboBox()
        lo_panel.addWidget(self.lst_control_type)
        self.lst_control_type.currentTextChanged.connect(self.changeKeyControl)

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
            self.shared_led[i] = LedIndicator()
            lo_arp_steps.addWidget(self.shared_led[i], 2, i, 1, 1)
            self.shared_led[i].clicked.connect(
                lambda _, led=self.shared_led[i]: self.temp_toggleState(led)
            )

        for i in range(16):
            self.shared_pitch[i] = qtw.QSlider(maximum=6, minimum=-6, value=0)
            self.shared_pitch[i].setObjectName("CustomSlider")
            self.shared_pitch[i].setOrientation(qtc.Qt.Horizontal)
            lo_arp_steps.addWidget(self.shared_pitch[i], 3, i, 1, 1)
            self.shared_pitch[i].sliderReleased.connect(
                lambda pitch=self.shared_pitch[i]: print(pitch.value())
            )

        for i in range(16):
            self.shared_gates[i] = qtw.QSlider(maximum=100, minimum=0, value=100)
            self.shared_gates[i].setObjectName("CustomSlider")
            lo_arp_steps.addWidget(
                self.shared_gates[i], 4, i, 1, 1, alignment=qtc.Qt.AlignCenter
            )

        self.btn_arp_enable = qtw.QPushButton("Arp Off", checkable=True)
        lo_arp_controls.addWidget(self.btn_arp_enable)
        self.btn_arp_enable.clicked.connect(self.toggleArp)

        btn_latch = qtw.QPushButton("Latch", checkable=True)
        lo_arp_controls.addWidget(btn_latch)

        self.lst_presets = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_presets)

        self.lst_pattern = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_pattern)

        self.lst_n_type = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_n_type)
        self.lst_n_type.currentIndexChanged.connect(self.changeNoteSpeed)

        self.lst_n_mod = qtw.QComboBox()
        lo_arp_controls.addWidget(self.lst_n_mod)
        self.lst_n_mod.currentIndexChanged.connect(self.changeNoteModifier)

        self.spn_steps = qtw.QSpinBox(prefix="Steps: ", maximum=16, minimum=4, value=8)
        lo_arp_controls.addWidget(self.spn_steps)
        self.spn_steps.valueChanged.connect(self.changeSteps)

    def setupKeyboardButtons(self):
        self.dict_keyboard.clear()

        for i in range(1, 6):
            for n in NOTES:
                note = f"{n}{i}"
                self.dict_keyboard[note] = KeySlide(note.replace("s", "#")[:-1])
                self.dict_keyboard[note].setSizePolicy(
                    qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Expanding
                )
                if "s" in note:
                    self.dict_keyboard[note].setObjectName("PianoSharp")
                else:
                    self.dict_keyboard[note].setObjectName("PianoKey")

                self.dict_keyboard[note].pressed.connect(
                    lambda note=note: self.playNote(note)
                )

                self.dict_keyboard[note].released.connect(
                    lambda note=note: self.releaseNote(note)
                )

    def setupKeyboard(self):
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

    def setupKeyboardSounds(self, instrument):
        self.dict_sounds.clear()
        for i in range(1, 5):
            for n in NOTES:
                note = f"{n}{i}"
                self.dict_sounds[note] = qtm.QSoundEffect()
                self.dict_sounds[note].setSource(
                    qtc.QUrl.fromLocalFile(f"sound/{instrument}/{note}.wav")
                )

    def playNote(self, note):
        print(note)
        self.dict_sounds[note].play()
        index = NOTES_INDEX[note]

        one = INDEX_NOTES[index + 3]
        two = INDEX_NOTES[index + 6]
        three = INDEX_NOTES[index + 9]

        self.dict_sounds[one].play()
        self.dict_keyboard[one].setDown(True)
        self.dict_sounds[two].play()
        self.dict_keyboard[two].setDown(True)
        self.dict_sounds[three].play()
        self.dict_keyboard[three].setDown(True)

        print(note)
        print(three)

    def releaseNote(self, note):
        index = NOTES_INDEX[note]

        one = INDEX_NOTES[index + 3]

        two = INDEX_NOTES[index + 6]

        three = INDEX_NOTES[index + 9]

        self.dict_keyboard[one].setDown(False)
        self.dict_keyboard[two].setDown(False)
        self.dict_keyboard[three].setDown(False)

    def connectPanel(self):
        self.lst_instrument.addItem("Piano", "piano")
        self.lst_instrument.addItem("Clavinet", "clav")
        self.lst_instrument.addItem("Wurlitzer", "wurl")
        self.lst_chord.addItem("Major 7th")
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

        self.lst_instrument.currentIndexChanged.connect(self.changeInstrument)
        self.btn_oct_up.clicked.connect(lambda _: self.changeOctave("up"))
        self.btn_oct_down.clicked.connect(lambda _: self.changeOctave("down"))

    def changeInstrument(self, x):
        instrument = self.lst_instrument.itemData(x)
        self.setupKeyboardSounds(instrument)

    def changeOctave(self, direction):
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
        self.clearKeyboard()
        self.setupKeyboardButtons()
        self.setupKeyboard()

        # Change the key control type
        self.changeKeyControl(self.lst_control_type.currentText())

    def clearKeyboard(self):
        while self.lo_keyboard.count():
            item = self.lo_keyboard.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.lo_keyboard.removeItem(item)

        self.dict_keyboard.clear()

    def changeSteps(self, num_of_steps):
        for i in range(16):
            self.shared_led[i].show()
            self.shared_pitch[i].show()
            self.shared_gates[i].show()

        for i in range(15, num_of_steps - 1, -1):
            self.shared_led[i].hide()
            self.shared_pitch[i].hide()
            self.shared_gates[i].hide()

        self.shared_common["steps"] = num_of_steps

    def changeKeyControl(self, value):
        for key in self.dict_keyboard.keys():
            self.dict_keyboard[key].state = value

    def changeBPM(self, value):
        self.shared_common["bpm"] = value

    def toggleArp(self, value):
        if value:
            self.btn_arp_enable.setText("Arp On")
            self.shared_common["bpm"] = self.spn_bpm.value()
            self.shared_common["steps"] = self.spn_steps.value()
            self.shared_common["n_type"] = self.lst_n_type.currentData()
            self.shared_common["n_mod"] = self.lst_n_mod.currentData()
            self.arp.powerOn()
        else:
            self.btn_arp_enable.setText("Arp Off")
            self.arp.powerOff()

    def changeNoteSpeed(self):
        self.shared_common["n_type"] = self.lst_n_type.currentData()

    def changeNoteModifier(self):
        self.shared_common["n_mod"] = self.lst_n_mod.currentData()

    def temp_toggleState(self, led):
        pass


class ArpStepper(qtc.QThread):

    update_signal = qtc.pyqtSignal(bool)

    def __init__(self, led, pitch, gates, common):
        self.led = led
        self.pitch = pitch
        self.gates = gates
        self.common = common
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

            elapsed = start_time.msecsTo(qtc.QTime.currentTime())
            qtc.QThread.msleep(
                max(0, int((((60000 / beats) * n_type) * n_mod) - elapsed))
            )

    def toggle(self):
        self.go = not self.go

    def powerOff(self):
        self.arpeggiate = False
        for index in self.led.keys():
            self.led[index].setChecked(False)

    def powerOn(self):
        self.step_current = 0
        self.step_last = 0
        self.arpeggiate = True
        self.start()


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
