import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtMultimedia as qtm
import sys


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arp Toy")

        self.setMinimumSize(800, 600)

        self.setupUI()

    def setupUI(self):
        lo_master = qtw.QVBoxLayout()
        self.setLayout(lo_master)
        lo_top = qtw.QHBoxLayout()
        struct_top = qtw.QFrame()
        struct_top.setObjectName("LShapeFrame")
        struct_top.setLayout(lo_top)

        self.lo_keyboard = qtw.QGridLayout()
        struct_keyboard = qtw.QWidget()
        struct_keyboard.setLayout(self.lo_keyboard)
        lo_master.addWidget(struct_top)
        lo_master.addWidget(struct_keyboard)

        lo_panel = qtw.QGridLayout()
        lo_stepper = qtw.QGridLayout()

        struct_panel = qtw.QWidget()
        struct_stepper = qtw.QWidget()

        struct_panel.setLayout(lo_panel)
        struct_stepper.setLayout(lo_stepper)

        lo_top.addWidget(struct_panel)
        lo_top.addWidget(struct_stepper)

        # Top left - Buttons

        lbl_logo = qtw.QLabel("Arp Toy")
        lo_panel.addWidget(lbl_logo, 0, 0, 2, 1)
        self.lst_instrument = qtw.QComboBox()
        lo_panel.addWidget(self.lst_instrument, 0, 3, 1, 2)
        self.lst_chord = qtw.QComboBox()
        lo_panel.addWidget(self.lst_chord, 1, 3, 1, 1)
        self.lst_pattern = qtw.QComboBox()
        lo_panel.addWidget(self.lst_pattern, 1, 4, 1, 1)
        self.spn_bpm = qtw.QSpinBox(maximum=260, minimum=40, value=110)
        lo_panel.addWidget(self.spn_bpm, 2, 3, 1, 1)
        self.btn_tap = qtw.QPushButton("Tap Tempo")
        lo_panel.addWidget(self.btn_tap, 2, 4, 1, 1)
        self.btn_oct_down = qtw.QPushButton("Octave -")
        lo_panel.addWidget(self.btn_oct_down, 3, 3, 1, 1)
        self.btn_oct_up = qtw.QPushButton("Octave +")
        lo_panel.addWidget(self.btn_oct_up, 3, 4, 1, 1)

        self.lst_instrument.addItem("Piano")
        self.lst_chord.addItem("Major 7th")
        self.lst_pattern.addItem("Up/Down")

        # Top right - Stepper

        # Bottom - Keyboard
        self.keyboard_dict = {}
        notes = ["A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"]
        for i in range(1, 5):  # We've only got notes for 4 octaves
            for n in notes:
                note = f"{n}{i}"
                self.keyboard_dict[note] = qtw.QPushButton(note.replace("s", "#")[:-1])
                self.keyboard_dict[note].setSizePolicy(
                    qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Expanding
                )
                if "s" in note:
                    self.keyboard_dict[note].setObjectName("PianoSharp")
                else:
                    self.keyboard_dict[note].setObjectName("PianoKey")

        self.setupKeyboard(low_octave=1)

    def setupKeyboard(self, low_octave):
        self.lo_keyboard.addWidget(self.keyboard_dict[f"C{low_octave}"], 1, 0, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Cs{low_octave}"], 0, 1, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"D{low_octave}"], 1, 2, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Ds{low_octave}"], 0, 3, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"E{low_octave}"], 1, 4, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"F{low_octave}"], 1, 6, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Fs{low_octave}"], 0, 7, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"G{low_octave}"], 1, 8, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Gs{low_octave}"], 0, 9, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"A{low_octave}"], 1, 10, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"As{low_octave}"], 0, 11, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"B{low_octave}"], 1, 12, 1, 2)

        self.lo_keyboard.addWidget(self.keyboard_dict[f"C{low_octave+1}"], 1, 14, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Cs{low_octave+1}"], 0, 15, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"D{low_octave+1}"], 1, 16, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Ds{low_octave+1}"], 0, 17, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"E{low_octave+1}"], 1, 18, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"F{low_octave+1}"], 1, 20, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Fs{low_octave+1}"], 0, 21, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"G{low_octave+1}"], 1, 22, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"Gs{low_octave+1}"], 0, 23, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"A{low_octave+1}"], 1, 24, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"As{low_octave+1}"], 0, 25, 1, 2)
        self.lo_keyboard.addWidget(self.keyboard_dict[f"B{low_octave+1}"], 1, 26, 1, 2)

        # We'll just fill out the extra spots with invisible buttons
        # to make sure it all aligns.
        empty_buttons = {}
        for i in range(3):
            empty_buttons[i] = qtw.QPushButton("Z#")
            empty_buttons[i].setObjectName("Invisible")

        self.lo_keyboard.addWidget(empty_buttons[0], 0, 5, 1, 2)
        self.lo_keyboard.addWidget(empty_buttons[1], 0, 13, 1, 2)
        self.lo_keyboard.addWidget(empty_buttons[2], 0, 19, 1, 2)


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

    style_file = qtc.QFile("ghostmood/stylesheet.qss")
    style_file.open(qtc.QFile.ReadOnly | qtc.QFile.Text)
    stream = qtc.QTextStream(style_file)
    app.setStyleSheet(stream.readAll())

    mw.show()

    sys.exit(app.exec())
