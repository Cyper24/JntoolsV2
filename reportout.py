import streamlit as st
from datetime import datetime, timedelta
from streamlit_date_picker import date_range_picker, date_picker, PickerType
import requests
import pandas as pd

at=(st.session_state.ato).strip(" ")
st.title("Report Harian Outgoing")
default_start, default_end = datetime.now().replace(hour=0, minute=0, second=0)- timedelta(days=3), datetime.now().replace(hour=23, minute=59, second=59)- timedelta(days=3)
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

list = []
url = "https://jmsgw.jntexpress.id/transportation/tmsShipment/page"
url2 = "https://jmsgw.jntexpress.id/transportation/trackingDeatil/loading/scan/list"



payload = ""
headers = {
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "authtoken": f"{at}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
}
if st.button("Cari"):
    querystring = {"current":"1","size":"100","shipmentState":"4","startCode":"SOC999","startDateTime":f"{start}","endDateTime":f"{end}","searchType":"manage"}
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    rjson=response.json()
    for x in rjson["data"]["records"]:
        unload = []
        shipmentNo = x["shipmentNo"]
        querystring2 = {"shipmentNo":f"{shipmentNo}"}
        response2 = requests.request("GET", url2, headers=headers, params=querystring2)
        rjson2=response2.json()
        for lo in rjson2["data"]:
                    if lo["scanNetworkCode"] == "SOC999" and lo["loadingTypeName"] == "1":
                        valuelo = lo["scanWaybillNum"]
                        valuelo = int(valuelo)
                    else:
                            value = 0
        for unl in rjson2["data"]:
                    if unl["loadingTypeName"] == "2":
                            valueunl = unl["scanWaybillNum"]
                            valueunl = int(valueunl)
                            unload.append(valueunl)
                    else:
                            value = 0
        un = sum(unload)
        shipmentName = x["shipmentName"]
        vehicleTypegroup =x["vehicleTypegroup"]
        carrierName=x["carrierName"]
        ket = "Mobil Balikan"
        carrierCheckoutAgentName=x["carrierCheckoutAgentName"]
        if carrierCheckoutAgentName == "AGENT18":
            ket = "Mobil SOC999"
        plannedDepartureTime=x["plannedDepartureTime"]
        actualDepartureTime=x["actualDepartureTime"]
        plannedArrivalTime=x["plannedArrivalTime"]
        actualArrivalTime=x["actualArrivalTime"]
        final = {"No Waybill":shipmentNo,"Rute":shipmentName,"Load":valuelo,"Unload":un,"Jenis Kendaraan" :vehicleTypegroup,"Vendor":carrierName,"Keterangan" :ket,
                    "Perencanaan Waktu Keberangkatan":plannedDepartureTime,"Keberangkatan Aktual Mobil":actualDepartureTime,
                    "Rencanakan Waktu Kedatangan":plannedArrivalTime,"Waktu aktual kedatangan Mobil":actualArrivalTime}
        list.append(final)

    st.caption("Result :")
    df = pd.DataFrame(list)
    st.dataframe(df,hide_index=True)
    st.caption(f"{len(df.index)}" + " Data")