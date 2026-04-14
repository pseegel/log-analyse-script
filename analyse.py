"""Analysiert eine Webserver-Logdatei und erstellt einen JSON-Report."""

from collections import defaultdict
from dataclasses import dataclass, asdict
import json
import argparse

DEFAULT_INPUT_PATH = "access.log"
DEFAULT_OUTPUT_PATH = "report.json"
VERSION = "0.2.0"

@dataclass
class LogEntry:
    datum: str
    zeit: str
    methode: str
    pfad: str
    status: int
    dauer_ms: int


def parse_zeile(zeile: str) -> LogEntry:
    teile = zeile.split()
    return LogEntry(
        datum=teile[0],
        zeit=teile[1],
        methode=teile[2],
        pfad=teile[3],
        status=int(teile[4]),
        dauer_ms=int(teile[5]),
    )


def lade_logs(pfad: str) -> list[LogEntry]:
    with open(pfad, encoding="utf-8") as file:
        return [parse_zeile(zeile) for zeile in file]


def zaehle_status(logs: list[LogEntry]) -> dict[int, int]:
    result = defaultdict(int)
    for entry in logs:
        result[entry.status] += 1
    return dict(result)


def zaehle_endpoints(logs: list[LogEntry]) -> dict[str, int]:
    result = defaultdict(int)
    for entry in logs:
        result[entry.pfad] += 1
    return dict(result)


def zaehle_pro_stunde(logs: list[LogEntry]) -> dict[str, int]:
    result = defaultdict(int)
    for entry in logs:
        result[entry.zeit[:2]] += 1
    return dict(result)


def top_langsamste(logs: list[LogEntry], n: int = 10) -> list[LogEntry]:
    return sorted(logs, key=lambda e: e.dauer_ms, reverse=True)[:n]


def erstelle_report(logs: list[LogEntry]) -> dict:
    fehler = sum(1 for entry in logs if entry.status >= 400)
    return {
        "anzahl_requests": len(logs),
        "status_verteilung": zaehle_status(logs),
        "endpoints": zaehle_endpoints(logs),
        "requests_pro_stunde": zaehle_pro_stunde(logs),
        "fehlerquote": fehler / len(logs),
        "top_langsamste": [asdict(entry) for entry in top_langsamste(logs, 5)],
    }


def schreibe_json(pfad: str, inhalt: dict) -> None:
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(inhalt, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Parst Webserver-Logs und erzeugt einen aggregierten JSON-Report "
            "(Status, Endpoints, Latenz)"
        )
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=DEFAULT_INPUT_PATH,
        metavar="PFAD",
        help="Pfad zur einzulesenden Log Datei"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default=DEFAULT_OUTPUT_PATH,
        metavar="PFAD",
        help="Pfad zur ausgegebenen JSON Datei"
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    args = parser.parse_args()
    logs = lade_logs(args.input_file)
    report = erstelle_report(logs)
    schreibe_json(args.output_file, report)
    print(f"Report erstellt: {len(logs)} Einträge analysiert")
    print(f"Fehlerquote: {report['fehlerquote']:.1%}")


if __name__ == "__main__":
    main()