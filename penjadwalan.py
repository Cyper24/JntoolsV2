import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from streamlit_date_picker import date_range_picker, date_picker, PickerType

at=(st.session_state.ato).strip(" ")
st.title("Cek Load Penjadwalan KT")

default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0), datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=1)
col1, col2,col3 = st.columns([3, 1, 2])
with col1:
    date_range_string = date_range_picker(picker_type=PickerType.time,
                                            start=default_start, end=default_end,
                                            key='time_range_picker')
    if date_range_string:
            start, end = date_range_string
    else:
        start = " "
        end = " "


def isi(kt):
    valuelo = 0
    url = "https://jmsgw.jntexpress.id/transportation/trackingDeatil/loading/scan/list"
    querystring = {"shipmentNo":f"{kt}"}
    payload = ""
    headers = {
        "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
        "authtoken": f"{at}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    rjson=response.json()
    for x in rjson["data"]:
        if x["scanNetworkCode"] == "SOC999" and x["loadingTypeName"] == "1":
            valuelo = x["scanWaybillNum"]
            valuelo = int(valuelo)
    return valuelo

@st.cache_data
def dframe():
    st.caption("Result :")
    df = pd.DataFrame(list)
    st.dataframe(df)
    st.caption(f"{len(df.index)}" + " Data")

url = "https://jmsgw.jntexpress.id/transportation/tmsShipment/page"
querystring = {"current":"1","size":"100","tmsType":"1","startDateTime":f"{start}","endDateTime":f"{end}","searchType":"schedule"}
headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "Content-Type": "application/json",
    "authtoken": at,
    "lang": "ID"
}
list=[]
if st.button("Cari"):
    st.cache_data.clear()
    response = requests.request("GET", url, headers=headers, params=querystring)
    rjson = response.json()
    for x in rjson["data"]["records"]:
        if x["shipmentState"] != 0:
            shipmentNo=x["shipmentNo"]
            shipmentName=x["shipmentName"]
            plateNumber=x["plateNumber"]
            plannedDepartureTime=x["plannedDepartureTime"]
            driverName=x["driverName"]
            valuelo=isi(shipmentNo)
            final = {"Kode Tugas":shipmentNo,"Nama Tugas":shipmentName,'Jadwal_Keberangkatan_Mobil' : plannedDepartureTime,"Nama Driver":driverName,"Plat Mobil":plateNumber,"Jumlah_Load":valuelo}
            list.append(final)
dframe()