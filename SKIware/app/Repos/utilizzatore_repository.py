import json
from Models import Cliente, SkiMan, Amministratore

class UtilizzatoreRepository: # Repos
    # un unico file di persistenza per tutti gli utilizzatori

    _CLASSI = {
        "Cliente": Cliente,
        "SkiMan": SkiMan,
        "Amministratore": Amministratore
    }

    def __init__(self, path: str = "Data/utilizzatori.json"):
        self._path = path # file di persistenza a cui deve puntare la repository
        self._utilizzatori: dict = {} 
        self.carica() # la repo carica immediatamente gli oggetti dalla memoria

    def carica(self) -> None: # ricrea gli oggetti dal file di persistenza
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                dati = json.load(f) # lista di dict, uno per utilizzatore
            self._utilizzatori = {
                d["codice"]: self._CLASSI[d["tipo"]].fromDict(d) for d in dati
                # d["tipo"] dice quale sottoclasse ricreare (Cliente, SkiMan, Amministratore)
            }
        except FileNotFoundError:
            self._utilizzatori = {} # al primo avvio

    def salva(self) -> None:
        dati = []
        for u in self._utilizzatori.values():
            d = u.toDict()
            d["tipo"] = type(u).__name__ # salvo anche il tipo per poterlo ricreare
            dati.append(d)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(dati, f)

    def trovaPerId(self, codice: int):
        return self._utilizzatori.get(codice) # la ricerca nei dict è per chiave

    def trovaPerCF(self, codiceFiscale: str):
        for u in self._utilizzatori.values():
            if u.getCodiceFiscale() == codiceFiscale:
                return u
        return None

    def trovaPerNomeCognome(self, nome: str, cognome: str):
        for u in self._utilizzatori.values():
            if u.getNome() == nome and u.getCognome() == cognome:
                return u
        return None

    def aggiungi(self, utilizzatore) -> None:
        self._utilizzatori[utilizzatore.getCodice()] = utilizzatore
        self.salva()

    def rimuovi(self, codice: int) -> None:
        if codice in self._utilizzatori:
            del self._utilizzatori[codice]
            self.salva()

    def tutti(self) -> list:
        return list(self._utilizzatori.values())
