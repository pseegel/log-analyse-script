import pytest

from analyse import parse_zeile, LogEntry, zaehle_status


def test_parse_zeile_gueltige_zeile():
    zeile = "2024-01-15 08:23:45 GET /api/users 200 150"

    ergebnis = parse_zeile(zeile)

    assert ergebnis == LogEntry(
        datum="2024-01-15",
        zeit="08:23:45",
        methode="GET",
        pfad="/api/users",
        status=200,
        dauer_ms=150,
    )


def test_parse_zeile_zu_kurze_zeile():
    with pytest.raises(IndexError):
        parse_zeile("2024-01-15 08:23:45 GET /api/users 200")


def test_parse_zeile_ungueltige_status():
    with pytest.raises(ValueError):
        parse_zeile("2024-01-15 08:23:45 GET /api/users ABC 150")


def test_parse_zeile_ungueltige_dauer():
    with pytest.raises(ValueError):
        parse_zeile("2024-01-15 08:23:45 GET /api/users 200 XYZ")


def test_zaehle_status_eintrag():
    logs = [
        LogEntry("2024-01-15", "08:23:45", "GET", "/api/users", 200, 150),
        LogEntry("2024-01-15", "08:24:00", "POST", "/api/users", 404, 200),
        LogEntry("2024-01-15", "08:25:00", "GET", "/api/products", 200, 100),
        LogEntry("2024-01-15", "08:26:00", "GET", "/api/products", 500, 300),
    ]

    ergebnis = zaehle_status(logs)

    assert ergebnis == {200: 2, 404: 1, 500: 1}
