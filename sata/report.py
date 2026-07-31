
from __future__ import annotations
from datetime import date
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from .mission import get_mission_status, get_daily_story, DISTANCE_KM
from .content import daily_analysis, daily_recommendation, probability_phrase, WHAT_SYSTEM_KNOWS, WHAT_SYSTEM_DOES_NOT_KNOW

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        str(Path(ImageFont.__file__).resolve().parent / "fonts" / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")),
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def _wrap(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = word if not line else f"{line} {word}"
        if draw.textbbox((0,0), test, font=font)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def _box(draw, xy, title, body_lines, accent="#263238"):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=20, fill="#ffffff", outline="#d7dde2", width=3)
    draw.rectangle((x1, y1, x1+14, y2), fill=accent)
    draw.text((x1+34, y1+24), title.upper(), font=_font(30, True), fill="#1d252c")
    y = y1 + 76
    for line, style in body_lines:
        f = _font(25 if style == "normal" else 30, style == "bold")
        fill = "#263238" if style != "muted" else "#657786"
        for wrapped in _wrap(draw, line, f, x2-x1-72):
            draw.text((x1+34, y), wrapped, font=f, fill=fill)
            y += 38
        y += 8

def create_report(today: date, declassified: bool = False) -> bytes:
    status = get_mission_status(today)
    analysis_title, analysis_value, analysis_note = daily_analysis(today)
    rec_type, recommendation = daily_recommendation(today)
    phrase, probability, phrase_note = probability_phrase(today)

    width, height = 1400, 2000
    img = Image.new("RGB", (width, height), "#eef1f4")
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle((0, 0, width, 250), fill="#17212b")
    draw.text((70, 50), "S.A.T.A.", font=_font(72, True), fill="white")
    draw.text((72, 135), "Sistem Automat pentru Tensiunea Alexandrei", font=_font(28), fill="#d7e1ea")
    report_no = f"SATA-{today.strftime('%Y%m%d')}-001"
    draw.text((72, 190), f"RAPORT {report_no}", font=_font(22, True), fill="#9fb3c4")

    stamp_path = ASSETS / "top_secret.png"
    if stamp_path.exists():
        stamp = Image.open(stamp_path).convert("RGBA")
        stamp.thumbnail((260, 140))
        img.paste(stamp, (1060, 55), stamp)

    if declassified:
        draw.rounded_rectangle((70, 320, 1330, 1780), radius=30, fill="#ffffff", outline="#cbd3d9", width=4)
        draw.text((130, 390), "DECLASIFICAT", font=_font(58, True), fill="#a22522")
        text = (
            "Concluzia sistemului\n\n"
            "Lui Răzvan îi este foarte dor de Alexandra.\n\n"
            "Cea mai mare provocare nu este întâlnirea, ci distanța care a existat între ei până acum.\n\n"
            "Operațiunea din august nu are ca obiectiv să demonstreze ceva și nu conține obligații ascunse.\n\n"
            "Obiectivul este simplu: să petreacă timp împreună, să se cunoască mai bine și să lase lucrurile să evolueze firesc.\n\n"
            "Restul sunt grafice, protocoale și panică inventate de S.A.T.A."
        )
        y = 500
        for paragraph in text.split("\n\n"):
            for line in _wrap(draw, paragraph, _font(34, paragraph == "Concluzia sistemului"), 1080):
                draw.text((130, y), line, font=_font(34, paragraph == "Concluzia sistemului"), fill="#263238")
                y += 52
            y += 28
        draw.text((130, 1660), "Nu există niciun cronometru.", font=_font(38, True), fill="#2f6fb2")
    else:
        # Status strip
        draw.rounded_rectangle((70, 290, 1330, 430), radius=20, fill="#ffffff", outline="#d7dde2", width=3)
        draw.rectangle((70, 290, 90, 430), fill=status.color)
        draw.text((115, 315), status.phase.upper(), font=_font(31, True), fill="#1d252c")
        draw.text((115, 365), f"{status.status}  •  {status.countdown}", font=_font(24), fill="#54616b")

        # Tension
        draw.rounded_rectangle((70, 470, 1330, 650), radius=20, fill="#ffffff", outline="#d7dde2", width=3)
        draw.text((110, 505), "NIVEL DE TENSIUNE", font=_font(30, True), fill="#1d252c")
        draw.text((1060, 495), f"{status.tension}%", font=_font(62, True), fill=status.color)
        draw.rounded_rectangle((110, 580, 1250, 615), radius=16, fill="#dfe5e9")
        bar_w = int(1140 * status.tension / 100)
        draw.rounded_rectangle((110, 580, 110+bar_w, 615), radius=16, fill=status.color)

        _box(draw, (70, 690, 670, 1000), "Analiza sistemului", [
            (analysis_title, "muted"),
            (analysis_value, "bold"),
            (analysis_note, "normal"),
        ], status.color)

        _box(draw, (730, 690, 1330, 1000), "Probabilitate declarație", [
            (phrase, "bold"),
            (f"{probability}%", "bold"),
            (phrase_note, "normal"),
        ], "#7b61a8")

        knows = [(f"• {k}: {v}", "normal") for k, v in WHAT_SYSTEM_KNOWS]
        _box(draw, (70, 1040, 670, 1430), "Ce știe S.A.T.A.", knows, "#2f6fb2")

        doesnt = [(f"• {x}", "normal") for x in WHAT_SYSTEM_DOES_NOT_KNOW[:4]]
        doesnt.append(("Din fericire, nu toate lucrurile merită prezise.", "bold"))
        _box(draw, (730, 1040, 1330, 1430), "Ce nu știe S.A.T.A.", doesnt, "#657786")

        _box(draw, (70, 1470, 1330, 1700), "Recomandarea sistemului", [
            (f"Tip mesaj: {rec_type}", "muted"),
            (recommendation, "bold"),
        ], "#c88a00" if rec_type == "comic" else "#2f6fb2")

        draw.text((90, 1745), "REZUMATUL MISIUNII", font=_font(27, True), fill="#1d252c")
        y = 1795
        for line in _wrap(draw, get_daily_story(today), _font(26), 1200):
            draw.text((90, y), line, font=_font(26), fill="#36454f")
            y += 39

    draw.text(
        (70, 1940),
        "Raport generat automat de S.A.T.A. Cu o marjă de eroare imposibil de estimat.",
        font=_font(19),
        fill="#657786",
    )
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=94)
    return buffer.getvalue()
