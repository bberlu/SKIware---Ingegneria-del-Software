from Models.utilizzatore import Utilizzatore

class Cliente(Utilizzatore): # Entity - eredita da Utilizzatore
    def __init__(self, codice: int, codiceFiscale: str, cognome: str,
                 email: str, nome: str, password: str, telefono: int,
                 altezza: float, eta: int, livelloAbilita: str,
                 misuraScarponi: int, peso: float):
        # richiama il costruttore della classe base per gli attributi comuni
        super().__init__(codice, codiceFiscale, cognome, email, nome, password, telefono)
        # attributi propri di Cliente
        self._altezza        = altezza        
        self._eta            = eta            
        self._livelloAbilita = livelloAbilita 
        self._misuraScarponi = misuraScarponi 
        self._peso           = peso           

    # il cliente NON accede direttamente al sistema
    # le operazioni che lo riguardano le svolge il personale allo sportello
    # ridefinisce il metodo della classe base 
    def puoAccedere(self) -> bool:
        return False

    def getAltezza(self) -> float:
        return self._altezza

    def getEta(self) -> int:
        return self._eta

    def getLivelloAbilita(self) -> str:
        return self._livelloAbilita

    def getMisuraScarponi(self) -> int:
        return self._misuraScarponi

    def getPeso(self) -> float:
        return self._peso

    def setAltezza(self, v: float) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("altezza deve essere un numero") # controllo setter
        self._altezza = float(v)

    def setEta(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("eta deve essere int")
        self._eta = v

    def setLivelloAbilita(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("livelloAbilita deve essere str")
        self._livelloAbilita = v

    def setMisuraScarponi(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("misuraScarponi deve essere int")
        self._misuraScarponi = v

    def setPeso(self, v: float) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("peso deve essere un numero")
        self._peso = float(v)

    # serializzatore
    def toDict(self) -> dict:
        d = super().toDict() # dict con gli attributi ereditati da Utilizzatore
        d.update({
            "altezza": self._altezza,
            "eta": self._eta,
            "livelloAbilita": self._livelloAbilita,
            "misuraScarponi": self._misuraScarponi,
            "peso": self._peso
        })
        return d

    # costruttore alternativo
    @classmethod
    def fromDict(cls, d: dict) -> "Cliente":
        return cls(d["codice"], d["codiceFiscale"], d["cognome"],
                   d["email"], d["nome"], d["password"], d["telefono"],
                   d["altezza"], d["eta"], d["livelloAbilita"],
                   d["misuraScarponi"], d["peso"]) 

    # dunder method
    def __str__(self) -> str:
        return (f"{self.getNome()} {self.getCognome()} (codice: {self.getCodice()}) — "
                f"livello: {self._livelloAbilita}, scarponi: {self._misuraScarponi}")
