class Theme:
    def __init__(self, name, primary, secondary, bg, text, accent):
        self.name = name
        self.primary = primary
        self.secondary = secondary
        self.bg = bg
        self.text = text
        self.accent = accent

class ThemeManager:
    THEMES = {
        "purple": Theme(
            "Purple Love",
            "#d9b3ff", "#a259ff", "#1a0b2e", "#ffffff", "#EE82EE"
        ),
        "butter": Theme(
            "Butter",
            "#FFA500", "#FFFF00", "#FFFACD", "#333333", "#FFD700"
        ),
        "dynamite": Theme(
            "Dynamite",
            "#FF69B4", "#87CEEB", "#E0FFFF", "#333333", "#00BFFF"
        ),
        "dark": Theme(
            "Dark Mode",
            "#BB86FC", "#03DAC6", "#121212", "#ffffff", "#3700B3"
        )
    }

    @staticmethod
    def get_theme(name):
        return ThemeManager.THEMES.get(name.lower(), ThemeManager.THEMES["purple"])

    @staticmethod
    def get_stylesheet(theme_name):
        t = ThemeManager.get_theme(theme_name)

        # QSS (Qt Style Sheet)
        return f"""
            QMainWindow {{
                background-color: {t.bg};
            }}
            QWidget {{
                color: {t.text};
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            /* Header */
            QLabel#header {{
                font-size: 24px;
                font-weight: bold;
                color: {t.primary};
                margin-bottom: 10px;
            }}

            /* Inputs */
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid {t.primary};
                border-radius: 10px;
                padding: 8px;
                color: {t.text};
            }}
            QLineEdit:focus {{
                border: 2px solid {t.accent};
            }}

            /* Buttons */
            QPushButton {{
                background-color: {t.secondary};
                color: {t.bg if t.text == "#ffffff" else "#000000"};
                border-radius: 10px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {t.primary};
            }}
            QPushButton#settings_btn {{
                background-color: transparent;
                border: none;
            }}
            QPushButton#delete_btn {{
                background-color: transparent;
                color: #ff5555;
                font-weight: bold;
                border: 1px solid transparent;
            }}
            QPushButton#delete_btn:hover {{
                border: 1px solid #ff5555;
                background-color: rgba(255, 85, 85, 0.1);
            }}

            /* Task List */
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QWidget#scroll_content {{
                background: transparent;
            }}
            QCheckBox {{
                spacing: 10px;
                font-size: 16px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {t.primary};
                border-radius: 5px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {t.primary};
                image: url(resources/check_icon.png); /* Need to create this or use simple rect */
            }}

            /* Progress Bar */
            QProgressBar {{
                border: 2px solid {t.primary};
                border-radius: 5px;
                text-align: center;
                background-color: rgba(255, 255, 255, 0.1);
                color: {t.text};
            }}
            QProgressBar::chunk {{
                background-color: {t.primary};
                border-radius: 3px;
            }}
        """
