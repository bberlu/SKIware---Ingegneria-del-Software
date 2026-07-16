from datetime import datetime
from Repos import UtilizzatoreRepository
from Models import Cliente, SkiMan, Amministratore

class GestoreUtenti: # Control
    # gestisce i casi d'uso CUD degli utilizzatori
    # inserimento, modifica e rimozione degli utilizzatori
    def __init__(self, utilizzatore_repo: UtilizzatoreRepository):
        self._utilizzatore_repo = utilizzatore_repo

    def aggiungiCliente(self, codice: int, codiceFiscale: str, cognome: str,
                        email: str, nome: str, password: str, telefono: int,
                        altezza: float, eta: int, livelloAbilita: str,
                        misuraScarponi: int, peso: float) -> str:
     
        if self._utilizzatore_repo.trovaPerId(codice) is not None \
           or self._utilizzatore_repo.trovaPerCF(codiceFiscale) is not None:
            return "Il cliente esiste già"
        try:
            cliente = Cliente(codice, codiceFiscale, cognome, email, nome, password,
                              telefono, altezza, eta, livelloAbilita, misuraScarponi, peso)
        except ValueError as e: 
            return f"Errore: {e}"
        self._utilizzatore_repo.aggiungi(cliente) 
        return f"Inserimento ok: {cliente}"

    def aggiungiSkiMan(self, codice: int, codiceFiscale: str, cognome: str,
                       email: str, nome: str, password: str, telefono: int,
                       dataNascita: datetime, luogoNascita: str,
                       qualificaTecnica: str) -> str:
        if self._utilizzatore_repo.trovaPerId(codice) is not None \
           or self._utilizzatore_repo.trovaPerCF(codiceFiscale) is not None:
            return "Lo ski-man esiste già"
        try:
            skiman = SkiMan(codice, codiceFiscale, cognome, email, nome, password,
                            telefono, dataNascita, luogoNascita, qualificaTecnica)
        except ValueError as e: 
            return f"Errore: {e}"
        self._utilizzatore_repo.aggiungi(skiman)
        return f"Inserimento ok: {skiman}"

    def aggiungiAmministratore(self, codice: int, codiceFiscale: str, cognome: str,
                               email: str, nome: str, password: str,
                               telefono: int) -> str:
        if self._utilizzatore_repo.trovaPerId(codice) is not None \
           or self._utilizzatore_repo.trovaPerCF(codiceFiscale) is not None:
            return "L'amministratore esiste già"
        try:
            amministratore = Amministratore(codice, codiceFiscale, cognome, email,
                                            nome, password, telefono)
        except ValueError as e: 
            return f"Errore: {e}"
        self._utilizzatore_repo.aggiungi(amministratore)
        return f"Inserimento ok: {amministratore}"

   
    def modificaCliente(self, codice: int, dati: dict) -> str:
        cliente = self._utilizzatore_repo.trovaPerId(codice)
        if cliente is None:
            return "Cliente non trovato"
        # ogni campo modificabile è associato al proprio setter
    
        setters = {
            "email": cliente.setEmail,
            "password": cliente.setPassword,
            "telefono": cliente.setTelefono,
            "altezza": cliente.setAltezza,
            "eta": cliente.setEta,
            "livelloAbilita": cliente.setLivelloAbilita,
            "misuraScarponi": cliente.setMisuraScarponi,
            "peso": cliente.setPeso,
        }
        for campo, valore in dati.items():
            setter = setters.get(campo)
            if setter is None:
                return f"Campo '{campo}' non modificabile"
            try:
                setter(valore) # i setter fanno i controlli
            except (TypeError, ValueError) as e:
                return f"Errore: {e}"
        self._utilizzatore_repo.salva()
        return f"Modifica ok: {cliente}"

    # come da act CUD Cliente, ricerca, se trovato -> destroy
    def rimuoviCliente(self, codice: int) -> str:
        cliente = self._utilizzatore_repo.trovaPerId(codice)
        if cliente is None or not isinstance(cliente, Cliente):
            return "Cliente non trovato"
        self._utilizzatore_repo.rimuovi(codice)
        return "Rimozione ok"

    
    def rimuoviSkiMan(self, codice: int) -> str:
        skiman = self._utilizzatore_repo.trovaPerId(codice)
        if skiman is None or not isinstance(skiman, SkiMan):
            return "Ski-man non trovato"
        self._utilizzatore_repo.rimuovi(codice)
        return "Rimozione ok"

    
    def rimuoviAmministratore(self, codice: int) -> str:
        amministratore = self._utilizzatore_repo.trovaPerId(codice)
        if amministratore is None or not isinstance(amministratore, Amministratore):
            return "Amministratore non trovato"
        self._utilizzatore_repo.rimuovi(codice)
        return "Rimozione ok"

    # autentica l'utente tramite
    # codice e password; se le credenziali sono valide restituisce l'oggetto

    def autentica(self, codice: int, password: str):
        utilizzatore = self._utilizzatore_repo.trovaPerId(codice)
        if utilizzatore is not None and utilizzatore.getPassword() == password:
            return utilizzatore
        return None # credenziali non valide

    # le tre modalità di ricerca 
    def ricercaUtilizzatoreCodice(self, codice: int):
        return self._utilizzatore_repo.trovaPerId(codice)

    def ricercaUtilizzatoreCF(self, codiceFiscale: str):
        return self._utilizzatore_repo.trovaPerCF(codiceFiscale)

    def ricercaUtilizzatoreNomeCognome(self, nome: str, cognome: str):
        return self._utilizzatore_repo.trovaPerNomeCognome(nome, cognome)

    def elencaUtilizzatori(self) -> list: # boundary parla con il control
        return self._utilizzatore_repo.tutti()

    def elencaClienti(self) -> list:
        return [u for u in self._utilizzatore_repo.tutti() if isinstance(u, Cliente)]
