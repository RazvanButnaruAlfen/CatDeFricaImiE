from __future__ import annotations

import streamlit as st


def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] { display: none; }
        .stApp { background: #eef1f4; }
        .block-container { max-width: 1180px; padding-top: 1.25rem; padding-bottom: 3rem; }
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
        .declassified {
          background:white; border:2px solid #cfd6dc; border-radius:22px; padding:42px;
          text-align:center; box-shadow:0 8px 28px rgba(0,0,0,.08);
        }
        .top-nav {
          display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:0 0 16px 0;
        }
        .top-nav a, .open-tool {
          display:inline-block; text-decoration:none !important; padding:10px 15px;
          border-radius:10px; border:1px solid #cbd3d9; background:#ffffff;
          color:#25323c !important; font-weight:750; box-shadow:0 2px 7px rgba(0,0,0,.04);
        }
        .top-nav a:hover, .open-tool:hover { border-color:#738493; background:#f8fafb; }
        .tool-card {
          background:#111820; color:#e7eef4; border:1px solid #384854; border-radius:14px;
          padding:22px; margin-bottom:15px; box-shadow:inset 0 0 25px rgba(0,0,0,.20);
        }
        .tool-status { font-family:monospace; letter-spacing:.05em; }
        .status-green { color:#55db8a; }
        .status-yellow { color:#ffd166; }
        .status-red { color:#ff6b6b; }
        .win95 {
          background:#c0c0c0; border-top:3px solid white; border-left:3px solid white;
          border-right:3px solid #333; border-bottom:3px solid #333; padding:4px;
          font-family:monospace; color:#111;
        }
        .win95-title {
          background:#000080; color:white; padding:8px 10px; font-weight:bold; font-size:1.05rem;
        }
        .win95-panel {
          border-top:2px solid #555; border-left:2px solid #555;
          border-right:2px solid white; border-bottom:2px solid white;
          margin:14px; padding:22px; background:#d4d0c8;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(section: str, subtitle: str | None = None) -> None:
    extra = f"<p style='margin-top:14px;'><b>Modul:</b> {section}</p>"
    if subtitle:
        extra += f"<p>{subtitle}</p>"
    st.markdown(
        f"""
        <div class="hero">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;">
            <div>
              <h1>S.A.T.A.</h1>
              <p>Sistem Automat pentru Tensiunea Alexandrei</p>
              {extra}
            </div>
            <div class="secret">TOP SECRET</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_navigation() -> None:
    st.markdown(
        """
        <div class="top-nav">
          <a href="/" target="_self">📄 Raport oficial</a>
          <a href="/laborator" target="_self">🧪 Laborator</a>
          <a href="/fricometru" target="_blank">📈 Fricometru ↗</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_new_tab_link(path: str, label: str) -> None:
    st.markdown(
        f'<a class="open-tool" href="{path}" target="_blank" rel="noopener noreferrer">{label}</a>',
        unsafe_allow_html=True,
    )
