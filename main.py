from re import L
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtMultimedia as qtm
import sys
from src.led import LedIndicator


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arp Toy")

        self.setMinimumSize(1000, 700)

        self.setupPanelUI()

        self.octave = 2
        self.setupKeyboardButtons()
        self.setupKeyboard()
        self.setupKeyboardSounds("piano")

        self.connectPanel()

    def setupPanelUI(self):
        lo_master = qtw.QVBoxLayout()
        self.setLayout(lo_master)
        lo_top = qtw.QHBoxLayout()
        struct_top = qtw.QFrame()
        struct_top.setObjectName("LShapeFrame")
        struct_top.setLayout(lo_top)

        lo_top_holder = qtw.QHBoxLayout()
        struct_top_holder = qtw.QWidget()
        struct_top_holder.setLayout(lo_top_holder)

        spacer1 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)

        lo_top_holder.addWidget(struct_top)
        lo_top_holder.addSpacerItem(spacer1)

        self.lo_keyboard = qtw.QGridLayout()
        struct_keyboard = qtw.QWidget()
        struct_keyboard.setLayout(self.lo_keyboard)
        lo_master.addWidget(struct_top_holder)
        lo_master.addWidget(struct_keyboard)

        lo_panel = qtw.QGridLayout()
        lo_stepper_top = qtw.QVBoxLayout()
        lo_stepper = qtw.QGridLayout()
        lo_step_dials = qtw.QHBoxLayout()

        struct_panel = qtw.QWidget()
        struct_stepper_top = qtw.QFrame()
        struct_stepper_top.setObjectName("LeftI")
        struct_stepper = qtw.QWidget()
        struct_step_dials = qtw.QWidget()

        struct_panel.setLayout(lo_panel)
        struct_stepper_top.setLayout(lo_stepper_top)
        struct_stepper.setLayout(lo_stepper)
        struct_step_dials.setLayout(lo_step_dials)

        lo_stepper_top.addWidget(struct_step_dials)
        lo_stepper_top.addWidget(struct_stepper)

        lo_panel_holder = qtw.QVBoxLayout()
        struct_panel_holder = qtw.QWidget()
        struct_panel_holder.setLayout(lo_panel_holder)

        spacer2 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        lo_panel_holder.addSpacerItem(spacer2)
        lo_panel_holder.addWidget(struct_panel)

        spacer3 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)

        lo_top.addWidget(struct_panel_holder)
        lo_top.addSpacerItem(spacer3)
        lo_top.addWidget(struct_stepper_top)

        # Top left - Buttons

        lbl_logo = qtw.QLabel("Arp<br>Toy")
        lo_panel.addWidget(lbl_logo, 0, 0, 3, 1)
        self.lst_instrument = qtw.QComboBox()
        lo_panel.addWidget(self.lst_instrument, 0, 3, 1, 2)
        self.lst_chord = qtw.QComboBox()
        lo_panel.addWidget(self.lst_chord, 1, 3, 1, 2)
        self.btn_oct_down = qtw.QPushButton("Octave -")
        lo_panel.addWidget(self.btn_oct_down, 2, 3, 1, 1)
        self.btn_oct_up = qtw.QPushButton("Octave +")
        lo_panel.addWidget(self.btn_oct_up, 2, 4, 1, 1)

        struct_bpm_frame = qtw.QFrame()
        struct_bpm_frame.setObjectName("FullFrame")
        lo_bpm_frame = qtw.QVBoxLayout()
        struct_bpm_frame.setLayout(lo_bpm_frame)

        lbl_bpm = qtw.QLabel("BPM")
        lo_bpm_frame.addWidget(lbl_bpm)
        self.spn_bpm = qtw.QSpinBox(maximum=260, minimum=40, value=110)
        lo_bpm_frame.addWidget(self.spn_bpm)
        self.btn_tap = qtw.QPushButton("Tap Tempo")
        lo_bpm_frame.addWidget(self.btn_tap)

        lo_panel.addWidget(struct_bpm_frame, 0, 6, 3, 1)



        # Top right - Stepper
        lbl_gate1 = qtw.QLabel("G<br>a<br>t<br>e<br><br>L<br>e<br>n")
        lo_stepper.addWidget(lbl_gate1, 3, 0, 2, 1)

        dict_gates = {}
        for i in range(16):
            dict_gates[i] = qtw.QSlider(maximum=100, minimum=0, value=100)
            lo_stepper.addWidget(dict_gates[i], 3, i + 1, 2, 1)

        dict_led = {}
        for i in range(16):
            dict_led[i] = LedIndicator()
            lo_stepper.addWidget(dict_led[i], 2, i + 1, 1, 1)
            dict_led[i].clicked.connect(lambda _, led=dict_led[i]: self.temp_toggleState(led))

        self.lst_pattern = qtw.QComboBox()
        lo_step_dials.addWidget(self.lst_pattern)

        spn_steps = qtw.QSpinBox(prefix='Steps: ', maximum=16, minimum=4, value=8)
        lo_step_dials.addWidget(spn_steps)



    def setupKeyboardButtons(self):
        self.keyboard_dict = {}
        self.notes = ["A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"]
        for i in range(1, 5):  # We fill up with 2 octaves at a time
            for n in self.notes:
                note = f"{n}{i}"
                self.keyboard_dict[note] = qtw.QPushButton(note.replace("s", "#")[:-1])
                self.keyboard_dict[note].setSizePolicy(
                    qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Expanding
                )
                if "s" in note:
                    self.keyboard_dict[note].setObjectName("PianoSharp")
                else:
                    self.keyboard_dict[note].setObjectName("PianoKey")

                self.keyboard_dict[note].clicked.connect(
                    lambda _, note=note: self.playNote(note)
                )

    def setupKeyboard(self):
        oct = self.octave
        self.lo_keyboard.addWidget(self.keyboard_dict[f"C{oct}"], 1, 0, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Cs{oct}"], 0, 1, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"D{oct}"], 1, 2, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Ds{oct}"], 0, 3, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"E{oct}"], 1, 4, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"F{oct}"], 1, 6, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Fs{oct}"], 0, 7, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"G{oct}"], 1, 8, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Gs{oct}"], 0, 9, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"A{oct}"], 1, 10, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"As{oct}"], 0, 11, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"B{oct}"], 1, 12, 1, 2)

        self.lo_keyboard.addWidget(self.keyboard_dict[f"C{oct+1}"], 1, 14, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Cs{oct+1}"], 0, 15, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"D{oct+1}"], 1, 16, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Ds{oct+1}"], 0, 17, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"E{oct+1}"], 1, 18, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"F{oct+1}"], 1, 20, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Fs{oct+1}"], 0, 21, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"G{oct+1}"], 1, 22, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Gs{oct+1}"], 0, 23, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"A{oct+1}"], 1, 24, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"As{oct+1}"], 0, 25, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"B{oct+1}"], 1, 26, 1, 2)

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
        self.sounds_dict = {}
        for i in range(1, 5):
            for n in self.notes:
                note = f"{n}{i}"
                self.sounds_dict[note] = qtm.QSoundEffect()
                self.sounds_dict[note].setSource(
                    qtc.QUrl.fromLocalFile(f"sound/{instrument}/{note}.wav")
                )

    def playNote(self, note):
        self.sounds_dict[note].play()

    def connectPanel(self):
        self.lst_instrument.addItem("Piano", "piano")
        self.lst_instrument.addItem("Clavinet", "clav")
        self.lst_instrument.addItem("Wurlitzer", "wurl")
        self.lst_chord.addItem("Major 7th")
        self.lst_pattern.addItem("Up/Down")

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

    def clearKeyboard(self):
        while self.lo_keyboard.count():
            item = self.lo_keyboard.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.lo_keyboard.removeItem(item)

        self.keyboard_dict = {}

    def temp_toggleState(self, led):
        led.state += 1

        if led.state >= 4:
            led.state = 1


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
