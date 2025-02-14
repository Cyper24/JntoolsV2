import streamlit as st
import requests
import pandas as pd

at=(st.session_state.ato).strip(" ")
st.title("Cek Load KT")

kt = st.text_input("Input Kode Tugas","")

headers = {
        "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
        "authtoken": at,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "langtype": "ID",
        "Content-Type": "application/json;charset=UTF-8"
    }

list = []

def tgl():
    url = "https://jmsgw.jntexpress.id/transportation/tmsShipment/traceDetail"
    querystring = {"shipmentNo":kt}
    response = requests.request("GET", url, headers=headers, params=querystring)
    rjson = response.json()
    start = rjson["data"]["shipmentDetail"]["tmsShipmentStopVOList"][0]["loadStartTime"]
    end = rjson["data"]["shipmentDetail"]["tmsShipmentStopVOList"][0]["loadEndTime"]
    return start,end

def jmlahkt():
    url = "https://jmsgw.jntexpress.id/operatingplatform/scanRecordQuery/listPage"
    start,end = tgl()
    payload = {
        "current": 1,
        "size": 30000,
        "billType": 4,
        "startDates": start,
        "endDates": end,
        "scanType": "装车扫描",
        "sortName": "scanDate",
        "sortOrder": "asc",
        "bilNos": [f"{kt}"],
        "querySub": "",
        "isAllPod": "",
        "reachAddressList": [],
        "scanSite": ["SOC999"],
        "sendSites": [],
        "destinationFinancialId": [],
        "pickFinanceId": [],
        "countryId": "1"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    rjson = response.json()
    for x in rjson["data"]["records"]:
        upOrNextStation=x["upOrNextStation"]
        billNo=x["billNo"]
        final = {'Lokasi_Selanjutnya' : upOrNextStation,"No_Waybill":billNo}
        list.append(final)

if st.button("Exec..."):
    jmlahkt()
    st.caption("Result :")
    df = pd.DataFrame(list)
    table = pd.pivot_table(df, values='No_Waybill', index=['Lokasi_Selanjutnya'],columns=['Lokasi_Selanjutnya'], aggfunc="count", fill_value=" ")
    st.dataframe(table,hide_index=True)
    st.text("Total Load : " + f"{len(df.index)}" + " Data")

