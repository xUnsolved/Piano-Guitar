import os
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMenu, QLabel
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation

error_files = set()

# Анімація клавіш
class KeyPressEater:
    # Натискання
    def start_animation(btn):
        if btn.is_black:
            btn.setStyleSheet("background-color: gray; color: black;")
        if not hasattr(btn, 'animation'):
            btn.animation = QPropertyAnimation(btn, b"geometry")
            btn.animation.setDuration(100)
            btn.animation.setStartValue(btn.geometry())
            btn.animation.setEndValue(QRect(btn.x(), btn.y(), btn.width(), btn.height() + 10))
            btn.animation.start()

    # Відтискання
    def end_animation(btn):
        if btn.is_black:
            btn.setStyleSheet("background-color: black; color: white;")
        if hasattr(btn, 'animation'):
            btn.animation.stop()
            btn.animation.deleteLater()
            del btn.animation

# Клас кнопок, кольор та інші ініціалізація запуску звуків
class AnimatedButton(QPushButton):
    def __init__(self, key, file_path, is_black=False):
        super(AnimatedButton, self).__init__(key)
        self.setFixedSize(90, 275)
        self.is_black = is_black
        if is_black:
            self.setStyleSheet("background-color: black; color: white;")
        else:
            self.setStyleSheet("background-color: white;")

        self.clicked.connect(lambda _, path=file_path: play_sound(path))
        self.pressed.connect(lambda: KeyPressEater.start_animation(self))
        self.released.connect(lambda: KeyPressEater.end_animation(self))

# Клас для запуску звуків
def play_sound(file_path):
    QSound.play(file_path)

# Пресет назви звуків
def set_instrument(instrument):
    instrument_keys = {
        'Піаніно': {
            'C': 'C.wav',
            'D': 'D.wav',
            'E': 'E.wav',
            'F': 'F.wav',
            'G': 'G.wav',
            'A': 'A.wav',
            'B': 'B.wav',
            'C1': 'C1.wav',
            'D1': 'D1.wav',
            'E1': 'E1.wav',
            'F1': 'F1.wav',
            'C#': 'C_s.wav',
            'D#': 'D_s.wav',
            'F#': 'F_s.wav',
            'G#': 'G_s.wav',
            'Bb': 'Bb.wav',
            'C#1': 'C_s1.wav',
            'D#1': 'D_s1.wav',
        },
        'Гітара': {
            'C': 'guitar_C.wav',
            'D': 'guitar_D.wav',
            'E': 'guitar_E.wav',
            'F': 'guitar_F.wav',
            'G': 'guitar_G.wav',
            'A': 'guitar_A.wav',
            'B': 'guitar_B.wav',
            'C1': 'guitar_C1.wav',
            'D1': 'guitar_D1.wav',
            'E1': 'guitar_E1.wav',
            'F1': 'guitar_F1.wav',
            'C#': 'guitar_C_s.wav',
            'D#': 'guitar_D_s.wav',
            'F#': 'guitar_F_s.wav',
            'G#': 'guitar_G_s.wav',
            'Bb': 'guitar_Bb.wav',
            'C#1': 'guitar_C_s1.wav',
            'D#1': 'guitar_D_s1.wav',
        }
    }

    global keys
    keys = instrument_keys.get(instrument, {})

    # Перевірка файлів
    for key, file_path in keys.items():
        if not os.path.isfile(file_path):
            print(f"Sound file not found: {file_path}")

    update_selected_instrument_label(instrument)

def update_selected_instrument_label(instrument):
    selected_instrument_label.setText(f"Обраний інструмент: {instrument.capitalize()}")

app = QApplication([])

window = QWidget()
window.resize(1200, 700)
window.setWindowTitle("Play for your soul")

option_btn = QPushButton("Вибір інструмента")
option_btn.setFixedSize(120, 30)

# Меню
instrument_menu = QMenu(option_btn)
instrument_menu.addAction("Піанино", lambda: set_instrument('Піаніно'))
instrument_menu.addAction("Гітара", lambda: set_instrument('Гітара'))
option_btn.setMenu(instrument_menu)

# Елемент для відображення вибраного інструменту
selected_instrument_label = QLabel("Обраний інструмент: Піаніно")
selected_instrument_label.setAlignment(Qt.AlignCenter)

option_line = QHBoxLayout()
help_line = QVBoxLayout()
upper_keys_line = QHBoxLayout()
main_keys_line = QHBoxLayout()

keys = {}
set_instrument('Піаніно')  # Піаніно по дефолту

# Для двох рядів - дві змінні
white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C1', 'D1', 'E1', 'F1']
black_keys = ['C#', 'D#', 'F#', 'G#', 'Bb', 'C#1']

for key in white_keys:
    file_path = keys.get(key, '')
    btn = AnimatedButton(key, file_path)
    main_keys_line.addWidget(btn)

for key in black_keys:
    file_path = keys.get(key, '')
    btn = AnimatedButton(key, file_path, is_black=True)
    upper_keys_line.addWidget(btn)

# Лейаути
help_line.addLayout(option_line)
help_line.addWidget(selected_instrument_label)
help_line.addLayout(upper_keys_line)
help_line.addLayout(main_keys_line)
option_line.addWidget(option_btn, alignment=Qt.AlignLeft)

window.setLayout(help_line)
window.show()

app.exec_()