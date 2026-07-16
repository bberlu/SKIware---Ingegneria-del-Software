import json
from datetime import datetime
from Models import Ricevuta
from Repos.assegnamento_repository import AssegnamentoRepository

class RicevutaRepository: # Repos
    # la Ricevuta dipende da un Assegnamento per esistere
    # per ricostruirla serve il repository degli assegnamenti
    def __init__(self, path: str = "Data/ricevute.json",
                 assegnamento_repo: AssegnamentoRepository = None):
        self._path              = path
        self._assegnamento_repo = assegnamento_repo 
        self._ricevute: dict = {} # chiave = codice della ricevuta
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                dati = json.load(f)
            self._ricevute = {}
            for d in dati:
                assegnamento = self._assegnamento_repo.trovaPerId(d["assegnamento_codice"])
                if assegnamento: # controllo che esiste
                    self._ricevute[d["codice"]] = Ricevuta(
                        d["codice"],
                        datetime.fromisoformat(d["dataOraEmissione"]),
                        d["importoTotale"], assegnamento, d["anno"]
                    )
        except FileNotFoundError:
            self._ricevute = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([r.toDict() for r in self._ricevute.values()], f)

    def trovaPerId(self, codice: int):
        return self._ricevute.get(codice)

    def aggiungi(self, ricevuta: Ricevuta) -> None:
        self._ricevute[ricevuta.getCodice()] = ricevuta
        self.salva()

    def rimuovi(self, codice: int) -> None: 
        if codice in self._ricevute:
            del self._ricevute[codice]
            self.salva()

    def tutti(self) -> list:
        return list(self._ricevute.values())
