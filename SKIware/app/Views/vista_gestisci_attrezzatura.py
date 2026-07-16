from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget)
from Services import GestoreAttrezzatura
from Views.vista_attrezzatura import VistaAttrezzatura
from Views.vista_inserisci_attrezzatura import VistaInserisciAttrezzatura

class VistaGestisciAttrezzatura(QWidget): # Boundary
    # vista principale del package GestioneAttrezzatura 
    def __init__(self, gestore_attrezzatura: GestoreAttrezzatura):
        super().__init__()
        self._gestore = gestore_attrezzatura 
        self.setWindowTitle("Gestione Attrezzatura")

        self.attrezzature: list = [] 
        self.list_view = QListWidget() 

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.list_view)
        h_layout = QHBoxLayout()
        self.bottone_nuovo = QPushButton("Nuova attrezzatura")
        self.bottone_nuovo.clicked.connect(self.show_new)
        h_layout.addWidget(self.bottone_nuovo)
        self.bottone_info = QPushButton("Info attrezzatura selezionata")
        self.bottone_info.clicked.connect(self.show_selected_info)
        h_layout.addWidget(self.bottone_info)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

        self.load_attrezzatura()
        self.update_ui()

    
    def load_attrezzatura(self) -> None:
        self.attrezzature = self._gestore.elencaServizi()

   
    def update_ui(self) -> None:
        self.list_view.clear()
        for servizio in self.attrezzature:
            self.list_view.addItem(str(servizio))

    
    def show_new(self) -> None:
        self.vista_inserisci = VistaInserisciAttrezzatura(self._aggiungi_attrezzatura)
        self.vista_inserisci.show()

    # callback per VistaInserisciAttrezzatura: smista al metodo giusto del
    # Control in base al tipo scelto nella combo
    def _aggiungi_attrezzatura(self, tipo: str, codice: str, descrizione: str,
                               prezzo: float, extra: str) -> str:
        if tipo == "Sci":
            esito = self._gestore.aggiungiSci(codice, descrizione, prezzo, extra)
        elif tipo == "Snowboard":
            esito = self._gestore.aggiungiSnowboard(codice, descrizione, prezzo, extra)
        elif tipo == "Scarpone":
            esito = self._gestore.aggiungiScarpone(codice, descrizione, prezzo)
        elif tipo == "Casco":
            esito = self._gestore.aggiungiCasco(codice, descrizione, prezzo)
        else: # Armadietto
            esito = self._gestore.aggiungiArmadietto(codice, descrizione, prezzo, extra)
        self.load_attrezzatura()
        self.update_ui()
        return esito

    
    def show_selected_info(self) -> None:
        riga = self.list_view.currentRow()
        if riga < 0 or riga >= len(self.attrezzature):
            return
        self.vista_attrezzatura = VistaAttrezzatura(self.attrezzature[riga],
                                                    self._elimina_attrezzatura)
        self.vista_attrezzatura.show()

    # callback per VistaAttrezzatura
    def _elimina_attrezzatura(self, servizio) -> str:
        esito = self._gestore.rimuoviServizio(servizio.getCodice())
        self.load_attrezzatura()
        self.update_ui()
        return esito
