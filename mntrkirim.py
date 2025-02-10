import streamlit as st 
from datetime import datetime, timedelta
from streamlit_date_picker import date_range_picker, date_picker, PickerType
import requests
import pandas as pd
from dtlkirim import dc,dp

at=(st.session_state.ato).strip(" ")

st.title("Monitor Kirim Outgoing")
default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0), datetime.now().replace(hour=23, minute=59, second=59)
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


url = "https://jmsgw.jntexpress.id/businessindicator/bigdataReport/detail/arrival_monitor_total_doris"


payload = {
    "current": 1,
    "size": 100,
    "dimension": 2,
    "startDates": f"{start}",
    "endDates": f"{end}",
    "previousSiteLevel": "DC",
    "siteLevel": "GW",
    "previousSiteType": 1,
    "countryId": "1"
}

payload2 = {
    "current": 1,
    "size": 100,
    "dimension": 2,
    "startDates": f"{start}",
    "endDates": f"{end}",
    "previousSiteLevel": "DP",
    "siteLevel": "GW",
    "previousSiteType": 1,
    "countryId": "1"
}


headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "authtoken": f"{at}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "Content-Type": "application/json"}

list = []
list2 = []

tab1, tab2= st.tabs(["DC", "DP"])
    
response = requests.request("POST", url, json=payload, headers=headers)
rjson = response.json()
for x in rjson["data"]["records"]:
        previousSiteCode=x["previousSiteCode"]
        arriveDate=x["arriveDate"]
        notArriveCnt=x["notArriveCnt"]
        previousNoSendCnt=x["previousNoSendCnt"]
        final = {"Tanggal":arriveDate,"Lokasi Sebelum":previousSiteCode,"Belum Sampai":notArriveCnt,"Tidak Kirim":previousNoSendCnt}
        list.append(final)

response2 = requests.request("POST", url, json=payload2, headers=headers)
rjson2 = response2.json()
for y in rjson2["data"]["records"]:
        previousSiteCode=y["previousSiteCode"]
        arriveDate=y["arriveDate"]
        notArriveCnt=y["notArriveCnt"]
        previousNoSendCnt=y["previousNoSendCnt"]
        final2 = {"Tanggal":arriveDate,"Lokasi Sebelum":previousSiteCode,"Belum Sampai":notArriveCnt,"Tidak Kirim":previousNoSendCnt}
        list2.append(final2)

with tab1:
        st.caption("Result :")
        df = pd.DataFrame(list)
        st.dataframe(df,hide_index=True)
        st.caption(f"{len(df.index)}" + " Data")
        dc(start,end,headers,df)
with tab2:
        st.caption("Result :")
        df = pd.DataFrame(list2)
        st.dataframe(df,hide_index=True)
        st.caption(f"{len(df.index)}" + " Data")
        dp(start,end,headers,df)

