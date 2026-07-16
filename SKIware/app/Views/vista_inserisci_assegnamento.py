from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox)

class VistaInserisciAssegnamento(QWidget): # Boundary
    # GestioneAssegnamenti
    def __init__(self, callback, clienti_provider, attrezzature_provider):
        super().__init__()
        self.callback = callback # funzione del chiamante per l'inserimento
        self._clienti_provider      = clienti_provider
        self._attrezzature_provider = attrezzature_provider
        self.setWindowTitle("Inserisci Assegnamento")

        self.v_layout = QVBoxLayout()
        self._campi = {}

        self._clienti = self.get_clienti() 
        self.combo = QComboBox()
        self.combo.addItems(list(self._clienti.keys()))
        self.combo.currentTextChanged.connect(self.onChanged)
        self.v_layout.addWidget(QLabel("Cliente:"))
        self.v_layout.addWidget(self.combo)

        self._attrezzature = self.get_attrezzature() 
        self.combo_attrezzatura = QComboBox()
        self.combo_attrezzatura.addItems(list(self._attrezzature.keys()))
        self.v_layout.addWidget(QLabel("Attrezzatura disponibile:"))
        self.v_layout.addWidget(self.combo_attrezzatura)

        self.add_info_text("inizio", "data e ora inizio (AAAA-MM-GG HH:MM)")
        self.add_info_text("fine", "data e ora fine (AAAA-MM-GG HH:MM)")
        self.add_info_text("fascia", "fascia oraria (mattina/pomeriggio/giornata)")

        self.bottone_aggiungi = QPushButton("Aggiungi assegnamento")
        self.bottone_aggiungi.clicked.connect(self.aggiungi_assegnamento)
        self.v_layout.addWidget(self.bottone_aggiungi)
        self.label_esito = QLabel("")
        self.v_layout.addWidget(self.label_esito)
        self.setLayout(self.v_layout)


    def get_clienti(self) -> dict:
        return {str(c): c for c in self._clienti_provider()}

    # solo l'attrezzatura DISPONIBILE è proponibile per un nuovo assegnamento
    def get_attrezzature(self) -> dict:
        return {str(s): s for s in self._attrezzature_provider()}

    def add_info_text(self, campo: str, testo: str) -> None:
        self.v_layout.addWidget(QLabel(testo))
        self._campi[campo] = QLineEdit()
        self.v_layout.addWidget(self._campi[campo])

    def onChanged(self, testo: str) -> None:
        self.label_esito.setText("")

    def aggiungi_assegnamento(self) -> None:
        cliente      = self._clienti.get(self.combo.currentText())
        attrezzatura = self._attrezzature.get(self.combo_attrezzatura.currentText())
        if cliente is None or attrezzatura is None:
            self.label_esito.setText("Errore: seleziona cliente e attrezzatura")
            return
        try:
            inizio = datetime.fromisoformat(self._campi["inizio"].text().strip())
            fine   = datetime.fromisoformat(self._campi["fine"].text().strip())
            esito  = self.callback(cliente, attrezzatura, inizio, fine,
                                   self._campi["fascia"].text().strip())
        except ValueError:
            esito = "Errore: data non valida (usa AAAA-MM-GG HH:MM)"
        self.label_esito.setText(str(esito))
