import unittest
from Models import Sci, Snowboard, Scarpone, Casco, Armadietto, Servizio, AttrezzaturaPrincipale

class TestServizio(unittest.TestCase):

    def setUp(self): # richiamata a ogni test
        self.sci        = Sci("SCI001", "Sci Rossignol 170cm", 25.0, "intermedio")
        self.snowboard  = Snowboard("SNB001", "Burton 155cm", 28.0, "avanzato")
        self.scarpone   = Scarpone("SCA001", "Scarpone 42", 10.0)
        self.casco      = Casco("CAS001", "Casco M", 5.0)
        self.armadietto = Armadietto("ARM001", "Armadietto PT", 3.0, "grande")

    def test_gerarchia(self): # verifica che la gerarchia rispetta UML
        self.assertIsInstance(self.sci, AttrezzaturaPrincipale)
        self.assertIsInstance(self.snowboard, AttrezzaturaPrincipale)
        self.assertIsInstance(self.scarpone, Servizio)
        self.assertNotIsInstance(self.scarpone, AttrezzaturaPrincipale)
        self.assertIsInstance(self.armadietto, Servizio)

    def test_stato_iniziale(self):
        self.assertEqual(self.sci.getStato(), "Disponibile")

    def test_aggiorna_stato(self):
        self.sci.aggiornaStato("Assegnato")
        self.assertEqual(self.sci.getStato(), "Assegnato")

    def test_aggiorna_stato_tipo_errato(self):
        with self.assertRaises(TypeError):
            self.sci.aggiornaStato(1)

    def test_livello_tecnico(self): # attributo proprio di AttrezzaturaPrincipale
        self.assertEqual(self.sci.getLivelloTecnico(), "intermedio")
        self.sci.setLivelloTecnico("avanzato")
        self.assertEqual(self.sci.getLivelloTecnico(), "avanzato")

    def test_dimensione_armadietto(self): # attributo proprio di Armadietto
        self.assertEqual(self.armadietto.getDimensione(), "grande")

    def test_to_dict(self):
        d = self.sci.toDict()
        self.assertEqual(d["codice"], "SCI001")
        self.assertEqual(d["prezzo"], 25.0)
        self.assertEqual(d["livelloTecnico"], "intermedio")


if __name__ == "__main__":
    unittest.main()
