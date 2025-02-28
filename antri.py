import requests
import streamlit as st 
from datetime import datetime, timedelta
import pandas as pd

default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0)- timedelta(days=1), datetime.now().replace(hour=23, minute=59, second=59)
default_start = default_start.strftime('%Y-%m-%d %H:%M:%S')
default_end =  default_end.strftime('%Y-%m-%d %H:%M:%S')


at=(st.session_state.ato).strip(" ")
st.title("Cek Antrian")

list = []
url = "https://jmsgw.jntexpress.id/transportation/tmsShipmentEvent/report"
querystring = {"current":"1",
               "size":"100"
               ,"shipmentState":"4"
               ,"tmsType":"1",
               "arriveNetworkCode":"SOC999"
               ,"timeType":"1",
               "startTime":default_start,
               "endTime": default_end 
               }
headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "Content-Type": "application/json",
    "authtoken": at,
    "lang": "ID"
}

response = requests.request("GET", url, headers=headers, params=querystring)
rjson = response.json()
for x in rjson["data"]["records"]:
    if x["endHandlingType"] != "1" and x["unLoadingScanStartTime"] == None:
        shipmentName = x["shipmentName"]
        shipmentNo = x["shipmentNo"]
        appTrackArrivalTime = x["appTrackArrivalTime"]
        plateNumber = x["plateNumber"]
        vehicletypeName = x["vehicletypeName"]
        scanPackageNum= x["scanPackageNum"]
        scanWaybillNum=x["scanWaybillNum"]
        final = {"Kode Tugas":shipmentNo,"Nama Rute":shipmentName,"Plat":plateNumber,"Tipe Mobil":vehicletypeName,"Sampai APP Driver":appTrackArrivalTime,"Isi":scanWaybillNum,"Bagging":scanPackageNum}
        list.append(final)

st.caption("Result :")
df = pd.DataFrame(list)
st.dataframe(df,hide_index=True)
st.caption(f"{len(df.index)}" + " Data")