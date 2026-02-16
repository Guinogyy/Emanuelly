import flet as ft

class Theme:
    def __init__(self, name, primary_color, secondary_color, background_color, text_color, glass_opacity=0.8, background_image=None, font_family="Roboto"):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.background_color = background_color
        self.text_color = text_color
        self.glass_opacity = glass_opacity
        self.background_image = background_image
        self.font_family = font_family

class ThemeManager:
    THEMES = {
        "purple": Theme(
            name="Purple Love",
            primary_color="#d9b3ff",  # Light Purple
            secondary_color="#a259ff", # Darker Purple
            background_color="#1a0b2e", # Very Dark Purple
            text_color="#ffffff",
            glass_opacity=0.85,
            background_image="https://i.postimg.cc/B6b9m6H3/foto.jpg" # Original Image
        ),
        "butter": Theme(
            name="Butter",
            primary_color="#FFA500",  # Orange
            secondary_color="#FFFF00", # Yellow
            background_color="#FFFACD", # Lemon Chiffon (Light Yellow)
            text_color="#333333", # Dark Grey for contrast
            glass_opacity=0.9,
            background_image="https://images.unsplash.com/photo-1623696123478-f73587399450?q=80&w=1974&auto=format&fit=crop" # Yellow/Abstract
        ),
        "dynamite": Theme(
            name="Dynamite",
            primary_color="#FF69B4",  # Hot Pink
            secondary_color="#87CEEB", # Sky Blue
            background_color="#E0FFFF", # Light Cyan
            text_color="#333333",
            glass_opacity=0.8,
            background_image="https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop" # Retro/Neon
        ),
        "dark": Theme(
            name="Dark Mode",
            primary_color="#BB86FC",  # Material Dark Primary
            secondary_color="#03DAC6", # Teal
            background_color="#121212", # Dark Grey
            text_color="#ffffff",
            glass_opacity=0.95,
            background_image=None # Pure color
        )
    }

    @staticmethod
    def get_theme(name):
        return ThemeManager.THEMES.get(name.lower(), ThemeManager.THEMES["purple"])

    @staticmethod
    def get_all_themes():
        return list(ThemeManager.THEMES.values())

    @staticmethod
    def apply_theme(page: ft.Page, theme_name):
        theme = ThemeManager.get_theme(theme_name)

        page.theme_mode = ft.ThemeMode.DARK if theme.text_color == "#ffffff" else ft.ThemeMode.LIGHT
        page.bgcolor = theme.background_color
        page.fonts = {"CustomFont": theme.font_family}
        page.theme = ft.Theme(font_family="CustomFont", color_scheme_seed=theme.primary_color)

        return theme
