#!/usr/bin/env python3
"""Skrypt tworzy webhooki GitGuardian i TruffleHog dla repozytorium oraz wszystkich jego forków.
Wymagane zmienne środowiskowe: GITHUB_TOKEN, REPO, GITGUARDIAN_URL, TRUFFLEHOG_URL."""
import os
import requests

TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]  # format właściciel/nazwa
GITGUARDIAN_URL = os.environ["GITGUARDIAN_URL"]
TRUFFLEHOG_URL = os.environ["TRUFFLEHOG_URL"]

SESJA = requests.Session()
SESJA.headers["Authorization"] = f"token {TOKEN}"
SESJA.headers["Accept"] = "application/vnd.github+json"


def stworz_webhook(repozytorium: str, adres: str) -> None:
    """Tworzy webhook o podanym adresie dla wskazanego repozytorium."""
    dane = {
        "name": "web",
        "active": True,
        "events": ["push"],
        "config": {
            "url": adres,
            "content_type": "json",
            "insecure_ssl": "0"
        }
    }
    odpowiedz = SESJA.post(f"https://api.github.com/repos/{repozytorium}/hooks", json=dane, timeout=30)
    odpowiedz.raise_for_status()


def skonfiguruj_repo(repozytorium: str) -> None:
    """Dodaje webhooki GitGuardian i TruffleHog do repozytorium."""
    stworz_webhook(repozytorium, GITGUARDIAN_URL)
    stworz_webhook(repozytorium, TRUFFLEHOG_URL)


def skonfiguruj_forki(repozytorium: str) -> None:
    """Dodaje webhooki do wszystkich forków repozytorium."""
    odpowiedz = SESJA.get(f"https://api.github.com/repos/{repozytorium}/forks", timeout=30)
    odpowiedz.raise_for_status()
    for fork in odpowiedz.json():
        skonfiguruj_repo(fork["full_name"])


if __name__ == "__main__":
    skonfiguruj_repo(REPO)
    skonfiguruj_forki(REPO)
