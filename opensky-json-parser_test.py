import unittest
from io import StringIO
import sys

class TestFlightConversion(unittest.TestCase):
    def setUp(self):
        self.json_file_path = "./test_resources/found-flights.json"
        # Speichere den aktuellen Wert von sys.stdin
        self.saved_stdin = sys.stdin

    def tearDown(self):
        # Stelle sys.stdin auf den ursprünglichen Wert zurück
        sys.stdin = self.saved_stdin

    def test_flight_conversion(self):
        # Öffne die JSON-Testdatei und lese den Inhalt
        with open(self.json_file_path, "r") as json_file:
            json_data = json_file.read()

        # Simuliere die Standardeingabe mit StringIO
        sys.stdin = StringIO(json_data)

        # Importiere das Skript, das die Flugkonvertierung durchführt (angenommen, es heißt main.py)
        import __main__

        # Fange die Ausgabe des Skripts ab, um sicherzustellen, dass es keine Fehler gibt
        with StringIO() as output:
            sys.stdout = output
            try:
                __main__.main()  # Rufe die Hauptfunktion deines Skripts auf
            except SystemExit:
                pass
            sys.stdout = sys.__stdout__

        # Prüfe, ob die Ausgabe des Skripts den erwarteten JSON-String enthält
        expected_json = json_data.strip()
        self.assertEqual(expected_json, output.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
