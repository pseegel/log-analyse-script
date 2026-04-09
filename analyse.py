"""Analysiert eine Webserver-Logdatei und erstellt einen JSON-Report."""

from enum import Enum
from collections import defaultdict
import csv
import json

class Row_Type():
    DATUM = "datum"
    ZEIT = "zeit"
    METHODE = "methode"
    PFAD = "pfad"
    STATUS = "status"
    DAUER_MS = "dauer_ms"



def parse_zeile(zeile):
    result_dict = {}
    strings = zeile.split()
    result_dict[Row_Type.DATUM] = strings[0]
    result_dict[Row_Type.ZEIT] = strings[1]
    result_dict[Row_Type.METHODE] = strings[2]
    result_dict[Row_Type.PFAD] = strings[3]
    result_dict[Row_Type.STATUS] = int(strings[4])
    result_dict[Row_Type.DAUER_MS] = int(strings[5])
    return result_dict


def lade_logs(pfad):
    result_dics = []
    with open(pfad, newline="", encoding="utf-8") as file:
        for row in file:
            result_dics.append(parse_zeile(row))

    return result_dics


def zaehle_status(logs):
    result = defaultdict(int)
    for row in logs:
        result[str(row[Row_Type.STATUS])] += 1
    return dict(result)

def zaehle_endpoints(logs):
    result = defaultdict(int)
    for row in logs:
        result[row[Row_Type.PFAD]] += 1
    return dict(result)

def zaehle_pro_stunde(logs):
    result = defaultdict(int)
    for row in logs:
        result[row[Row_Type.ZEIT][:2]] += 1
    return dict(result)

def top_langsamste(logs, n=10):
    return sorted(logs, key=lambda row: row[Row_Type.DAUER_MS], reverse=True)[:n]

def erstelle_report(logs):
    report = {}
    report["anzahl_requests"] = len(logs)
    report["status_verteilung"] = zaehle_status(logs)
    report["endpoints"] = zaehle_endpoints(logs)
    report["requests_pro_stunde"] = zaehle_pro_stunde(logs)
    report["fehlerquote"] = sum(1 for log in logs if log[Row_Type.STATUS] >= 400) / len(logs)
    report["top_langsamste"] = top_langsamste(logs,5)
    return report

def create_json(name, json_inhalt):
    with open(name, "w", encoding="utf-8") as json_file:
        json.dump(json_inhalt, json_file, indent=2, ensure_ascii=False)

def main():
    logs = lade_logs("access.log")
    report = erstelle_report(logs)
    create_json("report.json", report)
    print(f"Report erstellt: {len(logs)} Einträge analysiert")
    print(f"Fehlerquote: {report['fehlerquote']:.1%}")

if __name__ == "__main__":
    main()