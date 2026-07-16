import unittest
from datetime import datetime, timedelta
from Models import Prenotazione, Assegnamento, Ricevuta, Cliente, Sci

class TestPrenotazione(unittest.TestCase):
    # Prenotazione è una classe associazione reificata:
    # per i test servono anche gli oggetti Cliente e Servizio collegati

    def setUp(self): # richiamata a ogni test
        self.cliente = Cliente(1, "RSSMRA00A01H501X", "Rossi", "mario@mail.it",
                               "Mario", "Neve2027", 333111, 1.75, 25, "intermedio",
                               42, 70.5)
        self.sci = Sci("SCI001", "Sci Rossignol 170cm", 25.0, "intermedio")
        self.futura = datetime.now() + timedelta(days=3)
        self.prenotazione = Prenotazione(100, self.futura, "mattina",
                                         self.sci, self.cliente)

    def test_dati(self):
        self.assertEqual(self.prenotazione.getCodice(), 100)
        self.assertEqual(self.prenotazione.getFasciaOraria(), "mattina")
        self.assertEqual(self.prenotazione.getServizio().getCodice(), "SCI001")
        self.assertEqual(self.prenotazione.getCliente().getCodice(), 1)

    def test_verifica_fine(self):
        self.assertFalse(self.prenotazione.verificaFine()) 
        passata = Prenotazione(101, datetime.now() - timedelta(hours=1),
                               "mattina", self.sci, self.cliente)
        self.assertTrue(passata.verificaFine()) # già passata

    def test_to_dict_con_foreign_key(self): # degli oggetti collegati
        # si salva solo il codice 
        d = self.prenotazione.toDict()
        self.assertEqual(d["servizio_codice"], "SCI001")
        self.assertEqual(d["cliente_codice"], 1)
        self.assertNotIn("servizio", d) 


class TestAssegnamento(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(1, "RSSMRA00A01H501X", "Rossi", "mario@mail.it",
                               "Mario", "Neve2027", 333111, 1.75, 25, "intermedio",
                               42, 70.5)
        self.sci = Sci("SCI001", "Sci Rossignol 170cm", 25.0, "intermedio")
        self.inizio = datetime.now() - timedelta(hours=1)
        self.fine   = datetime.now() + timedelta(hours=3)
        self.assegnamento = Assegnamento(200, self.inizio, self.fine,
                                         "mattina", self.sci, self.cliente)

    def test_dati(self):
        self.assertEqual(self.assegnamento.getCodice(), 200)
        self.assertIsNone(self.assegnamento.getValoreDIN()) # non ancora impostato

    def test_valore_din(self):
        self.assegnamento.setValoreDIN(7.5)
        self.assertEqual(self.assegnamento.getValoreDIN(), 7.5)
        with self.assertRaises(TypeError):
            self.assegnamento.setValoreDIN("sette")

    def test_verifica_fine(self):
        self.assertFalse(self.assegnamento.verificaFine()) # ancora in corso
        finito = Assegnamento(201, self.inizio,
                              datetime.now() - timedelta(minutes=1),
                              "mattina", self.sci, self.cliente)
        self.assertTrue(finito.verificaFine())

    def test_to_dict_con_foreign_key(self):
        d = self.assegnamento.toDict()
        self.assertEqual(d["servizio_codice"], "SCI001")
        self.assertEqual(d["cliente_codice"], 1)


class TestRicevuta(unittest.TestCase):

    def setUp(self):
        cliente = Cliente(1, "RSSMRA00A01H501X", "Rossi", "mario@mail.it",
                          "Mario", "Neve2027", 333111, 1.75, 25, "intermedio", 42, 70.5)
        sci = Sci("SCI001", "Sci Rossignol 170cm", 25.0, "intermedio")
        self.assegnamento = Assegnamento(200, datetime(2027, 1, 10, 9),
                                         datetime(2027, 1, 10, 13),
                                         "mattina", sci, cliente)
        self.ricevuta = Ricevuta(300, datetime(2027, 1, 10, 9, 5), 25.0,
                                 self.assegnamento)

    def test_dati(self):
        self.assertEqual(self.ricevuta.getCodice(), 300)
        self.assertEqual(self.ricevuta.getImportoTotale(), 25.0)
        self.assertEqual(self.ricevuta.getAssegnamento().getCodice(), 200)

    def test_anno_ricavato_dalla_data(self): # se non indicato, l'anno
        # viene ricavato dalla data di emissione
        self.assertEqual(self.ricevuta.getAnno(), 2027)

    def test_to_dict_con_foreign_key(self):
        d = self.ricevuta.toDict()
        self.assertEqual(d["assegnamento_codice"], 200)
        self.assertEqual(d["anno"], 2027)


if __name__ == "__main__":
    unittest.main()
