from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget)
from Services import GestoreNoleggi, GestoreUtenti, GestoreAttrezzatura
from Views.vista_assegnamento import VistaAssegnamento
from Views.vista_inserisci_assegnamento import VistaInserisciAssegnamento

class VistaGestisciAssegnamenti(QWidget): # Boundary
    # vista principale del package GestioneAssegnamenti
    def __init__(self, gestore_noleggi: GestoreNoleggi,
                 gestore_utenti: GestoreUtenti,
                 gestore_attrezzatura: GestoreAttrezzatura):
        super().__init__()
        self._gestore              = gestore_noleggi
        self._gestore_utenti       = gestore_utenti
        self._gestore_attrezzatura = gestore_attrezzatura
        self.setWindowTitle("Gestione Assegnamenti")

        self.assegnamenti: list = []
        self.list_view = QListWidget() 

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.list_view)
        h_layout = QHBoxLayout()
        self.bottone_nuovo = QPushButton("Nuovo assegnamento")
        self.bottone_nuovo.clicked.connect(self.show_new)
        h_layout.addWidget(self.bottone_nuovo)
        self.bottone_info = QPushButton("Info assegnamento selezionato")
        self.bottone_info.clicked.connect(self.show_selected_info)
        h_layout.addWidget(self.bottone_info)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

        self.load_assegnamenti() 
        self.update_ui()

 
    def load_assegnamenti(self) -> None:
        self.assegnamenti = self._gestore.elencaAssegnamenti()


    def update_ui(self) -> None:
        self.list_view.clear()
        for assegnamento in self.assegnamenti:
            self.list_view.addItem(str(assegnamento))

    
    def show_new(self) -> None:
        self.vista_inserisci = VistaInserisciAssegnamento(
            self._aggiungi_assegnamento,
            self._gestore_utenti.elencaClienti,
            self._gestore_attrezzatura.elencaDisponibili)
        self.vista_inserisci.show()

    # callback per VistaInserisciAssegnamento: gira l'inserimento al Control
    # (che applica vincolo stagionale, fascia oraria, vincolo armadietti
    # ed emette la ricevuta)
    def _aggiungi_assegnamento(self, cliente, attrezzatura, inizio, fine,
                               fascia: str) -> str:
        esito = self._gestore.inserisciAssegnamento(cliente.getCodice(),
                                                    attrezzatura.getCodice(),
                                                    inizio, fine, fascia)
        self.load_assegnamenti()
        self.update_ui()
        return esito


    def show_selected_info(self) -> None:
        riga = self.list_view.currentRow()
        if riga < 0 or riga >= len(self.assegnamenti):
            return
        self.vista_assegnamento = VistaAssegnamento(
            self.assegnamenti[riga],
            self._consegna, self._ritiro, self._inserisci_din,
            self._gestore.elencaRicevute)
        self.vista_assegnamento.show()

    # callback per VistaAssegnamento 
    def _consegna(self, assegnamento) -> str:
        esito = self._gestore.consegnaAttrezzatura(assegnamento.getCodice())
        self.load_assegnamenti()
        self.update_ui()
        return esito

    def _ritiro(self, assegnamento) -> str:
        esito = self._gestore.ritiraAttrezzatura(assegnamento.getCodice())
        self.load_assegnamenti()
        self.update_ui()
        return esito

    # callback per VistaAssegnamento 
    def _inserisci_din(self, assegnamento, valore: float, skiman_codice: int) -> str:
        return self._gestore.inserisciValoreDIN(assegnamento.getCodice(),
                                                valore, skiman_codice)
