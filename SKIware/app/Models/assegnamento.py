from datetime import datetime
from Models import Cliente, Servizio

class Assegnamento: # Entity
    def __init__(self, codice: int, dataOraInizio: datetime, dataOraFine: datetime,
                 fasciaOraria: str, servizio: Servizio, cliente: Cliente,
                 valoreDIN: float = None, skiman = None):
        self._codice        = codice        
        self._dataOraInizio = dataOraInizio 
        self._dataOraFine   = dataOraFine   
        self._fasciaOraria  = fasciaOraria  
        self._servizio      = servizio      
        self._cliente       = cliente      
        self._valoreDIN     = valoreDIN     
        self._skiman        = skiman        
        #i parametri valoreDIN e skiman servono
        # al repository per ricostruire l'oggetto dal file json

    def getCodice(self) -> int:
        return self._codice

    def getDataOraInizio(self) -> datetime:
        return self._dataOraInizio

    def getDataOraFine(self) -> datetime:
        return self._dataOraFine

    def getFasciaOraria(self) -> str:
        return self._fasciaOraria

    def getServizio(self) -> Servizio:
        return self._servizio

    def getCliente(self) -> Cliente:
        return self._cliente

    def getValoreDIN(self) -> float:
        return self._valoreDIN

    def setValoreDIN(self, v: float) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("valoreDIN deve essere un numero") # controllo setter
        self._valoreDIN = float(v)

    def getSkiMan(self):
        return self._skiman

    # registra valore DIN
    def registraDIN(self, valoreDIN: float, skiman) -> None:
        if self._skiman is not None: # l'associazione è irrevocabile!
            raise ValueError("valore DIN già registrato: l'associazione "
                             "dello ski-man è irrevocabile")
        self.setValoreDIN(valoreDIN) # il setter fa il controllo di tipo
        self._skiman = skiman

    # True se il noleggio è terminato
    def verificaFine(self) -> bool:
        return datetime.now() >= self._dataOraFine

    # serializzatore
    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "dataOraInizio": self._dataOraInizio.isoformat(),
            "dataOraFine": self._dataOraFine.isoformat(),
            "fasciaOraria": self._fasciaOraria,
            "servizio_codice": self._servizio.getCodice(),
            "cliente_codice": self._cliente.getCodice(),
            "valoreDIN": self._valoreDIN,
            # dello ski-man responsabile si salva solo il codice 
            "skiman_codice": self._skiman.getCodice() if self._skiman else None
        }

    # niente fromDict: per ricostruire l'Assegnamento servono gli oggetti
    # Servizio e Cliente

    # dunder method
    def __str__(self) -> str:
        din = f", DIN: {self._valoreDIN}" if self._valoreDIN is not None else ""
        return (f"Assegnamento {self._codice}: {self._servizio.getDescrizione()} → "
                f"{self._cliente.getNome()} {self._cliente.getCognome()} "
                f"dal {self._dataOraInizio} al {self._dataOraFine}{din}")
