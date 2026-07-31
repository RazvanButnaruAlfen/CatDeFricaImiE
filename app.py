
import base64
import io
import random
import textwrap
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import plotly.graph_objects as go
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


st.set_page_config(
    page_title="S.A.T.A.",
    page_icon="📡",
    layout="centered",
)

ROMANIA_DATE = date(2026, 8, 9)
PLOIESTI_DATE = date(2026, 8, 14)
BRASOV_START = date(2026, 8, 15)
BRASOV_END = date(2026, 8, 17)

TIMEZONE = ZoneInfo("Europe/Bucharest")
BASE_DIR = Path(__file__).parent
SOUND_DIR = BASE_DIR / "sounds"

RECOMMENDATIONS = [
    "Se recomandă consum moderat de cafea.",
    "Evitați verificarea telefonului din 30 în 30 de secunde.",
    "Respirați normal. Sistemul monitorizează situația.",
    "Nu împachetați bagajul pentru Brașov de cinci ori.",
    "Încă nu este cazul să intrați în panică.",
    "Zâmbitul fără motiv este considerat un efect secundar normal.",
    "Sistemul nu poate garanta că Răzvan nu va apărea cu o surpriză.",
    "Se recomandă păstrarea unei aparențe rezonabile de calm.",
    "Nu întrebați sistemul de câte ori a fost recitită ultima conversație.",
    "Planul pentru Brașov este real. Negarea nu mai este o strategie eficientă.",
    "O noapte petrecută împreună nu reprezintă o urgență. Deocamdată.",
    "Se recomandă să nu fie analizat fiecare mesaj timp de 45 de minute.",
]

FUNNY_MESSAGES = [
    "Surse din Olanda confirmă că Răzvan își verifică bagajele.",
    "Telefonul Alexandrei a vibrat. Poate fi Răzvan. Poate fi Glovo.",
    "Un martor afirmă că Răzvan a verificat traseul către Brașov.",
    "Nivelul rezervelor de calm ale Alexandrei este în scădere.",
    "Un prieten a spus «stai liniștită». Tensiunea a crescut imediat.",
    "Radarul nu detectează nimic. Tocmai de aceea situația este suspectă.",
    "Sistemul a detectat zâmbete fără explicație aparentă.",
    "Rezervarea pentru Brașov rămâne activă. Retragerea devine improbabilă.",
]


def today_ro():
    return datetime.now(TIMEZONE).date()


def tension_level(today):
    if today < ROMANIA_DATE:
        days_left = (ROMANIA_DATE - today).days
        return max(8, 28 - days_left * 2)

    progression = {
        date(2026, 8, 9): 45,
        date(2026, 8, 10): 50,
        date(2026, 8, 11): 58,
        date(2026, 8, 12): 65,
        date(2026, 8, 13): 72,
        date(2026, 8, 14): 80,
        date(2026, 8, 15): 92,
        date(2026, 8, 16): 100,
        date(2026, 8, 17): 100,
    }
    return progression.get(today, 100 if today > BRASOV_END else 80)


def operational_report(today):
    if today < ROMANIA_DATE:
        return (
            "Ținta se află încă în Olanda. Nu au fost detectate deplasări "
            "majore. Pregătirile sunt însă considerate probabile."
        )
    if today == ROMANIA_DATE:
        return (
            "Confirmare oficială: ținta a intrat pe teritoriul României. "
            "Protocolul GALBEN a fost activat."
        )
    if today < PLOIESTI_DATE:
        return (
            "Ținta se află în România. Distanța față de Alexandra scade, "
            "iar planul pentru Brașov rămâne activ."
        )
    if today == PLOIESTI_DATE:
        return (
            "Contact vizual confirmat în Ploiești. Tensiunea Alexandrei a "
            "depășit nivelul obișnuit. Plecarea spre Brașov este iminentă."
        )
    if today == BRASOV_START:
        return (
            "Deplasare detectată pe direcția Brașov. Alexandra și Răzvan "
            "se află singuri în aceeași misiune."
        )
    if today == date(2026, 8, 16):
        return (
            "Protocol NEGRU activ. Prima noapte petrecută împreună a fost "
            "confirmată. Sistemul nu mai poate reduce tensiunea."
        )
    if today == BRASOV_END:
        return (
            "Operațiunea Brașov se apropie de final. Datele indică faptul "
            "că Alexandra a supraviețuit evenimentului principal."
        )
    return (
        "Operațiunea Brașov s-a încheiat. Sistemul continuă monitorizarea "
        "efectelor secundare."
    )


def protocol(value):
    if value < 50:
        return "NORMAL", "Monitorizare"
    if value < 80:
        return "GALBEN", "Atenție"
    if value < 92:
        return "PORTOCALIU", "Alertă ridicată"
    if value < 100:
        return "ROȘU", "Pericol iminent"
    return "NEGRU", "Alertă maximă"


def location(today):
    if today < ROMANIA_DATE:
        return "Olanda"
    if today < PLOIESTI_DATE:
        return "România"
    if today < BRASOV_START:
        return "Ploiești"
    if today <= BRASOV_END:
        return "Brașov"
    return "Locație clasificată"


def alert_zone(value):
    if value >= 100:
        return 100
    if value >= 80:
        return 80
    if value >= 50:
        return 50
    return 0


def autoplay_sound(filename):
    path = SOUND_DIR / filename
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{encoded}" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True,
    )


def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_wrapped(draw, text, xy, width_chars, font_obj, fill, spacing=10):
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width_chars) or [""])
    draw.multiline_text(xy, "\n".join(lines), font=font_obj, fill=fill, spacing=spacing)
    bbox = draw.multiline_textbbox(xy, "\n".join(lines), font=font_obj, spacing=spacing)
    return bbox[3]


def create_daily_report_jpg(today, tension, recommendation):
    width, height = 1200, 1600
    bg = (13, 20, 28)
    panel = (24, 34, 45)
    white = (238, 242, 246)
    muted = (166, 180, 194)
    green = (65, 210, 140)
    yellow = (245, 199, 71)
    orange = (245, 139, 67)
    red = (235, 78, 78)

    protocol_name, protocol_text = protocol(tension)
    accent = green if tension < 50 else yellow if tension < 80 else orange if tension < 100 else red

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    draw.rectangle((55, 55, width - 55, height - 55), outline=accent, width=5)
    draw.text((95, 90), "S.A.T.A.", font=font(82, True), fill=accent)
    draw.text(
        (95, 190),
        "Sistem Automat pentru Tensiunea Alexandrei",
        font=font(31, True),
        fill=white,
    )
    draw.text(
        (95, 245),
        f"RAPORT ZILNIC • {today.strftime('%d.%m.%Y')}",
        font=font(26),
        fill=muted,
    )

    draw.rounded_rectangle((85, 320, width - 85, 650), radius=28, fill=panel)
    draw.text((125, 360), "NIVEL DE TENSIUNE", font=font(30, True), fill=muted)
    draw.text((125, 415), f"{tension}%", font=font(110, True), fill=accent)
    draw.text(
        (575, 435),
        f"PROTOCOL {protocol_name}\n{protocol_text}",
        font=font(34, True),
        fill=white,
        spacing=15,
    )

    bar_x1, bar_y1, bar_x2, bar_y2 = 125, 570, width - 125, 610
    draw.rounded_rectangle((bar_x1, bar_y1, bar_x2, bar_y2), radius=20, fill=(56, 68, 80))
    filled = bar_x1 + int((bar_x2 - bar_x1) * tension / 100)
    draw.rounded_rectangle((bar_x1, bar_y1, max(bar_x1 + 20, filled), bar_y2), radius=20, fill=accent)

    y = 720
    draw.text((95, y), "BULETIN OPERATIV", font=font(31, True), fill=accent)
    y += 65
    y = draw_wrapped(
        draw,
        operational_report(today),
        (95, y),
        60,
        font(31),
        white,
        spacing=13,
    ) + 65

    draw.text((95, y), "DATE MONITORIZATE", font=font(31, True), fill=accent)
    y += 65
    details = [
        f"Țintă monitorizată: Răzvan",
        f"Localizare estimată: {location(today)}",
        f"Obiectiv principal: Brașov, 15–17 august",
        f"Stare sistem: OPERAȚIONAL",
    ]
    for line in details:
        draw.text((115, y), f"• {line}", font=font(28), fill=white)
        y += 48

    y += 35
    draw.text((95, y), "RECOMANDAREA SISTEMULUI", font=font(31, True), fill=accent)
    y += 65
    draw.rounded_rectangle((85, y - 20, width - 85, y + 220), radius=24, fill=panel)
    draw_wrapped(draw, recommendation, (125, y + 20), 55, font(31, True), white, spacing=13)

    draw.text(
        (95, height - 130),
        "DOCUMENT GENERAT AUTOMAT • NIVEL DE CLASIFICARE: STRICT SECRET",
        font=font(21, True),
        fill=muted,
    )

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=94)
    return output.getvalue()


today = today_ro()
automatic_tension = tension_level(today)

if "recommendation" not in st.session_state:
    st.session_state.recommendation = random.choice(RECOMMENDATIONS)
if "random_message" not in st.session_state:
    st.session_state.random_message = random.choice(FUNNY_MESSAGES)
if "last_alert_zone" not in st.session_state:
    st.session_state.last_alert_zone = 0

st.markdown(
    """
    <div style="text-align:center">
        <div style="font-size:64px;font-weight:900;letter-spacing:8px">📡 S.A.T.A.</div>
        <div style="font-size:25px;font-weight:700">Sistem Automat pentru Tensiunea Alexandrei</div>
        <div style="margin-top:10px">CLASIFICARE: <b>STRICT SECRET</b></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

protocol_name, protocol_text = protocol(automatic_tension)
a, b, c = st.columns(3)
a.metric("Stare sistem", "OPERAȚIONAL")
b.metric("Țintă", "Răzvan")
c.metric("Protocol", protocol_name)

st.caption(
    f"Ultima sincronizare: {datetime.now(TIMEZONE).strftime('%d.%m.%Y %H:%M')} "
    f"• Localizare estimată: {location(today)}"
)

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=automatic_tension,
        number={"suffix": "%", "font": {"size": 58}},
        title={"text": "TENSIUNEA ALEXANDREI", "font": {"size": 23}},
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

st.subheader("📑 Buletin operativ")
st.info(operational_report(today))

st.subheader("🤖 Recomandarea sistemului")
st.success(st.session_state.recommendation)

rec_col, msg_col = st.columns(2)
with rec_col:
    if st.button("🔄 Recomandare nouă", use_container_width=True):
        st.session_state.recommendation = random.choice(RECOMMENDATIONS)
        st.rerun()
with msg_col:
    if st.button("📡 Interceptare nouă", use_container_width=True):
        st.session_state.random_message = random.choice(FUNNY_MESSAGES)
        st.rerun()

st.write(f"**Interceptare curentă:** {st.session_state.random_message}")

st.divider()
st.subheader("🎚️ Declarația oficială a Alexandrei")

manual_tension = st.slider(
    "Alexandra poate corecta aici estimarea sistemului:",
    0,
    100,
    automatic_tension,
)

active_tension = max(automatic_tension, manual_tension)
active_protocol, active_status = protocol(active_tension)

x, y, z = st.columns(3)
x.metric("Tensiune automată", f"{automatic_tension}%")
y.metric("Tensiune declarată", f"{manual_tension}%")
z.metric("Protocol activ", active_protocol)

current_zone = alert_zone(active_tension)
previous_zone = st.session_state.last_alert_zone

if current_zone > previous_zone:
    if current_zone == 50:
        autoplay_sound("beep50.wav")
        st.warning("🔔 Protocol GALBEN: bip rar activat.")
    elif current_zone == 80:
        autoplay_sound("beep80.wav")
        st.error("🚨 Protocol PORTOCALIU: bip rapid activat.")
    elif current_zone == 100:
        autoplay_sound("siren100.wav")
        st.balloons()
        st.error("💀 PROTOCOL NEGRU: WEEEO! WEEEO! WEEEO!")

st.session_state.last_alert_zone = current_zone

st.divider()
st.subheader("🖼️ Raportul zilei")

report_jpg = create_daily_report_jpg(
    today=today,
    tension=active_tension,
    recommendation=st.session_state.recommendation,
)

st.download_button(
    "📥 Generează și descarcă raportul zilei (.jpg)",
    data=report_jpg,
    file_name=f"Raport_SATA_{today.strftime('%Y-%m-%d')}.jpg",
    mime="image/jpeg",
    use_container_width=True,
)

with st.expander("Previzualizare raport"):
    st.image(report_jpg, use_container_width=True)

st.divider()
st.subheader("🔊 Testarea alarmelor")
s1, s2, s3 = st.columns(3)
with s1:
    if st.button("🔔 Test 50%", use_container_width=True):
        autoplay_sound("beep50.wav")
with s2:
    if st.button("🚨 Test 80%", use_container_width=True):
        autoplay_sound("beep80.wav")
with s3:
    if st.button("💀 Test 100%", use_container_width=True):
        autoplay_sound("siren100.wav")

st.caption(
    "Unele browsere blochează prima redare automată. "
    "Apasă unul dintre butoanele de test pentru a permite sunetul."
)
