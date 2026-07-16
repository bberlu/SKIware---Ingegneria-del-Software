from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox)

class VistaInserisciCarnet(QWidget): # Boundary
    # GestioneCarnet
    def __init__(self, callback, clienti_provider):
        super().__init__()
        self.callback = callback # funzione del chiamante per la vendita
        self._clienti_provider = clienti_provider # funzione che fornisce i clienti
        
        self.setWindowTitle("Vendi Carnet")

        self.v_layout = QVBoxLayout()
        self._campi = {}

        # combo con i clienti a cui intestare il carnet
        self._clienti = self.get_clienti()
        self.combo = QComboBox()
        self.combo.addItems(list(self._clienti.keys()))
        self.combo.currentTextChanged.connect(self.onChanged)
        self.v_layout.addWidget(QLabel("Cliente:"))
        self.v_layout.addWidget(self.combo)

        self.add_info_text("tipo", "tipo (numero noleggi, es. 10 o 20)")
        self.add_info_text("stagionale", "stagionale (si/no)")

        self.bottone_vendi = QPushButton("Vendi carnet")
        self.bottone_vendi.clicked.connect(self.aggiungi_carnet)
        self.v_layout.addWidget(self.bottone_vendi)
        self.label_esito = QLabel("")
        self.v_layout.addWidget(self.label_esito)
        self.setLayout(self.v_layout)

    # dizionario {rappresentazione testuale: oggetto Cliente} per la combo
    def get_clienti(self) -> dict:
        return {str(c): c for c in self._clienti_provider()}

    def add_info_text(self, campo: str, testo: str) -> None:
        self.v_layout.addWidget(QLabel(testo))
        self._campi[campo] = QLineEdit()
        self.v_layout.addWidget(self._campi[campo])

    def onChanged(self, testo: str) -> None:
        self.label_esito.setText("") # ripulisce l'esito al cambio cliente

    def aggiungi_carnet(self) -> None:
        cliente = self._clienti.get(self.combo.currentText())
        if cliente is None:
            self.label_esito.setText("Errore: seleziona un cliente")
            return
        try:
            tipo = int(self._campi["tipo"].text().strip())
            stagionale = self._campi["stagionale"].text().strip().lower() == "si"
            esito = self.callback(cliente, tipo, stagionale)
        except ValueError:
            esito = "Errore: controlla i campi numerici"
        self.label_esito.setText(str(esito))
