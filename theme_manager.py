import flet as ft

class Theme:
    def __init__(self, name, primary, secondary, bg, text, glass_opacity=0.8, bg_image=""):
        self.name = name
        self.primary = primary
        self.secondary = secondary
        self.bg = bg
        self.text = text
        self.glass_opacity = glass_opacity
        self.bg_image = bg_image

class ThemeManager:
    THEMES = {
        "purple": Theme(
            "Purple Love", "#d9b3ff", "#a259ff", "#1a0b2e", "#ffffff", 0.85,
            bg_image="resources/foto.jfif"
        ),
        "butter": Theme(
            "Butter", "#FFA500", "#FFFF00", "#FFFACD", "#333333", 0.9,
            bg_image=""
        ),
        "dynamite": Theme(
            "Dynamite", "#FF69B4", "#87CEEB", "#E0FFFF", "#333333", 0.8,
            bg_image=""
        ),
        "dark": Theme(
            "Dark Mode", "#BB86FC", "#03DAC6", "#121212", "#ffffff", 0.95,
            bg_image=""
        )
    }

    @staticmethod
    def get_theme(name):
        return ThemeManager.THEMES.get(name.lower(), ThemeManager.THEMES["purple"])

    @staticmethod
    def apply_theme(page: ft.Page, theme_name):
        t = ThemeManager.get_theme(theme_name)

        page.theme_mode = ft.ThemeMode.DARK if t.text == "#ffffff" else ft.ThemeMode.LIGHT
        page.bgcolor = t.bg # Solid fallback

        # We also return the theme object so the app can use specific colors
        return t
