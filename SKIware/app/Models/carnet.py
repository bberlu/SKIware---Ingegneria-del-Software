from datetime import datetime

class Carnet: # Entity
    def __init__(self, codice: int, dataRilascio: datetime,
                 saldoResiduo: int, stagionale: bool = False,
                 cliente = None):

        # per convenzione indico con _ gli attributi da considerarsi private
        self._codice       = codice     
        self._dataRilascio = dataRilascio 
        self._saldoResiduo = saldoResiduo
        self._stagionale   = stagionale   
        self._cliente      = cliente      
        # realizza l'associazione Cliente-Carnet dell'UML

    def getCliente(self):
        return self._cliente

    def associaCliente(self, cliente) -> None:
        self._cliente = cliente

    def getCodice(self) -> int:
        return self._codice

    def getDataRilascio(self) -> datetime:
        return self._dataRilascio

    def getSaldoResiduo(self) -> int:
        return self._saldoResiduo

    def isStagionale(self) -> bool:
        return self._stagionale

    def aggiornaCredito(self, valore: int) -> None:
        if not isinstance(valore, int):
            raise TypeError("valore deve essere int") # controllo settter
        if self._saldoResiduo + valore < 0:
            raise ValueError("saldo residuo insufficiente")
        self._saldoResiduo += valore

 
    def verificaSaldoSufficiente(self) -> bool:
        return self._saldoResiduo > 0

    # serializzatore
    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "dataRilascio": self._dataRilascio.isoformat(),
            "saldoResiduo": self._saldoResiduo,
            "stagionale": self._stagionale,
            # del cliente associato si salva solo il codice 
            "cliente_codice": self._cliente.getCodice() if self._cliente else None
        }

    # costruttore alternativo
    @classmethod
    def fromDict(cls, d: dict) -> "Carnet":
        return cls(d["codice"],
                   datetime.fromisoformat(d["dataRilascio"]),
                   d["saldoResiduo"], d["stagionale"])

    # dunder method
    def __str__(self) -> str:
        tipo = "stagionale" if self._stagionale else "a ingressi"
        return f"Carnet {self._codice} ({tipo}) — saldo residuo: {self._saldoResiduo}"
