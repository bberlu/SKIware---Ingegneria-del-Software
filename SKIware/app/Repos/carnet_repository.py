import json
from Models import Carnet

class CarnetRepository: # Repos
    def __init__(self, path: str = "Data/carnet.json",
                 utilizzatore_repo = None):
        self._path = path
        self._utilizzatore_repo = utilizzatore_repo # realizza l'associazione Cliente-Carnet
        self._carnet: dict = {} # chiave = codice del carnet, valore = l'OGGETTO Carnet stesso
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                dati = json.load(f)
            self._carnet = {}
            for d in dati:
                carnet = Carnet.fromDict(d)
                # ricostruisco l'associazione con il Cliente tramite il codice salvato
                if d.get("cliente_codice") is not None and self._utilizzatore_repo:
                    cliente = self._utilizzatore_repo.trovaPerId(d["cliente_codice"])
                    if cliente:
                        carnet.associaCliente(cliente)
                self._carnet[d["codice"]] = carnet
        except FileNotFoundError:
            self._carnet = {} # al primo avvio

    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump([c.toDict() for c in self._carnet.values()], f)

    def trovaPerId(self, codice: int): 
        return self._carnet.get(codice)

    def aggiungi(self, carnet: Carnet) -> None:
        self._carnet[carnet.getCodice()] = carnet
        self.salva()

    def rimuovi(self, codice: int) -> None: 
        if codice in self._carnet:
            del self._carnet[codice]
            self.salva()

    def tutti(self) -> list:
        return list(self._carnet.values())
