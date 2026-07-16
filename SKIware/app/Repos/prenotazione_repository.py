import json
from datetime import datetime
from Models import Prenotazione
from Repos.servizio_repository import ServizioRepository
from Repos.utilizzatore_repository import UtilizzatoreRepository

class PrenotazioneRepository: # Repos
    # Prenotazione è una classe associazione reificata
    # mette in relazione un Cliente e un Servizio
    # Una sua istanza dipende dalle altre due classi per esistere:

    def __init__(self, path: str = "Data/prenotazioni.json",
                 servizio_repo: ServizioRepository = None,
                 utilizzatore_repo: UtilizzatoreRepository = None):
        self._path              = path
        self._servizio_repo     = servizio_repo    
        self._utilizzatore_repo = utilizzatore_repo 
        self._prenotazioni: dict = {} # chiave = codice della prenotazione
    
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                dati = json.load(f)
            self._prenotazioni = {}
            for d in dati:
                servizio = self._servizio_repo.trovaPerId(d["servizio_codice"])
                cliente  = self._utilizzatore_repo.trovaPerId(d["cliente_codice"])
                if servizio and cliente: # controllo che esistano entrambi
                    self._prenotazioni[d["codice"]] = Prenotazione(
                        d["codice"],
                        datetime.fromisoformat(d["dataOraInizio"]),
                        d["fasciaOraria"], servizio, cliente
                    )
        except FileNotFoundError:
            self._prenotazioni = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([p.toDict() for p in self._prenotazioni.values()], f)

    def trovaPerId(self, codice: int): 
        return self._prenotazioni.get(codice)

    def aggiungi(self, prenotazione: Prenotazione) -> None:
        self._prenotazioni[prenotazione.getCodice()] = prenotazione
        self.salva()

    def rimuovi(self, codice: int) -> None: 
        if codice in self._prenotazioni:
            del self._prenotazioni[codice]
            self.salva()

    def tutti(self) -> list:
        return list(self._prenotazioni.values())
