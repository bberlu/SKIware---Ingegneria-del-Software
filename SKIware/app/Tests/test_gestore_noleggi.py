import unittest
import os
from datetime import datetime
from Repos import (UtilizzatoreRepository, ServizioRepository,
                   AssegnamentoRepository, RicevutaRepository)
from Services import GestoreUtenti, GestoreAttrezzatura, GestoreNoleggi

class TestGestoreNoleggi(unittest.TestCase):
    # testa i casi d'uso: Inserisci Assegnamento (vincolo stagionale, fascia,
    # vincolo armadietti, emissione ricevuta), Consegna e Ritiro, valore DIN

    def setUp(self): # richiamata a ogni test
        self.file_utilizzatori = "test_utilizzatori.json"
        self.file_servizi      = "test_servizi.json"
        self.file_assegnamenti = "test_assegnamenti.json"
        self.file_ricevute     = "test_ricevute.json"

        self.utilizzatore_repo = UtilizzatoreRepository(self.file_utilizzatori)
        self.servizio_repo     = ServizioRepository(self.file_servizi)
        self.assegnamento_repo = AssegnamentoRepository(self.file_assegnamenti,
                                                        self.servizio_repo,
                                                        self.utilizzatore_repo)
        self.ricevuta_repo     = RicevutaRepository(self.file_ricevute,
                                                    self.assegnamento_repo)
        # isolamento totale dei test
        self.utilizzatore_repo._utilizzatori = {}
        self.servizio_repo._servizi = {}
        self.assegnamento_repo._assegnamenti = {}
        self.ricevuta_repo._ricevute = {}

        self.gestore_attrezzatura = GestoreAttrezzatura(self.servizio_repo,
                                                        self.assegnamento_repo)
        self.gestore = GestoreNoleggi(self.assegnamento_repo, self.servizio_repo,
                                      self.utilizzatore_repo, self.ricevuta_repo,
                                      self.gestore_attrezzatura)
        # dati di base 
        gestore_utenti = GestoreUtenti(self.utilizzatore_repo)
        gestore_utenti.aggiungiCliente(1, "RSSMRA00A01H501X", "Rossi",
                                       "mario@mail.it", "Mario", "Neve2027", 333111,
                                       1.75, 25, "intermedio", 42, 70.5)
        gestore_utenti.aggiungiSkiMan(2, "VRDLGU90B02H501Y", "Verdi",
                                      "luigi@ski.it", "Luigi", "Sciare27", 333222,
                                      datetime(1990, 2, 2), "Trento", "Maestro")
        self.cliente = self.utilizzatore_repo.trovaPerId(1)
        self.gestore_attrezzatura.aggiungiSci("SCI001", "Sci Rossignol 170cm",
                                              25.0, "intermedio")
        self.gestore_attrezzatura.aggiungiArmadietto("ARM001", "Armadietto PT",
                                                     3.0, "grande")
        # date in stagione (gennaio)
        self.inizio = datetime(2027, 1, 10, 9)
        self.fine   = datetime(2027, 1, 10, 13)

    def tearDown(self): # eseguita DOPO ogni test: elimina i file di appoggio
        for file in (self.file_utilizzatori, self.file_servizi,
                     self.file_assegnamenti, self.file_ricevute):
            if os.path.exists(file):
                os.remove(file)

    def test_assegnamento_successo_con_ricevuta(self): # sd InserisciAssegnamento
        risultato = self.gestore.inserisciAssegnamento(1, "SCI001", self.inizio,
                                                       self.fine, "mattina")
        self.assertIn("Assegnamento ok", risultato)
        self.assertEqual(len(self.gestore.elencaAssegnamenti()), 1)
        # EmissioneRicevuta: la ricevuta viene emessa automaticamente
        self.assertEqual(len(self.gestore.elencaRicevute()), 1)
        self.assertEqual(self.gestore.elencaRicevute()[0].getImportoTotale(), 25.0)

    def test_cliente_non_trovato(self): # test di errore possibile
        risultato = self.gestore.inserisciAssegnamento(99, "SCI001", self.inizio,
                                                       self.fine, "mattina")
        self.assertIn("cliente non trovato", risultato)

    def test_vincolo_apertura_stagionale(self): # errore: data fuori stagione
        risultato = self.gestore.inserisciAssegnamento(
            1, "SCI001", datetime(2026, 8, 1, 9), datetime(2026, 8, 1, 13), "mattina")
        self.assertIn("fuori stagione", risultato)

    def test_fascia_oraria_non_valida(self): # errore: indisponibilità temporale
        risultato = self.gestore.inserisciAssegnamento(1, "SCI001", self.inizio,
                                                       self.fine, "notte")
        self.assertIn("indisponibilità temporale", risultato)

    def test_vincolo_armadietto(self): # sd AssegnaArmadietto
        risultato = self.gestore.inserisciAssegnamento(1, "ARM001", self.inizio,
                                                       self.fine, "mattina")
        self.assertIn("senza attrezzatura principale", risultato)
        # dopo il noleggio principale l'armadietto diventa assegnabile
        self.gestore.inserisciAssegnamento(1, "SCI001",
                                           datetime(2026, 12, 20, 9),
                                           datetime(2027, 4, 10, 18), "giornata")
        risultato = self.gestore.inserisciAssegnamento(1, "ARM001", self.inizio,
                                                       self.fine, "mattina")
        self.assertIn("Assegnamento ok", risultato)

    def test_consegna_sci_richiede_din(self): 
        self.gestore.inserisciAssegnamento(1, "SCI001", self.inizio, self.fine,
                                           "mattina")
        risultato = self.gestore.consegnaAttrezzatura(1)
        self.assertIn("DIN", risultato) # senza DIN la consegna è rifiutata
        # lo ski-man imposta il DIN, poi la consegna va a buon fine
        self.gestore.inserisciValoreDIN(1, 7.5, 2)
        risultato = self.gestore.consegnaAttrezzatura(1)
        self.assertIn("Consegna ok", risultato)
        self.assertEqual(self.servizio_repo.trovaPerId("SCI001").getStato(),
                         "Assegnato")

    def test_ritiro(self): 
        self.gestore.inserisciAssegnamento(1, "SCI001", self.inizio, self.fine,
                                           "mattina")
        self.gestore.inserisciValoreDIN(1, 7.5, 2)
        self.gestore.consegnaAttrezzatura(1)
        risultato = self.gestore.ritiraAttrezzatura(1)
        self.assertIn("Ritiro ok", risultato)
        self.assertEqual(self.servizio_repo.trovaPerId("SCI001").getStato(),
                         "Disponibile")

    def test_ritiro_senza_consegna(self): # test di errore possibile
        self.gestore.inserisciAssegnamento(1, "SCI001", self.inizio, self.fine,
                                           "mattina")
        risultato = self.gestore.ritiraAttrezzatura(1)
        self.assertIn("non in consegna", risultato)

    
if __name__ == "__main__":
    unittest.main()
