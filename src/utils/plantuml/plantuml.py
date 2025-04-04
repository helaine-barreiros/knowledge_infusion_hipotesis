import requests
import zlib


class PlantUML:
    def __init__(self, url="http://www.plantuml.com/plantuml/png/"):
        self.url = url

    def _encode(self, text):
        """
        Encodes PlantUML text into a format suitable for the PlantUML server.
        """
        compressed = zlib.compress(text.encode('utf-8'))
        return ''.join([chr((b >> 4) + 33) + chr((b & 0xF) + 33) for b in compressed])

    def processes(self, text):
        """
        Processes PlantUML text and returns the diagram as bytes.
        """
        if not text:
            return None

        encoded = self._encode(text)
        response = requests.get(f"{self.url}{encoded}")
        
        if response.status_code != 200:
            return None
            
        return response.content 