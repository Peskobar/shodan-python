import requests
import json

from .exception import APIError


class Threatnet:
    """Owijka wokół interfejsów REST i strumieniowego Threatnet

    :param key: Klucz API Shodana dostępny na stronie konta (https://account.shodan.io)
    :type key: str
    :ivar stream: Instancja `shodan.Threatnet.Stream` zapewniająca dostęp do API strumieniowego.
    """

    class Stream:

        base_url = 'https://stream.shodan.io'

        def __init__(self, parent, proxies=None):
            self.parent = parent
            self.proxies = proxies

        def _create_stream(self, name):
            try:
                odpowiedz = requests.get(
                    self.base_url + name,
                    params={'key': self.parent.api_key},
                    stream=True,
                    proxies=self.proxies,
                    timeout=30,
                )
                odpowiedz.raise_for_status()
            except requests.exceptions.Timeout as exc:
                raise APIError(
                    f'Przekroczono limit czasu podczas łączenia ze strumieniem Threatnet: {exc}'
                )
            except requests.exceptions.RequestException as exc:
                raise APIError(
                    f'Błąd połączenia ze strumieniem Threatnet: {exc}'
                )
            return odpowiedz

        def events(self):
            stream = self._create_stream('/threatnet/events')
            for line in stream.iter_lines():
                if line:
                    banner = json.loads(line)
                    yield banner

        def backscatter(self):
            stream = self._create_stream('/threatnet/backscatter')
            for line in stream.iter_lines():
                if line:
                    banner = json.loads(line)
                    yield banner

        def activity(self):
            stream = self._create_stream('/threatnet/ssh')
            for line in stream.iter_lines():
                if line:
                    banner = json.loads(line)
                    yield banner

    def __init__(self, key):
        """Inicjalizuje obiekt API.

        :param key: Klucz API Shodana.
        :type key: str
        """
        self.api_key = key
        self.base_url = 'https://api.shodan.io'
        self.stream = self.Stream(self)
