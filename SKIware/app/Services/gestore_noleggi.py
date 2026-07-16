from datetime import datetime
from Repos import (AssegnamentoRepository, ServizioRepository,
                   UtilizzatoreRepository, RicevutaRepository)
from Models import Assegnamento, Ricevuta, Sci, Armadietto, SkiMan

class GestoreNoleggi: # Control
    # gestisce i casi d'uso "Inserisci Assegnamento",
    # "Consegna e Ritiro" e la gestione del valore DIN
    

    # vincolo di apertura stagionale (RF18): noleggi e prenotazioni sono
    # possibili esclusivamente dal 1 dicembre al 10 aprile 
    APERTURA_STAGIONE = (12, 1) # (mese, giorno)
    CHIUSURA_STAGIONE = (4, 10) # (mese, giorno)

    FASCE_ORARIE = ("mattina", "pomeriggio", "giornata")

    def __init__(self, assegnamento_repo: AssegnamentoRepository,
                 servizio_repo: ServizioRepository,
                 utilizzatore_repo: UtilizzatoreRepository,
                 ricevuta_repo: RicevutaRepository,
                 gestore_attrezzatura = None):
        self._assegnamento_repo    = assegnamento_repo
        self._servizio_repo        = servizio_repo
        self._utilizzatore_repo    = utilizzatore_repo
        self._ricevuta_repo        = ricevuta_repo
        self._gestore_attrezzatura = gestore_attrezzatura # per il vincolo armadietti

    # --- vincoli con metodo statico
    @staticmethod
    def vincoloAperturaStagionale(data: datetime) -> bool:
        giorno = (data.month, data.day)
      
        return (giorno >= GestoreNoleggi.APERTURA_STAGIONE
                or giorno <= GestoreNoleggi.CHIUSURA_STAGIONE)

    def verificaFasciaOraria(self, fascia: str) -> bool:
        return fascia in self.FASCE_ORARIE

    # inserimento assegnamento
    def inserisciAssegnamento(self, cliente_codice: int, servizio_codice: str,
                              dataOraInizio: datetime, dataOraFine: datetime,
                              fascia: str) -> str:
        cliente = self._utilizzatore_repo.trovaPerId(cliente_codice) 
        if cliente is None:
            return "Errore: cliente non trovato"
        servizio = self._servizio_repo.trovaPerId(servizio_codice) 
        if servizio is None or servizio.getStato() != "Disponibile":
            return "Errore: attrezzatura non disponibile"
       
        if not (self.vincoloAperturaStagionale(dataOraInizio)
                and self.vincoloAperturaStagionale(dataOraFine)):
            return "Errore: data fuori stagione"
        if not self.verificaFasciaOraria(fascia):
            return "Errore: indisponibilità temporale"
       

        if isinstance(servizio, Armadietto) and self._gestore_attrezzatura is not None:
            if not self._gestore_attrezzatura.verificaVincoloNoleggioPrincipale(cliente):
                return "Errore: cliente senza attrezzatura principale"

        codici = [a.getCodice() for a in self._assegnamento_repo.tutti()]
        codice = max(codici) + 1 if codici else 1
        assegnamento = Assegnamento(codice, dataOraInizio, dataOraFine,
                                    fascia, servizio, cliente)
        self._assegnamento_repo.aggiungi(assegnamento) 
        self._emissioneRicevuta(assegnamento) 
        return f"Assegnamento ok: {assegnamento}"

    def _emissioneRicevuta(self, assegnamento: Assegnamento) -> None:
        codici = [r.getCodice() for r in self._ricevuta_repo.tutti()]
        codice = max(codici) + 1 if codici else 1
        ricevuta = Ricevuta(codice, datetime.now(),
                            assegnamento.getServizio().getPrezzo(), assegnamento)
        self._ricevuta_repo.aggiungi(ricevuta)

    def rimuoviAssegnamento(self, codice: int) -> str:
        assegnamento = self._assegnamento_repo.trovaPerId(codice)
        if assegnamento is None:
            return "Errore: assegnamento non trovato"
        self._assegnamento_repo.rimuovi(codice)
        return "Rimozione ok"

    # cponsegna e ritiro
    def consegnaAttrezzatura(self, codiceAssegnamento: int) -> str:
        assegnamento = self._assegnamento_repo.trovaPerId(codiceAssegnamento)
        if assegnamento is None:
            return "Errore: assegnamento non trovato"
        servizio = assegnamento.getServizio()
        if servizio.getStato() != "Disponibile": 
            return "Errore: attrezzatura non disponibile"
        
        # per gli sci, prima della consegna va gestito il valore DIN
        if isinstance(servizio, Sci) and assegnamento.getValoreDIN() is None:
            return "Errore: valore DIN non impostato per gli sci"
        servizio.aggiornaStato("Assegnato") 
        self._servizio_repo.salva()
        return f"Consegna ok: {servizio}"

    def ritiraAttrezzatura(self, codiceAssegnamento: int) -> str:
        assegnamento = self._assegnamento_repo.trovaPerId(codiceAssegnamento)
        if assegnamento is None:
            return "Errore: assegnamento non trovato"
        servizio = assegnamento.getServizio()
        if servizio.getStato() != "Assegnato":
            return "Errore: attrezzatura non in consegna"
        servizio.aggiornaStato("Disponibile") 
        self._servizio_repo.salva()
        return f"Ritiro ok: {servizio}"

    # --- gestione valore DIN con calcolo semplificato
    def calcolaRangeDINConsigliato(self, cliente) -> tuple:
        base = cliente.getPeso() / 10 # regola pratica: peso/10
        livelli = {"principiante": 0.85, "intermedio": 1.0, "avanzato": 1.15}
        fattore = livelli.get(cliente.getLivelloAbilita(), 1.0)
        din = base * fattore
        return (round(din - 0.5, 1), round(din + 0.5, 1))

    # inserisce il valore DIN effettivo scelto dallo ski-man, con associazione
    # IRREVOCABILE dello ski-man responsabile 
    def inserisciValoreDIN(self, codiceAssegnamento: int, valoreDIN: float,
                           skiman_codice: int) -> str:
        assegnamento = self._assegnamento_repo.trovaPerId(codiceAssegnamento)
        if assegnamento is None:
            return "Errore: assegnamento non trovato"
        skiman = self._utilizzatore_repo.trovaPerId(skiman_codice)
        # il responsabile deve essere davvero uno ski-man (non un cliente o admin)
        if skiman is None or not isinstance(skiman, SkiMan):
            return "Errore: ski-man non trovato"
        try:
            assegnamento.registraDIN(valoreDIN, skiman) # associaResponsabilita
        except (TypeError, ValueError) as e:
            return f"Errore: {e}"
        self._assegnamento_repo.salva() 
        return "Registrazione completata"

    def elencaAssegnamenti(self) -> list: # boundary parla con il control
        return self._assegnamento_repo.tutti()

    def elencaRicevute(self) -> list:
        return self._ricevuta_repo.tutti()
