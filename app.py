import streamlit as st

st.set_page_config(
    page_title="CatDeFricaImiE",
    page_icon="😱",
    layout="centered"
)

st.title("😱 Fricometru")

st.write(
    "### Cât de frică îmi este de ce se va întâmpla când va veni Răzvan în România?"
)

frica = st.slider(
    "",
    min_value=0,
    max_value=100,
    value=50,
    step=1
)

st.markdown(f"# **{frica}%**")

if frica <= 20:
    st.success("😎 Nicio grijă.")
elif frica <= 40:
    st.info("🙂 Există o ușoară îngrijorare.")
elif frica <= 60:
    st.warning("😬 Începe să devină serios.")
elif frica <= 80:
    st.warning("😨 Nivel ridicat de panică!")
elif frica < 100:
    st.error("😱 Pericol iminent!")
else:
    st.balloons()
    st.error("💀 100% - Răzvan este deja în România!")
