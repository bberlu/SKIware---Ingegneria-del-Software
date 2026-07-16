from Models.servizio import Servizio

class Scarpone(Servizio): # Entity - come da UML eredita direttamente da Servizio
    # e non ha attributi propri 

    # dunder method
    def __str__(self) -> str:
        return "Scarpone: " + super().__str__()
