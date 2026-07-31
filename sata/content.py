
from __future__ import annotations
from datetime import date
import hashlib
import random

FUNNY_ANALYSES = [
    ("Declarație interceptată", "„Nu sunt emoționată.”", "Credibilitate estimată: 4%"),
    ("Calm declarat", "94%", "Calm măsurat: 17%"),
    ("Protocol comportamental", "NEGARE", "Stare: activă și foarte convingătoare doar pentru operator."),
    ("Telefon verificat", "17 ori", "Interval analizat: suspect de scurt."),
    ("Expresie probabilă", "„Vedem...”", "Probabilitate de apariție: 91%"),
    ("Expresie probabilă", "„Nu contează.”", "Evaluarea S.A.T.A.: contează."),
    ("Indicator operațional", "Zâmbete fără motiv: 6", "Cauza nu a putut fi confirmată oficial."),
    ("Nivel de planificare", "Ridicat", "Nivel de control asupra realității: modest."),
    ("Problemă principală detectată", "Olanda", "Soluția este temporar în curs de deplasare."),
    ("Nivel de «Lasă că vedem»", "98%", "Sistemul consideră valoarea plauzibilă."),
    ("Bagaj verificat", "De 3 ori", "Nu s-au detectat modificări importante."),
    ("Vremea din Brașov", "Verificată din nou", "Prognoza nu se schimbă prin insistență."),
]

FUNNY_RECOMMENDATIONS = [
    "Telefonul nu răspunde mai repede dacă este privit continuu.",
    "Cafeaua nu reduce emoțiile. Uneori le oferă doar viteză.",
    "Respirația rămâne o funcție recomandată de sistem.",
    "Nu este necesară verificarea vremii din Brașov pentru a 18-a oară.",
    "Evitați împachetarea aceluiași bagaj în cinci variante.",
    "Sistemul recomandă hidratare, răbdare și mai puține scenarii.",
    "Păstrați nivelul de negare sub limita tehnică de 95%.",
    "Nu toate mesajele trebuie recitite pentru analiză criminalistică.",
    "Încercați să nu transformați fiecare pauză de răspuns într-un documentar.",
    "Reduceți frecvența afirmației «nu sunt stresată». Sistemul nu o mai procesează.",
]

WARM_RECOMMENDATIONS = [
    "Nu toate momentele importante trebuie planificate.",
    "Uneori este suficient să fiți împreună.",
    "Nu există niciun cronometru.",
    "Cele mai frumoase amintiri apar adesea când planul se schimbă.",
    "Distanța a fost partea grea. Restul se construiește pas cu pas.",
    "Nimic nu trebuie demonstrat. Timpul petrecut împreună este suficient.",
    "Weekendul nu are obiective obligatorii. Doar posibilități.",
    "Sistemul recomandă mai puține așteptări și mai multă prezență.",
]

WHAT_SYSTEM_KNOWS = [
    ("Prima conexiune", "Martie 2026"),
    ("Distanță", "1984 km"),
    ("Timp petrecut împreună", "Prea puțin"),
    ("Conversații", "Suficiente pentru o conexiune reală"),
]

WHAT_SYSTEM_DOES_NOT_KNOW = [
    "Cum va decurge fiecare zi.",
    "Care va fi cea mai frumoasă amintire.",
    "Ce moment va rămâne cel mai important.",
    "De câte ori se va schimba planul.",
    "Ce poate deveni această poveste în timp.",
]

def _seed(today: date, salt: str) -> int:
    key = f"{today.isoformat()}::{salt}".encode("utf-8")
    return int(hashlib.sha256(key).hexdigest()[:12], 16)

def daily_analysis(today: date):
    return random.Random(_seed(today, "analysis")).choice(FUNNY_ANALYSES)

def daily_recommendation(today: date) -> tuple[str, str]:
    rng = random.Random(_seed(today, "recommendation"))
    if rng.random() < 0.8:
        return "comic", rng.choice(FUNNY_RECOMMENDATIONS)
    return "cald", rng.choice(WARM_RECOMMENDATIONS)

def probability_phrase(today: date) -> tuple[str, int, str]:
    phrases = [
        ("„Vedem.”", 91, "Traducere: există deja cel puțin trei scenarii."),
        ("„Lasă...”", 84, "Sistemul recomandă să nu insiste nimeni."),
        ("„Nu contează.”", 93, "Evaluare: foarte probabil contează."),
        ("„Nu sunt stresată.”", 97, "Credibilitate estimată: 2%."),
        ("„Mai vorbim.”", 81, "Interpretare: subiectul rămâne deschis."),
    ]
    return random.Random(_seed(today, "phrase")).choice(phrases)
