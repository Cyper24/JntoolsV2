import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from streamlit_date_picker import date_range_picker, date_picker, PickerType
from stqdm import stqdm
import time

at=(st.session_state.ato).strip(" ")
st.title("Monitor Paket Tidak Sampai")
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

if st.button("Cari"):
    
    url = "https://jmsgw.jntexpress.id/businessindicator/bigdataReport/detail/bus_allocateinoutportmonitor_detailsend"
    list2= []
    payload = {
        "current": 1,
        "size": 10000,
        "agents": ["6660011"],
        "distributeCodes": ["SOC999"],
        "dimension": "center",
        "startTime": start,
        "endTime": end,
        "ifarr": 0,
        "isJump": 1,
        "countryId": "1"
    }
    headers = {
        "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
        "authtoken": at,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "Content-Type": "application/json",
        "lang": "ID",
        "langtype": "ID"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    rjson = response.json()
    l = int(len(rjson["data"]["records"]))
    s = rjson["data"]["total"]
    f = rjson["data"]["records"][0:l]
    pbar = stqdm(total=s)
    for gw in f:
        billCode = gw["billcode"]
        # urltrack = "https://jmsgw.jntexpress.id/operatingplatform/podTracking/inner/query/keywordList"
        # payloadtrack = {
        #     "keywordList": [f"{billCode}"],
        #     "trackingTypeEnum": "WAYBILL",
        #     "countryId": "1"}
        
        # response2 = requests.request("POST", urltrack, json=payloadtrack, headers=headers)
        # rjson2 = response2.json()
        # sk = rjson2["data"][0]["details"]
        list = []
        xyz = "N"
        # for x in range(0, len(sk)):
        #     y = sk[x]["waybillTrackingContent"]
        #     if "Dikirim ke【SOC_GATEWAY】" in y:
        #             xyz = "Y"
        pickNetworkName = gw["pickNetworkName"]
        destinationName = gw["destinationName"]
        sendScanTime = gw["sendScanTime"]
        nextStationName = gw["nextStationName"]
        scanuser = gw["scanuser"]
        expressTypeName = gw["expressTypeName"]
        final = {"No Waybill":billCode,"Drop Point":pickNetworkName,"Tujuan" :destinationName,"Waktu Kirim":sendScanTime,
                "Lokasi Selanjutnya":nextStationName,"Discan Oleh":scanuser,"Layanan":expressTypeName}
        list2.append(final)
        # time.sleep(0.1)
        pbar.update(1)
    st.caption("Result :")
    df = pd.DataFrame(list2)
    st.dataframe(df,hide_index=True)
    st.caption(f"{len(df.index)}" + " Data")
