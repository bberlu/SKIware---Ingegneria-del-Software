from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget)
from Services import GestoreCarnet, GestoreUtenti
from Views.vista_carnet import VistaCarnet
from Views.vista_inserisci_carnet import VistaInserisciCarnet

class VistaGestisciCarnet(QWidget): # Boundary
    # vista principale del package GestioneCarnet 
    def __init__(self, gestore_carnet: GestoreCarnet,
                 gestore_utenti: GestoreUtenti):
        super().__init__()
        self._gestore        = gestore_carnet 
        self._gestore_utenti = gestore_utenti # serve per la combo dei clienti
        self.setWindowTitle("Gestione Carnet")

        self.carnet: list = [] 
        self.list_view = QListWidget() 

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.list_view)
        h_layout = QHBoxLayout()
        self.bottone_nuovo = QPushButton("Vendi carnet")
        self.bottone_nuovo.clicked.connect(self.show_new)
        h_layout.addWidget(self.bottone_nuovo)
        self.bottone_info = QPushButton("Info carnet selezionato")
        self.bottone_info.clicked.connect(self.show_selected_info)
        h_layout.addWidget(self.bottone_info)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

        self.load_carnet() 
        self.update_ui()

    
    def load_carnet(self) -> None:
        self.carnet = self._gestore.elencaCarnet()

    
    def update_ui(self) -> None:
        self.list_view.clear()
        for carnet in self.carnet:
            self.list_view.addItem(str(carnet))

   
    def show_new(self) -> None:
        self.vista_inserisci = VistaInserisciCarnet(
            self._vendi_carnet,
            self._gestore_utenti.elencaClienti) # provider dei clienti per la combo
        self.vista_inserisci.show()

    # callback per VistaInserisciCarnet: gira la vendita al Control
    def _vendi_carnet(self, cliente, tipo: int, stagionale: bool) -> str:
        carnet = self._gestore.vendiCarnet(cliente, tipo, stagionale)
        self.load_carnet()
        self.update_ui()
        return f"Vendita ok: {carnet}"

    def show_selected_info(self) -> None:
        riga = self.list_view.currentRow()
        if riga < 0 or riga >= len(self.carnet):
            return
        self.vista_carnet = VistaCarnet(self.carnet[riga], self._elimina_carnet)
        self.vista_carnet.show()

    # callback per VistaCarnet
    def _elimina_carnet(self, carnet) -> str:
        esito = self._gestore.rimuoviCarnet(carnet.getCodice())
        self.load_carnet()
        self.update_ui()
        return esito
