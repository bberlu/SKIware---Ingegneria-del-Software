from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget)
from Services import GestoreCarnet, GestoreUtenti, GestoreAttrezzatura
from Views.vista_prenotazione import VistaPrenotazione
from Views.vista_inserisci_prenotazione import VistaInserisciPrenotazione

class VistaGestisciPrenotazioni(QWidget): # Boundary
    # vista principale del package GestionePrenotazioni 
    # le prenotazioni sono gestite dal GestoreCarnet (come da UML class Gestione)
    def __init__(self, gestore_carnet: GestoreCarnet,
                 gestore_utenti: GestoreUtenti,
                 gestore_attrezzatura: GestoreAttrezzatura):
        super().__init__()
        self._gestore              = gestore_carnet
        self._gestore_utenti       = gestore_utenti
        self._gestore_attrezzatura = gestore_attrezzatura
        self.setWindowTitle("Gestione Prenotazioni")

        self.prenotazioni: list = [] 
        self.list_view = QListWidget() 

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.list_view)
        h_layout = QHBoxLayout()
        self.bottone_nuovo = QPushButton("Nuova prenotazione")
        self.bottone_nuovo.clicked.connect(self.show_new)
        h_layout.addWidget(self.bottone_nuovo)
        self.bottone_info = QPushButton("Info prenotazione selezionata")
        self.bottone_info.clicked.connect(self.show_selected_info)
        h_layout.addWidget(self.bottone_info)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

        self.load_prenotazioni() 
        self.update_ui()

    
    def load_prenotazioni(self) -> None:
        self.prenotazioni = self._gestore.elencaPrenotazioni()

   
    def update_ui(self) -> None:
        self.list_view.clear()
        for prenotazione in self.prenotazioni:
            self.list_view.addItem(str(prenotazione))


    def show_new(self) -> None:
        self.vista_inserisci = VistaInserisciPrenotazione(
            self._aggiungi_prenotazione,
            self._gestore_utenti.elencaClienti)
        self.vista_inserisci.show()

    # callback per VistaInserisciPrenotazione: risolve il servizio tramite il
    # Control dell'attrezzatura e gira l'inserimento al GestoreCarnet
    def _aggiungi_prenotazione(self, cliente, servizio_codice: str,
                               data, fascia: str) -> str:
        servizio = self._gestore_attrezzatura.ricercaServizio(servizio_codice)
        esito = self._gestore.inserisciPrenotazione(cliente, servizio, data, fascia)
        self.load_prenotazioni()
        self.update_ui()
        if isinstance(esito, str): # messaggio di errore
            return esito
        return f"Prenotazione ok: {esito}"


    def show_selected_info(self) -> None:
        riga = self.list_view.currentRow()
        if riga < 0 or riga >= len(self.prenotazioni):
            return
        self.vista_prenotazione = VistaPrenotazione(self.prenotazioni[riga],
                                                    self._disdici_prenotazione,
                                                    self._elimina_prenotazione)
        self.vista_prenotazione.show()

    # callback per VistaPrenotazione: disdetta con logica rimborso 48h
    def _disdici_prenotazione(self, prenotazione) -> str:
        esito = self._gestore.disdiciPrenotazione(prenotazione.getCodice())
        self.load_prenotazioni()
        self.update_ui()
        return esito

    # callback per VistaPrenotazione
    def _elimina_prenotazione(self, prenotazione) -> str:
        esito = self._gestore.eliminaPrenotazione(prenotazione.getCodice())
        self.load_prenotazioni()
        self.update_ui()
        return esito
