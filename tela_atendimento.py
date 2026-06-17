import flet as ft
from sushi_data import SushiDataManager

class TelaAtendimento(ft.Container):
    def __init__(self, dm: SushiDataManager, on_pedido_finalizado=None):
        super().__init__()
        self.dm = dm
        self.on_pedido_finalizado = on_pedido_finalizado
        self.carrinho = {}  # {combo_id: quantidade}

        # UI Elements
        self.endereco_input = ft.TextField(
            label="Endereço / Cliente",
            hint_text="Rua, número ou nome WhatsApp",
            expand=True,
            border_color=ft.Colors.BLUE_400,
            text_size=16
        )

        self.carrinho_list_view = ft.Column(spacing=5)
        self.carrinho_container = ft.Container(
            content=ft.Column([
                ft.Text("Carrinho Atual", weight=ft.FontWeight.BOLD, size=16),
                self.carrinho_list_view
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            visible=False
        )

        self.btn_finalizar = ft.ElevatedButton(
            content=ft.Text("FINALIZAR PEDIDO"),
            icon=ft.Icons.CHECK_CIRCLE,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            disabled=True,
            on_click=self.finalizar_pedido,
            expand=True
        )

        self.combos_grid = self._construir_grid_combos()

        self.content = ft.Column([
            ft.Text("Novo Pedido", size=24, weight=ft.FontWeight.BOLD),
            self.endereco_input,
            ft.Divider(),
            ft.Text("Combos Rápidos", size=18, weight=ft.FontWeight.W_500),
            self.combos_grid,
            ft.Divider(),
            self.carrinho_container,
            ft.Row([self.btn_finalizar])
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

        self.padding = 20
        self.expand = True

    def _construir_grid_combos(self):
        combos = self.dm.obter_combos()
        botoes = []
        for combo_id, combo_info in combos.items():
            btn = ft.Container(
                content=ft.Text(combo_info["nome"], text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.BLUE_500,
                padding=20,
                border_radius=12,
                alignment=ft.alignment.center,
                on_click=self.criar_on_combo_click(combo_id),
                # Responsive width for mobile
                col={"xs": 12, "sm": 6, "md": 4}
            )
            botoes.append(btn)

        return ft.ResponsiveRow(botoes)

    def criar_on_combo_click(self, combo_id):
        def on_click(e):
            # Incrementa o item (Requisito)
            if combo_id in self.carrinho:
                self.carrinho[combo_id] += 1
            else:
                self.carrinho[combo_id] = 1
            self.atualizar_carrinho_ui()
        return on_click

    def remover_item(self, combo_id):
        if combo_id in self.carrinho:
            del self.carrinho[combo_id]
            self.atualizar_carrinho_ui()

    def atualizar_carrinho_ui(self):
        self.carrinho_list_view.controls.clear()
        combos = self.dm.obter_combos()

        if not self.carrinho:
            self.carrinho_container.visible = False
            self.btn_finalizar.disabled = True
        else:
            self.carrinho_container.visible = True
            self.btn_finalizar.disabled = False

            for combo_id, qtd in self.carrinho.items():
                nome = combos[combo_id]["nome"]
                item_row = ft.Row([
                    ft.Text(f"{qtd}x {nome}", expand=True, weight=ft.FontWeight.W_500),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_400,
                        on_click=lambda e, cid=combo_id: self.remover_item(cid)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                self.carrinho_list_view.controls.append(item_row)

        self.update()

    def finalizar_pedido(self, e):
        endereco = self.endereco_input.value.strip()
        if not endereco:
            # Feedback visual se esqueceu o endereço
            self.endereco_input.border_color = ft.Colors.RED
            self.endereco_input.focus()
            self.update()

            # Show snackbar
            self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha o endereço/cliente!"), bgcolor=ft.Colors.RED_700)
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Registrar no DM
        self.dm.registrar_pedido(endereco, self.carrinho)

        # Sucesso
        self.page.snack_bar = ft.SnackBar(ft.Text("Pedido lançado com sucesso! Insumos descontados."), bgcolor=ft.Colors.GREEN_700)
        self.page.snack_bar.open = True
        self.page.update()

        # Resetar Tela
        self.endereco_input.value = ""
        self.endereco_input.border_color = ft.Colors.BLUE_400
        self.carrinho = {}
        self.atualizar_carrinho_ui()

        # Callback para atualizar a tela de estoque (Tela 2) se necessário
        if self.on_pedido_finalizado:
            self.on_pedido_finalizado()
