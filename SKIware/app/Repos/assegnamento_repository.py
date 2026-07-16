import json
from datetime import datetime
from Models import Assegnamento
from Repos.servizio_repository import ServizioRepository
from Repos.utilizzatore_repository import UtilizzatoreRepository

class AssegnamentoRepository: # Repository di Assegnamenti
    # Assegnamento è una classe associazione
    # reificata tra Cliente e Servizio: per ricostruirla servono gli altri repository!
    def __init__(self, path: str = "Data/assegnamenti.json",
                 servizio_repo: ServizioRepository = None,
                 utilizzatore_repo: UtilizzatoreRepository = None):
        self._path              = path
        self._servizio_repo     = servizio_repo     # realizza l'associazione
        self._utilizzatore_repo = utilizzatore_repo # realizza l'associazione
        self._assegnamenti: dict = {} # chiave = codice dell'assegnamento
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                dati = json.load(f)
            self._assegnamenti = {}
            for d in dati:
                servizio = self._servizio_repo.trovaPerId(d["servizio_codice"])
                cliente  = self._utilizzatore_repo.trovaPerId(d["cliente_codice"])
                # ricostruisco anche lo ski-man responsabile del DIN, se registrato
                skiman = None
                if d.get("skiman_codice") is not None:
                    skiman = self._utilizzatore_repo.trovaPerId(d["skiman_codice"])
                if servizio and cliente: # controllo che esistano entrambi
                    self._assegnamenti[d["codice"]] = Assegnamento(
                        d["codice"],
                        datetime.fromisoformat(d["dataOraInizio"]),
                        datetime.fromisoformat(d["dataOraFine"]),
                        d["fasciaOraria"], servizio, cliente,
                        d["valoreDIN"], skiman
                    )
        except FileNotFoundError:
            self._assegnamenti = {} 

    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([a.toDict() for a in self._assegnamenti.values()], f)

    def trovaPerId(self, codice: int):
        return self._assegnamenti.get(codice)

    def aggiungi(self, assegnamento: Assegnamento) -> None:
        self._assegnamenti[assegnamento.getCodice()] = assegnamento
        self.salva()

    def rimuovi(self, codice: int) -> None:
        if codice in self._assegnamenti:
            del self._assegnamenti[codice]
            self.salva()

    def tutti(self) -> list:
        return list(self._assegnamenti.values())
