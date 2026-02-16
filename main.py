import flet as ft
import asyncio
import os
from data_manager import DataManager
from theme_manager import ThemeManager

# Modern Flet: Use Component class or just a function returning a Control
# We'll use a class inheriting from ft.Container or ft.Column for composition
class TaskItem(ft.Container):
    def __init__(self, task, on_toggle, on_delete, theme):
        super().__init__()
        self.task = task
        self.on_toggle = on_toggle
        self.on_delete = on_delete
        self.theme = theme

        self.padding = ft.padding.symmetric(horizontal=10, vertical=5)
        self.border_radius = 10
        self.bgcolor = ft.Colors.with_opacity(0.1, self.theme.text)
        self.animate = ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)

        self.checkbox = ft.Checkbox(
            label=self.task["text"],
            value=self.task["completed"],
            on_change=lambda e: asyncio.create_task(self.on_toggle(self.task["id"], e.control.value)),
            fill_color=self.theme.primary,
            check_color=self.theme.bg,
            label_style=ft.TextStyle(
                color=self.theme.text,
                decoration=ft.TextDecoration.LINE_THROUGH if self.task["completed"] else ft.TextDecoration.NONE,
                size=16
            ),
        )

        self.delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
            icon_color=ft.Colors.RED_400,
            tooltip="Delete Task",
            on_click=lambda e: asyncio.create_task(self.on_delete(self.task["id"]))
        )

        self.content = ft.Row(
            [self.checkbox, self.delete_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

async def main(page: ft.Page):
    page.title = "BTS To-Do List"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"} # Example font loading if needed

    # Initialize Managers
    dm = DataManager()
    data = dm.load_data()

    # State
    tasks = data.get("tasks", [])
    current_theme = data.get("theme", "purple")
    current_bias = data.get("bias", "V")
    custom_bg_path = data.get("custom_bg", "") # New field
    panel_opacity = data.get("panel_opacity", 0.8) # New field

    # Audio
    audio = ft.Audio(src="resources/success.mp3", autoplay=False)
    page.overlay.append(audio)

    # File Picker for BG
    async def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            nonlocal custom_bg_path
            custom_bg_path = e.files[0].path
            bg_image.src = custom_bg_path
            bg_image.opacity = 1
            await save_state()
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # UI Components
    bg_image = ft.Image(
        src=custom_bg_path if custom_bg_path else ThemeManager.get_theme(current_theme).bg_image,
        src_base64=None,
        fit=ft.ImageFit.COVER,
        opacity=1 if (custom_bg_path or ThemeManager.get_theme(current_theme).bg_image) else 0,
        expand=True
    )

    celebration_gif = ft.Image(
        src="resources/confetti.gif",
        fit=ft.ImageFit.CONTAIN,
        visible=False,
        expand=True
    )

    header_text = ft.Text(f"Olá, {current_bias} Stan! 💜", size=24, weight=ft.FontWeight.BOLD)
    progress_bar = ft.ProgressBar(value=0, height=8, border_radius=4)
    task_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    new_task_input = ft.TextField(hint_text="Nova tarefa...", expand=True, border_color="transparent")

    async def save_state():
        dm.save_data({
            "tasks": tasks,
            "theme": current_theme,
            "bias": current_bias,
            "custom_bg": custom_bg_path,
            "panel_opacity": panel_opacity
        })

    async def update_theme_ui(t_name):
        nonlocal current_theme
        current_theme = t_name
        t = ThemeManager.get_theme(t_name)
        
        # Update colors
        header_text.color = t.text
        new_task_input.text_style = ft.TextStyle(color=t.text)
        new_task_input.hint_style = ft.TextStyle(color=ft.Colors.with_opacity(0.5, t.text))
        
        main_card.bgcolor = ft.Colors.with_opacity(panel_opacity, t.bg)
        fab.bgcolor = t.primary
        fab.content.color = t.bg
        
        if not custom_bg_path:
            bg_image.src = t.bg_image
            bg_image.opacity = 1 if t.bg_image else 0

        await render_tasks()
        await save_state()
        page.update()

    async def update_bias(bias_name):
        nonlocal current_bias
        current_bias = bias_name
        header_text.value = f"Olá, {current_bias} Stan! 💜"
        await save_state()
        page.update()

    async def update_opacity(e):
        nonlocal panel_opacity
        panel_opacity = e.control.value
        t = ThemeManager.get_theme(current_theme)
        main_card.bgcolor = ft.Colors.with_opacity(panel_opacity, t.bg)
        await save_state()
        page.update()

    async def render_tasks():
        task_column.controls.clear()
        t = ThemeManager.get_theme(current_theme)
        sorted_tasks = sorted(tasks, key=lambda x: x["completed"])
        
        for task in sorted_tasks:
            task_column.controls.append(
                TaskItem(task, toggle_task, delete_task, t)
            )
        
        completed = sum(1 for t in tasks if t["completed"])
        total = len(tasks)
        progress_bar.value = completed / total if total > 0 else 0
        progress_bar.color = t.primary
        
        page.update()

    async def add_task(e):
        if new_task_input.value:
            tasks.append(dm.add_task(new_task_input.value))
            new_task_input.value = ""
            await save_state()
            await render_tasks()

    async def toggle_task(tid, val):
        for task in tasks:
            if task["id"] == tid:
                task["completed"] = val
                break
        await save_state()
        await render_tasks()

        if val and all(t["completed"] for t in tasks) and len(tasks) > 0:
            await play_celebration()

    async def delete_task(tid):
        nonlocal tasks
        tasks = [t for t in tasks if t["id"] != tid]
        await save_state()
        await render_tasks()

    async def play_celebration():
        audio.play()
        celebration_gif.visible = True
        page.update()
        await asyncio.sleep(4)
        celebration_gif.visible = False
        page.update()

    async def open_settings(e):
        t = ThemeManager.get_theme(current_theme)

        dlg = ft.AlertDialog(
            title=ft.Text("Configurações"),
            content=ft.Column([
                ft.Text("Tema", weight="bold"),
                ft.Dropdown(
                    value=current_theme,
                    options=[ft.dropdown.Option(k) for k in ThemeManager.THEMES.keys()],
                    on_change=lambda e: asyncio.create_task(update_theme_ui(e.control.value))
                ),
                ft.Text("Bias", weight="bold"),
                ft.Dropdown(
                    value=current_bias,
                    options=[ft.dropdown.Option(b) for b in ["RM", "Jin", "Suga", "J-Hope", "Jimin", "V", "Jungkook"]],
                    on_change=lambda e: asyncio.create_task(update_bias(e.control.value))
                ),
                ft.Text("Transparência do Painel", weight="bold"),
                ft.Slider(min=0.1, max=1.0, value=panel_opacity, on_change=lambda e: asyncio.create_task(update_opacity(e))),
                ft.ElevatedButton("Escolher Fundo", on_click=lambda _: file_picker.pick_files(allow_multiple=False))
            ], tight=True, width=300),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.close(dlg))],
        )
        page.open(dlg)
        page.update()

    # Main Card
    main_card = ft.Container(
        content=ft.Column([
            ft.Row([header_text, ft.IconButton(ft.Icons.SETTINGS, on_click=open_settings)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            progress_bar,
            ft.Divider(color="transparent"),
            task_column,
        ]),
        padding=20,
        margin=20,
        border_radius=20,
        blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.with_opacity(0.3, "black")),
        expand=True,
        # Responsive width constraints
        constraints=ft.BoxConstraints(max_width=600)
    )

    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda e: page.open(
            ft.BottomSheet(
                ft.Container(
                    ft.Column([
                        ft.Text("Nova Tarefa", size=18, weight="bold"),
                        ft.Row([new_task_input, ft.IconButton(ft.Icons.SEND, on_click=add_task)])
                    ], tight=True),
                    padding=20, bgcolor=ThemeManager.get_theme(current_theme).bg
                )
            )
        )
    )

    # Initial Render
    await update_theme_ui(current_theme) # Applies theme colors to card

    page.add(
        ft.Stack([
            bg_image,
            ft.Row([main_card], alignment=ft.MainAxisAlignment.CENTER, expand=True), # Center Card
            celebration_gif
        ], expand=True)
    )
    page.floating_action_button = fab

# Ensure assets_dir is correct for packaging (relative to main.py)
ft.app(target=main, assets_dir=".")
