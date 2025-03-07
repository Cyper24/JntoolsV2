import requests
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

at=(st.session_state.ato).strip(" ")
st.title("Cek Antrian Kota")

list = []
default_start, default_end = datetime.now()- timedelta(hours=12), datetime.now()
default_start = default_start.strftime('%Y-%m-%d %H:%M:%S')
default_end =  default_end.strftime('%Y-%m-%d %H:%M:%S')

url = "https://jmsgw.jntexpress.id/transportation/tmsBranchTrackingDetail/page"

payload = {
    "current": 1,
    "size": 100,
    "startDepartureTime": default_start,
    "endDepartureTime": default_end,
    "endCode": "SOC999",
    "shipmentState": 4,
    "countryId": "1"
}
headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "authtoken": at,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
    "langtype": "ID",
    "Content-Type": "application/json;charset=UTF-8"
}

response = requests.request("POST", url, json=payload, headers=headers)
rjson = response.json()
for x in rjson["data"]["records"]:
    if x["unLoadCount"] == None:
        shipmentNo=x["shipmentNo"]
        shipmentName = x["shipmentName"]
        plateNumber = x["plateNumber"]
        loadCount = x["loadCount"]
        actualArrivalTime =x["actualArrivalTime"]
        final = {"Kode Tugas":shipmentNo,"Nama Rute":shipmentName,"Plat":plateNumber,"Sampai APP Driver":actualArrivalTime,"Isi":loadCount}
        list.append(final)

st.caption("Result :")
df = pd.DataFrame(list)
st.dataframe(df,hide_index=True)
st.caption(f"{len(df.index)}" + " Data")