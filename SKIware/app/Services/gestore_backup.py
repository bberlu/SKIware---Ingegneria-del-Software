import json
from datetime import datetime

class GestoreBackup: # Control
    # come da UML (class Gestione) e sd Backup: copia i dati di tutte le
    # entità in un unico backup. "Il backup è effettuato ogni giorno alle 23.30"
    def __init__(self, utilizzatore_repo, servizio_repo, carnet_repo,
                 prenotazione_repo, assegnamento_repo, ricevuta_repo,
                 path: str = "Data/backup.json"):
        self._utilizzatore_repo = utilizzatore_repo
        self._servizio_repo     = servizio_repo
        self._carnet_repo       = carnet_repo
        self._prenotazione_repo = prenotazione_repo
        self._assegnamento_repo = assegnamento_repo
        self._ricevuta_repo     = ricevuta_repo
        self._path   = path
        self._backup: dict = {} 


    # invoca in sequenza i sei metodi di copia e salva su file
    def effettuaBackup(self) -> str:
        self.copiaDatiUtilizzatori()
        self.copiaDatiServizi()
        self.copiaDatiCarnet()
        self.copiaDatiPrenotazioni()
        self.copiaDatiAssegnamenti()
        self.copiaDatiRicevute()
        self._backup["dataOraBackup"] = datetime.now().isoformat()
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._backup, f)
        return f"Backup effettuato: {self._path}"


    def copiaDatiUtilizzatori(self) -> None:
        self._backup["utilizzatori"] = [u.toDict() for u in self._utilizzatore_repo.tutti()]

    def copiaDatiServizi(self) -> None:
        self._backup["servizi"] = [s.toDict() for s in self._servizio_repo.tutti()]

    def copiaDatiCarnet(self) -> None:
        self._backup["carnet"] = [c.toDict() for c in self._carnet_repo.tutti()]

    def copiaDatiPrenotazioni(self) -> None:
        self._backup["prenotazioni"] = [p.toDict() for p in self._prenotazione_repo.tutti()]

    def copiaDatiAssegnamenti(self) -> None:
        self._backup["assegnamenti"] = [a.toDict() for a in self._assegnamento_repo.tutti()]

    def copiaDatiRicevute(self) -> None:
        self._backup["ricevute"] = [r.toDict() for r in self._ricevuta_repo.tutti()]
