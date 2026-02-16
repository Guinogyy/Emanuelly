import sys
import os
import pygame
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QProgressBar, QScrollArea,
                             QCheckBox, QDialog, QComboBox, QSizePolicy, QGraphicsOpacityEffect)
from PySide6.QtGui import QIcon, QFont, QMovie, QPainter, QColor, QPalette, QCursor
from PySide6.QtCore import Qt, QSize, QTimer, Property, QPropertyAnimation, QEasingCurve, QUrl
from data_manager import DataManager
from theme_manager import ThemeManager

class TaskItem(QWidget):
    def __init__(self, task, on_toggle, on_delete, theme):
        super().__init__()
        self.task = task
        self.on_toggle = on_toggle
        self.on_delete = on_delete
        self.theme = theme
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.checkbox = QCheckBox(task["text"])
        self.checkbox.setChecked(task["completed"])
        self.checkbox.stateChanged.connect(self._toggle)
        self.checkbox.setCursor(Qt.PointingHandCursor)
        self.update_style()

        self.delete_btn = QPushButton("🗑")
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(lambda: on_delete(task["id"]))

        layout.addWidget(self.checkbox)
        layout.addStretch()
        layout.addWidget(self.delete_btn)
        self.setLayout(layout)

        # Simple animation on create
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def _toggle(self, state):
        self.on_toggle(self.task["id"], bool(state))
        self.update_style()

    def update_style(self):
        color = self.theme.text if not self.task['completed'] else '#777'
        deco = 'line-through' if self.task['completed'] else 'none'
        self.checkbox.setStyleSheet(f"font-size: 16px; color: {color}; text-decoration: {deco};")

class SettingsDialog(QDialog):
    def __init__(self, parent, current_theme, current_bias, on_save):
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.setFixedSize(300, 200)

        t = ThemeManager.get_theme(current_theme)
        self.setStyleSheet(f"background-color: {t.bg}; color: {t.text};")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Escolha o Tema:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Purple", "Butter", "Dynamite", "Dark"])
        self.theme_combo.setCurrentText(current_theme.capitalize())
        layout.addWidget(self.theme_combo)

        layout.addWidget(QLabel("Seu Bias:"))
        self.bias_combo = QComboBox()
        self.bias_combo.addItems(["RM", "Jin", "Suga", "J-Hope", "Jimin", "V", "Jungkook"])
        self.bias_combo.setCurrentText(current_bias)
        layout.addWidget(self.bias_combo)

        save_btn = QPushButton("Salvar")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(lambda: on_save(self.theme_combo.currentText().lower(), self.bias_combo.currentText()))
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

        self.setLayout(layout)

class BTSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.load_data()

        # Setup Window
        self.setWindowTitle("BTS To-Do List")
        self.resize(400, 600)
        
        # Initialize Audio
        try:
            pygame.mixer.init()
        except Exception:
            print("Audio not available")

        # Setup UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Initialize components before applying theme
        self.setup_header()
        self.setup_progress()
        self.setup_task_list()
        self.setup_input()

        # Overlay for celebration
        self.overlay_label = QLabel(self)
        self.overlay_label.setGeometry(0, 0, 400, 600)
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setVisible(False)
        self.overlay_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Setup Movie (GIF)
        gif_path = "resources/confetti.gif"
        if not os.path.exists(gif_path):
             self.overlay_label.setText("🎉 PARABÉNS! 🎉")
             self.overlay_label.setStyleSheet("font-size: 30px; font-weight: bold; color: gold;")
        else:
             self.movie = QMovie(gif_path)
             self.movie.setScaledSize(QSize(400, 600))
             self.overlay_label.setMovie(self.movie)

        self.apply_theme()
        self.render_tasks()

    def load_data(self):
        data = self.data_manager.load_data()
        self.tasks = data.get("tasks", [])
        self.current_theme = data.get("theme", "purple")
        self.current_bias = data.get("bias", "V")

    def save_state(self):
        self.data_manager.save_data({
            "tasks": self.tasks,
            "theme": self.current_theme,
            "bias": self.current_bias
        })

    def apply_theme(self):
        self.setStyleSheet(ThemeManager.get_stylesheet(self.current_theme))
        
        self.header_label.setText(f"Olá, {self.current_bias} Stan! 💜")
        self.update_progress()
        self.repaint()

    def setup_header(self):
        header_layout = QHBoxLayout()
        
        self.header_label = QLabel("Olá, Army! 💜")
        self.header_label.setObjectName("header")
        header_layout.addWidget(self.header_label)
        
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setObjectName("settings_btn")
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_btn)
        
        self.main_layout.addLayout(header_layout)

    def setup_progress(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p% Concluído")
        self.progress_bar.setFixedHeight(20)
        self.main_layout.addWidget(self.progress_bar)

    def setup_task_list(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scroll_content")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

    def setup_input(self):
        input_layout = QHBoxLayout()
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("O que vamos fazer hoje?")
        self.task_input.returnPressed.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        
        add_btn = QPushButton("+")
        add_btn.setFixedSize(40, 40)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(add_btn)

        self.main_layout.addLayout(input_layout)

    def render_tasks(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        sorted_tasks = sorted(self.tasks, key=lambda x: x["completed"])
        t = ThemeManager.get_theme(self.current_theme)

        for task in sorted_tasks:
            item = TaskItem(task, self.toggle_task, self.delete_task, t)
            self.scroll_layout.addWidget(item)

        self.update_progress()

    def update_progress(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        val = int((completed / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(val)

    def add_task(self):
        text = self.task_input.text().strip()
        if text:
            new_task = self.data_manager.add_task(text)
            self.tasks.append(new_task)
            self.save_state()
            self.task_input.clear()
            self.render_tasks()

    def toggle_task(self, task_id, value):
        completed_count = sum(1 for t in self.tasks if t["completed"])
        total = len(self.tasks)
        was_all_done = (completed_count == total and total > 0)

        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = value
                break
        self.save_state()
        self.render_tasks()

        # Check for celebration condition AFTER toggle
        completed_count_new = sum(1 for t in self.tasks if t["completed"])
        if value and completed_count_new == total and total > 0 and not was_all_done:
            self.play_celebration()

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_state()
        self.render_tasks()

    def play_celebration(self):
        try:
            pygame.mixer.music.load("resources/success.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Audio Error: {e}")

        self.overlay_label.setVisible(True)
        self.overlay_label.raise_()

        if hasattr(self, 'movie') and self.movie:
            self.movie.start()

        QTimer.singleShot(4000, self.stop_celebration)

    def stop_celebration(self):
        if hasattr(self, 'movie') and self.movie:
            self.movie.stop()
        self.overlay_label.setVisible(False)

    def open_settings(self):
        def on_save(theme, bias):
            self.update_settings(theme, bias)

        dialog = SettingsDialog(self, self.current_theme, self.current_bias, on_save)
        dialog.exec()

    def update_settings(self, theme, bias):
        self.current_theme = theme
        self.current_bias = bias
        self.save_state()
        self.apply_theme()
        self.render_tasks()

    def resizeEvent(self, event):
        self.overlay_label.resize(self.width(), self.height())
        if hasattr(self, 'movie') and self.movie:
             self.movie.setScaledSize(QSize(self.width(), self.height()))
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BTSApp()
    window.show()
    sys.exit(app.exec())
