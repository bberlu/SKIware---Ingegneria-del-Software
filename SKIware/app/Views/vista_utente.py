from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from Models import Utilizzatore

class VistaUtente(QWidget): # Boundary
    # scheda di dettaglio di un utilizzatore, qualunque sia il suo tipo
    def __init__(self, utilizzatore: Utilizzatore, elimina_callback):
        super().__init__()
        self._utilizzatore = utilizzatore
        self.elimina_callback = elimina_callback
        self.setWindowTitle(f"Utente {utilizzatore.getCodice()}")

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel(f"tipo: {type(utilizzatore).__name__}"))
        # informazioni dell'utilizzatore 
        # la password non va mai mostrata in chiaro
        for campo, valore in utilizzatore.toDict().items():
            if campo == "password":
                valore = "*" * 8
            v_layout.addWidget(QLabel(f"{campo}: {valore}"))

        self.bottone_elimina = QPushButton("Elimina utente")
        # lambda: funzione anonima, serve per passare l'argomento alla funzione collegata al click
        self.bottone_elimina.clicked.connect(
            lambda: self.elimina_utente_click(self._utilizzatore))
        v_layout.addWidget(self.bottone_elimina)
        self.setLayout(v_layout)

    def elimina_utente_click(self, utilizzatore: Utilizzatore) -> None:
        self.elimina_callback(utilizzatore)
        self.close()
