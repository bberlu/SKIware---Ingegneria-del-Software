from datetime import datetime
from Models import Cliente, Servizio

class Prenotazione: # Entity
    def __init__(self, codice: int, dataOraInizio: datetime,
                 fasciaOraria: str, servizio: Servizio, cliente: Cliente):
        self._codice        = codice        
        self._dataOraInizio = dataOraInizio 
        self._fasciaOraria  = fasciaOraria  
        self._servizio      = servizio      
        self._cliente       = cliente      

    def getCodice(self) -> int:
        return self._codice

    def getDataOraInizio(self) -> datetime:
        return self._dataOraInizio

    def getFasciaOraria(self) -> str:
        return self._fasciaOraria

    def getServizio(self) -> Servizio:
        return self._servizio

    def getCliente(self) -> Cliente:
        return self._cliente

    # True se la data/ora di inizio della prenotazione è già passata
    def verificaFine(self) -> bool:
        return datetime.now() >= self._dataOraInizio

    # serializzatore
    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "dataOraInizio": self._dataOraInizio.isoformat(),
            "fasciaOraria": self._fasciaOraria,
            "servizio_codice": self._servizio.getCodice(),
            "cliente_codice": self._cliente.getCodice()
        }

    # dunder method
    def __str__(self) -> str:
        return (f"Prenotazione {self._codice}: {self._servizio.getDescrizione()} → "
                f"{self._cliente.getNome()} {self._cliente.getCognome()} "
                f"il {self._dataOraInizio} ({self._fasciaOraria})")
