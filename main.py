import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt

from pdf_generator import create_baggage_pdf

class BaggageControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Controle de Bagagem")
        self.resize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Form layout
        form_layout = QHBoxLayout()
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        form_layout.addWidget(self.nome_input)

        self.cidade_input = QLineEdit()
        self.cidade_input.setPlaceholderText("Cidade")
        form_layout.addWidget(self.cidade_input)

        self.poltrona_input = QLineEdit()
        self.poltrona_input.setPlaceholderText("Poltrona")
        form_layout.addWidget(self.poltrona_input)

        self.add_btn = QPushButton("Adicionar")
        self.add_btn.clicked.connect(self.add_passenger)
        form_layout.addWidget(self.add_btn)

        layout.addLayout(form_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Nome", "Cidade", "Poltrona"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons layout
        btn_layout = QHBoxLayout()
        
        self.remove_btn = QPushButton("Remover Selecionado")
        self.remove_btn.clicked.connect(self.remove_passenger)
        btn_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("Limpar Tudo")
        self.clear_btn.clicked.connect(self.clear_passengers)
        btn_layout.addWidget(self.clear_btn)

        btn_layout.addStretch()

        self.copies_label = QLabel("Cópias:")
        btn_layout.addWidget(self.copies_label)
        self.copies_spin = QSpinBox()
        self.copies_spin.setRange(1, 100)
        self.copies_spin.setValue(20)
        btn_layout.addWidget(self.copies_spin)

        self.generate_btn = QPushButton("Gerar PDF Preenchido")
        self.generate_btn.clicked.connect(self.generate_pdf)
        self.generate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        btn_layout.addWidget(self.generate_btn)

        self.generate_blank_btn = QPushButton("Gerar PDF em Branco")
        self.generate_blank_btn.clicked.connect(self.generate_blank_pdf)
        self.generate_blank_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        btn_layout.addWidget(self.generate_blank_btn)

        layout.addLayout(btn_layout)

    def add_passenger(self):
        nome = self.nome_input.text().strip()
        cidade = self.cidade_input.text().strip()
        poltrona = self.poltrona_input.text().strip()

        if nome or cidade or poltrona:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(nome))
            self.table.setItem(row, 1, QTableWidgetItem(cidade))
            self.table.setItem(row, 2, QTableWidgetItem(poltrona))

            self.nome_input.clear()
            self.cidade_input.clear()
            self.poltrona_input.clear()
            self.nome_input.setFocus()

    def remove_passenger(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def clear_passengers(self):
        self.table.setRowCount(0)

    def get_passengers_from_table(self):
        passengers = []
        for row in range(self.table.rowCount()):
            nome = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            cidade = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            poltrona = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            passengers.append({"nome": nome, "cidade": cidade, "poltrona": poltrona})
        return passengers

    def generate_pdf(self):
        passengers = self.get_passengers_from_table()
        if not passengers:
            QMessageBox.warning(self, "Aviso", "Nenhum passageiro adicionado.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Salvar PDF Preenchido", "controle_bagagem_preenchido.pdf", "PDF Files (*.pdf)")
        if filename:
            copies = self.copies_spin.value()
            try:
                # Resolve path to logo which should be in the same dir as the main script or within /app/assets
                logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
                create_baggage_pdf(filename, passengers, copies=copies, logo_path=logo_path)
                QMessageBox.information(self, "Sucesso", "PDF gerado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF: {e}")

    def generate_blank_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Salvar PDF em Branco", "controle_bagagem_branco.pdf", "PDF Files (*.pdf)")
        if filename:
            copies = self.copies_spin.value()
            try:
                logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
                create_baggage_pdf(filename, [], copies=copies, logo_path=logo_path)
                QMessageBox.information(self, "Sucesso", "PDF em branco gerado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaggageControlApp()
    window.show()
    sys.exit(app.exec())
