import unittest
from datetime import datetime
from Models import SkiMan, Amministratore

class TestSkiMan(unittest.TestCase):

    def setUp(self): # richiamata a ogni test
        self.skiman = SkiMan(2, "VRDLGU90B02H501Y", "Verdi", "luigi@ski.it",
                             "Luigi", "Sciare27", 333222, datetime(1990, 2, 2),
                             "Trento", "Maestro di sci")

    def test_dati_ereditati(self): # attributi ereditati da Utilizzatore
        self.assertEqual(self.skiman.getCodice(), 2)
        self.assertEqual(self.skiman.getNome(), "Luigi")
        self.assertEqual(self.skiman.getCognome(), "Verdi")

    def test_dati_propri(self):
        self.assertEqual(self.skiman.getDataNascita(), datetime(1990, 2, 2))
        self.assertEqual(self.skiman.getLuogoNascita(), "Trento")
        self.assertEqual(self.skiman.getQualificaTecnica(), "Maestro di sci")

    def test_to_dict(self):
        d = self.skiman.toDict()
        self.assertEqual(d["codice"], 2)
        self.assertEqual(d["qualificaTecnica"], "Maestro di sci")
        # datetime serializzato come stringa isoformat (per il json)
        self.assertEqual(d["dataNascita"], "1990-02-02T00:00:00")

    def test_from_dict(self): # round-trip di persistenza
        s2 = SkiMan.fromDict(self.skiman.toDict())
        self.assertEqual(s2.getCodice(), self.skiman.getCodice())
        self.assertEqual(s2.getDataNascita(), self.skiman.getDataNascita())

    def test_setter_tipo_errato(self):
        with self.assertRaises(TypeError):
            self.skiman.setQualificaTecnica(5)


class TestAmministratore(unittest.TestCase):

    def setUp(self):
        self.admin = Amministratore(3, "BNCGNN80C03H501Z", "Bianchi",
                                    "admin@ski.it", "Gianni", "Admin2027", 333333)

    def test_dati(self):
        self.assertEqual(self.admin.getCodice(), 3)
        self.assertEqual(self.admin.getNome(), "Gianni")

    def test_from_dict(self): # eredita toDict/fromDict da Utilizzatore
        a2 = Amministratore.fromDict(self.admin.toDict())
        self.assertIsInstance(a2, Amministratore)
        self.assertEqual(a2.getCodiceFiscale(), "BNCGNN80C03H501Z")


if __name__ == "__main__":
    unittest.main()
