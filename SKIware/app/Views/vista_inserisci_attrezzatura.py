from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox)

class VistaInserisciAttrezzatura(QWidget): # Boundary
    # GestioneAttrezzatura
 
    TIPI = ("Sci", "Snowboard", "Scarpone", "Casco", "Armadietto")

    def __init__(self, callback):
        super().__init__()
        self.callback = callback # funzione del chiamante per l'inserimento
        self.setWindowTitle("Inserisci Attrezzatura")

        self.v_layout = QVBoxLayout()
        self._campi = {}

        # combo per scegliere il tipo di servizio da inserire
        self.combo = QComboBox()
        self.combo.addItems(self.TIPI)
        # aggiungo un segnale: attivo una funzione se cambia la selezione
        self.combo.currentTextChanged.connect(self.onChanged)
        self.v_layout.addWidget(QLabel("Tipo di servizio:"))
        self.v_layout.addWidget(self.combo)

        # campi comuni
        self.add_info_text("codice", "codice")
        self.add_info_text("descrizione", "descrizione")
        self.add_info_text("prezzo", "prezzo")
        # campo aggiuntivo che dipende dal tipo selezionato
        self.label_extra = QLabel("livelloTecnico")
        self.campo_extra = QLineEdit()
        self.v_layout.addWidget(self.label_extra)
        self.v_layout.addWidget(self.campo_extra)

        self.bottone_aggiungi = QPushButton("Aggiungi attrezzatura")
        self.bottone_aggiungi.clicked.connect(self.aggiungi_attrezzatura)
        self.v_layout.addWidget(self.bottone_aggiungi)
        self.label_esito = QLabel("")
        self.v_layout.addWidget(self.label_esito)
        self.setLayout(self.v_layout)

    # aggiunge al layout una label statica e il relativo campo di input
    def add_info_text(self, campo: str, testo: str) -> None:
        self.v_layout.addWidget(QLabel(testo))
        self._campi[campo] = QLineEdit()
        self.v_layout.addWidget(self._campi[campo])

    # adatta il campo aggiuntivo al tipo selezionato nella combo
    def onChanged(self, tipo: str) -> None:
        if tipo in ("Sci", "Snowboard"):
            self.label_extra.setText("livelloTecnico")
        elif tipo == "Armadietto":
            self.label_extra.setText("dimensione")
        else: # Scarpone e Casco non hanno attributi propri
            self.label_extra.setText("(nessun campo aggiuntivo)")

    def aggiungi_attrezzatura(self) -> None:
        try:
            esito = self.callback(
                self.combo.currentText(), # tipo scelto
                self._campi["codice"].text().strip(),
                self._campi["descrizione"].text().strip(),
                float(self._campi["prezzo"].text().strip()),
                self.campo_extra.text().strip()
            )
        except ValueError:
            esito = "Errore: controlla i campi numerici"
        self.label_esito.setText(str(esito))
