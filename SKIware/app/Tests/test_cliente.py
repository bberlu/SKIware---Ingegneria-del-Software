import unittest
from Models import Cliente

class TestCliente(unittest.TestCase):

    def setUp(self): # richiamata a ogni test
        self.cliente = Cliente(1, "RSSMRA00A01H501X", "Rossi", "mario@mail.it",
                               "Mario", "Neve2027", 333111, 1.75, 25, "intermedio",
                               42, 70.5)

    def test_codice(self):
        self.assertEqual(self.cliente.getCodice(), 1)

    def test_dati_anagrafici(self):
        self.assertEqual(self.cliente.getNome(), "Mario")
        self.assertEqual(self.cliente.getCognome(), "Rossi")
        self.assertEqual(self.cliente.getCodiceFiscale(), "RSSMRA00A01H501X")

    def test_dati_fisici(self):
        self.assertEqual(self.cliente.getAltezza(), 1.75)
        self.assertEqual(self.cliente.getEta(), 25)
        self.assertEqual(self.cliente.getLivelloAbilita(), "intermedio")
        self.assertEqual(self.cliente.getMisuraScarponi(), 42)
        self.assertEqual(self.cliente.getPeso(), 70.5)

    def test_to_dict(self):
        d = self.cliente.toDict()
        self.assertEqual(d["codice"], 1)
        self.assertEqual(d["nome"], "Mario")
        self.assertEqual(d["livelloAbilita"], "intermedio")
        self.assertEqual(d["peso"], 70.5)

    def test_from_dict(self):
        d = self.cliente.toDict()
        c2 = Cliente.fromDict(d)
        self.assertEqual(c2.getCodice(), self.cliente.getCodice())
        self.assertEqual(c2.getCognome(), self.cliente.getCognome())
        self.assertEqual(c2.getMisuraScarponi(), self.cliente.getMisuraScarponi())

    def test_setter_validi(self):
        self.cliente.setPeso(72)
        self.assertEqual(self.cliente.getPeso(), 72.0)
        self.cliente.setLivelloAbilita("avanzato")
        self.assertEqual(self.cliente.getLivelloAbilita(), "avanzato")

    def test_password_alfanumerica(self): # password str con caratteri misti
        self.assertEqual(self.cliente.getPassword(), "Neve2027")
        self.cliente.setPassword("NuovaPass99")
        self.assertEqual(self.cliente.getPassword(), "NuovaPass99")
        with self.assertRaises(TypeError):
            self.cliente.setPassword(1234) # int non ammesso

    def test_password_non_conforme(self): #almeno 7 caratteri alfanumerici
        with self.assertRaises(ValueError):
            self.cliente.setPassword("Abc12") # troppo corta
        with self.assertRaises(ValueError):
            self.cliente.setPassword("Neve2027!") # '!' non è alfanumerico
        with self.assertRaises(ValueError): # vale anche alla creazione
            Cliente(2, "CF", "X", "y", "Z", "corta1", 2, 1.7, 20, "base", 40, 60.0)

    def test_setter_tipo_errato(self): # i setter devono rifiutare i tipi sbagliati
        with self.assertRaises(TypeError):
            self.cliente.setEta("venticinque")
        with self.assertRaises(TypeError):
            self.cliente.setMisuraScarponi(42.5)
        with self.assertRaises(TypeError):
            self.cliente.setLivelloAbilita(3)


if __name__ == "__main__":
    unittest.main()
