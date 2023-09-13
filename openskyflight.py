# Domain-Objekt eines Flugzeug-Status
import time


class OpenskyFlight:
    def __init__(self, data):
        # custom meta data
        self.created_at = round(time.time())

        # data[i] are derived from the OpenFlight API
        self.icao = data[0]
        self.callsign = data[1]
        self.country = data[2]
        self.timestamp_start = data[3]
        self.timestamp_end = data[4]

        self.longitude = data[5]
        self.latitude = data[6]

        if data[7] is None:
            self.altitude = 0
        else:
            self.altitude = data[7]

        self.degree = data[10]

        self.velocity = data[9] if data[9] is not None else 0
        self.velocity_kmh = (self.velocity * 3.6) if self.velocity is not None else 0

        # data[11] is vertical rate
        if data[11] is not None and data[11] < 0:
            self.landing = True
        else:
            self.landing = False