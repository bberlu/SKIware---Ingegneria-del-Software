from Models.attrezzatura_principale import AttrezzaturaPrincipale

class Snowboard(AttrezzaturaPrincipale): # Entity 
    # eredita tutto da AttrezzaturaPrincipale

    # dunder method
    def __str__(self) -> str:
        return "Snowboard: " + super().__str__()
