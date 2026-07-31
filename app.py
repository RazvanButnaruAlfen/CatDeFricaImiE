import base64
import io
import math
import random
import struct
import wave

import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Fricometrul lui Răzvan",
    page_icon="🚨",
    layout="centered",
)

FUNNY_MESSAGES = [
    "Răzvan și-a verificat pașaportul. Coincidență? Nu cred.",
    "Cineva a întrebat unde este berea. Nivelul de alertă crește.",
    "Telefonul a vibrat. Poate fi Răzvan. Poate fi Glovo.",
    "Vecinii au raportat râsete suspecte în apropiere.",
    "Frigiderul tremură. Situația devine serioasă.",
    "Surse neconfirmate spun că bagajul este deja pregătit.",
    "Un prieten a spus «stai liniștit». Panica a crescut imediat.",
    "Radarul nu detectează nimic. Asta este și mai suspect.",
]


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


def status_for(value: int) -> tuple[str, str]:
    if value < 20:
        return "😎", "Totul este sub control. Deocamdată."
    if value < 40:
        return "🙂", "Există mici motive de îngrijorare."
    if value < 60:
        return "😬", "Pregătirile ar trebui să înceapă."
    if value < 80:
        return "😨", "Nivel ridicat de panică."
    if value < 100:
        return "😱", "Răzvan este foarte aproape!"
    return "💀", "Este prea târziu. Răzvan a ajuns."


if "frica" not in st.session_state:
    st.session_state.frica = 50

if "mesaj" not in st.session_state:
    st.session_state.mesaj = random.choice(FUNNY_MESSAGES)


st.title("🚨 FRICOMETRU 2.0")
st.subheader("Ediția oficială: Răzvan vine în România")
st.caption("Gauge, sirenă, predicții și mesaje aleatorii.")

left, right = st.columns(2)

with left:
    if st.button("🎲 PREDICȚIE AUTOMATĂ", use_container_width=True):
        st.session_state.frica = random.randint(0, 100)
        st.session_state.mesaj = random.choice(FUNNY_MESSAGES)

with right:
    if st.button("😂 MESAJ ALEATORIU", use_container_width=True):
        st.session_state.mesaj = random.choice(FUNNY_MESSAGES)


frica = st.slider(
    "Cât de frică îmi este de ce se va întâmpla când va veni Răzvan în România?",
    0,
    100,
    key="frica",
)

emoji, message = status_for(frica)

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=frica,
        number={"suffix": "%", "font": {"size": 52}},
        title={"text": "NIVEL DE FRICĂ", "font": {"size": 24}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkred", "thickness": 0.3},
            "steps": [
                {"range": [0, 25], "color": "lightgreen"},
                {"range": [25, 50], "color": "khaki"},
                {"range": [50, 75], "color": "orange"},
                {"range": [75, 100], "color": "tomato"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 6},
                "thickness": 0.8,
                "value": 85,
            },
        },
    )
)

gauge.update_layout(height=350, margin=dict(l=20, r=20, t=80, b=20))
st.plotly_chart(gauge, use_container_width=True)

st.markdown(
    f"""
    <div style="text-align:center;font-size:105px">{emoji}</div>
    <div style="text-align:center;font-size:26px;font-weight:bold">{message}</div>
    """,
    unsafe_allow_html=True,
)

st.info(f"📢 {st.session_state.mesaj}")

m1, m2, m3 = st.columns(3)
m1.metric("Panică", f"{frica}%")
m2.metric("Șanse de scăpare", f"{100 - frica}%")
m3.metric("Zile până la haos", max(0, round((100 - frica) / 10)))

st.divider()

if st.button("🚨 TESTEAZĂ SIRENA", use_container_width=True):
    play_audio(make_siren())
    st.error("SIRENA A FOST ACTIVATĂ!")

if frica >= 85:
    st.warning("Ascunde berea. Încuie ușa. Nu răspunde la telefon.")

if frica == 100:
    st.balloons()
    play_audio(make_siren())
    st.error("💀 ALERTĂ MAXIMĂ: RĂZVAN ESTE DEJA ÎN ROMÂNIA!")
