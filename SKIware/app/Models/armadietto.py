from Models.servizio import Servizio

class Armadietto(Servizio): # Entity - eredita da Servizio 
    def __init__(self, codice: str, descrizione: str, prezzo: float,
                 dimensione: str, stato: str = "Disponibile"):
        # richiama il costruttore della classe base per gli attributi comuni
        super().__init__(codice, descrizione, prezzo, stato)
        # attributo proprio di Armadietto 
        self._dimensione = dimensione 

    def getDimensione(self) -> str:
        return self._dimensione

    def setDimensione(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("dimensione deve essere str") # controllo sui setter
        self._dimensione = v

    # serializzatore: aggiunge dimensione al dict della classe base
    def toDict(self) -> dict:
        d = super().toDict() # dict con gli attributi ereditati da Servizio
        d.update({
            "dimensione": self._dimensione
        })
        return d

    # costruttore alternativo
    @classmethod
    def fromDict(cls, d: dict) -> "Armadietto":
        return cls(d["codice"], d["descrizione"], d["prezzo"],
                   d["dimensione"], d["stato"])

    # dunder method
    def __str__(self) -> str:
        return (f"Armadietto {self._dimensione}: {self._descrizione} "
                f"({self._codice}) — {self._stato}, {self._prezzo}€")
