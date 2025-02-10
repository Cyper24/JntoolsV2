import streamlit as st
import requests
import pandas as pd

url = "https://jmsgw.jntexpress.id/businessindicator/bigdataReport/detail/arrival_monitor_detail_doris"

def dc(start,end,headers,df):
        list2 = []
        options = df["Lokasi Sebelum"]
        selection = st.segmented_control(
            "Directions", options, selection_mode="single",
            label_visibility="hidden"
        )
        payload2 = {
            "current": 1,
            "size": 20000,
            "type": "notArriveCnt",
            "startTime": f"{start}",
            "endTime": f"{end}",
            "previousSiteCodeList": [f"{selection}"],
            "previousSiteLevel": "DC",
            "siteCodeList": ["SOC999"],
            "proxyAreaCodeList": ["6660011"],
            "dataSource": "arrival",
            "countryId": "1"
            }
        response2 = requests.request("POST", url, json=payload2, headers=headers)
        rjson2 = response2.json()
        for y in rjson2["data"]["records"]:
               billCode=y["billCode"]
               pickNetworkName=y["pickNetworkName"]
               destinationName=y["destinationName"]
               expressTypeName=y["expressTypeName"]
               sendTime=y["sendTime"]
               final2 = {"No Waybill":billCode,"Drop Point":pickNetworkName,"Tujuan":destinationName,"Layanan":expressTypeName,"Waktu Kirim":sendTime}
               list2.append(final2)
        st.caption("Result :")
        df2 = pd.DataFrame(list2)
        st.dataframe(df2,hide_index=True,use_container_width=True)
        st.caption(f"{len(df2.index)}" + " Data")

def dp(start,end,headers,df):
        list2 = []
        options = df["Lokasi Sebelum"]
        selection = st.segmented_control(
            "Directions", options, selection_mode="single",
            label_visibility="hidden"
        )
        payload2 = {
            "current": 1,
            "size": 20000,
            "type": "notArriveCnt",
            "startTime": f"{start}",
            "endTime": f"{end}",
            "previousSiteCodeList": [f"{selection}"],
            "previousSiteLevel": "DP",
            "siteCodeList": ["SOC999"],
            "proxyAreaCodeList": ["6660011"],
            "dataSource": "arrival",
            "countryId": "1"
            }
        response2 = requests.request("POST", url, json=payload2, headers=headers)
        rjson2 = response2.json()
        for y in rjson2["data"]["records"]:
               billCode=y["billCode"]
               pickNetworkName=y["pickNetworkName"]
               destinationName=y["destinationName"]
               expressTypeName=y["expressTypeName"]
               sendTime=y["sendTime"]
               final2 = {"No Waybill":billCode,"Drop Point":pickNetworkName,"Tujuan":destinationName,"Layanan":expressTypeName,"Waktu Kirim":sendTime}
               list2.append(final2)

        st.caption("Result :")
        df2 = pd.DataFrame(list2)
        st.dataframe(df2,hide_index=True,use_container_width=True)
        st.caption(f"{len(df2.index)}" + " Data")