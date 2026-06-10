import flet as ft
from sushi_data import SushiDataManager

class TelaEstoque(ft.Container):
    def __init__(self, dm: SushiDataManager):
        super().__init__()
        self.dm = dm

        self.insumos_list = ft.Column(spacing=15, expand=True, scroll=ft.ScrollMode.AUTO)

        self.btn_atualizar_estoque = ft.ElevatedButton(
            text="Definir Estoque Inicial",
            icon=ft.Icons.EDIT_DOCUMENT,
            on_click=self.mostrar_modal_estoque,
            style=ft.ButtonStyle(
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        self.content = ft.Column([
            ft.Text("Retaguarda / Estoque", size=24, weight=ft.FontWeight.BOLD),
            self.btn_atualizar_estoque,
            ft.Divider(),
            ft.Text("Consumo em Tempo Real", size=18, weight=ft.FontWeight.W_500),
            self.insumos_list
        ], spacing=15, expand=True)

        self.padding = 20
        self.expand = True

        self.atualizar_lista()

    def atualizar_lista(self):
        self.insumos_list.controls.clear()
        insumos = self.dm.obter_insumos()

        for insumo_id, info in insumos.items():
            usado = info["usado"]
            total = info["total"]

            # Evitar divisão por zero e calcular porcentagem
            perc = 0
            if total > 0:
                perc = usado / total
                if perc > 1.0:
                    perc = 1.0 # Cap em 100%

            # Cor da barra
            cor_barra = ft.Colors.GREEN
            if perc > 0.7:
                cor_barra = ft.Colors.AMBER
            if perc > 0.9:
                cor_barra = ft.Colors.RED

            info_text = f"Usado: {usado} / {total} {info['nome'].split('(')[-1].replace(')', '').strip()}"
            if usado >= total:
                info_text += " (ESGOTADO!)"

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(info["nome"], weight=ft.FontWeight.BOLD),
                        ft.Text(f"{int(perc*100)}%", weight=ft.FontWeight.BOLD, color=cor_barra)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.ProgressBar(value=perc, color=cor_barra, bgcolor=ft.Colors.GREY_300, height=8),
                    ft.Text(info_text, size=12, color=ft.Colors.GREY_700)
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8
            )
            self.insumos_list.controls.append(card)

        self.update()

    def mostrar_modal_estoque(self, e):
        insumos = self.dm.obter_insumos()
        inputs = {}

        content_controls = [ft.Text("Atualizar Estoque Inicial", weight=ft.FontWeight.BOLD, size=18)]

        for insumo_id, info in insumos.items():
            inp = ft.TextField(
                label=info["nome"],
                value=str(info["total"]),
                keyboard_type=ft.KeyboardType.NUMBER
            )
            inputs[insumo_id] = inp
            content_controls.append(inp)

        def salvar(e):
            novos_totais = {}
            for i_id, inp_ctrl in inputs.items():
                try:
                    novos_totais[i_id] = int(inp_ctrl.value)
                except ValueError:
                    novos_totais[i_id] = insumos[i_id]["total"]

            self.dm.atualizar_estoque_inicial(novos_totais)
            self.atualizar_lista()
            self.page.close_dialog()
            self.page.snack_bar = ft.SnackBar(ft.Text("Estoque atualizado!"), bgcolor=ft.Colors.GREEN)
            self.page.snack_bar.open = True
            self.page.update()

        dialog = ft.AlertDialog(
            content=ft.Column(content_controls, scroll=ft.ScrollMode.AUTO, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close_dialog()),
                ft.TextButton("Salvar", on_click=salvar, style=ft.ButtonStyle(color=ft.Colors.GREEN))
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
