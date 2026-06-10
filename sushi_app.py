import flet as ft
from sushi_data import SushiDataManager
from tela_atendimento import TelaAtendimento
from tela_estoque import TelaEstoque

def main(page: ft.Page):
    page.title = "Sushi Delivery MVP"
    # Mobile first constraints e tema
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    dm = SushiDataManager()

    # Instanciando as telas
    tela_estoque = TelaEstoque(dm=dm)

    # Ao finalizar o pedido na tela 1, atualiza a tela 2
    tela_atendimento = TelaAtendimento(
        dm=dm,
        on_pedido_finalizado=tela_estoque.atualizar_lista
    )

    # Container principal onde as telas serão alternadas
    main_container = ft.Container(
        content=tela_atendimento, # Começa no atendimento
        expand=True
    )

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            main_container.content = tela_atendimento
        elif idx == 1:
            tela_estoque.atualizar_lista()
            main_container.content = tela_estoque
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.POINT_OF_SALE, label="Atendimento"),
            ft.NavigationDestination(icon=ft.Icons.INVENTORY, label="Estoque"),
        ],
        on_change=on_nav_change,
        selected_index=0
    )

    page.add(main_container)

if __name__ == "__main__":
    ft.app(target=main)
