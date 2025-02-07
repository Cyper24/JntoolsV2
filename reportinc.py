import streamlit as st
from datetime import datetime, timedelta
from streamlit_date_picker import date_range_picker, date_picker, PickerType
import requests
import pandas as pd

st.title("Report Harian Inc")

at=(st.session_state.ato).strip(" ")
default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0)- timedelta(days=2), datetime.now().replace(hour=23, minute=59, second=59)- timedelta(days=2)
col1, col2 = st.columns([3, 1])
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
    list = []
    url = "https://jmsgw.jntexpress.id/transportation/tmsBranchTrackingDetail/page"
    payload = {
        "current": 1,
        "size": 100,
        "startDepartureTime": f"{start}",
        "endDepartureTime": f"{end}",
        "startCode": "SOC999",
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
    r=response.json()
    f = r["data"]["records"]
    for x in f:
        shipmentNo = x["shipmentNo"]
        lineName = x["lineName"]
        loadCount = x["loadCount"]
        actualVehicleTypegroup = x["actualVehicleTypegroup"]
        carrierName = x["carrierName"]
        plannedDepartureTime = x["plannedDepartureTime"]
        actualDepartureTime = x["actualDepartureTime"]
        plannedArrivalTime = x["plannedArrivalTime"]
        actualArrivalTime = x["actualArrivalTime"]
        shifts = x["shifts"]
        final = {'kode Tugas' : shipmentNo,'Rute' : lineName,'Load' : loadCount,'Tipe Armada' : actualVehicleTypegroup,'Vendor' : carrierName,
                 'Perencanaan Waktu Keberangkatan (CUT OFF)' : plannedDepartureTime,'Keberangkatan Aktual Mobil' : actualDepartureTime,'Rencanakan Waktu Kedatangan' : plannedArrivalTime,
                 'Waktu aktual kedatangan Mobil' : actualArrivalTime,'Rit' : shifts}
        list.append(final)
    st.caption("Result :")
    df = pd.DataFrame(list)
    st.dataframe(df,hide_index=True)
    st.caption(f"{len(df.index)}" + " Data")