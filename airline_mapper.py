class AirlineMapper:
    def __init__(self):
        self.airline_mapping = {
            "AAB": "LuxAviation Belgium",
            "AEE": "Aegean Airlines",
            "AFR": "Air France",
            "AIB": "Airbus Hamburg",
            "AUA": "Austrian Airlines",
            "AWU": "Sylt Air",
            "BAW": "British Airways",
            "BGA": "Airbus Hamburg",
            "BPO": "Bundespolizei",
            "CFG": "Condor",
            "DLH": "Deutsche Lufthansa",
            "EIN": "Aer Lingus",
            "EWG": "GermanWings",
            "EZY": "EasyJet",
            "FHB": "Freebird Airlines",
            "FIN": "FinnAir",
            "IBE": "Iberia",
            "ICE": "Iceland Air",
            "IJM": "International Flight Management",
            "ITY": "Italia",
            "JK": "JetKontor",
            "KLM": "Royal Dutch Airlines",
            "LGL": "LuxAir",
            "LOT": "LOT Poland",
            "MTO": "Marathon Airlines",
            "MBU": "Marabu",
            "MSC": "Air Cairo",
            "NJ": "NetJet",
            "NO": "Norwegian",
            "PGT": "Pegasus",
            "RYR": "RyanAir",
            "SAS": "Nordic Airlines",
            "SQP": "SkyUp Airlines",
            "SWR": "Helvetic Airlines",
            "SXS": "SunExpress",
            "TAP": "TAP Portugal",
            "THY": "Turkish Airlines",
            "UAE": "Emirates",
            "VKA": "Intercom",
            "VLG": "Vueling",
            "WZZ": "WizzAir",
        }

    def get_airline_name(self, flight_number):
        # Wenn kein direkter Treffer gefunden wurde, versuche die ersten drei Buchstaben
        airline_code = flight_number[:3]

        if airline_code in self.airline_mapping:
            return self.airline_mapping[airline_code]

        # Ansonsten verwende die ersten zwei Buchstaben der Flugnummer
        airline_code = flight_number[:2]

        if airline_code in self.airline_mapping:
            return self.airline_mapping[airline_code]

        # else
        return "Unknown"
