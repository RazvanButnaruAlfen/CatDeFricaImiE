
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

ARRIVAL_ROMANIA = date(2026, 8, 9)
ARRIVAL_PLOIESTI = date(2026, 8, 14)
BRASOV_START = date(2026, 8, 15)
BRASOV_END = date(2026, 8, 17)
RETURN_NL = date(2026, 8, 27)
FIRST_CONNECTION = date(2026, 3, 1)
DISTANCE_KM = 1984


@dataclass(frozen=True)
class MissionStatus:
    phase: str
    status: str
    protocol: str
    tension: int
    location: str
    countdown: str
    summary: str
    color: str


def _days_phrase(days: int) -> str:
    if days == 1:
        return "1 zi"
    return f"{days} zile"


def get_mission_status(today: date) -> MissionStatus:
    if today < ARRIVAL_ROMANIA:
        remaining = (ARRIVAL_ROMANIA - today).days
        tension = min(48, max(8, 48 - remaining * 4))
        return MissionStatus(
            phase="Monitorizare la distanță",
            status="Subiectul se află încă în Olanda",
            protocol="VERDE",
            tension=tension,
            location="Olanda",
            countdown=f"T - {_days_phrase(remaining)} până la România",
            summary="Monitorizarea continuă. Sistemul confirmă că ultimele zile înainte de plecare trec suspect de încet.",
            color="#1f9d55",
        )

    if ARRIVAL_ROMANIA <= today < ARRIVAL_PLOIESTI:
        remaining = (ARRIVAL_PLOIESTI - today).days
        tension = 52 + (4 - min(4, remaining)) * 6
        return MissionStatus(
            phase="Prezență în România",
            status="Subiectul a intrat pe teritoriul României",
            protocol="GALBEN",
            tension=min(76, tension),
            location="România",
            countdown=f"T - {_days_phrase(remaining)} până la Ploiești",
            summary="Distanța fizică a început să scadă. S.A.T.A. detectează o creștere simultană a nerăbdării și a negației.",
            color="#d6a800",
        )

    if today == ARRIVAL_PLOIESTI:
        return MissionStatus(
            phase="Contact în Ploiești",
            status="Contact vizual confirmat",
            protocol="PORTOCALIU",
            tension=84,
            location="Ploiești",
            countdown="Distanță operațională: câțiva pași",
            summary="Aproape 2000 km au fost reduși la câțiva pași. Se recomandă mai puține scenarii și mai mult timp petrecut împreună.",
            color="#e67e22",
        )

    if BRASOV_START <= today <= BRASOV_END:
        day_no = (today - BRASOV_START).days + 1
        return MissionStatus(
            phase="Operațiunea Brașov",
            status=f"Weekendul este în desfășurare — ziua {day_no}",
            protocol="ROȘU",
            tension=min(100, 91 + day_no * 3),
            location="Brașov",
            countdown="Obiectiv: amintiri, nu obiective prestabilite",
            summary="Sistemul încearcă să prezică programul și primește aceeași eroare: realitatea refuză să respecte scenariile.",
            color="#c0392b",
        )

    if BRASOV_END < today < RETURN_NL:
        remaining = (RETURN_NL - today).days
        return MissionStatus(
            phase="Concediu în desfășurare",
            status="Monitorizare discretă activă",
            protocol="ALBASTRU",
            tension=max(40, 76 - (BRASOV_END - BRASOV_START).days),
            location="România",
            countdown=f"{_days_phrase(remaining)} până la întoarcerea în Olanda",
            summary="Datele colectate indică faptul că timpul petrecut împreună valorează mai mult decât toate simulările făcute înainte.",
            color="#2f6fb2",
        )

    if today == RETURN_NL:
        return MissionStatus(
            phase="Raport final",
            status="Operațiunea România s-a încheiat",
            protocol="DECLASIFICARE",
            tension=58,
            location="În tranzit spre Olanda",
            countdown="Următoarea etapă: continuitate la distanță",
            summary="Distanța revine. Conexiunea nu este obligată să o urmeze.",
            color="#6c5ce7",
        )

    return MissionStatus(
        phase="Post-operațiune",
        status="Arhivare și analiză",
        protocol="GRI",
        tension=32,
        location="Olanda / România",
        countdown="Următoarea întâlnire: de stabilit",
        summary="Operațiunea s-a încheiat, dar sistemul păstrează în arhivă suficiente dovezi că distanța nu a oprit apropierea.",
        color="#657786",
    )


def get_daily_story(today: date) -> str:
    special = {
        date(2026, 7, 31): "Sistemul a început numărătoarea inversă.",
        date(2026, 8, 5): "Se observă primele semne serioase de nerăbdare.",
        date(2026, 8, 9): "Subiectul a aterizat în România. Distanța fizică a început să scadă.",
        date(2026, 8, 14): "Distanța de aproape 2000 km a fost redusă la câțiva pași.",
        date(2026, 8, 15): "Brașovul nu este un test. Este o ocazie de a crea amintiri.",
        date(2026, 8, 18): "Simulările au fost mai complicate decât realitatea.",
        date(2026, 8, 27): "Operațiunea România s-a încheiat. Urmează o nouă etapă, cu mai multe amintiri decât înainte.",
    }
    return special.get(today, get_mission_status(today).summary)
