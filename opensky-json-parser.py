import json
import sys
from openskyflight import OpenskyFlight

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
flights = [OpenskyFlight(flight) for flight in flight_data]

# JSON ausgeben
result = json.dumps([vars(flight) for flight in flights], indent=1).replace("\n","").replace("\r","").replace("  ", "")
print(result)