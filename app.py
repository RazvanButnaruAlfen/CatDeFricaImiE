import base64
import io
import math
import random
import struct
import wave
from datetime import date, datetime
from zoneinfo import ZoneInfo

import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Operațiunea Ploiești",
    page_icon="🚨",
    layout="centered",
)

# Important dates
ROMANIA_DATE = date(2026, 8, 9)
PLOIESTI_DATE = date(2026, 8, 14)
TIMEZONE = ZoneInfo("Europe/Bucharest")

FUNNY_MESSAGES = [
    "Surse din Olanda confirmă că Răzvan își verifică bagajele.",
    "Telefonul Alexandrei a vibrat. Poate fi Răzvan. Poate fi Glovo.",
    "Un martor afirmă că Răzvan a întrebat unde se găsește bere rece.",
    "Frigiderul din Ploiești a început să tremure fără explicație.",
    "Autoritățile recomandă calm, provizii și răspunsuri întârziate la mesaje.",
    "Radarul nu detectează nimic. Tocmai de aceea situația este suspectă.",
    "Un prieten a spus «stai liniștită». Nivelul de panică a crescut imediat.",
    "Surse neconfirmate spun că Răzvan și-a făcut deja planul de atac.",
]


def today_in_romania() -> date:
    return datetime.now(TIMEZONE).date()


def fear_level(today: date) -> int:
    """Automatic fear level based on Răzvan's travel timeline."""
    if today < ROMANIA_DATE:
        days_left = (ROMANIA_DATE - today).days
        return max(5, 20 - days_left * 2)

    if ROMANIA_DATE <= today < PLOIESTI_DATE:
        progression = {
            date(2026, 8, 9): 25,
            date(2026, 8, 10): 40,
            date(2026, 8, 11): 55,
            date(2026, 8, 12): 70,
            date(2026, 8, 13): 90,
        }
        return progression.get(today, 90)

    return 100


def intelligence_report(today: date) -> str:
    if today < ROMANIA_DATE:
        days = (ROMANIA_DATE - today).days
        return (
            f"🛰️ Răzvan se află încă în Olanda. "
            f"Intrarea pe teritoriul României este estimată peste {days} zile."
        )

    if today == ROMANIA_DATE:
        return "🛬 CONFIRMAT: ținta a intrat pe teritoriul României, dar se află încă departe de Alexandra."

    if today == date(2026, 8, 10):
        return "📡 Semnal detectat în România. Distanța față de Alexandra rămâne momentan acceptabilă."

    if today == date(2026, 8, 11):
        return "🧳 Bagajele au fost repoziționate. Intențiile țintei sunt încă neclare."

    if today == date(2026, 8, 12):
        return "🚗 Activitate rutieră suspectă. Ploieștiul a fost introdus în sistemul de navigație."

    if today == date(2026, 8, 13):
        return "⚠️ ULTIMA AVERTIZARE: sosirea în Ploiești este estimată pentru mâine."

    if today == PLOIESTI_DATE:
        return "🚨 CONTACT VIZUAL: Răzvan a ajuns în Ploiești. Nu mai există cale de scăpare."

    return "💀 Operațiunea a intrat în faza post-impact. Răzvan se află deja în zona Ploiești."


def status_for(value: int) -> tuple[str, str]:
    if value < 20:
        return "😎", "Situația este calmă. Alexandra poate dormi liniștită."
    if value < 40:
        return "🙂", "Există mici motive de îngrijorare."
    if value < 60:
        return "😬", "Răzvan este deja în România. Se recomandă vigilență."
    if value < 80:
        return "😨", "Distanța față de Ploiești scade."
    if value < 100:
        return "😱", "Pericol iminent. Sosirea este foarte aproape."
    return "💀", "Răzvan a ajuns în Ploiești."


def make_siren(duration: float = 3.0, sample_rate: int = 22050) -> bytes:
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = bytearray()

        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            sweep = 0.5 + 0.5 * math.sin(2 * math.pi * 0.8 * t)
            frequency = 500 + 450 * sweep
            sample = 0.38 * math.sin(2 * math.pi * frequency * t)
            sample += 0.10 * math.sin(2 * math.pi * frequency * 2 * t)
            sample = max(-1.0, min(1.0, sample))
            frames.extend(struct.pack("<h", int(sample * 32767)))

        wav_file.writeframes(frames)

    return buffer.getvalue()


def play_audio(audio_bytes: bytes) -> None:
    encoded = base64.b64encode(audio_bytes).decode("utf-8")
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{encoded}" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True,
    )


today = today_in_romania()
automatic_fear = fear_level(today)
emoji, status = status_for(automatic_fear)

if "random_message" not in st.session_state:
    st.session_state.random_message = random.choice(FUNNY_MESSAGES)

st.title("🚨 OPERAȚIUNEA PLOIEȘTI")
st.subheader("Sistem automat de avertizare pentru Alexandra")
st.caption(f"Data sistemului: {today.strftime('%d.%m.%Y')} · Ora României")

# Countdown area
if today < ROMANIA_DATE:
    st.info(f"🇷🇴 Răzvan intră în România peste **{(ROMANIA_DATE - today).days} zile**.")
elif today < PLOIESTI_DATE:
    st.warning(
        f"🇷🇴 Răzvan este deja în România. "
        f"Ajunge în Ploiești peste **{(PLOIESTI_DATE - today).days} zile**."
    )
else:
    st.error("📍 Răzvan este în Ploiești.")

# Automatic gauge
gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=automatic_fear,
        number={"suffix": "%", "font": {"size": 54}},
        title={"text": "NIVEL AUTOMAT DE FRICĂ", "font": {"size": 23}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkred", "thickness": 0.30},
            "steps": [
                {"range": [0, 25], "color": "lightgreen"},
                {"range": [25, 50], "color": "khaki"},
                {"range": [50, 75], "color": "orange"},
                {"range": [75, 100], "color": "tomato"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 6},
                "thickness": 0.8,
                "value": 90,
            },
        },
    )
)
gauge.update_layout(height=350, margin=dict(l=20, r=20, t=80, b=20))
st.plotly_chart(gauge, use_container_width=True)

st.markdown(
    f"""
    <div style="text-align:center;font-size:105px">{emoji}</div>
    <div style="text-align:center;font-size:25px;font-weight:bold">{status}</div>
    """,
    unsafe_allow_html=True,
)

st.divider()
st.subheader("🛰️ Raport de informații")
st.info(intelligence_report(today))

col1, col2 = st.columns(2)

with col1:
    if st.button("😂 MESAJ ALEATORIU", use_container_width=True):
        st.session_state.random_message = random.choice(FUNNY_MESSAGES)

with col2:
    if st.button("🎲 PREDICȚIE SECRETĂ", use_container_width=True):
        predicted = random.randint(max(automatic_fear, 20), 100)
        st.session_state.random_message = (
            f"Modelul secret estimează că frica reală a Alexandrei este de {predicted}%."
        )

st.write(f"📢 **{st.session_state.random_message}**")

st.divider()
st.subheader("🎚️ Declarația oficială a Alexandrei")

manual_fear = st.slider(
    "Alexandra poate declara aici cât de frică îi este în realitate:",
    min_value=0,
    max_value=100,
    value=automatic_fear,
    step=1,
)

difference = manual_fear - automatic_fear

if difference > 15:
    st.warning("Analiza indică faptul că Alexandra este mai speriată decât admite sistemul.")
elif difference < -15:
    st.success("Alexandra pretinde că situația este sub control. Sistemul rămâne sceptic.")
else:
    st.info("Declarația Alexandrei este aproximativ compatibilă cu datele serviciilor secrete.")

m1, m2, m3 = st.columns(3)
m1.metric("Frică automată", f"{automatic_fear}%")
m2.metric("Frică declarată", f"{manual_fear}%")
m3.metric("Zile până la Ploiești", max(0, (PLOIESTI_DATE - today).days))

st.divider()

if st.button("🚨 TESTEAZĂ SIRENA", use_container_width=True):
    play_audio(make_siren())
    st.error("SIRENA A FOST ACTIVATĂ!")

if automatic_fear >= 90:
    st.warning("Ascunde berea. Încuie ușa. Nu răspunde imediat la telefon.")

if today >= PLOIESTI_DATE:
    st.balloons()
    st.error("💀 ALERTĂ MAXIMĂ: RĂZVAN A AJUNS ÎN PLOIEȘTI!")
    # Browsers may block automatic audio until the user interacts with the page.
    play_audio(make_siren())

st.caption(
    "Notă tehnică: unele browsere blochează sunetul automat. "
    "Butonul «Testează sirena» funcționează după interacțiunea cu pagina."
)
