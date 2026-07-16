import unittest
from datetime import datetime
from Models import Carnet, Cliente

class TestCarnet(unittest.TestCase):

    def setUp(self): # richiamata a ogni test
        self.carnet = Carnet(10, datetime(2026, 12, 1), 5, False)
        self.cliente = Cliente(1, "RSSMRA00A01H501X", "Rossi", "mario@mail.it",
                               "Mario", "Neve2027", 333111, 1.75, 25, "intermedio",
                               42, 70.5)

    def test_dati(self):
        self.assertEqual(self.carnet.getCodice(), 10)
        self.assertEqual(self.carnet.getSaldoResiduo(), 5)
        self.assertFalse(self.carnet.isStagionale())

    def test_aggiorna_credito_decurtazione(self):
        self.carnet.aggiornaCredito(-1)
        self.assertEqual(self.carnet.getSaldoResiduo(), 4)

    def test_aggiorna_credito_ricarica(self):
        self.carnet.aggiornaCredito(10)
        self.assertEqual(self.carnet.getSaldoResiduo(), 15)

    def test_saldo_non_negativo(self): # il saldo non può mai andare sotto zero
        with self.assertRaises(ValueError):
            self.carnet.aggiornaCredito(-6)

    def test_aggiorna_credito_tipo_errato(self):
        with self.assertRaises(TypeError):
            self.carnet.aggiornaCredito("uno")

    def test_verifica_saldo_sufficiente(self):
        self.assertTrue(self.carnet.verificaSaldoSufficiente())
        self.carnet.aggiornaCredito(-5) # saldo a zero
        self.assertFalse(self.carnet.verificaSaldoSufficiente())

    def test_associa_cliente(self): # associazione Cliente-Carnet
        self.assertIsNone(self.carnet.getCliente())
        self.carnet.associaCliente(self.cliente)
        self.assertEqual(self.carnet.getCliente().getCodice(), 1)
        
        self.assertEqual(self.carnet.toDict()["cliente_codice"], 1)

    def test_from_dict(self): 
        c2 = Carnet.fromDict(self.carnet.toDict())
        self.assertEqual(c2.getCodice(), 10)
        self.assertEqual(c2.getSaldoResiduo(), 5)
        self.assertEqual(c2.getDataRilascio(), datetime(2026, 12, 1))


if __name__ == "__main__":
    unittest.main()
