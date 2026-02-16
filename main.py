import flet as ft
import flet_audio as fa
import flet_lottie as fl
from data_manager import DataManager
from theme_manager import ThemeManager
import time

# Initialize Managers
data_manager = DataManager()

def main(page: ft.Page):
    page.title = "BTS To-Do List"
    page.padding = 0
    page.spacing = 0

    # --- Load Data ---
    app_data = data_manager.load_data()
    current_tasks = app_data.get("tasks", [])
    current_theme_name = app_data.get("theme", "purple")
    current_bias = app_data.get("bias", "V")

    # --- Assets ---
    success_audio = fa.Audio(src="audios/success.mp3", autoplay=False)
    page.overlay.append(success_audio)

    lottie_success = fl.Lottie(
        src="https://lottie.host/56a2db8f-8c31-411a-96b5-0b04751e7075/9x4l6g6g1X.json",
        repeat=False,
        animate=False,
        width=300,
        height=300,
    )
    
    lottie_container = ft.Container(
        content=lottie_success,
        alignment=ft.alignment.center,
        visible=False,
        expand=True,
    )

    # --- UI Controls Definition ---
    
    # Header Elements
    header_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)
    settings_btn = ft.IconButton(icon=ft.Icons.SETTINGS, icon_size=24)

    # Progress
    progress_bar = ft.ProgressBar(value=0, height=6, border_radius=3)
    progress_text = ft.Text(size=12, opacity=0.8)

    # Task List
    task_list_view = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    # Inputs
    new_task_input = ft.TextField(
        hint_text="O que vamos fazer hoje?",
        expand=True,
        border_color="transparent",
        bgcolor="transparent",
        text_size=16
    )

    # FAB
    fab = ft.FloatingActionButton(icon=ft.Icons.ADD)

    # Background Image
    bg_image = ft.Image(
        src="",
        fit=ft.ImageFit.COVER,
        opacity=0.3,
        expand=True,
    )

    # Main Container
    main_container = ft.Container(
        padding=20,
        margin=ft.margin.symmetric(horizontal=10, vertical=20),
        border_radius=20,
        blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.3, "black"),
            offset=ft.Offset(0, 0),
        ),
        constraints=ft.BoxConstraints(max_width=600),
        expand=True,
    )

    # Settings Modal Controls
    settings_drawer = ft.NavigationDrawer(controls=[], bgcolor="transparent", surface_tint_color="transparent")


    # --- Logic & Helper Functions ---

    def save_state():
        data = {
            "tasks": current_tasks,
            "theme": current_theme_name,
            "bias": current_bias
        }
        data_manager.save_data(data)

    def play_success_animation():
        lottie_container.visible = True
        lottie_success.animate = True
        success_audio.play()
        page.update()
        
        # Simple timeout logic would be better with asyncio but this is triggered by UI event
        # We will let the user click away or use a timer if possible.
        # For now, let's just make the lottie container clickable to dismiss
        lottie_container.on_click = lambda e: hide_anim()
        
    def hide_anim():
        lottie_container.visible = False
        lottie_success.animate = False
        page.update()

    def update_header_and_settings():
        theme = ThemeManager.get_theme(current_theme_name)
        header_text.value = f"Olá, {current_bias} Stan! 💜"
        header_text.color = theme.text_color
        progress_text.color = theme.text_color
        settings_btn.icon_color = theme.text_color

        # Update progress bar color
        progress_bar.color = theme.primary_color
        progress_bar.bgcolor = ft.Colors.with_opacity(0.2, theme.text_color)

    def update_progress():
        total = len(current_tasks)
        completed = sum(1 for t in current_tasks if t["completed"])
        
        if total == 0:
            progress_bar.value = 0
            progress_text.value = "Nenhuma tarefa ainda."
        else:
            progress_bar.value = completed / total
            progress_text.value = f"{completed}/{total} Tarefas Concluídas"
        
        update_header_and_settings() # Call this here to ensure colors are right

    def delete_task(task_id):
        nonlocal current_tasks
        current_tasks = [t for t in current_tasks if t["id"] != task_id]
        save_state()
        render_tasks()

    def toggle_task(task_id, value):
        for task in current_tasks:
            if task["id"] == task_id:
                task["completed"] = value
                break
        save_state()
        render_tasks()

        if value and all(t["completed"] for t in current_tasks) and len(current_tasks) > 0:
            play_success_animation()

    def create_task_item(task):
        theme = ThemeManager.get_theme(current_theme_name)

        checkbox = ft.Checkbox(
            value=task["completed"],
            on_change=lambda e: toggle_task(task["id"], e.control.value),
            fill_color=theme.primary_color,
            check_color=theme.background_color,
        )

        text = ft.Text(
            task["text"],
            size=16,
            color=theme.text_color,
            weight=ft.FontWeight.W_500,
            opacity=0.5 if task["completed"] else 1.0,
            decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else ft.TextDecoration.NONE,
            expand=True
        )
        
        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
            icon_color=ft.Colors.RED_400,
            on_click=lambda e: delete_task(task["id"])
        )

        return ft.Container(
            content=ft.Row(
                [checkbox, text, delete_btn],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor=ft.Colors.with_opacity(0.1, theme.text_color),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        )

    def render_tasks():
        task_list_view.controls.clear()
        sorted_tasks = sorted(current_tasks, key=lambda x: x["completed"])
        for task in sorted_tasks:
            task_list_view.controls.append(create_task_item(task))
        update_progress()
        page.update()

    def add_task_action(e):
        if new_task_input.value.strip():
            new_task = data_manager.add_task(new_task_input.value.strip())
            current_tasks.append(new_task)
            save_state()
            new_task_input.value = ""
            render_tasks()
            page.close_bottom_sheet()

    def show_add_task_modal(e):
        theme = ThemeManager.get_theme(current_theme_name)
        # Update modal style
        page.bottom_sheet = ft.BottomSheet(
            ft.Container(
                content=ft.Column([
                    ft.Text("Nova Tarefa", size=18, weight=ft.FontWeight.BOLD, color=theme.text_color),
                    ft.Row([
                        new_task_input,
                        ft.IconButton(icon=ft.Icons.SEND_ROUNDED, icon_color=theme.primary_color, on_click=add_task_action)
                    ])
                ], tight=True),
                padding=20,
                bgcolor=theme.background_color,
                border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ),
            on_dismiss=lambda e: print("Dismissed")
        )
        new_task_input.text_color = theme.text_color
        new_task_input.focus()
        page.bottom_sheet.open = True
        page.update()

    def update_theme(name):
        nonlocal current_theme_name
        current_theme_name = name
        t = ThemeManager.apply_theme(page, name)
        save_state()
        
        # Update Controls
        fab.bgcolor = t.primary_color
        fab.content = ft.Icon(ft.Icons.ADD, color=t.background_color)
        
        bg_image.src = t.background_image if t.background_image else ""
        bg_image.opacity = 0.3 if t.background_image else 0
        
        main_container.bgcolor = ft.Colors.with_opacity(t.glass_opacity, t.background_color)
        
        update_header_and_settings()
        render_tasks()
        page.update()

    def update_bias(name):
        nonlocal current_bias
        current_bias = name
        save_state()
        update_header_and_settings()
        page.update()

    def build_settings_drawer():
        theme = ThemeManager.get_theme(current_theme_name)

        def on_theme_click(e):
            update_theme(e.control.data)
            # Rebuild drawer to show selection
            page.close_end_drawer()

        def on_bias_click(e):
            update_bias(e.control.data)
            page.close_end_drawer()

        # Theme Options
        theme_controls = []
        for t_name in ["purple", "butter", "dynamite", "dark"]:
            t = ThemeManager.get_theme(t_name)
            is_active = (t_name == current_theme_name)
            theme_controls.append(
                ft.Container(
                    width=50, height=50, border_radius=25,
                    bgcolor=t.primary_color,
                    border=ft.border.all(3, ft.Colors.WHITE if is_active else "transparent"),
                    on_click=on_theme_click,
                    data=t_name,
                    tooltip=t.name,
                    content=ft.Icon(ft.Icons.CHECK, color="white", size=20) if is_active else None
                )
            )

        # Bias Options
        biases = ["RM", "Jin", "Suga", "J-Hope", "Jimin", "V", "Jungkook"]
        bias_controls = []
        for b in biases:
            is_active = (b == current_bias)
            bias_controls.append(
                ft.Chip(
                    label=ft.Text(b),
                    selected=is_active,
                    on_select=on_bias_click,
                    data=b,
                    check_color=theme.background_color,
                    selected_color=theme.primary_color,
                    label_style=ft.TextStyle(color=theme.text_color if not is_active else theme.background_color)
                )
            )

        content = ft.Container(
            content=ft.Column([
                ft.Text("Configurações", size=22, weight="bold", color=theme.text_color),
                ft.Divider(color=theme.text_color),
                
                ft.Text("Escolha o Tema", size=16, weight="bold", color=theme.text_color),
                ft.Row(theme_controls, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(color=theme.text_color),
                
                ft.Text("Seu Bias", size=16, weight="bold", color=theme.text_color),
                ft.Row(bias_controls, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(color=theme.text_color),
                ft.Text("Versão 2.0 💜", size=12, color=theme.text_color, opacity=0.5, text_align=ft.TextAlign.CENTER)
            ], spacing=20, scroll=ft.ScrollMode.AUTO),
            padding=30,
            bgcolor=ft.Colors.with_opacity(0.95, theme.background_color),
            expand=True
        )
        return content

    def show_settings_modal(e):
        settings_drawer.controls = [build_settings_drawer()]
        page.end_drawer = settings_drawer
        page.show_end_drawer(settings_drawer)

    # --- Final Assembly ---
    
    settings_btn.on_click = show_settings_modal
    fab.on_click = show_add_task_modal

    # Compose Main Container
    main_container.content = ft.Column([
        ft.Row(
            [header_text, settings_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        progress_text,
        progress_bar,
        ft.Divider(color="transparent", height=10),
        task_list_view
    ])

    # Initial Theme Application
    update_theme(current_theme_name)

    # Add to Page
    page.add(
        ft.Stack(
            [
                bg_image,
                ft.Row(
                    [main_container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                lottie_container
            ],
            expand=True
        )
    )
    page.floating_action_button = fab

ft.app(target=main, assets_dir=".")
