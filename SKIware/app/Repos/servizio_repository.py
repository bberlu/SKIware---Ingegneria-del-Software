import json
from Models import Sci, Snowboard, Scarpone, Casco, Armadietto

class ServizioRepository: # Repos
    # un unico file di persistenza per tutti i servizi


    _CLASSI = {
        "Sci": Sci,
        "Snowboard": Snowboard,
        "Scarpone": Scarpone,
        "Casco": Casco,
        "Armadietto": Armadietto
    }

    def __init__(self, path: str = "Data/servizi.json"):
        self._path = path # file di persistenza a cui deve puntare la repository
        self._servizi: dict = {} 
        self.carica()

    def carica(self) -> None: # ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                dati = json.load(f)
            self._servizi = {
                d["codice"]: self._CLASSI[d["tipo"]].fromDict(d) for d in dati
                # d["tipo"] dice quale sottoclasse ricreare (Sci, Snowboard, ...)
            }
        except FileNotFoundError:
            self._servizi = {} # al primo avvio

    def salva(self) -> None:
        dati = []
        for s in self._servizi.values():
            d = s.toDict()
            d["tipo"] = type(s).__name__ # salvo anche il tipo per poterlo ricreare
            dati.append(d)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(dati, f)

    def trovaPerId(self, codice: str):
        return self._servizi.get(codice)

    def aggiungi(self, servizio) -> None:
        self._servizi[servizio.getCodice()] = servizio
        self.salva()

    def rimuovi(self, codice: str) -> None: 
        if codice in self._servizi:
            del self._servizi[codice]
            self.salva()

    def tutti(self) -> list:
        return list(self._servizi.values())
