import streamlit as st
import requests
st.set_page_config(layout="wide",
                   initial_sidebar_state="auto",)

url = "https://jmsgw.jntexpress.id/notice/web/getBannerList"
with st.sidebar:
        ato = st.text_input("Input AuthToken","",key="ato")
at=(st.session_state.ato).strip(" ")
payload = ""
headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "authtoken": f"{at}"
}

response = requests.request("GET", url, data=payload, headers=headers)

pages = {
    "Dashboard": [
        st.Page("dashboard.py", title="Dashboard", icon=":material/home:"),
    ],
    "Tools": [
        st.Page("manifest.py", title="Manifest",icon=":material/menu:"),
        st.Page("allnew.py", title="Pencarian Status Terupdate",icon=":material/menu:"),
        st.Page("tidaksampai.py", title="Monitor Paket Tidak Sampai",icon=":material/menu:"),
        st.Page("loadunload.py", title="Load Unload Kode Tugas",icon=":material/menu:"),
        st.Page("reportinc.py", title="Report Harian Inc",icon=":material/menu:"),
        st.Page("reportout.py", title="Report Harian Out",icon=":material/menu:"),
    ],
}
if response.status_code == 200:
    pg = st.navigation(pages)
    pg.run()
else:
    st.caption("Enter Valid AuthToken")