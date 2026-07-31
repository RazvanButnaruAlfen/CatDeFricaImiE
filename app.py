
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
    width, height = 1400, 1800

    bg = (10, 17, 24)
    panel = (25, 36, 48)
    panel_alt = (33, 46, 59)
    white = (242, 245, 248)
    muted = (174, 188, 201)
    green = (74, 214, 145)
    yellow = (248, 204, 83)
    orange = (247, 143, 68)
    red = (238, 79, 79)
    cream = (246, 235, 205)
    ink = (38, 42, 46)

    protocol_name, protocol_text = protocol(tension)
    accent = (
        green if tension < 50
        else yellow if tension < 80
        else orange if tension < 100
        else red
    )

    days_to_brasov = max(0, (BRASOV_START - today).days)

    if tension < 30:
        verdict = "Alexandra pare calmă. Sistemul rămâne suspicios."
        face = ":)"
        mood = "CALM SUSPECT"
    elif tension < 50:
        verdict = "Primele semne de nerăbdare au fost detectate."
        face = ":|"
        mood = "UȘOR AGITATĂ"
    elif tension < 80:
        verdict = "Tensiunea crește. Telefonul trebuie lăsat jos din când în când."
        face = ":O"
        mood = "EMOȚII ACTIVE"
    elif tension < 100:
        verdict = "Brașovul se apropie. Negarea nu mai este o strategie."
        face = "!!!"
        mood = "ALERTĂ SERIOASĂ"
    else:
        verdict = "Contact total confirmat. Sistemul nu mai poate interveni."
        face = "X_X"
        mood = "PROTOCOL NEGRU"

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Border and header
    draw.rounded_rectangle(
        (35, 35, width - 35, height - 35),
        radius=28,
        outline=accent,
        width=5,
    )

    draw.text((80, 70), "S.A.T.A.", font=font(96, True), fill=accent)
    draw.text(
        (82, 175),
        "Sistem Automat pentru Tensiunea Alexandrei",
        font=font(36, True),
        fill=white,
    )
    draw.text(
        (82, 230),
        f"RAPORTUL ZILEI  |  {today.strftime('%d.%m.%Y')}",
        font=font(29, True),
        fill=muted,
    )

    # Stamp
    stamp_box = (940, 75, 1310, 235)
    draw.rounded_rectangle(stamp_box, radius=18, outline=red, width=7)
    draw.text((993, 100), "STRICT", font=font(43, True), fill=red)
    draw.text((980, 154), "SECRET", font=font(43, True), fill=red)

    # Main tension card
    draw.rounded_rectangle((70, 305, 1330, 720), radius=34, fill=panel)
    draw.text((110, 345), "NIVELUL DE TENSIUNE ALEXANDRA", font=font(35, True), fill=muted)
    draw.text((110, 405), f"{tension}%", font=font(142, True), fill=accent)

    draw.rounded_rectangle((765, 365, 1260, 600), radius=26, fill=panel_alt)
    draw.text((805, 400), f"PROTOCOL {protocol_name}", font=font(35, True), fill=white)
    draw.text((805, 455), protocol_text, font=font(30), fill=muted)
    draw.text((805, 520), face, font=font(58, True), fill=accent)

    bar_x1, bar_y1, bar_x2, bar_y2 = 110, 630, 1260, 685
    draw.rounded_rectangle((bar_x1, bar_y1, bar_x2, bar_y2), radius=27, fill=(68, 80, 92))
    filled = bar_x1 + int((bar_x2 - bar_x1) * tension / 100)
    draw.rounded_rectangle(
        (bar_x1, bar_y1, max(bar_x1 + 35, filled), bar_y2),
        radius=27,
        fill=accent,
    )
    draw.text((110, 694), "0%", font=font(22, True), fill=muted)
    draw.text((650, 694), "50%", font=font(22, True), fill=muted)
    draw.text((1205, 694), "100%", font=font(22, True), fill=muted)

    # Verdict strip
    draw.rounded_rectangle((70, 750, 1330, 885), radius=26, fill=cream)
    draw.text((105, 785), "CONCLUZIA SISTEMULUI", font=font(28, True), fill=ink)
    draw.text((105, 830), verdict, font=font(31, True), fill=ink)

    # Operational report
    draw.rounded_rectangle((70, 925, 835, 1245), radius=28, fill=panel)
    draw.text((110, 965), "BULETIN OPERATIV", font=font(34, True), fill=accent)
    draw_wrapped(
        draw,
        operational_report(today),
        (110, 1030),
        44,
        font(31),
        white,
        spacing=15,
    )

    # Fun diagnostics
    draw.rounded_rectangle((865, 925, 1330, 1245), radius=28, fill=panel_alt)
    draw.text((905, 965), "INDICATORI SUSPECȚI", font=font(31, True), fill=accent)

    checks = [
        ("Verificare telefon", "FRECVENTĂ"),
        ("Zâmbete fără motiv", "DETECTATE"),
        ("Calm afișat", "NECONVINGĂTOR"),
        ("Gânduri despre Brașov", "CONFIRMATE"),
    ]
    y = 1030
    for label, value in checks:
        draw.text((905, y), label, font=font(25), fill=white)
        draw.text((905, y + 31), value, font=font(24, True), fill=accent)
        y += 69

    # Timeline
    draw.rounded_rectangle((70, 1285, 1330, 1465), radius=28, fill=panel)
    draw.text((110, 1320), "CRONOLOGIA MISIUNII", font=font(32, True), fill=accent)

    timeline = [
        ("09 AUG", "Intrare în România"),
        ("14 AUG", "Contact în Ploiești"),
        ("15-17 AUG", "Misiunea Brașov"),
    ]
    x_positions = [130, 510, 930]
    for (date_label, event), x in zip(timeline, x_positions):
        draw.ellipse((x, 1382, x + 32, 1414), fill=accent)
        draw.text((x + 48, 1365), date_label, font=font(25, True), fill=white)
        draw.text((x + 48, 1403), event, font=font(23), fill=muted)

    # Recommendation card
    draw.rounded_rectangle((70, 1505, 1330, 1690), radius=28, fill=cream)
    draw.text((110, 1540), "RECOMANDAREA ZILEI", font=font(31, True), fill=ink)
    draw_wrapped(
        draw,
        recommendation,
        (110, 1600),
        67,
        font(32, True),
        ink,
        spacing=13,
    )

    # Footer
    footer = (
        f"Stare: {mood}  |  Localizare: {location(today)}  |  "
        f"Zile până la Brașov: {days_to_brasov}"
    )
    draw.text((80, 1735), footer, font=font(24, True), fill=accent)
    draw.text(
        (80, 1770),
        "Raport generat automat. Orice asemănare cu realitatea este absolut intenționată.",
        font=font(20),
        fill=muted,
    )

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=95)
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
