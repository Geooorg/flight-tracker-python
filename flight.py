# Domain-Objekt eines Flugzeug-Status
class Flight:
    def __init__(self, data):
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
        self.landing = self.velocity < 0 if self.velocity is not None else False
        self.ground = self.velocity = 0
        # self.squawk = data[14]
