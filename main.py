import flet as ft
import flet_audio as fa
import flet_lottie as fl # RE-INTRODUZIDO Lottie
import asyncio 
import json 
import os   

# Definindo cores temáticas
PURPLE_LIGHT = "#d9b3ff"
PURPLE_DARK = "#a259ff"
COLOR_PENDING_BAR = "#9966CC" 
COLOR_NEON_GLOW = "#EE82EE"
CONTAINER_OPACITY = 0.85 
INITIAL_BLUR = 3.0
DEFAULT_OPACITY = 0.70 

# Variáveis Globais de Estado
user_bias_icon = ft.Icons.TAG_FACES_OUTLINED 
CONFIG_FILE = "config.json"


# ---------------------- FUNÇÕES DE PERSISTÊNCIA JSON ----------------------

def load_config():
    """Carrega o estado do app (tarefas, bias, opacidade) do JSON."""
    global user_bias_icon
    
    loaded_tasks_strings = []
    loaded_opacity = DEFAULT_OPACITY
    bias_icon_name = "TAG_FACES_OUTLINED"

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                loaded_tasks_strings = config.get("tasks", [])
                loaded_opacity = config.get("opacity", DEFAULT_OPACITY)
                bias_icon_name = config.get("bias_icon_name", "TAG_FACES_OUTLINED")
                
                if hasattr(ft.Icons, bias_icon_name.upper()):
                     user_bias_icon = getattr(ft.Icons, bias_icon_name.upper())
                
        except Exception as e:
            print(f"Erro ao carregar config.json, usando padrões: {e}")
            pass 
            
    return loaded_tasks_strings, loaded_opacity

# ---------------------- CRIAÇÃO DO OVERLAY (LOTTIE + TEXTO) ----------------------

def create_animated_overlay(page: ft.Page):
    """Cria e retorna o controle de texto animado e o Lottie para o overlay."""
    
    congrats_text = ft.Text(
        "🎉 Parabéns, Fedida! Você é incrível! 💜",
        size=30, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.WHITE,
        animate_scale=ft.Animation(500, ft.AnimationCurve.ELASTIC_OUT),
        animate_opacity=ft.Animation(300),
        scale=0.5, 
        opacity=0.0, 
    )
    
    # Lottie Control (Usando o link do GitHub que funciona)
    success_lottie = fl.Lottie(
        src="https://gist.githubusercontent.com/Guinogyy/1cb8bdd4a7ee13e789f373060a5e980f/raw/d753be492b51beb881adaf163bc04a45324669e7/gistfile1.txt", 
        repeat=False,
        animate=False,
        width=250, 
        height=250,
        # 'alignment' foi removido para evitar o TypeError
    )
    
    # Empacota ambos (Lottie e Texto) em uma Coluna
    container = ft.Container(
        ft.Column([success_lottie, congrats_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        visible=False,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
    )
    # Retorna o container principal E a referência ao controle Lottie
    return container, success_lottie


# ---------------------- FUNÇÃO PRINCIPAL ----------------------

async def main(page: ft.Page): 
    # Carrega as configurações ANTES de construir a UI
    loaded_tasks, loaded_opacity = load_config()

    page.title = "💜 To-Do List BTS Pro Edition 💜"
    page.bgcolor = ft.Colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START 
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    page.scroll = ft.ScrollMode.AUTO 

    tasks = [] 
    
    # ---------------------- ÁUDIO ----------------------
    audio_player = fa.Audio(src="audios/success.mp3", autoplay=False)
    page.overlay.append(audio_player)

    # ---------------------- ANIMAÇÃO DE PARABÉNS (INICIALIZAÇÃO) ----------------------
    animated_congrats, lottie_control = create_animated_overlay(page)
    page.overlay.append(animated_congrats)

    async def animate_congrats():
        """Lógica assíncrona para mostrar e esconder a animação de parabéns."""
        text_control = animated_congrats.content.controls[1]
        
        # 1. Mostrar e animar
        animated_congrats.visible = True
        lottie_control.animate = True # Inicia a animação Lottie
        text_control.scale = 1.0 
        text_control.opacity = 1.0 
        page.update()
        
        # 2. Esperar 3 segundos
        await asyncio.sleep(3)
        
        # 3. Animar para sumir
        text_control.scale = 0.5 
        text_control.opacity = 0.0
        lottie_control.animate = False # Para a animação Lottie
        page.update() 
        
        await asyncio.sleep(0.5)
        animated_congrats.visible = False
        page.update()

    # ---------------------- FUNDO E UX ----------------------
    fundo_imagem = ft.Image(src="https://i.postimg.cc/B6b9m6H3/foto.jpg", fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT, width=page.width, height=page.height)
    fundo = ft.Container(expand=True, alignment=ft.alignment.center, content=fundo_imagem)

    # ---------------------- CONTROLES PRINCIPAIS (REFERÊNCIAS) ----------------------
    task_list = ft.ListView(spacing=12, auto_scroll=True)
    message = ft.Text("", size=18, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
    main_box_ref = ft.Ref[ft.Container]()
    task_list_container_ref = ft.Ref[ft.Container]()

    stats_chart = ft.BarChart(
        border=ft.border.all(1, ft.Colors.with_opacity(0.4, PURPLE_LIGHT)),
        horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.GREY_700, width=1, dash_pattern=[3, 3]),
        left_axis=ft.ChartAxis(labels_size=20, title=ft.Text("Contagem", size=10), title_size=15),
        bottom_axis=ft.ChartAxis(labels_size=25),
        max_y=5, interactive=False, height=180,
    )
    
    # ---------------------- FUNÇÃO DE SALVAR (JSON) ----------------------

    def save_all_settings():
        """Salva o estado atual (tarefas, opacidade, bias) no JSON."""
        
        task_strings = []
        for task_card in task_list.controls:
            list_tile = task_card.content.content.controls[0]
            checkbox = list_tile.title
            task_strings.append(checkbox.label) 

        current_opacity = opacity_slider.value
        current_bias_name = str(user_bias_icon).lower()

        config_data = {
            "tasks": task_strings,
            "opacity": current_opacity,
            "bias_icon_name": current_bias_name
        }
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
            print("Configurações salvas com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    # ---------------------- FUNÇÕES DE ESTADO E LÓGICA ----------------------

    def update_stats():
        """Calcula e atualiza o BarChart e a mensagem de conclusão."""
        done_count = 0
        current_tasks = task_list.controls
        
        for task_card in current_tasks:
            task_content = task_card.content.content.controls[0]
            checkbox = task_content.title 
            
            if checkbox.value:
                done_count += 1
                
        total_count = len(current_tasks)
        pending_count = total_count - done_count
        
        global tasks
        tasks = current_tasks[:] 
        
        # Lógica do Gráfico
        max_y = max(total_count + 1, 5) 
        stats_chart.max_y = max_y
        
        stats_chart.bar_groups = [
            ft.BarChartGroup(x=0, bar_rods=[ft.BarChartRod(to_y=done_count, width=30, color=PURPLE_LIGHT, border_radius=5)]),
            ft.BarChartGroup(x=1, bar_rods=[ft.BarChartRod(to_y=pending_count, width=30, color=COLOR_PENDING_BAR, border_radius=5)]),
        ]
        
        stats_chart.bottom_axis.labels = [
            ft.ChartAxisLabel(value=0, label=ft.Text(f"Feitas: {done_count}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.ChartAxisLabel(value=1, label=ft.Text(f"Pendentes: {pending_count}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
        ]
        
        # LÓGICA DE SUCESSO COM ANIMAÇÃO
        if total_count > 0 and pending_count == 0:
            audio_player.play() 
            page.run_task(animate_congrats) 
            message.value = "" 
        else:
            message.value = ""
        
        page.update()


    def toggle_task(e):
        """Alterna o estado da tarefa e atualiza estatísticas."""
        cb = e.control
        
        if cb.value: 
            cb.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
            cb.scale = 1.1 
        else:
            cb.scale = 1.0
            
        cb.update()
        update_stats() 
    
    
    def delete_task(e):
        """Remove a tarefa da lista e força o redesenho."""
        
        card_to_remove = e.control
        while card_to_remove.parent and card_to_remove.parent != task_list:
            card_to_remove = card_to_remove.parent
            
        if card_to_remove in task_list.controls:
            task_list.controls.remove(card_to_remove)
            task_list.update() 
            save_all_settings() # SALVA O JSON

        update_stats()


    def create_task_row(task_text):
        """Cria um Card/ListTile para a nova tarefa."""
        cb = ft.Checkbox(
            label=task_text,
            value=False,
            on_change=toggle_task,
            label_style=ft.TextStyle(color=ft.Colors.WHITE, size=16),
        )

        task_list_tile = ft.ListTile(
            leading=ft.Icon(user_bias_icon, color=PURPLE_LIGHT, size=24),
            title=cb, 
            trailing=ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.RED_ACCENT_100,
                icon_size=20,
                tooltip="Excluir Tarefa",
                on_click=delete_task,
                style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
            ),
            min_height=45,
        )
        
        task_card = ft.Card(
            content=ft.Container(
                content=ft.Column([task_list_tile], spacing=0),
                padding=ft.padding.symmetric(vertical=5, horizontal=10),
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            ),
            elevation=3,
            color=PURPLE_DARK, 
            margin=ft.margin.only(bottom=10)
        )
        return task_card


    def add_task(e):
        """Adiciona uma nova tarefa."""
        if new_task.value.strip() != "":
            task_card = create_task_row(new_task.value)

            task_list.controls.append(task_card)
            
            new_task.value = ""
            update_stats() 
            page.update()
            save_all_settings() # SALVA O JSON


    def change_background_start(e):
        """Função que dispara a abertura do seletor de arquivos."""
        file_picker.pick_files(allow_multiple=False)

    def on_file_picked(e: ft.FilePickerResultEvent):
        """Função de callback para trocar a imagem de fundo."""
        if e.files:
            fundo_imagem.src = e.files[0].path
            page.update()
            
    def change_panel_style(e):
        """Atualiza a opacidade e o blur do painel principal e da lista."""
        new_opacity = e.control.value 
        new_blur = max(0.0, (new_opacity - 0.1) * (5.0 / 0.9))
        
        main_box = main_box_ref.current
        task_list_container = task_list_container_ref.current

        main_box.bgcolor = ft.Colors.with_opacity(new_opacity, PURPLE_DARK)
        main_box.blur = ft.Blur(new_blur, new_blur, ft.BlurTileMode.CLAMP)
        
        task_list_container.bgcolor = ft.Colors.with_opacity(new_opacity * 0.5, ft.Colors.BLACK)
        
        page.update()
        save_all_settings() # SALVA O JSON
        
        
    def save_bias(e):
        """Salva o Bias e atualiza o ícone de adicionar tarefa."""
        bias_input_field = settings_panel.controls[3].controls[0]
        bias_name = bias_input_field.value.strip().upper()
        
        global user_bias_icon 
        if bias_name in ["V", "TAEHYUNG"]:
            user_bias_icon = ft.Icons.TAG_FACES_OUTLINED
        elif bias_name in ["JUNGKOOK", "JK"]:
            user_bias_icon = ft.Icons.MUSIC_NOTE_OUTLINED
        elif bias_name in ["RM", "NAMJOON"]:
            user_bias_icon = ft.Icons.BOOK_OUTLINED
        else:
            user_bias_icon = ft.Icons.PERSON_OUTLINE 
        
        # 1. Atualiza o ícone do botão de adicionar tarefa
        add_button.icon = user_bias_icon
        
        # 2. Fecha o painel de configurações
        settings_panel.expanded = False
        
        page.update()
        update_stats()
        save_all_settings() # SALVA O JSON

    # ---------------------- INTERFACE E LAYOUT (Criação de Variáveis de Interface) ----------------------
    
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    new_task = ft.TextField(
        hint_text="Adicionar nova tarefa...",
        border_color=PURPLE_LIGHT,
        color=ft.Colors.WHITE,
        cursor_color=PURPLE_LIGHT,
        bgcolor=ft.Colors.with_opacity(0.25, PURPLE_DARK),
        on_submit=add_task,
        expand=True,
    )

    add_button = ft.IconButton(
        icon=user_bias_icon, # Usa o ícone carregado
        icon_color=PURPLE_LIGHT,
        tooltip="Adicionar tarefa",
        on_click=add_task,
    )

    change_bg_button = ft.IconButton(
        icon=ft.Icons.IMAGE_OUTLINED,
        icon_color=PURPLE_LIGHT,
        tooltip="Trocar imagem de fundo",
        on_click=change_background_start,
    )
    
    opacity_slider = ft.Slider(
        min=0.1, max=1.0, 
        value=loaded_opacity, # Usa o valor carregado
        divisions=9, 
        label="Opacidade: {value:.1f}", active_color=PURPLE_LIGHT, 
        inactive_color=ft.Colors.WHITE30, on_change=change_panel_style, expand=True
    )
    
    bias_input_field = ft.TextField(
        hint_text="Qual o Bias (Membro Favorito)? V, JK, RM...",
        color=ft.Colors.WHITE,
        border_color=PURPLE_LIGHT,
        expand=True,
    )
    
    settings_panel = ft.ExpansionTile(
        title=ft.Text("Configurações de Fundo e Estilo", size=14, color=ft.Colors.WHITE54, weight=ft.FontWeight.W_300),
        leading=ft.Icon(ft.Icons.SETTINGS, color=PURPLE_LIGHT, 
            shadows=[ft.BoxShadow(spread_radius=1, blur_radius=5, color=COLOR_NEON_GLOW)]), 
        trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN_ROUNDED, color=ft.Colors.WHITE54),
        collapsed_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        tile_padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.BRIGHTNESS_LOW_ROUNDED, color=PURPLE_LIGHT, shadows=[ft.BoxShadow(spread_radius=1, blur_radius=5, color=COLOR_NEON_GLOW)]),
                opacity_slider,
                ft.Icon(ft.Icons.BRIGHTNESS_HIGH_ROUNDED, color=PURPLE_LIGHT, shadows=[ft.BoxShadow(spread_radius=1, blur_radius=5, color=COLOR_NEON_GLOW)]),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text(
                "Ajuste a barra para ver mais ou menos a imagem de fundo do BTS (Opacidade do Painel).",
                size=11, color=ft.Colors.WHITE54, italic=True, text_align=ft.TextAlign.CENTER
            ),
            ft.Divider(color=ft.Colors.WHITE10),
            ft.Row([
                bias_input_field, 
                ft.ElevatedButton("Salvar Bias", on_click=save_bias, color=ft.Colors.BLACK, bgcolor=PURPLE_LIGHT),
            ]),
        ]
    )

    task_list_container = ft.Container(
        ref=task_list_container_ref,
        expand=True, 
        content=task_list, 
        padding=ft.padding.all(5),
        bgcolor=ft.Colors.with_opacity(loaded_opacity * 0.5, ft.Colors.BLACK), 
        border_radius=10 
    )
    
    # CONTAINER PRINCIPAL COM GLOW (GLASSMORPHISM)
    main_box = ft.Container(
        ref=main_box_ref, 
        width={"xs": "85%", "sm": "70%", "md": 450}, 
        expand=True, 
        bgcolor=ft.Colors.with_opacity(loaded_opacity, PURPLE_DARK), 
        border_radius=25,
        padding=25,
        blur=ft.Blur(INITIAL_BLUR, INITIAL_BLUR, ft.BlurTileMode.CLAMP), 
        
        shadow=ft.BoxShadow( # Corrigido para 'shadow' (singular)
            spread_radius=1,
            blur_radius=20,
            color=PURPLE_LIGHT, 
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        
        content=ft.Column(
            [
                ft.Row(
                    [
                        # Título principal (Sem sombra para estabilidade)
                        ft.Text(
                            "💜 To-Do List Emanuelly 💜",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                            expand=True,
                        ),
                        change_bg_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                
                settings_panel, 
                
                ft.Row([new_task, add_button]), 
                
                ft.Divider(color=ft.Colors.WHITE30),

                task_list_container,
                
                message,
                
                ft.Divider(color=ft.Colors.WHITE30),

                ft.Text("Estatísticas de Tarefas", size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=stats_chart, 
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                    border_radius=10,
                    padding=10,
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )
    
    # Preenche a lista com as tarefas salvas no JSON
    for task_text in loaded_tasks:
        task_list.controls.append(create_task_row(task_text))
    
    update_stats()

    page.add(
        ft.Stack(
            [
                fundo,
                ft.Container(alignment=ft.alignment.top_center, content=main_box, padding=ft.padding.symmetric(vertical=25, horizontal=0), expand=True),
            ]
        )
    )

# ---------------------- CHAMADA FINAL DO APP (COM ASSETS) ----------------------
ft.app(
    target=main,
    assets_dir="." # Informa ao Flet para incluir todas as pastas (lottie/, audios/, fotos/)
)