from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from Models import Servizio

class VistaAttrezzatura(QWidget): # Boundary
    # scheda di dettaglio di un singolo servizio/attrezzatura
    def __init__(self, servizio: Servizio, elimina_callback):
        super().__init__()
        self._servizio = servizio
        self.elimina_callback = elimina_callback
        self.setWindowTitle(f"Servizio {servizio.getCodice()}")

        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel(f"tipo: {type(servizio).__name__}"))
        # mostro tutte le informazioni del servizio 
        for campo, valore in servizio.toDict().items():
            v_layout.addWidget(QLabel(f"{campo}: {valore}"))

        self.bottone_elimina = QPushButton("Elimina attrezzatura")
        # lambda: funzione anonima, serve per passare l'argomento alla funzione collegata al click
        self.bottone_elimina.clicked.connect(
            lambda: self.elimina_attrezzatura_click(self._servizio))
        v_layout.addWidget(self.bottone_elimina)
        self.setLayout(v_layout)

    def elimina_attrezzatura_click(self, servizio: Servizio) -> None:
        self.elimina_callback(servizio)
        self.close()
