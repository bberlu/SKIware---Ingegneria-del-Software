from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton)

class VistaLogin(QWidget): # Boundary
    # finestra di autenticazione 
    # è la prima finestra mostrata all'avvio; il resto dell'applicazione
    # si apre solo dopo un accesso riuscito.
    # View non parla con il Control
    def __init__(self, callback):
        super().__init__()
        self.callback = callback # funzione del chiamante che effettua il login
        self.setWindowTitle("SKIware — Accesso")

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("codice utente (numero intero)"))
        self.campo_codice = QLineEdit()
        v_layout.addWidget(self.campo_codice)
        v_layout.addWidget(QLabel("password"))
        self.campo_password = QLineEdit()
        # la password non va mostrata in chiaro
        self.campo_password.setEchoMode(QLineEdit.EchoMode.Password)
        v_layout.addWidget(self.campo_password)

        self.bottone_accedi = QPushButton("Accedi")
        # attivo una funzione se clicco sul bottone
        self.bottone_accedi.clicked.connect(self.accedi_click)
        v_layout.addWidget(self.bottone_accedi)
        self.label_esito = QLabel("")
        v_layout.addWidget(self.label_esito)
        self.setLayout(v_layout)

    # legge le credenziali e le passa alla callback; se la callback
    # restituisce un messaggio, l'accesso è fallito e viene mostrato
    def accedi_click(self) -> None:
        try:
            codice = int(self.campo_codice.text().strip())
        except ValueError:
            self.label_esito.setText("Errore: il codice deve essere un numero")
            return
        esito = self.callback(codice, self.campo_password.text())
        if esito: # messaggio di errore
            self.label_esito.setText(str(esito))
