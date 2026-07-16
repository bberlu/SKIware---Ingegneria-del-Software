class Servizio: # Entity 
    def __init__(self, codice: str, descrizione: str, prezzo: float,
                 stato: str = "Disponibile"):

        # per convenzione indico con _ gli attributi da considerarsi private
        self._codice      = codice     
        self._descrizione = descrizione 
        self._prezzo      = prezzo     
        self._stato       = stato       

    def getCodice(self) -> str:
        return self._codice

    def getDescrizione(self) -> str:
        return self._descrizione

    def getPrezzo(self) -> float:
        return self._prezzo

    def getStato(self) -> str:
        return self._stato

    # setter dello stato
    def aggiornaStato(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("stato deve essere str") 
        self._stato = v

    # serializzatore
    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "descrizione": self._descrizione,
            "prezzo": self._prezzo,
            "stato": self._stato
        }

    # costruttore
    @classmethod
    def fromDict(cls, d: dict) -> "Servizio":
        return cls(d["codice"], d["descrizione"], d["prezzo"], d["stato"])

    # dunder method
    
    def __str__(self) -> str:
        return f"{self._descrizione} ({self._codice}) — {self._stato}, {self._prezzo}€"
