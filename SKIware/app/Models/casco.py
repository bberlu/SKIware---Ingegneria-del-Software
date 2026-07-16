from Models.servizio import Servizio

class Casco(Servizio): # Entity - come da UML eredita direttamente da Servizio
    # e non ha attributi propri (codice, descrizione, prezzo, stato).

    # dunder method
    def __str__(self) -> str:
        return "Casco: " + super().__str__()
