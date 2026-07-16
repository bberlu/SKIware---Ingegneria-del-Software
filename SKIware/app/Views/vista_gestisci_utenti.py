from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget)
from Models import Cliente, SkiMan
from Services import GestoreUtenti
from Views.vista_utente import VistaUtente
from Views.vista_inserisci_utente import VistaInserisciUtente

class VistaGestisciUtenti(QWidget): # Boundary
    # vista principale del package GestioneUtenti
    # elenca tutti gli utilizzatori (clienti, ski-man, amministratori) e apre
    # le viste di dettaglio e di inserimento.
    def __init__(self, gestore_utenti: GestoreUtenti):
        super().__init__()
        self._gestore = gestore_utenti
        self.setWindowTitle("Gestione Utenti")

        self.utenti: list = [] 
        self.list_view = QListWidget() 

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.list_view)
        h_layout = QHBoxLayout()
        self.bottone_nuovo = QPushButton("Nuovo utente")
        self.bottone_nuovo.clicked.connect(self.show_new)
        h_layout.addWidget(self.bottone_nuovo)
        self.bottone_info = QPushButton("Info utente selezionato")
        self.bottone_info.clicked.connect(self.show_selected_info)
        h_layout.addWidget(self.bottone_info)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

        self.load_utenti() 
        self.update_ui()

    
    def load_utenti(self) -> None:
        self.utenti = self._gestore.elencaUtilizzatori()

    
    def update_ui(self) -> None:
        self.list_view.clear()
        for utente in self.utenti:
            self.list_view.addItem(str(utente))

    def show_new(self) -> None:
        self.vista_inserisci = VistaInserisciUtente(self._aggiungi_utente)
        self.vista_inserisci.show()

    # callback per VistaInserisciUtente
    def _aggiungi_utente(self, tipo: str, v: dict) -> str:
        if tipo == "Cliente":
            esito = self._gestore.aggiungiCliente(
                v["codice"], v["codiceFiscale"], v["cognome"], v["email"],
                v["nome"], v["password"], v["telefono"], v["altezza"],
                v["eta"], v["livelloAbilita"], v["misuraScarponi"], v["peso"])
        elif tipo == "Ski-man":
            esito = self._gestore.aggiungiSkiMan(
                v["codice"], v["codiceFiscale"], v["cognome"], v["email"],
                v["nome"], v["password"], v["telefono"], v["dataNascita"],
                v["luogoNascita"], v["qualificaTecnica"])
        else: # Amministratore
            esito = self._gestore.aggiungiAmministratore(
                v["codice"], v["codiceFiscale"], v["cognome"], v["email"],
                v["nome"], v["password"], v["telefono"])
        self.load_utenti()
        self.update_ui()
        return esito


    def show_selected_info(self) -> None:
        riga = self.list_view.currentRow()
        if riga < 0 or riga >= len(self.utenti):
            return
        self.vista_utente = VistaUtente(self.utenti[riga], self._elimina_utente)
        self.vista_utente.show()

    # callback per VistaUtente: smista la rimozione al metodo giusto del Control
    def _elimina_utente(self, utilizzatore) -> str:
        if isinstance(utilizzatore, Cliente):
            esito = self._gestore.rimuoviCliente(utilizzatore.getCodice())
        elif isinstance(utilizzatore, SkiMan):
            esito = self._gestore.rimuoviSkiMan(utilizzatore.getCodice())
        else: 
            esito = self._gestore.rimuoviAmministratore(utilizzatore.getCodice())
        self.load_utenti()
        self.update_ui()
        return esito
