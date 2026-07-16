from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox)

class VistaInserisciUtente(QWidget): # Boundary
    # form di inserimento per tutti i tipi di utilizzatore
    TIPI = ("Cliente", "Ski-man", "Amministratore")

    # etichette con il suggerimento sul formato atteso tra parentesi
    CAMPI_BASE = {
        "codice":        "codice (numero intero, es. 1)",
        "codiceFiscale": "codiceFiscale",
        "cognome":       "cognome",
        "email":         "email",
        "nome":          "nome",
        "password":      "password (almeno 7 caratteri alfanumerici)",
        "telefono":      "telefono (solo cifre, senza spazi)",
    }
    CAMPI_CLIENTE = {
        "altezza":        "altezza in metri (usare il punto, es. 1.75)",
        "eta":            "eta (numero intero, es. 25)",
        "livelloAbilita": "livelloAbilita (principiante/intermedio/avanzato)",
        "misuraScarponi": "misuraScarponi (numero intero, es. 42)",
        "peso":           "peso in kg (usare il punto, es. 70.5)",
    }
    CAMPI_SKIMAN = {
        "dataNascita":      "data di nascita (AAAA-MM-GG)",
        "luogoNascita":     "luogoNascita",
        "qualificaTecnica": "qualificaTecnica (es. Maestro di sci)",
    }

    def __init__(self, callback):
        super().__init__()
        self.callback = callback # funzione del chiamante per l'inserimento
        self.setWindowTitle("Inserisci Utente")

        self.v_layout = QVBoxLayout()
        self._campi = {}
        self._widget_cliente = [] # widget da mostrare solo per i clienti
        self._widget_skiman  = [] # widget da mostrare solo per gli ski-man

        # combo per scegliere il tipo di utilizzatore da inserire
        self.combo = QComboBox()
        self.combo.addItems(self.TIPI)
        # aggiungo un segnale: attivo una funzione se cambia la selezione
        self.combo.currentTextChanged.connect(self.onChanged)
        self.v_layout.addWidget(QLabel("Tipo di utilizzatore:"))
        self.v_layout.addWidget(self.combo)

        # campi comuni a tutti
        for campo, etichetta in self.CAMPI_BASE.items():
            self.add_info_text(campo, etichetta)
        # campi specifici, raggruppati per tipo
        for campo, etichetta in self.CAMPI_CLIENTE.items():
            self.add_info_text(campo, etichetta, self._widget_cliente)
        for campo, etichetta in self.CAMPI_SKIMAN.items():
            self.add_info_text(campo, etichetta, self._widget_skiman)

        self.bottone_aggiungi = QPushButton("Aggiungi utente")
        self.bottone_aggiungi.clicked.connect(self.aggiungi_utente)
        self.v_layout.addWidget(self.bottone_aggiungi)
        self.label_esito = QLabel("")
        self.v_layout.addWidget(self.label_esito)
        self.setLayout(self.v_layout)

        self.onChanged(self.combo.currentText()) # mostra i campi del tipo iniziale

    # crea label e campo di input; se indicato, li aggiunge a un gruppo
    def add_info_text(self, campo: str, testo: str, gruppo: list = None) -> None:
        label = QLabel(testo)
        self._campi[campo] = QLineEdit()
        if campo == "password": # la password va nascosta
            self._campi[campo].setEchoMode(QLineEdit.EchoMode.Password)
        self.v_layout.addWidget(label)
        self.v_layout.addWidget(self._campi[campo])
        if gruppo is not None: # tengo traccia dei widget specifici del tipo
            gruppo.append(label)
            gruppo.append(self._campi[campo])

    # mostra solo i campi pertinenti al tipo selezionato nella combo
    def onChanged(self, tipo: str) -> None:
        for w in self._widget_cliente:
            w.setVisible(tipo == "Cliente")
        for w in self._widget_skiman:
            w.setVisible(tipo == "Ski-man")
        self.label_esito.setText("")

    # legge i campi del tipo selezionato e invoca la callback
    def aggiungi_utente(self) -> None:
        tipo = self.combo.currentText()
        valori = {campo: box.text().strip() for campo, box in self._campi.items()}

        # conversione campo per campo: se una fallisce, diciamo QUALE campo è sbagliato
        try:
            for campo in ("codice", "telefono"):
                valori[campo] = int(valori[campo])
            if tipo == "Cliente":
                for campo in ("eta", "misuraScarponi"):
                    valori[campo] = int(valori[campo])
                for campo in ("altezza", "peso"):
                   #accetto la virgola decimale
                    valori[campo] = float(valori[campo].replace(",", "."))
            if tipo == "Ski-man":
                campo = "dataNascita"
                valori[campo] = datetime.fromisoformat(valori[campo])
        except ValueError:
            self.label_esito.setText(
                f"Errore: il campo '{campo}' non è nel formato richiesto")
            return
        esito = self.callback(tipo, valori)
        self.label_esito.setText(str(esito))
