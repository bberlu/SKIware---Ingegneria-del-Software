from Repos import (UtilizzatoreRepository, ServizioRepository, CarnetRepository,
                   PrenotazioneRepository, AssegnamentoRepository, RicevutaRepository)
from Services.gestore_utenti import GestoreUtenti
from Services.gestore_attrezzatura import GestoreAttrezzatura
from Services.gestore_carnet import GestoreCarnet
from Services.gestore_noleggi import GestoreNoleggi
from Services.gestore_backup import GestoreBackup

class GestoreSistema: # Control
    # coordinatore dell'applicazione, pkg Gestione
    # crea le repository nell'ordine giusto (prima le entità, poi le associazioni)
    # e mette a disposizione gli altri gestori al main e alle Views
    # punto in cui l'app viene cablata
    # le Views non devono sapere come si costruiscono repository e gestori)
    def __init__(self, cartella_dati: str = "Data"):
        # repos entity

        self._utilizzatore_repo = UtilizzatoreRepository(f"{cartella_dati}/utilizzatori.json")
        self._servizio_repo     = ServizioRepository(f"{cartella_dati}/servizi.json")
        self._carnet_repo       = CarnetRepository(f"{cartella_dati}/carnet.json",
                                                   self._utilizzatore_repo)
        # repos associazioni

        self._prenotazione_repo = PrenotazioneRepository(f"{cartella_dati}/prenotazioni.json",
                                                         self._servizio_repo,
                                                         self._utilizzatore_repo)
        self._assegnamento_repo = AssegnamentoRepository(f"{cartella_dati}/assegnamenti.json",
                                                         self._servizio_repo,
                                                         self._utilizzatore_repo)
        self._ricevuta_repo     = RicevutaRepository(f"{cartella_dati}/ricevute.json",
                                                     self._assegnamento_repo)
        # gestori

        self._gestore_utenti       = GestoreUtenti(self._utilizzatore_repo)
        self._gestore_attrezzatura = GestoreAttrezzatura(self._servizio_repo,
                                                         self._assegnamento_repo)
        self._gestore_carnet       = GestoreCarnet(self._carnet_repo,
                                                   self._prenotazione_repo,
                                                   self._servizio_repo)
        self._gestore_noleggi      = GestoreNoleggi(self._assegnamento_repo,
                                                    self._servizio_repo,
                                                    self._utilizzatore_repo,
                                                    self._ricevuta_repo,
                                                    self._gestore_attrezzatura)
        self._gestore_backup       = GestoreBackup(self._utilizzatore_repo,
                                                   self._servizio_repo,
                                                   self._carnet_repo,
                                                   self._prenotazione_repo,
                                                   self._assegnamento_repo,
                                                   self._ricevuta_repo,
                                                   f"{cartella_dati}/backup.json")

        # al primo avvio non esiste alcun utilizzatore: viene creato un
        # amministratore predefinito
        # (credenziali messe nel readme: codice 0, password Admin2027)
        if not self._utilizzatore_repo.tutti():
            self._gestore_utenti.aggiungiAmministratore(
                0, "ADMIN", "Predefinito", "admin@skiware.it",
                "Amministratore", "Admin2027", 0)

    def getGestoreUtenti(self) -> GestoreUtenti:
        return self._gestore_utenti

    def getGestoreAttrezzatura(self) -> GestoreAttrezzatura:
        return self._gestore_attrezzatura

    def getGestoreCarnet(self) -> GestoreCarnet:
        return self._gestore_carnet

    def getGestoreNoleggi(self) -> GestoreNoleggi:
        return self._gestore_noleggi

    def getGestoreBackup(self) -> GestoreBackup:
        return self._gestore_backup
