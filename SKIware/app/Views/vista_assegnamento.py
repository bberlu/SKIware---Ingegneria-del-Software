from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton)
from Models import Assegnamento

class VistaAssegnamento(QWidget): # Boundary
    # scheda di dettaglio di un singolo assegnamento
    def __init__(self, assegnamento: Assegnamento, consegna_callback,
                 ritiro_callback, din_callback, ricevuta_provider):
        super().__init__()
        self._assegnamento = assegnamento
        self.consegna_callback = consegna_callback
        self.ritiro_callback   = ritiro_callback
        self.din_callback      = din_callback
        self._ricevuta_provider = ricevuta_provider # per get_ricevuta
        self.setWindowTitle(f"Assegnamento {assegnamento.getCodice()}")

        v_layout = QVBoxLayout()
        # informazioni dell'assegnamento 
        for campo, valore in assegnamento.toDict().items():
            v_layout.addWidget(QLabel(f"{campo}: {valore}"))
        # ricevuta collegata 
        ricevuta = self.get_ricevuta(assegnamento)
        if ricevuta:
            v_layout.addWidget(QLabel(
                f"ricevuta n. {ricevuta['anno']}/{ricevuta['codice']} — "
                f"importo: {ricevuta['importoTotale']}€"))

        # campi per il valore DIN 
        v_layout.addWidget(QLabel("valore DIN effettivo:"))
        self.campo_din = QLineEdit()
        v_layout.addWidget(self.campo_din)
        v_layout.addWidget(QLabel("codice ski-man responsabile:"))
        self.campo_skiman = QLineEdit()
        v_layout.addWidget(self.campo_skiman)
        self.bottone_din = QPushButton("Registra valore DIN")
        # lambda: funzione anonima, serve per passare l'argomento alla funzione collegata al click
        self.bottone_din.clicked.connect(
            lambda: self.inserisci_din_click(self._assegnamento))
        v_layout.addWidget(self.bottone_din)

        self.bottone_consegna = QPushButton("Consegna attrezzatura")
        self.bottone_consegna.clicked.connect(
            lambda: self.consegna_click(self._assegnamento))
        v_layout.addWidget(self.bottone_consegna)
        self.bottone_ritiro = QPushButton("Ritira attrezzatura")
        self.bottone_ritiro.clicked.connect(
            lambda: self.ritiro_click(self._assegnamento))
        v_layout.addWidget(self.bottone_ritiro)

        self.label_esito = QLabel("")
        v_layout.addWidget(self.label_esito)
        self.setLayout(v_layout)

    
    def get_ricevuta(self, assegnamento: Assegnamento) -> dict:
        for r in self._ricevuta_provider():
            if r.getAssegnamento().getCodice() == assegnamento.getCodice():
                return r.toDict()
        return {}

    
    def inserisci_din_click(self, assegnamento: Assegnamento) -> None:
        try:
            valore = float(self.campo_din.text().strip())
            skiman = int(self.campo_skiman.text().strip())
            esito  = self.din_callback(assegnamento, valore, skiman)
        except ValueError:
            esito = "Errore: controlla valore DIN e codice ski-man"
        self.label_esito.setText(str(esito))

    
    def consegna_click(self, assegnamento: Assegnamento) -> None:
        self.label_esito.setText(str(self.consegna_callback(assegnamento)))

    
    def ritiro_click(self, assegnamento: Assegnamento) -> None:
        self.label_esito.setText(str(self.ritiro_callback(assegnamento)))
