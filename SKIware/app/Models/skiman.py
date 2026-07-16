from datetime import datetime
from Models.utilizzatore import Utilizzatore

class SkiMan(Utilizzatore): # Entity - eredita da Utilizzatore
    def __init__(self, codice: int, codiceFiscale: str, cognome: str,
                 email: str, nome: str, password: str, telefono: int,
                 dataNascita: datetime, luogoNascita: str, qualificaTecnica: str):
        # richiama il costruttore della classe base per gli attributi comuni
        super().__init__(codice, codiceFiscale, cognome, email, nome, password, telefono)
        # attributi propri di SkiMan 
        self._dataNascita      = dataNascita    
        self._luogoNascita     = luogoNascita     
        self._qualificaTecnica = qualificaTecnica 

    def getDataNascita(self) -> datetime:
        return self._dataNascita

    def getLuogoNascita(self) -> str:
        return self._luogoNascita

    def getQualificaTecnica(self) -> str:
        return self._qualificaTecnica

    def setQualificaTecnica(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("qualificaTecnica deve essere str") # controllo setter
        self._qualificaTecnica = v

    # serializzatore
    def toDict(self) -> dict:
        d = super().toDict() 
        d.update({
            "dataNascita": self._dataNascita.isoformat(),
            "luogoNascita": self._luogoNascita,
            "qualificaTecnica": self._qualificaTecnica
        })
        return d

    # costruttore
    @classmethod
    def fromDict(cls, d: dict) -> "SkiMan":
        return cls(d["codice"], d["codiceFiscale"], d["cognome"],
                   d["email"], d["nome"], d["password"], d["telefono"],
                   datetime.fromisoformat(d["dataNascita"]),
                   d["luogoNascita"], d["qualificaTecnica"])

    # dunder method
    def __str__(self) -> str:
        return (f"SkiMan {self.getNome()} {self.getCognome()} "
                f"(codice: {self.getCodice()}) — {self._qualificaTecnica}")
