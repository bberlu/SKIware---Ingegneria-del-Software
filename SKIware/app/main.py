import sys
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QPushButton, QLabel)
from PyQt6.QtCore import QTimer
from Models import Amministratore
from Services import GestoreSistema
from Views import (VistaLogin, VistaGestisciUtenti, VistaGestisciAttrezzatura,
                   VistaGestisciCarnet, VistaGestisciPrenotazioni,
                   VistaGestisciAssegnamenti)

class FinestraPrincipale(QWidget): # Boundary
    # menu principale: un bottone per ogni package di viste dell'UML.
    # Non fa logica: si limita ad aprire le viste passando loro i Control

    # orario del backup automatico (caso d'uso Backup, attore Tempo:
    # "il backup è effettuato ogni giorno alle 23.30")
    ORA_BACKUP = (23, 30)

    def __init__(self, gestore_sistema: GestoreSistema, utente):
        super().__init__()
        self._gs = gestore_sistema
        self._utente = utente # l'utilizzatore autenticato (RF3)
        self.setWindowTitle("SKIware — Gestionale Noleggio Sci")

        # BOUNDARY TEMPO (attore Tempo, realizzato con QTimer):
        self._avviaTimer()

        v_layout = QVBoxLayout()
        # mostriamo chi è collegato e con quale ruolo (= tipo della classe)
        v_layout.addWidget(QLabel(
            f"Accesso: {utente.getNome()} {utente.getCognome()} "
            f"({type(utente).__name__})"))

        # verifica accesso aree riservate (RF4): il menu mostra solo le
        # gestioni permesse al ruolo. L'Amministratore accede a tutto;
        # lo Ski-man alla sola Gestione Assegnamenti (consegna e ritiro,
        # valore DIN, assegnazione armadietti)
        if isinstance(utente, Amministratore):
            bottoni = (
                ("Gestione Utenti", self.apri_utenti),
                ("Gestione Attrezzatura", self.apri_attrezzatura),
                ("Gestione Carnet", self.apri_carnet),
                ("Gestione Prenotazioni", self.apri_prenotazioni),
                ("Gestione Assegnamenti", self.apri_assegnamenti),
            )
        else: # Ski-man
            bottoni = (
                ("Gestione Assegnamenti", self.apri_assegnamenti),
            )
        for testo, funzione in bottoni:
            bottone = QPushButton(testo)
            bottone.clicked.connect(funzione)
            v_layout.addWidget(bottone)

        # backup manuale (caso d'uso Backup, attore Amministratore):
        # oltre al backup automatico delle 23:30, l'amministratore
        # può effettuare il backup in qualsiasi momento (RF4: riservato)
        if isinstance(utente, Amministratore):
            self.bottone_backup = QPushButton("Effettua backup")
            self.bottone_backup.clicked.connect(self.effettua_backup)
            v_layout.addWidget(self.bottone_backup)
        self.label_esito = QLabel("")
        v_layout.addWidget(self.label_esito)
        self.setLayout(v_layout)

    # --- attore Amministratore: backup manuale ---
    def effettua_backup(self) -> None:
        esito = self._gs.getGestoreBackup().effettuaBackup()
        self.label_esito.setText(str(esito))

    # --- attore Tempo ---
    def _avviaTimer(self) -> None:
        self._data_ultimo_backup = None # data dell'ultimo backup effettuato
        self._timer = QTimer()
        self._timer.setInterval(60_000) # controlla l'orario ogni minuto
        self._timer.timeout.connect(self.onTimerScattato)
        self._timer.start()

    def onTimerScattato(self) -> None: # BOUNDARY TEMPO
        # alle 23:30 (o al primo scatto utile dopo) effettua il backup
        # giornaliero, una sola volta al giorno
        adesso = datetime.now()
        if (adesso.hour, adesso.minute) >= self.ORA_BACKUP \
           and self._data_ultimo_backup != adesso.date():
            esito = self._gs.getGestoreBackup().effettuaBackup()
            self._data_ultimo_backup = adesso.date()
            print(f"[Timer] {esito}")

    def apri_utenti(self) -> None:
        self.vista_utenti = VistaGestisciUtenti(self._gs.getGestoreUtenti())
        self.vista_utenti.show()

    def apri_attrezzatura(self) -> None:
        self.vista_attrezzatura = VistaGestisciAttrezzatura(
            self._gs.getGestoreAttrezzatura())
        self.vista_attrezzatura.show()

    def apri_carnet(self) -> None:
        self.vista_carnet = VistaGestisciCarnet(self._gs.getGestoreCarnet(),
                                                self._gs.getGestoreUtenti())
        self.vista_carnet.show()

    def apri_prenotazioni(self) -> None:
        self.vista_prenotazioni = VistaGestisciPrenotazioni(
            self._gs.getGestoreCarnet(), self._gs.getGestoreUtenti(),
            self._gs.getGestoreAttrezzatura())
        self.vista_prenotazioni.show()

    def apri_assegnamenti(self) -> None:
        self.vista_assegnamenti = VistaGestisciAssegnamenti(
            self._gs.getGestoreNoleggi(), self._gs.getGestoreUtenti(),
            self._gs.getGestoreAttrezzatura())
        self.vista_assegnamenti.show()

# punto di ingresso dell'applicazione: crea il GestoreSistema (che cabla
# repository e gestori) e mostra il login; la finestra principale si apre
# solo dopo un'autenticazione riuscita (RF3)
def main():
    app = QApplication(sys.argv)
    gestore_sistema = GestoreSistema()

    # callback per VistaLogin: autentica tramite il Control e, se il ruolo
    # è abilitato, apre la finestra principale; altrimenti torna l'errore
    def effettua_login(codice, password):
        utente = gestore_sistema.getGestoreUtenti().autentica(codice, password)
        if utente is None:
            return "Accesso negato: credenziali non valide"
        if not utente.puoAccedere(): # RF3: i clienti non accedono al sistema
            return "Accesso riservato al personale (amministratori e ski-man)"
        login.finestra = FinestraPrincipale(gestore_sistema, utente)
        login.finestra.show()
        login.close()
        return None # accesso riuscito

    login = VistaLogin(effettua_login)
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
