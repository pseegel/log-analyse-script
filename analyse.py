"""Analysiert eine Webserver-Logdatei und erstellt einen JSON-Report."""

from collections import defaultdict
from dataclasses import dataclass, asdict
import argparse
import json
import sys

DEFAULT_INPUT_PATH = "access.log"
DEFAULT_OUTPUT_PATH = "report.json"
VERSION = "0.4.0"


@dataclass
class LogEntry:
    """Stellt eine Zeile des übergebenen Logs dar."""

    datum: str
    zeit: str
    methode: str
    pfad: str
    status: int
    dauer_ms: int


def parse_zeile(zeile: str) -> LogEntry:
    """Parst eine übergebene Zeile als LogEntry Dataclass."""
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
    """Liest eine Log Datei ein und Parst sie zu einer Liste von LogEntry Dataclasses.

    Args:
        pfad: Pfad zur Eingabedatei.

    Returns:
        Liste der gefundenen Einträge.

    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert.
    """
    with open(pfad, encoding="utf-8") as file:
        return [parse_zeile(zeile) for zeile in file]


def zaehle_status(logs: list[LogEntry]) -> dict[int, int]:
    """Zählt Requests pro HTTP-Status.

    Returns:
        Dict aus Status und gefundener Anzahl.

    """
    result = defaultdict(int)
    for entry in logs:
        result[entry.status] += 1
    return dict(result)


def zaehle_endpoints(logs: list[LogEntry]) -> dict[str, int]:
    """Zählt Requests pro Endpoint.

    Returns:
        Dict aus Endpunkt und gefundener Anzahl.
    """
    result = defaultdict(int)
    for entry in logs:
        result[entry.pfad] += 1
    return dict(result)


def zaehle_pro_stunde(logs: list[LogEntry]) -> dict[str, int]:
    """Zählt Requests pro Stunde.

    Returns:
        Dict aus Stunde und gefundener Anzahl.
    """
    result = defaultdict(int)
    for entry in logs:
        result[entry.zeit[:2]] += 1
    return dict(result)


def top_langsamste(logs: list[LogEntry], n: int = 10) -> list[LogEntry]:
    """Listet eine n Anzahl an top langsamsten Einträgen in einer LogEntry Liste.

    Args:
        logs: LogEntry Liste
        n: Maximale Anzahl Ergebnisse.

    Returns:
        Liste der n langsamsten Einträge.
    """
    return sorted(logs, key=lambda e: e.dauer_ms, reverse=True)[:n]


def erstelle_report(logs: list[LogEntry]) -> dict:
    """Erstellt einen Report für eine Liste von LogEntry dataclasses.

    Returns:
        Dict mit Schlüsseln anzahl_requests, status_verteilung, endpoints, requests_pro_stunde, fehlerquote, top_langsamste.
    """
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
    """Schreibt ein Dict als JSON-Datei."""
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
        help="Pfad zur einzulesenden Log Datei",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default=DEFAULT_OUTPUT_PATH,
        metavar="PFAD",
        help="Pfad zur ausgegebenen JSON Datei",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    args = parser.parse_args()
    try:
        logs = lade_logs(args.input_file)
    except FileNotFoundError:
        print(
            f"Fehler: Datei '{args.input_file}' nicht gefunden",
            file=sys.stderr,
        )
        sys.exit(1)

    if not logs:
        print(
            f"Warnung: Keine Log-Einträge in '{args.input_file}' gefunden",
            file=sys.stderr,
        )
        sys.exit(1)

    report = erstelle_report(logs)
    schreibe_json(args.output_file, report)
    print(f"Report erstellt: {len(logs)} Einträge analysiert")
    print(f"Fehlerquote: {report['fehlerquote']:.1%}")


if __name__ == "__main__":
    main()
