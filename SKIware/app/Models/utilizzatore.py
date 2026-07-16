class Utilizzatore: # Entity - classe astratta nell'UML: non va istanziata direttamente,
    # serve solo come classe base per Cliente, SkiMan e Amministratore
    def __init__(self, codice: int, codiceFiscale: str, cognome: str,
                 email: str, nome: str, password: str, telefono: int):
       
        # per convenzione indico con _ gli attributi da considerarsi private
        self.validaPassword(password) 
        self._codice        = codice    
        self._codiceFiscale = codiceFiscale 
        self._cognome       = cognome     
        self._email         = email         
        self._nome          = nome          
        self._password      = password     
        self._telefono      = telefono      

    # password almeno 7 caratteri,
    @staticmethod
    def validaPassword(v) -> None:
        if not isinstance(v, str):
            raise TypeError("password deve essere str")
        if len(v) < 7 or not v.isalnum():
            raise ValueError("la password deve avere almeno "
                             "7 caratteri alfanumerici")

    def getCodice(self) -> int:
        return self._codice

    def getCodiceFiscale(self) -> str:
        return self._codiceFiscale

    def getCognome(self) -> str:
        return self._cognome

    def getEmail(self) -> str:
        return self._email

    def getNome(self) -> str:
        return self._nome

    def getPassword(self) -> str:
        return self._password

    def getTelefono(self) -> int:
        return self._telefono

    # questo tipo di utilizzatore puo accedere al sistema?
    def puoAccedere(self) -> bool:
        return True

    def setEmail(self, v: str) -> None:
        if not isinstance(v, str):
            raise TypeError("email deve essere str") # controllo da fare sempre sui setter
        self._email = v

    def setPassword(self, v: str) -> None:
        self.validaPassword(v) # controllo setter
        self._password = v

    def setTelefono(self, v: int) -> None:
        if not isinstance(v, int):
            raise TypeError("telefono deve essere int")
        self._telefono = v

    # serializzatore
    # converto prima la classe in un dict
    def toDict(self) -> dict:
        return {
            "codice": self._codice,
            "codiceFiscale": self._codiceFiscale,
            "cognome": self._cognome,
            "email": self._email,
            "nome": self._nome,
            "password": self._password,
            "telefono": self._telefono
        }

    # costruttore alternativo
    @classmethod
    def fromDict(cls, d: dict) -> "Utilizzatore":
        return cls(d["codice"], d["codiceFiscale"], d["cognome"],
                   d["email"], d["nome"], d["password"], d["telefono"])

    # dunder method
    def __str__(self) -> str:
        return f"{self._nome} {self._cognome} (codice: {self._codice})"
