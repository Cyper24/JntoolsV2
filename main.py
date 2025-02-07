import streamlit as st

st.set_page_config(layout="wide",
                   initial_sidebar_state="auto",)
with st.sidebar:
        ato = st.text_input("Input AuthToken","",key="ato")

pages = {
    "Dashboard": [
        st.Page("dashboard.py", title="Dashboard", icon=":material/home:"),
    ],
    "Tools": [
        st.Page("allnew.py", title="Pencarian Status Terupdate",icon=":material/menu:"),
        st.Page("tidaksampai.py", title="Monitor Paket Tidak Sampai",icon=":material/menu:"),
        st.Page("loadunload.py", title="Load Unload Kode Tugas",icon=":material/menu:"),
        st.Page("reportinc.py", title="Report Harian Inc",icon=":material/menu:"),
        st.Page("reportout.py", title="Report Harian Out",icon=":material/menu:"),
    ],
}
if st.session_state.ato:
    pg = st.navigation(pages)
    pg.run()