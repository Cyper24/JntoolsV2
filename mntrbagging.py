import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import requests
import random

at=(st.session_state.ato).strip(" ")
st.title("Monitor Bagging")

headers = {
        "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
        "authtoken": at,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "langtype": "ID",
        "Content-Type": "application/json;charset=UTF-8"
    }
default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0)- timedelta(days=2), datetime.now().replace(hour=23, minute=59, second=59)
default_start = default_start.strftime('%Y-%m-%d %H:%M:%S')
default_end =  default_end.strftime('%Y-%m-%d %H:%M:%S')

def allnew(billcd):
    fin = []
    url = "https://jmsgw.jntexpress.id/operatingplatform/waybill/pageQueryLastStatus"
    payload = {
        "current": 1,
        "size": 200,
        "type": 1,
        "inputStartTime": default_start,
        "inputEndTime": default_end,
        "codeType": 0,
        "billCodes": billcd,
        "scanFinanceCode": [],
        "scanSiteCode": [],
        "countryId": "1"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    rjson = response.json()
    for x in rjson["data"]["records"]:
        awb = x["waybillNo"]
        nineCharCode = x["nineCharCode"]
        final = {"No Bagging":awb,"NLC":nineCharCode}
        fin.append(final)
    df = pd.DataFrame(fin)
    st.dataframe(df,hide_index=True)
    st.caption(f"{len(df.index)}" + " Data")

def cariawb(pyload):
    lis = []
    url = "https://jmsgw.jntexpress.id/businessindicator/bigdataReport/detail/opt_pack_unpacking_bag_monitor_dl"
    payload = {
        "packageCodeList": [f"{pyload}"],
        "current": 1,
        "size": 200,
        "exportType": 3,
        "countryId": "1"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    rjson = response.json()
    for x in rjson["data"]["records"]:
        billCode = x["billCode"]
        lis.append(billCode)
    allnew(lis)
    
txt = st.text_area("Input No Bagging",)
lines = txt.split("\n")
awblist =[]

if st.button("Cari"):
    col1, col2, col3 = st.columns(3)
    st.cache_data.clear()
    for awb in lines:
            st.subheader(awb)
            cariawb(awb)
