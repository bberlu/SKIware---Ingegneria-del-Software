import unittest
import os
from datetime import datetime, timedelta
from Repos import (UtilizzatoreRepository, ServizioRepository,
                   CarnetRepository, PrenotazioneRepository)
from Services import GestoreUtenti, GestoreCarnet
from Models import Sci, Prenotazione

class TestGestoreCarnet(unittest.TestCase):
    # testa i casi d'uso: Vendita Carnet, Inserisci Prenotazione (vincolo 24h,
    # decurtazione credito), Disdetta (finestra 48h, rimborso)

    def setUp(self): # richiamata a ogni test
        self.file_utilizzatori = "test_utilizzatori.json"
        self.file_servizi      = "test_servizi.json"
        self.file_carnet       = "test_carnet.json"
        self.file_prenotazioni = "test_prenotazioni.json"

        self.utilizzatore_repo = UtilizzatoreRepository(self.file_utilizzatori)
        self.servizio_repo     = ServizioRepository(self.file_servizi)
        self.carnet_repo       = CarnetRepository(self.file_carnet,
                                                  self.utilizzatore_repo)
        self.prenotazione_repo = PrenotazioneRepository(self.file_prenotazioni,
                                                        self.servizio_repo,
                                                        self.utilizzatore_repo)
        # isolamento totale dei test

        self.utilizzatore_repo._utilizzatori = {}
        self.servizio_repo._servizi = {}
        self.carnet_repo._carnet = {}
        self.prenotazione_repo._prenotazioni = {}

        self.gestore = GestoreCarnet(self.carnet_repo, self.prenotazione_repo,
                                     self.servizio_repo)
        # dati di base 
        gestore_utenti = GestoreUtenti(self.utilizzatore_repo)
        gestore_utenti.aggiungiCliente(1, "RSSMRA00A01H501X", "Rossi",
                                       "mario@mail.it", "Mario", "Neve2027", 333111,
                                       1.75, 25, "intermedio", 42, 70.5)
        self.cliente = self.utilizzatore_repo.trovaPerId(1)
        self.sci = Sci("SCI001", "Sci Rossignol 170cm", 25.0, "intermedio")
        self.servizio_repo.aggiungi(self.sci)
        # data sempre nel futuro (>48h), dentro la stagione 
        self.data_stagionale = datetime(datetime.now().year + 1, 1, 15, 9)

    def tearDown(self): # eseguita DOPO ogni test
        for file in (self.file_utilizzatori, self.file_servizi,
                     self.file_carnet, self.file_prenotazioni):
            if os.path.exists(file):
                os.remove(file)

    def test_vendi_carnet(self): 
        carnet = self.gestore.vendiCarnet(self.cliente, 10)
        self.assertEqual(carnet.getSaldoResiduo(), 10)
        self.assertEqual(carnet.getCliente().getCodice(), 1)
        self.assertEqual(len(self.gestore.elencaCarnet()), 1)

    def test_verifica_carnet_attivo(self):
        self.assertFalse(self.gestore.verificaCarnetAttivo(self.cliente))
        self.gestore.vendiCarnet(self.cliente, 10)
        self.assertTrue(self.gestore.verificaCarnetAttivo(self.cliente))

    def test_vincolo_temporale_24h(self): 
        self.assertTrue(self.gestore.vincoloTemporalePrenotazione(
            datetime.now() + timedelta(hours=30)))
        self.assertFalse(self.gestore.vincoloTemporalePrenotazione(
            datetime.now() + timedelta(hours=2)))

    def test_prenotazione_senza_anticipo_24h(self): # test di errore possibile
        self.gestore.vendiCarnet(self.cliente, 10)
        risultato = self.gestore.inserisciPrenotazione(
            self.cliente, self.sci, datetime.now() + timedelta(hours=2), "mattina")
        self.assertIn("24h", risultato)

    def test_prenotazione_fuori_stagione(self): 
        self.gestore.vendiCarnet(self.cliente, 10)
        risultato = self.gestore.inserisciPrenotazione(
            self.cliente, self.sci,
            datetime(datetime.now().year + 1, 7, 15, 9), "mattina")
        self.assertIn("fuori stagione", risultato)

    def test_prenotazione_senza_carnet(self): # test di errore possibile
        risultato = self.gestore.inserisciPrenotazione(
            self.cliente, self.sci, self.data_stagionale, "mattina")
        self.assertIn("carnet", risultato)

    def test_prenotazione_decurta_credito(self): # sd InserisciPrenotazione
        carnet = self.gestore.vendiCarnet(self.cliente, 10)
        prenotazione = self.gestore.inserisciPrenotazione(
            self.cliente, self.sci, self.data_stagionale, "mattina")
        self.assertEqual(carnet.getSaldoResiduo(), 9) # un ingresso decurtato
        self.assertEqual(len(self.gestore.elencaPrenotazioni()), 1)
        self.assertEqual(prenotazione.getCodice(), 1)

    def test_disdetta_con_rimborso(self): # sd DisdettaPrenotazione 1 caso
        carnet = self.gestore.vendiCarnet(self.cliente, 10)
        prenotazione = self.gestore.inserisciPrenotazione(
            self.cliente, self.sci, self.data_stagionale, "mattina")
        risultato = self.gestore.disdiciPrenotazione(prenotazione.getCodice())
        self.assertIn("con rimborso", risultato)
        self.assertEqual(carnet.getSaldoResiduo(), 10) # ingresso riaccreditato
        self.assertEqual(len(self.gestore.elencaPrenotazioni()), 0)

    def test_disdetta_senza_rimborso(self): # sd DisdettaPrenotazione 2 caso
        carnet = self.gestore.vendiCarnet(self.cliente, 10)
        carnet.aggiornaCredito(-1) # ingresso già decurtato alla prenotazione
        # la prenotazione va creata direttamente nel repository: una data a
        # meno di 48h da oggi non è sempre costruibile dentro la stagione
        prenotazione = Prenotazione(1, datetime.now() + timedelta(hours=30),
                                    "mattina", self.sci, self.cliente)
        self.prenotazione_repo.aggiungi(prenotazione)
        risultato = self.gestore.disdiciPrenotazione(prenotazione.getCodice())
        self.assertIn("senza rimborso", risultato)
        self.assertEqual(carnet.getSaldoResiduo(), 9) # credito perso

    def test_disdetta_prenotazione_inesistente(self):
        risultato = self.gestore.disdiciPrenotazione(999)
        self.assertIn("non trovata", risultato)


if __name__ == "__main__":
    unittest.main()
