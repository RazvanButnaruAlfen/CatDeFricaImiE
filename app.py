from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="S.A.T.A. 4.1",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

report_page = st.Page(
    "views/report_page.py",
    title="Raport oficial",
    icon="📄",
    default=True,
)
laboratory_page = st.Page(
    "views/laboratory_page.py",
    title="Laborator S.A.T.A.",
    icon="🧪",
    url_path="laborator",
)
fricometru_page = st.Page(
    "views/fricometru_page.py",
    title="Fricometru.exe",
    icon="📈",
    url_path="fricometru",
)

page = st.navigation(
    [report_page, laboratory_page, fricometru_page],
    position="hidden",
)
page.run()
