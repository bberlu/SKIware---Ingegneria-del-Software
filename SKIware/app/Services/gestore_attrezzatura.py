from Repos import ServizioRepository, AssegnamentoRepository
from Models import (Sci, Snowboard, Scarpone, Casco, Armadietto,
                    AttrezzaturaPrincipale, Cliente)

class GestoreAttrezzatura: # Control
    # gestisce i casi d'uso CUD dell'attrezzatura e il vincolo
    # di assegnazione degli armadietti (sd AssegnaArmadietto)
    def __init__(self, servizio_repo: ServizioRepository,
                 assegnamento_repo: AssegnamentoRepository = None):
        self._servizio_repo     = servizio_repo
        self._assegnamento_repo = assegnamento_repo # serve per il vincolo armadietti

    # inserimento attrezzatura
    def aggiungiSci(self, codice: str, descrizione: str, prezzo: float,
                    livelloTecnico: str) -> str:
        if self._servizio_repo.trovaPerId(codice) is not None:
            return "Il servizio esiste già"
        self._servizio_repo.aggiungi(Sci(codice, descrizione, prezzo, livelloTecnico))
        return f"Inserimento ok: {self._servizio_repo.trovaPerId(codice)}"

    def aggiungiSnowboard(self, codice: str, descrizione: str, prezzo: float,
                          livelloTecnico: str) -> str:
        if self._servizio_repo.trovaPerId(codice) is not None:
            return "Il servizio esiste già"
        self._servizio_repo.aggiungi(Snowboard(codice, descrizione, prezzo, livelloTecnico))
        return f"Inserimento ok: {self._servizio_repo.trovaPerId(codice)}"

    def aggiungiScarpone(self, codice: str, descrizione: str, prezzo: float) -> str:
        if self._servizio_repo.trovaPerId(codice) is not None:
            return "Il servizio esiste già"
        self._servizio_repo.aggiungi(Scarpone(codice, descrizione, prezzo))
        return f"Inserimento ok: {self._servizio_repo.trovaPerId(codice)}"

    def aggiungiCasco(self, codice: str, descrizione: str, prezzo: float) -> str:
        if self._servizio_repo.trovaPerId(codice) is not None:
            return "Il servizio esiste già"
        self._servizio_repo.aggiungi(Casco(codice, descrizione, prezzo))
        return f"Inserimento ok: {self._servizio_repo.trovaPerId(codice)}"

    def aggiungiArmadietto(self, codice: str, descrizione: str, prezzo: float,
                           dimensione: str) -> str:
        if self._servizio_repo.trovaPerId(codice) is not None:
            return "Il servizio esiste già"
        self._servizio_repo.aggiungi(Armadietto(codice, descrizione, prezzo, dimensione))
        return f"Inserimento ok: {self._servizio_repo.trovaPerId(codice)}"

    def rimuoviServizio(self, codice: str) -> str:
        servizio = self._servizio_repo.trovaPerId(codice)
        if servizio is None:
            return "Servizio non trovato"
        if servizio.getStato() != "Disponibile": # non si rimuove attrezzatura assegnata!
            return "Impossibile rimuovere: il servizio non è disponibile"
        self._servizio_repo.rimuovi(codice)
        return "Rimozione ok"

    # vincolo armadietti
    # l'armadietto si può assegnare solo a un cliente che ha già un noleggio
    # ATTIVO di un'attrezzatura principale (Sci o Snowboard)
    def verificaVincoloNoleggioPrincipale(self, cliente: Cliente) -> bool:
        for a in self._assegnamento_repo.tutti():
            if a.getCliente().getCodice() == cliente.getCodice() \
               and isinstance(a.getServizio(), AttrezzaturaPrincipale) \
               and not a.verificaFine(): # il noleggio principale è ancora attivo
                return True
        return False

    def ricercaServizio(self, codice: str): 
        return self._servizio_repo.trovaPerId(codice)

    def elencaServizi(self) -> list: # la boundary parla con il control
        return self._servizio_repo.tutti()

    def elencaDisponibili(self) -> list:
        return [s for s in self._servizio_repo.tutti() if s.getStato() == "Disponibile"]
