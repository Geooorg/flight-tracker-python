import time

from openskyflight import OpenskyFlight


class FilteredFlight(OpenskyFlight):
    def __init__(self, data):
        # Rufe den Konstruktor der Basisklasse auf, um die vorhandenen Felder zu initialisieren
        super().__init__(data)

        self.airport = ""
        self.updated_at = round(time.time())
