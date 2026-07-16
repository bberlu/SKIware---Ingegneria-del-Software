from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from Models import Prenotazione

class VistaPrenotazione(QWidget): # Boundary
    # scheda di dettaglio di una singola prenotazione
    def __init__(self, prenotazione: Prenotazione,
                 disdici_callback, elimina_callback):
        super().__init__()
        self._prenotazione = prenotazione
        self.disdici_callback = disdici_callback # disdetta con logica rimborso 48h
        self.elimina_callback = elimina_callback # rimozione 
        self.setWindowTitle(f"Prenotazione {prenotazione.getCodice()}")

        v_layout = QVBoxLayout()
        # informazioni della prenotazione 
        for campo, valore in prenotazione.toDict().items():
            v_layout.addWidget(QLabel(f"{campo}: {valore}"))

        self.bottone_disdici = QPushButton("Disdici prenotazione")
        # lambda: funzione anonima, serve per passare l'argomento alla funzione collegata al click
        self.bottone_disdici.clicked.connect(
            lambda: self.disdici_prenotazione_click(self._prenotazione))
        v_layout.addWidget(self.bottone_disdici)

        self.bottone_elimina = QPushButton("Elimina prenotazione")
        self.bottone_elimina.clicked.connect(
            lambda: self.elimina_prenotazione_click(self._prenotazione))
        v_layout.addWidget(self.bottone_elimina)
        self.setLayout(v_layout)

    def disdici_prenotazione_click(self, prenotazione: Prenotazione) -> None:
        self.disdici_callback(prenotazione)
        self.close()

    def elimina_prenotazione_click(self, prenotazione: Prenotazione) -> None:
        self.elimina_callback(prenotazione)
        self.close()
