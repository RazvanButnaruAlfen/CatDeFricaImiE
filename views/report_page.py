from __future__ import annotations

from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo
import base64

import streamlit as st

from sata.mission import get_mission_status, get_daily_story
from sata.content import (
    daily_analysis, daily_recommendation, probability_phrase,
    WHAT_SYSTEM_KNOWS, WHAT_SYSTEM_DOES_NOT_KNOW
)
from sata.report import create_report
from sata.ui import apply_base_styles, render_header, render_navigation, render_new_tab_link

BASE_DIR = Path(__file__).resolve().parent.parent
SOUNDS = BASE_DIR / "sounds"

apply_base_styles()
render_navigation()
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

render_header("Raport oficial", f"Raport SATA-{today.strftime('%Y%m%d')}-001")

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

st.markdown("""
<div class="card" style="border-left:10px solid #55db8a;">
  <div class="label">Instrument experimental disponibil</div>
  <div class="value">FRICOMETRU.EXE</div>
  <div class="muted" style="margin:8px 0 16px;">Modulul se deschide într-o fereastră nouă. Departamentul oficial S.A.T.A. nu garantează nimic, ceea ce îl face probabil foarte precis.</div>
</div>
""", unsafe_allow_html=True)
render_new_tab_link("/fricometru", "📈 Deschide Fricometrul într-o fereastră nouă ↗")

st.caption("Raport generat automat de S.A.T.A. Cu o marjă de eroare imposibil de estimat.")
