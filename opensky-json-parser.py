import json
import sys
from flight import Flight

# JSON-Daten von der Standardeingabe mit UTF-8-Codierung lesen
json_data = sys.stdin.read()

# Entferne Zeilenumbrüche aus den JSON-Daten
json_data = ''.join(json_data.splitlines())

# JSON-Daten in ein Python-Dictionary umwandeln
data = json.loads(json_data)

# Die Liste der Flüge aus den JSON-Daten extrahieren
flight_data = data["states"]
#
# # Eine Liste von Flight-Objekten erstellen
flights = [Flight(flight) for flight in flight_data]
#
# # Beispiel: Alle Flüge ausgeben
for flight in flights:
    print(f"Flug ID: {flight.icao}, Callsign: {flight.callsign}, Höhe: {flight.altitude}, Geschwindigkeit: {flight.velocity_kmh}, Start/Landung? {flight.landing}")
