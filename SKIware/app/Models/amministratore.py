from Models.utilizzatore import Utilizzatore

class Amministratore(Utilizzatore): # Entity - come da UML non ha attributi propri:
    # eredita tutto da Utilizzatore

    # dunder method
    def __str__(self) -> str:
        return "Amministratore: " + super().__str__()
