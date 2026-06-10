import json
import os

DB_FILE = "sushi_db.json"

DEFAULT_DATA = {
    "insumos": {
        "salmao": {"nome": "Salmão (g)", "total": 5000, "usado": 0},
        "arroz": {"nome": "Arroz (g)", "total": 10000, "usado": 0},
        "alga": {"nome": "Alga (folhas)", "total": 100, "usado": 0},
        "cream_cheese": {"nome": "Cream Cheese (g)", "total": 2000, "usado": 0}
    },
    "combos": {
        "combo_casal": {
            "nome": "Combo Casal (40 peças)",
            "receita": {"salmao": 400, "arroz": 600, "alga": 5, "cream_cheese": 100}
        },
        "combinado_especial": {
            "nome": "Combinado Especial (60 peças)",
            "receita": {"salmao": 600, "arroz": 800, "alga": 8, "cream_cheese": 150}
        },
        "temaki_salmao": {
            "nome": "Temaki de Salmão",
            "receita": {"salmao": 80, "arroz": 100, "alga": 1, "cream_cheese": 30}
        }
    },
    "pedidos": []
}

class SushiDataManager:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """Carrega os dados do JSON ou inicializa com DEFAULT_DATA se não existir."""
        import copy
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao ler banco de dados: {e}. Usando dados padrão.")
                return copy.deepcopy(DEFAULT_DATA)
        else:
            return copy.deepcopy(DEFAULT_DATA)

    def save_data(self):
        """Salva o estado atual da memória no arquivo JSON de forma imediata."""
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def registrar_pedido(self, endereco, carrinho):
        """
        Registra um novo pedido no histórico e debita os insumos imediatamente.
        Salva no disco (persistência imediata).

        :param endereco: str, Endereço do cliente
        :param carrinho: dict, Ex: {"combo_casal": 2, "temaki_salmao": 1}
        """
        # 1. Registrar no histórico
        novo_pedido = {
            "endereco": endereco,
            "itens": carrinho
        }
        self.data["pedidos"].append(novo_pedido)

        # 2. Debitar insumos baseado na receita e quantidades
        for combo_id, quantidade in carrinho.items():
            if combo_id in self.data["combos"]:
                receita = self.data["combos"][combo_id]["receita"]
                for insumo_id, qtd_necessaria in receita.items():
                    if insumo_id in self.data["insumos"]:
                        gasto_total = qtd_necessaria * quantidade
                        self.data["insumos"][insumo_id]["usado"] += gasto_total

        # 3. Persistência Imediata (Requisito)
        self.save_data()

    def atualizar_estoque_inicial(self, novos_totais):
        """
        Atualiza a quantidade inicial de insumos (para o começo da noite).
        :param novos_totais: dict, Ex: {"salmao": 6000, "arroz": 12000}
        """
        for insumo_id, qtd in novos_totais.items():
            if insumo_id in self.data["insumos"]:
                self.data["insumos"][insumo_id]["total"] = qtd
                # Resetar os gastos? Para este MVP vamos assumir que apenas atualiza o total,
                # e o log de "usado" continua válido. Opcionalmente podemos criar um "reset_diario".
        self.save_data()

    def obter_insumos(self):
        return self.data.get("insumos", {})

    def obter_combos(self):
        return self.data.get("combos", {})

    def obter_pedidos(self):
        return self.data.get("pedidos", [])

    def resetar_noite(self):
        """Reseta o uso de insumos e limpa os pedidos (opcional)."""
        self.data["pedidos"] = []
        for insumo in self.data["insumos"].values():
            insumo["usado"] = 0
        self.save_data()
