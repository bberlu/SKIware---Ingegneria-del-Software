import unittest
import os
from Repos import UtilizzatoreRepository
from Services import GestoreUtenti

class TestGestoreUtenti(unittest.TestCase):
    # il test del controller dipende anche da entity e repository

    def setUp(self): # richiamata a ogni test
        self.file_utilizzatori = "test_utilizzatori.json"
        self.utilizzatore_repo = UtilizzatoreRepository(self.file_utilizzatori)
        self.utilizzatore_repo._utilizzatori = {} # isolamento totale dei test
        self.gestore = GestoreUtenti(self.utilizzatore_repo)
        # dati di base 
        self.gestore.aggiungiCliente(1, "RSSMRA00A01H501X", "Rossi",
                                     "mario@mail.it", "Mario", "Neve2027", 333111,
                                     1.75, 25, "intermedio", 42, 70.5)

    def tearDown(self): # eseguita DOPO ogni test: elimina i file di appoggio
        if os.path.exists(self.file_utilizzatori):
            os.remove(self.file_utilizzatori)

    def test_aggiungi_cliente_successo(self):
        risultato = self.gestore.aggiungiCliente(2, "BNCLRA95D45H501K", "Bianchi",
                                                 "laura@mail.it", "Laura", "Lago2027",
                                                 333222, 1.65, 30, "base", 38, 55.0)
        self.assertIn("Inserimento ok", risultato)
        self.assertEqual(len(self.gestore.elencaClienti()), 2)

    def test_aggiungi_cliente_duplicato(self): # test di errore possibile
        risultato = self.gestore.aggiungiCliente(1, "ALTROCF", "X", "y", "Z",
                                                 "pw", 2, 1.7, 20, "base", 40, 60.0)
        self.assertEqual(risultato, "Il cliente esiste già")
        self.assertEqual(len(self.gestore.elencaClienti()), 1)

    def test_modifica_cliente(self):
        risultato = self.gestore.modificaCliente(1, {"peso": 72.0,
                                                     "livelloAbilita": "avanzato"})
        self.assertIn("Modifica ok", risultato)
        cliente = self.gestore.ricercaUtilizzatoreCodice(1)
        self.assertEqual(cliente.getPeso(), 72.0)
        self.assertEqual(cliente.getLivelloAbilita(), "avanzato")


    def test_rimuovi_cliente(self):
        risultato = self.gestore.rimuoviCliente(1)
        self.assertEqual(risultato, "Rimozione ok")
        self.assertIsNone(self.gestore.ricercaUtilizzatoreCodice(1))

    def test_cud_skiman(self): # caso d'uso CUD Ski-man
        from datetime import datetime
        risultato = self.gestore.aggiungiSkiMan(2, "VRDLGU90B02H501Y", "Verdi",
                                                "luigi@ski.it", "Luigi", "Sciare27",
                                                333222, datetime(1990, 2, 2),
                                                "Trento", "Maestro")
        self.assertIn("Inserimento ok", risultato)
        risultato = self.gestore.rimuoviSkiMan(2)
        self.assertEqual(risultato, "Rimozione ok")
        self.assertIsNone(self.gestore.ricercaUtilizzatoreCodice(2))

    def test_cud_amministratore(self): # caso d'uso CUD Amministratore
        risultato = self.gestore.aggiungiAmministratore(3, "BNCGNN80C03H501Z",
                                                        "Bianchi", "admin@ski.it",
                                                        "Gianni", "Admin2027", 333333)
        self.assertIn("Inserimento ok", risultato)
        risultato = self.gestore.rimuoviAmministratore(3)
        self.assertEqual(risultato, "Rimozione ok")


    def test_autenticazione(self): # accesso con codice e pw
        from Models import Amministratore
        self.gestore.aggiungiAmministratore(3, "BNCGNN80C03H501Z", "Bianchi",
                                            "admin@ski.it", "Gianni",
                                            "Admin2027", 333333)
        utente = self.gestore.autentica(3, "Admin2027")
        self.assertIsInstance(utente, Amministratore) # il tipo è il ruolo
        self.assertTrue(utente.puoAccedere())
       
        self.assertIsNone(self.gestore.autentica(3, "sbagliata"))
        self.assertIsNone(self.gestore.autentica(99, "Admin2027"))

    def test_cliente_non_accede(self): #clienti non hanno accesso
        cliente = self.gestore.autentica(1, "Neve2027") # credenziali giuste
        self.assertIsNotNone(cliente)
        self.assertFalse(cliente.puoAccedere()) 

    def test_validazione_entro_3_secondi(self):
        import time
        inizio = time.time()
        self.gestore.autentica(1, "Neve2027")
        durata = time.time() - inizio
        self.assertLess(durata, 3.0)


if __name__ == "__main__":
    unittest.main()
