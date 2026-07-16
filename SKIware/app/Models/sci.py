from Models.attrezzatura_principale import AttrezzaturaPrincipale

class Sci(AttrezzaturaPrincipale): # Entity - come da UML non ha attributi propri:
    # eredita tutto da AttrezzaturaPrincipale 

    # dunder method
    def __str__(self) -> str:
        return "Sci: " + super().__str__()
