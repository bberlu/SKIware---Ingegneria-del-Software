from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox)

class VistaInserisciPrenotazione(QWidget): # Boundary
    # GestionePrenotazioni
    def __init__(self, callback, clienti_provider):
        super().__init__()
        self.callback = callback # funzione del chiamante per l'inserimento
        self._clienti_provider = clienti_provider
        self.setWindowTitle("Inserisci Prenotazione")

        self.v_layout = QVBoxLayout()
        self._campi = {}

        self._clienti = self.get_clienti()
        self.combo = QComboBox()
        self.combo.addItems(list(self._clienti.keys()))
        self.combo.currentTextChanged.connect(self.onChanged)
        self.v_layout.addWidget(QLabel("Cliente:"))
        self.v_layout.addWidget(self.combo)

        self.add_info_text("servizio", "codice servizio (es. SCI001)")
        self.add_info_text("data", "data e ora inizio (AAAA-MM-GG HH:MM)")
        self.add_info_text("fascia", "fascia oraria (mattina/pomeriggio/giornata)")

        self.bottone_aggiungi = QPushButton("Aggiungi prenotazione")
        self.bottone_aggiungi.clicked.connect(self.aggiungi_prenotazione)
        self.v_layout.addWidget(self.bottone_aggiungi)
        self.label_esito = QLabel("")
        self.v_layout.addWidget(self.label_esito)
        self.setLayout(self.v_layout)

    def get_clienti(self) -> dict:
        return {str(c): c for c in self._clienti_provider()}

    def add_info_text(self, campo: str, testo: str) -> None:
        self.v_layout.addWidget(QLabel(testo))
        self._campi[campo] = QLineEdit()
        self.v_layout.addWidget(self._campi[campo])

    def onChanged(self, testo: str) -> None:
        self.label_esito.setText("")

    def aggiungi_prenotazione(self) -> None:
        cliente = self._clienti.get(self.combo.currentText())
        if cliente is None:
            self.label_esito.setText("Errore: seleziona un cliente")
            return
        try:
            data = datetime.fromisoformat(self._campi["data"].text().strip())
            esito = self.callback(cliente,
                                  self._campi["servizio"].text().strip(),
                                  data,
                                  self._campi["fascia"].text().strip())
        except ValueError:
            esito = "Errore: data non valida (usa AAAA-MM-GG HH:MM)"
        self.label_esito.setText(str(esito))
