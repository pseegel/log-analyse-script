# Log-Analyse

Kleines Python-Tool zur Analyse von Webserver-Logs. 
Liest eine Logdatei im Format `datum zeit methode pfad status dauer_ms` und erstellt einen JSON-Report mit Status-Verteilung, Endpoint-Statistik, stündlichem Aufkommen und den langsamsten Requests.

## Nutzung

```bash
# Nutzt Standardwerte (access.log -> report.json)
python analyse.py

# Eigener Input, Standard-Output (report.json)
python analyse.py webserver.log

# Eigener Input und Output
python analyse.py webserver.log analyse_bericht.json
```

Das Tool erwartet Logdateien im Format `datum zeit methode pfad status dauer_ms`.