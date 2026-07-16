from Models.servizio import Servizio

class AttrezzaturaPrincipale(Servizio): # Entity - classe astratta nell'UML
    def __init__(self, codice: str, descrizione: str, prezzo: float,
                 livelloTecnico: str, stato: str = "Disponibile"):
    
        super().__init__(codice, descrizione, prezzo, stato)
    
        self._livelloTecnico = livelloTecnico 

    def getLivelloTecnico(self) -> str:
        return self._livelloTecnico

    def setLivelloTecnico(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("livelloTecnico deve essere str") # controllo setter
        self._livelloTecnico = v

    # serializzatore: aggiunge livelloTecnico al dict della classe base
    def toDict(self) -> dict:
        d = super().toDict() # dict con gli attributi ereditati da Servizio
        d.update({
            "livelloTecnico": self._livelloTecnico
        })
        return d

    # costruttore alternativo
    @classmethod
    def fromDict(cls, d: dict) -> "AttrezzaturaPrincipale":
        return cls(d["codice"], d["descrizione"], d["prezzo"],
                   d["livelloTecnico"], d["stato"])

    # dunder method
    def __str__(self) -> str:
        return (f"{self._descrizione} ({self._codice}) — livello {self._livelloTecnico}, "
                f"{self._stato}, {self._prezzo}€")
