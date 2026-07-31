
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
from matplotlib import font_manager


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
    """
    Folosește fonturile DejaVu livrate împreună cu Matplotlib.
    Astfel, aplicația nu depinde de fonturile instalate în Streamlit Cloud
    și redă corect diacriticele românești: ă â î ș ț.
    """
    properties = font_manager.FontProperties(
        family="DejaVu Sans",
        weight="bold" if bold else "normal",
    )
    font_path = font_manager.findfont(properties, fallback_to_default=True)

    if not font_path or not Path(font_path).exists():
        raise RuntimeError("Fontul Unicode DejaVu Sans nu a putut fi localizat.")

    return ImageFont.truetype(font_path, size)


def draw_wrapped(draw, text, xy, width_chars, font_obj, fill, spacing=10):
    """
    Desenează text pe mai multe rânduri și returnează coordonata Y
    a marginii inferioare. Folosește textwrap, deja importat în aplicație.
    """
    lines = []
    for paragraph in str(text).split("\n"):
        lines.extend(textwrap.wrap(paragraph, width=width_chars) or [""])

    wrapped_text = "\n".join(lines)
    draw.multiline_text(
        xy,
        wrapped_text,
        font=font_obj,
        fill=fill,
        spacing=spacing,
    )
    bbox = draw.multiline_textbbox(
        xy,
        wrapped_text,
        font=font_obj,
        spacing=spacing,
    )
    return bbox[3]


def verify_romanian_text_support():
    # Forțează încărcarea fontului înainte de generarea raportului.
    # Textul este folosit pentru a verifica toate diacriticele românești.
    test_font = font(32, False)
    test_img = Image.new("RGB", (900, 100), "white")
    test_draw = ImageDraw.Draw(test_img)
    test_draw.text(
        (10, 20),
        "Ă Â Î Ș Ț ă â î ș ț — România, Ploiești, Brașov, țintă",
        font=test_font,
        fill="black",
    )


def create_daily_report_jpg(today, tension, recommendation):
    verify_romanian_text_support()
    width, height = 1080, 1920

    bg = (8, 14, 20)
    panel = (21, 30, 39)
    panel2 = (29, 41, 52)
    white = (247, 248, 250)
    muted = (183, 195, 206)
    green = (77, 219, 148)
    yellow = (250, 208, 87)
    orange = (248, 144, 70)
    red = (239, 75, 75)
    cream = (248, 237, 205)
    ink = (34, 38, 42)

    protocol_name, protocol_text = protocol(tension)
    accent = green if tension < 50 else yellow if tension < 80 else orange if tension < 100 else red

    if tension < 30:
        verdict = "Alexandra pare calmă. Sistemul rămâne suspicios."
        mood = "CALM SUSPECT"
    elif tension < 50:
        verdict = "Primele semne de nerăbdare au fost detectate."
        mood = "UȘOR AGITATĂ"
    elif tension < 80:
        verdict = "Tensiunea crește. Telefonul trebuie lăsat jos din când în când."
        mood = "EMOȚII ACTIVE"
    elif tension < 100:
        verdict = "Brașovul se apropie. Negarea nu mai este o strategie."
        mood = "ALERTĂ SERIOASĂ"
    else:
        verdict = "Contact total confirmat. Sistemul nu mai poate interveni."
        mood = "PROTOCOL NEGRU"

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    def load_icon(name, size):
        p = BASE_DIR / "assets" / name
        icon = Image.open(p).convert("RGBA")
        icon.thumbnail((size, size), Image.LANCZOS)
        return icon

    def paste_icon(name, xy, size):
        icon = load_icon(name, size)
        img.paste(icon, xy, icon)

    # Outer frame
    draw.rounded_rectangle((22, 22, width-22, height-22), radius=26, outline=accent, width=5)

    # Header — larger typography
    draw.text((55, 42), "S.A.T.A.", font=font(110, True), fill=accent)
    draw.text((58, 160), "Sistem Automat pentru", font=font(40, True), fill=white)
    draw.text((58, 205), "Tensiunea Alexandrei", font=font(40, True), fill=white)
    draw.text((58, 262), f"RAPORT ZILNIC • {today.strftime('%d.%m.%Y')}", font=font(34, True), fill=muted)

    # TOP SECRET icon from assets
    paste_icon("top_secret.png", (610, 42), 420)

    # Main tension card
    draw.rounded_rectangle((45, 330, 1035, 670), radius=28, fill=panel)
    draw.text((80, 370), "NIVEL DE TENSIUNE ALEXANDRA™", font=font(40, True), fill=muted)
    draw.text((78, 420), f"{tension}%", font=font(170, True), fill=accent)

    draw.rounded_rectangle((610, 405, 985, 585), radius=22, fill=panel2)
    draw.text((642, 435), f"PROTOCOL {protocol_name}", font=font(36, True), fill=white)
    draw.text((642, 495), protocol_text, font=font(34), fill=muted)
    draw.text((642, 545), mood, font=font(32, True), fill=accent)

    draw.rounded_rectangle((80, 600, 985, 648), radius=24, fill=(68,80,92))
    filled = 80 + int((985-80)*tension/100)
    draw.rounded_rectangle((80, 600, max(120, filled), 648), radius=24, fill=accent)
    draw.text((80, 652), "0%", font=font(24, True), fill=muted)
    draw.text((495, 652), "50%", font=font(24, True), fill=muted)
    draw.text((935, 652), "100%", font=font(24, True), fill=muted)

    # Operational report + conclusion
    draw.rounded_rectangle((45, 700, 1035, 1015), radius=28, fill=panel)
    draw.text((80, 742), "BULETIN OPERATIV", font=font(42, True), fill=accent)
    draw_wrapped(draw, operational_report(today), (80, 815), 42, font(38), white, spacing=15)

    draw.rounded_rectangle((620, 790, 985, 965), radius=20, fill=cream)
    draw.text((650, 820), "CONCLUZIE", font=font(28, True), fill=ink)
    draw_wrapped(draw, verdict, (650, 870), 24, font(25, True), ink, spacing=8)

    # Route section
    draw.rounded_rectangle((45, 1045, 1035, 1395), radius=28, fill=panel2)
    draw.text((80, 1085), "TRASEU MONITORIZAT", font=font(42, True), fill=accent)

    points = [
        ("olanda.png", "OLANDA", "ACUM"),
        ("romania.png", "ROMÂNIA", "09 AUG"),
        ("ploiesti.png", "PLOIEȘTI", "14 AUG"),
        ("brasov.png", "BRAȘOV", "15–17 AUG"),
    ]
    xs = [70, 320, 565, 810]

    draw.line((145, 1215, 890, 1215), fill=muted, width=6)

    for (icon_name, place, date_label), x in zip(points, xs):
        paste_icon(icon_name, (x, 1135), 155)
        draw.text((x+5, 1282), place, font=font(29, True), fill=white)
        draw.text((x+5, 1325), date_label, font=font(27, True), fill=accent)

    # Indicators
    draw.rounded_rectangle((45, 1425, 1035, 1645), radius=28, fill=panel)
    draw.text((80, 1465), "INDICATORI SUSPECȚI", font=font(40, True), fill=accent)

    indicators = [
        ("Verificare telefon", "FRECVENTĂ"),
        ("Zâmbete fără motiv", "DETECTATE"),
        ("Calm afișat", "NECONVINGĂTOR"),
        ("Gânduri despre Brașov", "CONFIRMATE"),
    ]
    positions = [(80,1530),(545,1530),(80,1595),(545,1595)]
    for (label, value), (x,y) in zip(indicators, positions):
        draw.text((x,y), label, font=font(28), fill=white)
        draw.text((x,y+34), value, font=font(26, True), fill=accent)

    # Recommendation
    draw.rounded_rectangle((45, 1675, 1035, 1840), radius=28, fill=cream)
    draw.text((80, 1710), "RECOMANDAREA ZILEI", font=font(34, True), fill=ink)
    draw_wrapped(draw, recommendation, (80, 1762), 52, font(29, True), ink, spacing=8)

    # Footer
    days_to_brasov = max(0, (BRASOV_START - today).days)
    draw.text((55, 1865), f"Localizare: {location(today)} • Zile până la Brașov: {days_to_brasov}", font=font(25, True), fill=accent)
    draw.text((55, 1898), "Raport generat automat. Orice asemănare cu realitatea este intenționată.", font=font(21), fill=muted)

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=96)
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
