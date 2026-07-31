from __future__ import annotations

import streamlit as st

from sata.ui import apply_base_styles, render_header, render_navigation, render_new_tab_link

apply_base_styles()
render_navigation()
render_header("Laborator S.A.T.A.", "Instrumente experimentale și software cu validare discutabilă")

st.markdown(
    """
    <div class="card">
      <div class="label">Avertisment de laborator</div>
      <div class="value">Rezultatele pot părea științifice fără a comite greșeala de a fi științifice.</div>
      <div class="muted" style="margin-top:10px;">Utilizați toate modulele cu simțul umorului activat.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="tool-card">
      <div class="label" style="color:#9eb1bf;">Instrument 01</div>
      <div class="value" style="color:white;font-family:monospace;">FRICOMETRU.EXE</div>
      <p>Calculează un nivel complet neomologat de frică, panică anticipativă și negare operațională.</p>
      <div class="tool-status status-green">● STATUS: OPERAȚIONAL</div>
    </div>
    """,
    unsafe_allow_html=True,
)
render_new_tab_link("/fricometru", "📈 DESCHIDE FRICOMETRU.EXE ÎN FEREASTRĂ NOUĂ ↗")

st.markdown(
    """
    <div class="tool-card">
      <div class="label" style="color:#9eb1bf;">Instrument 02</div>
      <div class="value" style="color:white;font-family:monospace;">SIMULATOR_PANICA.EXE</div>
      <p>Simulează reacții la mesaje precum „Am ajuns”, „Pornesc spre Ploiești” și „Mâine plecăm la Brașov”.</p>
      <div class="tool-status status-yellow">● STATUS: ÎN DEZVOLTARE</div>
    </div>

    <div class="tool-card">
      <div class="label" style="color:#9eb1bf;">Instrument 03</div>
      <div class="value" style="color:white;font-family:monospace;">DETECTOR_NEGARE.DLL</div>
      <p>Analizează afirmații de tipul „Nu sunt stresată” și emite un procent de credibilitate.</p>
      <div class="tool-status status-yellow">● STATUS: CALIBRARE NECESARĂ</div>
    </div>

    <div class="tool-card">
      <div class="label" style="color:#9eb1bf;">Instrument 04</div>
      <div class="value" style="color:white;font-family:monospace;">ACCES_ANALIST.SYS</div>
      <p>Modul rezervat unei faze viitoare a proiectului.</p>
      <div class="tool-status status-red">● STATUS: CLASIFICAT — PRIORITATE REDUSĂ</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Laborator S.A.T.A. — unde ipotezele primesc grafice înainte să primească dovezi.")
