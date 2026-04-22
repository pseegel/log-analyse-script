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

## Beispiel-Output

[Beispiel](report.example.json)

## Deployment

Zunächst muss das Docker image gebaut werden
```bash
docker build -t log-analyse-script .
```

Anschließend kann auf dem Image das python script ausgeführt werden. Dafür muss der "host_path" zur log datei angegeben werden. Die Datei wird anschließend im Docker unter data gespeichert. Zudem wird der "log_file_name" zum zu parsenden log file und ein "report_file_name", wie der fertige report heißen soll, benötigt
```bash
docker run -v [host_path]:/data log-analyse-script /data/[log_file_name].log /data/[report_file_name].json
```

## Entwicklung

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1    # Windows PowerShell
source .venv/bin/activate      # Linux / macOS
pip install -r requirements-dev.txt
ruff check .
ruff format .
```
