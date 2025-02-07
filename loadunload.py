import streamlit as st
import requests
import pandas as pd

at=(st.session_state.ato).strip(" ")
url = "https://jmsgw.jntexpress.id/transportation/trackingDeatil/loading/scan/list"
headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "authtoken": at,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "Content-Type": "application/json",
    "lang": "ID",
    "langtype": "ID"
}

st.header("Load Unload Kode Tugas")
txt = st.text_area(
    "Input Kode Tugas :",
)
list = []
if st.button("Cari"):
    for kt in txt.split():
        unload = []
        
        querystring = {"shipmentNo":f"{kt}"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        rjson=response.json()
        for lo in rjson["data"]:
                if lo["scanNetworkCode"] == "SOC999" and lo["loadingTypeName"] == "1":
                    valuelo = lo["scanWaybillNum"]
                    valuelo = int(valuelo)
                else:
                        value = 0
        for unl in rjson["data"]:
                if unl["loadingTypeName"] == "2":
                        valueunl = unl["scanWaybillNum"]
                        valueunl = int(valueunl)
                        unload.append(valueunl)
                else:
                        value = 0

        un = sum(unload)
        final = {'Kode Tugas' : kt,'Load' : valuelo,'Unload':un}
        list.append(final)
    st.caption("Result :")
    df = pd.DataFrame(list)
    st.dataframe(df,hide_index=True)

# response = requests.request("GET", url2, headers=headers, params=querystring)

# st.text(txt.strip())

# if st.button("Cari"):

