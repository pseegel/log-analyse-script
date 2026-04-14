# Log-Analyse

Kleines Python-Tool zur Analyse von Webserver-Logs.
Liest eine Logdatei im Format `datum zeit methode pfad status dauer_ms` und erstellt einen JSON-Report mit Status-Verteilung, Endpoint-Statistik, stündlichem Aufkommen und den langsamsten Requests.

## Nutzung

    python analyse.py

Erwartet `access.log` im selben Verzeichnis. Schreibt `report.json`.

## Entwicklung

    python -m venv .venv
    .venv\Scripts\Activate.ps1    # Windows PowerShell
    pip install -r requirements-dev.txt
    ruff check .
    ruff format .
