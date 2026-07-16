from datetime import datetime
from Models import Assegnamento

class Ricevuta: # Entity
    def __init__(self, codice: int, dataOraEmissione: datetime,
                 importoTotale: float, assegnamento: Assegnamento,
                 anno: int = None):
        self._codice           = codice         
        self._dataOraEmissione = dataOraEmissione 
        self._importoTotale    = importoTotale    
        self._assegnamento     = assegnamento     
        # se l'anno non viene indicato, si ricava dalla data di emissione
        self._anno = anno if anno is not None else dataOraEmissione.year

    def getCodice(self) -> int:
        return self._codice

    def getDataOraEmissione(self) -> datetime:
        return self._dataOraEmissione

    def getImportoTotale(self) -> float:
        return self._importoTotale

    def getAssegnamento(self) -> Assegnamento:
        return self._assegnamento

    def getAnno(self) -> int:
        return self._anno

    # serializzatore
    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "anno": self._anno,
            "dataOraEmissione": self._dataOraEmissione.isoformat(),
            "importoTotale": self._importoTotale,
            "assegnamento_codice": self._assegnamento.getCodice()
        }

    # dunder method
    def __str__(self) -> str:
        return (f"Ricevuta {self._anno}/{self._codice} del {self._dataOraEmissione} — "
                f"totale: {self._importoTotale}€")
