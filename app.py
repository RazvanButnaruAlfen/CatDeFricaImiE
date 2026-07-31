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
        return "🛬 CONFIRMAT: ținta a intrat în România, dar se află încă departe de Alexandra."
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


def make_tone(
    duration: float,
    start_frequency: float,
    end_frequency: float,
    pulse_speed: float,
    sample_rate: int = 22050,
) -> bytes:
    """Create a WAV alert sound without needing separate audio files."""
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        phase = 0.0

        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            position = t / duration
            frequency = start_frequency + (end_frequency - start_frequency) * position

            pulse = 0.55 + 0.45 * math.sin(2 * math.pi * pulse_speed * t)
            phase += 2 * math.pi * frequency / sample_rate

            sample = 0.30 * pulse * math.sin(phase)
            sample += 0.08 * math.sin(2 * phase)
            sample = max(-1.0, min(1.0, sample))
            frames.extend(struct.pack("<h", int(sample * 32767)))

        wav_file.writeframes(frames)

    return buffer.getvalue()


def sound_50() -> bytes:
    # Short warning beep
    return make_tone(
        duration=1.2,
        start_frequency=520,
        end_frequency=680,
        pulse_speed=4.0,
    )


def sound_80() -> bytes:
    # More urgent rising alarm
    return make_tone(
        duration=2.2,
        start_frequency=650,
        end_frequency=1050,
        pulse_speed=6.0,
    )


def sound_100() -> bytes:
    # Full siren
    return make_tone(
        duration=4.0,
        start_frequency=480,
        end_frequency=1200,
        pulse_speed=1.4,
    )


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


def alert_zone(value: int) -> int:
    if value >= 100:
        return 100
    if value >= 80:
        return 80
    if value >= 50:
        return 50
    return 0


today = today_in_romania()
automatic_fear = fear_level(today)
emoji, status = status_for(automatic_fear)

if "random_message" not in st.session_state:
    st.session_state.random_message = random.choice(FUNNY_MESSAGES)

if "last_alert_zone" not in st.session_state:
    st.session_state.last_alert_zone = 0

st.title("🚨 OPERAȚIUNEA PLOIEȘTI")
st.subheader("Sistem automat de avertizare pentru Alexandra")
st.caption(f"Data sistemului: {today.strftime('%d.%m.%Y')} · Ora României")

if today < ROMANIA_DATE:
    st.info(f"🇷🇴 Răzvan intră în România peste **{(ROMANIA_DATE - today).days} zile**.")
elif today < PLOIESTI_DATE:
    st.warning(
        f"🇷🇴 Răzvan este deja în România. "
        f"Ajunge în Ploiești peste **{(PLOIESTI_DATE - today).days} zile**."
    )
else:
    st.error("📍 Răzvan este în Ploiești.")

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
                {"range": [0, 50], "color": "lightgreen"},
                {"range": [50, 80], "color": "khaki"},
                {"range": [80, 100], "color": "tomato"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 6},
                "thickness": 0.8,
                "value": 80,
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

# The strongest of the automatic and declared levels controls the sound.
active_fear = max(automatic_fear, manual_fear)
current_zone = alert_zone(active_fear)

# Play only when entering a higher alert zone, not on every Streamlit rerun.
if current_zone > st.session_state.last_alert_zone:
    if current_zone == 50:
        play_audio(sound_50())
        st.warning("🔔 Nivelul de 50% a fost depășit: avertizare moderată.")
    elif current_zone == 80:
        play_audio(sound_80())
        st.error("🚨 Nivelul de 80% a fost depășit: alertă severă.")
    elif current_zone == 100:
        play_audio(sound_100())
        st.balloons()
        st.error("💀 100%: RĂZVAN A AJUNS. NU MAI EXISTĂ SCĂPARE.")

st.session_state.last_alert_zone = current_zone

# Reset the trigger when the slider goes back below a threshold.
if current_zone < st.session_state.last_alert_zone:
    st.session_state.last_alert_zone = current_zone

st.divider()
st.subheader("🔊 Testarea alarmelor")

sound_col1, sound_col2, sound_col3 = st.columns(3)

with sound_col1:
    if st.button("🔔 Sunet 50%", use_container_width=True):
        play_audio(sound_50())

with sound_col2:
    if st.button("🚨 Sunet 80%", use_container_width=True):
        play_audio(sound_80())

with sound_col3:
    if st.button("💀 Sunet 100%", use_container_width=True):
        play_audio(sound_100())

if active_fear >= 80:
    st.warning("Ascunde berea. Încuie ușa. Nu răspunde imediat la telefon.")

if today >= PLOIESTI_DATE:
    st.error("💀 ALERTĂ MAXIMĂ: RĂZVAN A AJUNS ÎN PLOIEȘTI!")

st.caption(
    "Unele browsere blochează sunetele automate înainte de prima interacțiune. "
    "În acest caz, apasă o dată pe unul dintre butoanele de test."
)
