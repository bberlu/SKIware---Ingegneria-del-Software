from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from Models import Carnet

class VistaCarnet(QWidget): # Boundary
    # scheda di dettaglio di un singolo carnet
    def __init__(self, carnet: Carnet, elimina_callback):
        super().__init__()
        self._carnet = carnet
        self.elimina_callback = elimina_callback
        self.setWindowTitle(f"Carnet {carnet.getCodice()}")

        v_layout = QVBoxLayout()
        # informazioni del carnet 
        for campo, valore in carnet.toDict().items():
            v_layout.addWidget(QLabel(f"{campo}: {valore}"))
        # informazioni del cliente intestatario
        cliente = self.get_cliente(carnet)
        if cliente:
            v_layout.addWidget(QLabel(
                f"intestatario: {cliente['nome']} {cliente['cognome']}"))

        self.bottone_elimina = QPushButton("Elimina carnet")
        # lambda: funzione anonima, serve per passare l'argomento alla funzione collegata al click
        self.bottone_elimina.clicked.connect(
            lambda: self.elimina_carnet_click(self._carnet))
        v_layout.addWidget(self.bottone_elimina)
        self.setLayout(v_layout)

    # restituisce i dati del cliente intestatario del carnet
    def get_cliente(self, carnet: Carnet) -> dict:
        cliente = carnet.getCliente()
        return cliente.toDict() if cliente is not None else {}


    def elimina_carnet_click(self, carnet: Carnet) -> None:
        self.elimina_callback(carnet)
        self.close()
