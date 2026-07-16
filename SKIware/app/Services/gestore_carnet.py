from datetime import datetime, timedelta
from Repos import CarnetRepository, PrenotazioneRepository, ServizioRepository
from Models import Carnet, Prenotazione, Cliente
from Services.gestore_noleggi import GestoreNoleggi 

class GestoreCarnet: # Control
    # gestisce i casi d'uso "Vendita e Gestione Carnet", "Inserisci Prenotazione"
    # e "Disdetta Prenotazione e Rimborsi" (con i relativi vincoli temporali).
    def __init__(self, carnet_repo: CarnetRepository,
                 prenotazione_repo: PrenotazioneRepository,
                 servizio_repo: ServizioRepository):
        self._carnet_repo       = carnet_repo
        self._prenotazione_repo = prenotazione_repo
        self._servizio_repo     = servizio_repo

    
    def vendiCarnet(self, cliente: Cliente, tipo: int,
                    stagionale: bool = False) -> Carnet:
        codice = self._generaCodiceUnivoco() 
        carnet = Carnet(codice, datetime.now(), tipo, stagionale)
        carnet.associaCliente(cliente) 
        self._carnet_repo.aggiungi(carnet) 
        return carnet

    def _generaCodiceUnivoco(self) -> int:
        codici = [c.getCodice() for c in self._carnet_repo.tutti()]
        return max(codici) + 1 if codici else 1


    # un carnet è attivo se è stagionale oppure se ha ancora saldo residuo
    def verificaCarnetAttivo(self, cliente: Cliente) -> bool:
        return self._carnetDelCliente(cliente) is not None

    def _carnetDelCliente(self, cliente: Cliente):
        for c in self._carnet_repo.tutti():
            if c.getCliente() is not None \
               and c.getCliente().getCodice() == cliente.getCodice() \
               and (c.isStagionale() or c.verificaSaldoSufficiente()):
                return c
        return None

    # come da UML: decurtaCredito(carnet: Carnet, valore: int): void
    def decurtaCredito(self, carnet: Carnet, valore: int) -> None:
        carnet.aggiornaCredito(-valore)
        self._carnet_repo.salva() 

    # come da UML: vincoloTemporalePrenotazione(data: datetime): bool
    # (caso d'uso "Vincolo Temporale 24h": si prenota con almeno 24h di anticipo)
    def vincoloTemporalePrenotazione(self, data: datetime) -> bool:
        return data - datetime.now() >= timedelta(hours=24)

   
    def verificaFinestra48h(self, prenotazione: Prenotazione) -> bool:
        return prenotazione.getDataOraInizio() - datetime.now() >= timedelta(hours=48)

    # la prenotazione BLOCCA l'attrezzatura, quindi non sono ammesse due
    # prenotazioni della stessa attrezzatura nello stesso giorno con fasce
    # sovrapposte 
    def verificaDisponibilita(self, servizio, data: datetime, fascia: str) -> bool:
        for p in self._prenotazione_repo.tutti():
            if (p.getServizio().getCodice() == servizio.getCodice()
                    and p.getDataOraInizio().date() == data.date()
                    and (p.getFasciaOraria() == fascia
                         or "giornata" in (p.getFasciaOraria(), fascia))):
                return False
        return True

 
    def inserisciPrenotazione(self, cliente: Cliente, servizio, data: datetime,
                              fascia: str):
        if servizio is None or servizio.getStato() != "Disponibile":
            return "Errore: attrezzatura non trovata o non disponibile"
        if not self.vincoloTemporalePrenotazione(data):
            return "Errore: la prenotazione richiede almeno 24h di anticipo"
       
        if not GestoreNoleggi.vincoloAperturaStagionale(data):
            return "Errore: data fuori stagione"
        # la fascia oraria deve essere una di quelle ammesse dal gestionale

        if fascia not in GestoreNoleggi.FASCE_ORARIE:
            return "Errore: indisponibilità temporale"
        # RF14: l'attrezzatura non deve essere già bloccata da un'altra
        # prenotazione per lo stesso giorno e fascia 

        if not self.verificaDisponibilita(servizio, data, fascia):
            return "Errore: attrezzatura già prenotata per la data e fascia indicate"
        carnet = self._carnetDelCliente(cliente)
        if carnet is None:
            return "Errore: il cliente non ha un carnet attivo"
        if not carnet.isStagionale():
            self.decurtaCredito(carnet, 1) 
        codici = [p.getCodice() for p in self._prenotazione_repo.tutti()]
        codice = max(codici) + 1 if codici else 1
        prenotazione = Prenotazione(codice, data, fascia, servizio, cliente)
        self._prenotazione_repo.aggiungi(prenotazione)
        return prenotazione #ritorna quella creata

    
    def ricercaPrenotazione(self, codice: int):
        return self._prenotazione_repo.trovaPerId(codice)

 
    def disdiciPrenotazione(self, codice: int) -> str:
        prenotazione = self._prenotazione_repo.trovaPerId(codice)
        if prenotazione is None:
            return "Errore: prenotazione non trovata"
        if self.verificaFinestra48h(prenotazione): # rimborso
            carnet = self._carnetDelCliente(prenotazione.getCliente())
            if carnet is not None and not carnet.isStagionale():
                carnet.aggiornaCredito(1) # riaccredito dell'ingresso
                self._carnet_repo.salva()
            self._prenotazione_repo.rimuovi(codice) 
            return "Disdetta con rimborso ok"
        self._prenotazione_repo.rimuovi(codice) 
        return "Disdetta senza rimborso, credito perso"


    def rimuoviCarnet(self, codice: int) -> str:
        if self._carnet_repo.trovaPerId(codice) is None:
            return "Errore: carnet non trovato"
        self._carnet_repo.rimuovi(codice)
        return "Rimozione ok"

  
    def eliminaPrenotazione(self, codice: int) -> str:
        if self._prenotazione_repo.trovaPerId(codice) is None:
            return "Errore: prenotazione non trovata"
        self._prenotazione_repo.rimuovi(codice)
        return "Rimozione ok"

    def elencaCarnet(self) -> list: # la Boundary parla con il Control
        return self._carnet_repo.tutti()

    def elencaPrenotazioni(self) -> list:
        return self._prenotazione_repo.tutti()
