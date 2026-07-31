from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

from sata.mission import get_mission_status
from sata.ui import apply_base_styles

apply_base_styles()

today = datetime.now(ZoneInfo("Europe/Bucharest")).date()
status = get_mission_status(today)
fear = min(100, max(0, status.tension + 7))
credibility = max(1, 100 - fear - 5)
denial = min(100, fear + 9)
phone_checks = max(3, round(fear / 4))

st.markdown(
    """
    <div class="win95">
      <div class="win95-title">FRICOMETRU.EXE — Version 2.3 Beta</div>
      <div class="win95-panel">
        <b>ATENȚIE</b><br><br>
        Acest instrument nu a fost validat științific.<br>
        Rezultatele nu trebuie folosite pentru decizii importante.<br><br>
        Totuși... par surprinzător de exacte.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
with st.status("Inițializare senzori experimentali...", expanded=True, state="complete"):
    st.write("✓ Telefon localizat")
    st.write("✓ Cafea detectată cu probabilitate rezonabilă")
    st.write("✓ Emoții găsite")
    st.write("✓ Protocol de negare activ")

st.markdown(
    f"""
    <div class="card" style="text-align:center;border:3px solid #333;">
      <div class="label">Nivel de frică neomologat</div>
      <div class="big-number" style="font-family:monospace;color:#c0392b;margin:18px 0;">{fear}%</div>
      <div style="height:34px;background:#d6d6d6;border:2px inset #888;overflow:hidden;">
        <div style="height:100%;width:{fear}%;background:repeating-linear-gradient(45deg,#c0392b,#c0392b 12px,#e45b52 12px,#e45b52 24px);"></div>
      </div>
      <p style="margin-top:16px;font-family:monospace;">Clasificare: {'PANICĂ ADMINISTRABILĂ' if fear < 80 else 'NEGARE CU INDICATORII APRINȘI'}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Credibilitate: «Nu sunt stresată»", f"{credibility}%")
with c2:
    st.metric("Nivel de negare", f"{denial}%")
with c3:
    st.metric("Verificări telefon estimate", f"{phone_checks}/oră")

st.markdown(
    """
    <div class="card">
      <div class="label">Concluzia instrumentului</div>
      <div class="value">Subiectul declară calm. Senzorii declară că subiectul declară calm.</div>
      <div class="muted" style="margin-top:10px;">Diferența dintre cele două afirmații este responsabilitatea departamentului juridic.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<a class="open-tool" href="/laborator" target="_self">← Înapoi la Laborator</a>',
    unsafe_allow_html=True,
)
st.caption("FRICOMETRU.EXE este un instrument experimental. Precizia afișată a fost aleasă pentru efect dramatic.")
