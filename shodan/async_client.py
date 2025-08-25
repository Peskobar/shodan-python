# -*- coding: utf-8 -*-
"""
Klient asynchroniczny API Shodan.
"""

import asyncio
import httpx

from .exception import APIError
from .helpers import create_facet_string

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass


class ShodanAsynchroniczny:
    """Asynchroniczny interfejs do usług Shodan."""

    def __init__(self, klucz, timeout=10):
        self.klucz = klucz
        self.bazowy_adres = 'https://api.shodan.io'
        self._klient = httpx.AsyncClient(base_url=self.bazowy_adres, timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, typ, wartosc, stos):
        await self.zamknij()

    async def zamknij(self):
        await self._klient.aclose()

    async def _zapotrzebowanie(self, sciezka, parametry, metoda='GET'):
        parametry['key'] = self.klucz
        odpowiedz = await self._klient.request(metoda, sciezka, params=parametry)
        if odpowiedz.status_code != 200:
            try:
                blad = odpowiedz.json()['error']
            except Exception:
                blad = odpowiedz.text
            raise APIError(blad)
        return odpowiedz.json()

    async def wyszukaj(self, zapytanie, strona=1, facety=None, minify=True):
        parametry = {'query': zapytanie, 'page': strona}
        if not minify:
            parametry['minify'] = False
        if facety:
            parametry['facets'] = create_facet_string(facety)
        return await self._zapotrzebowanie('/shodan/host/search', parametry)

    async def policz(self, zapytanie, facety=None):
        parametry = {'query': zapytanie}
        if facety:
            parametry['facets'] = create_facet_string(facety)
        return await self._zapotrzebowanie('/shodan/host/count', parametry)
