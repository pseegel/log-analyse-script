# Log-Analyse

Kleines Python-Tool zur Analyse von Webserver-Logs.
Liest eine Logdatei im Format `datum zeit methode pfad status dauer_ms` und erstellt einen JSON-Report mit Status-Verteilung, Endpoint-Statistik, stündlichem Aufkommen und den langsamsten Requests.

## Anforderungen
- Python >= 3.12
- Keine externen Abhängigkeiten zur Laufzeit

## Nutzung

```bash
python analyse.py
```

```bash
python analyse.py [path to input log] [path to output log]
```

```bash
python analyse.py -h
```

Erwartet standardmäßig ein `access.log` im selben Verzeichnis. Schreibt standardmäßig ein `report.json`. Input und Output Files können als Parameter übergeben und somit geändert werden.

## Beispiel-Input

[Beispiel](access.log)

## Beispiel-Output

[Beispiel](report.example.json)

## Entwicklung

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1    # Windows PowerShell
source .venv/bin/activate      # Linux / macOS
pip install -r requirements-dev.txt
ruff check .
ruff format .
```
