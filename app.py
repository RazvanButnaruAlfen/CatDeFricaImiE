
from __future__ import annotations

from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo
import base64

import streamlit as st

from sata.mission import (
    ARRIVAL_ROMANIA, ARRIVAL_PLOIESTI, BRASOV_START, BRASOV_END, RETURN_NL,
    get_mission_status, get_daily_story
)
from sata.content import (
    daily_analysis, daily_recommendation, probability_phrase,
    WHAT_SYSTEM_KNOWS, WHAT_SYSTEM_DOES_NOT_KNOW
)
from sata.report import create_report

st.set_page_config(
    page_title="S.A.T.A. 4.0",
    page_icon="📡",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
SOUNDS = BASE_DIR / "sounds"

st.markdown("""
<style>
.stApp { background: #eef1f4; }
.block-container { max-width: 1180px; padding-top: 1.4rem; }
.hero {
  background: linear-gradient(135deg,#14212c,#243746);
  color:white; padding:28px 34px; border-radius:20px; margin-bottom:18px;
  box-shadow:0 8px 24px rgba(0,0,0,.15);
}
.hero h1 { margin:0; font-size:3rem; letter-spacing:.08em; }
.hero p { margin:.35rem 0 0; color:#cfdae3; }
.card {
  background:white; border:1px solid #d8dee4; border-radius:16px;
  padding:22px; margin-bottom:16px; box-shadow:0 3px 12px rgba(0,0,0,.05);
}
.label { font-size:.78rem; color:#657786; text-transform:uppercase; letter-spacing:.12em; font-weight:700; }
.value { font-size:1.45rem; font-weight:800; color:#1d252c; margin-top:.3rem; }
.big-number { font-size:4.5rem; line-height:1; font-weight:900; }
.muted { color:#657786; }
.secret {
  display:inline-block; border:3px solid #d63832; color:#d63832; font-weight:900;
  padding:7px 13px; transform:rotate(-5deg); letter-spacing:.12em;
}
.timeline { display:flex; justify-content:space-between; gap:8px; margin-top:10px; }
.timeline div { flex:1; text-align:center; font-size:.85rem; }
.timeline .dot { width:15px; height:15px; border-radius:50%; background:#9aa8b3; margin:0 auto 6px; }
.timeline .active .dot { background:#c0392b; box-shadow:0 0 0 6px rgba(192,57,43,.14); }
.declassified {
  background:white; border:2px solid #cfd6dc; border-radius:22px; padding:42px;
  text-align:center; box-shadow:0 8px 28px rgba(0,0,0,.08);
}
</style>
""", unsafe_allow_html=True)

def local_today() -> date:
    from datetime import datetime
    return datetime.now(ZoneInfo("Europe/Bucharest")).date()

def play_alarm(level: int):
    filename = None
    if level >= 100:
        filename = "siren100.wav"
    elif level >= 80:
        filename = "beep80.wav"
    elif level > 50:
        filename = "beep50.wav"
    if not filename:
        return
    path = SOUNDS / filename
    if path.exists():
        audio = base64.b64encode(path.read_bytes()).decode()
        st.markdown(
            f'<audio autoplay loop><source src="data:audio/wav;base64,{audio}" type="audio/wav"></audio>',
            unsafe_allow_html=True,
        )

with st.sidebar:
    st.header("Control S.A.T.A.")
    testing = st.toggle("Mod testare dată", value=False)
    today = st.date_input("Data simulată", value=local_today()) if testing else local_today()
    sound_on = st.toggle("Alarmă sonoră", value=False)
    st.caption("În modul normal, aplicația folosește automat data din România.")

status = get_mission_status(today)
analysis_title, analysis_value, analysis_note = daily_analysis(today)
rec_type, recommendation = daily_recommendation(today)
phrase, probability, phrase_note = probability_phrase(today)

st.markdown(f"""
<div class="hero">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;">
    <div>
      <h1>S.A.T.A.</h1>
      <p>Sistem Automat pentru Tensiunea Alexandrei</p>
      <p style="margin-top:14px;"><b>Raport:</b> SATA-{today.strftime('%Y%m%d')}-001</p>
    </div>
    <div class="secret">TOP SECRET</div>
  </div>
</div>
""", unsafe_allow_html=True)

if sound_on:
    play_alarm(status.tension)

if st.session_state.get("declassified", False):
    st.markdown("""
    <div class="declassified">
      <div class="secret" style="transform:none;margin-bottom:24px;">DECLASIFICAT</div>
      <h2>Concluzia sistemului</h2>
      <p style="font-size:1.35rem;line-height:1.65;">
      Lui Răzvan îi este foarte dor de Alexandra.<br><br>
      Cea mai mare provocare nu este întâlnirea, ci distanța care a existat între ei până acum.<br><br>
      Operațiunea din august nu are ca obiectiv să demonstreze ceva și nu conține obligații ascunse.<br><br>
      Obiectivul este să petreacă timp împreună, să se cunoască mai bine și să lase lucrurile să evolueze firesc.<br><br>
      <b>Restul sunt grafice, protocoale și panică inventate de S.A.T.A.</b>
      </p>
      <h3 style="color:#2f6fb2;margin-top:30px;">Nu există niciun cronometru.</h3>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔒 Reclasifică raportul", use_container_width=True):
            st.session_state.declassified = False
            st.rerun()
    with c2:
        data = create_report(today, declassified=True)
        st.download_button(
            "⬇️ Descarcă raportul declasificat",
            data=data,
            file_name=f"SATA_declasificat_{today.isoformat()}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
    st.stop()

st.markdown(f"""
<div class="card" style="border-left:12px solid {status.color};">
  <div class="label">{status.phase}</div>
  <div class="value">{status.status}</div>
  <div class="muted" style="margin-top:8px;">{status.countdown}</div>
  <div style="margin-top:14px;"><b>Protocol activ:</b> {status.protocol}</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.15, 1])

with left:
    st.markdown(f"""
    <div class="card">
      <div class="label">Nivel de tensiune</div>
      <div class="big-number" style="color:{status.color};">{status.tension}%</div>
      <div style="height:24px;background:#dfe5e9;border-radius:12px;overflow:hidden;margin-top:18px;">
        <div style="height:100%;width:{status.tension}%;background:{status.color};"></div>
      </div>
      <div class="muted" style="margin-top:12px;">Valoare calculată cu metode pe care sistemul refuză să le explice.</div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
      <div class="label">Analiza sistemului</div>
      <div class="muted" style="margin-top:10px;">{analysis_title}</div>
      <div class="value">{analysis_value}</div>
      <div style="margin-top:14px;">{analysis_note}</div>
    </div>
    """, unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="card">
      <div class="label">Ce știe S.A.T.A.</div>
    """, unsafe_allow_html=True)
    for key, value in WHAT_SYSTEM_KNOWS:
        st.markdown(f"**✓ {key}:** {value}")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
      <div class="label">Ce nu știe S.A.T.A.</div>
    """, unsafe_allow_html=True)
    for item in WHAT_SYSTEM_DOES_NOT_KNOW:
        st.markdown(f"**✗** {item}")
    st.markdown("**Din fericire, nu toate lucrurile merită prezise.**")
    st.markdown("</div>", unsafe_allow_html=True)

p1, p2 = st.columns(2)
with p1:
    st.markdown(f"""
    <div class="card">
      <div class="label">Probabilitatea ca Alexandra să spună</div>
      <div class="value">{phrase}</div>
      <div class="big-number" style="font-size:3.2rem;color:#7b61a8;">{probability}%</div>
      <div>{phrase_note}</div>
    </div>
    """, unsafe_allow_html=True)
with p2:
    st.markdown(f"""
    <div class="card">
      <div class="label">Recomandarea sistemului • {rec_type}</div>
      <div class="value" style="font-size:1.25rem;line-height:1.45;">{recommendation}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
  <div class="label">Rezumatul misiunii</div>
  <div class="value" style="font-size:1.25rem;line-height:1.5;">{get_daily_story(today)}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
  <div class="label">Cronologia operațiunii</div>
  <div class="timeline">
    <div><div class="dot"></div>Martie<br><span class="muted">Prima conexiune</span></div>
    <div><div class="dot"></div>9 august<br><span class="muted">România</span></div>
    <div><div class="dot"></div>14 august<br><span class="muted">Ploiești</span></div>
    <div><div class="dot"></div>15–17 august<br><span class="muted">Brașov</span></div>
    <div><div class="dot"></div>27 august<br><span class="muted">Întoarcere</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    if st.button("🔓 Declasifică raportul", use_container_width=True, type="primary"):
        st.session_state.declassified = True
        st.rerun()
with b2:
    data = create_report(today)
    st.download_button(
        "⬇️ Descarcă Raportul zilei (JPG)",
        data=data,
        file_name=f"SATA_raport_{today.isoformat()}.jpg",
        mime="image/jpeg",
        use_container_width=True,
    )

st.caption("Raport generat automat de S.A.T.A. Cu o marjă de eroare imposibil de estimat.")
