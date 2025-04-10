import streamlit as st
from datetime import datetime, timedelta
import requests
from openpyxl import load_workbook
from win32com import client 
import os
import pythoncom
import time
from openpyxl.drawing.image import Image
import subprocess
import pandas as pd
folder = os.getcwd()

at=(st.session_state.ato).strip(" ")
st.title("Surat Jalan Kota")
txt = st.text_area("Input Id Kode Tugas",)
lines = txt.split("\n")
rekap = []
if st.button("Exec"):
    for kt in lines:
            url = "https://jmsgw.jntexpress.id/transportation/tmsnewBranchShipment/detail"
            querystring = {"id":kt}
            headers = {
                "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
                "Content-Type": "application/json",
                "authtoken": at }
            response = requests.request("GET", url, headers=headers, params=querystring)
            rjson = response.json()
            shipmentNo = rjson["data"]["shipmentNo"]
            endCode = rjson["data"]["endCode"]
            plannedDepartureTime = rjson["data"]["plannedDepartureTime"]
            shifts = rjson["data"]["shifts"]
            driverName = rjson["data"]["driverName"]
            plateNumber = rjson["data"]["plateNumber"]
            actualVehicleTypegroup = rjson["data"]["actualVehicleTypegroup"]
            driverContact = rjson["data"]["driverContact"]
            carrierName = rjson["data"]["carrierName"]
            dt = datetime.strptime(plannedDepartureTime, '%Y-%m-%d %H:%M:%S')
            dtjdl = dt.strftime('%Y%m%d')
            maintgl = dt.strftime('%d/%m/%Y')
            jamber = dt.strftime('%H:%M')
            jdl = f"SOC{endCode}0{shifts}/{dtjdl}EZ"
            djmctk = dt - timedelta(minutes=15)
            jmctk = djmctk.strftime('%H:%M')
            rekaptgl = dt.strftime('%d-%m-%Y')
            if carrierName == "PT. PILAR PRIMA NUSANTARA" or carrierName == "PT. SERASI AUTORAYA":
                carrierName = "KABUL"
            if carrierName == "PT. JET TRANSPORT SERVICES":
                carrierName = "JTS"

            if endCode == "TCSOC041" and "01" or "00:00" in jamber:
                endCode = "TCSOC041_SAMPANGAN_SOLO"
            if endCode == "TCSOC041":
                endCode = "TCSOC041_JAGALAN"
            if endCode == "TCSOC041_SAMPANGAN_SOLO" or endCode == "TCSOC041_JAGALAN":
                alamat = " Jl. Suryo No.56, Purwodiningratan, Kec. Jebres, Kota Surakarta, Jawa Tengah 57128"
            if endCode == "TCSUJ051":
                alamat = " Jl. Solo-Sukoharjo, Sawah, Sidorejo, Kec. Bendosari, Kabupaten Sukoharjo, Jawa Tengah 57527"
            if endCode == "TCKAA171":
                alamat = " Jl. Adi Sucipto No.30, Kenaiban, Blulukan, Kec. Colomadu, Kabupaten Karanganyar, Jawa Tengah 57174"
            if endCode == "TCKLT021":
                alamat = " Jl. Raya Solo - Yogyakarta No.Km, RW.30, Jayan, Jombor, Kec. Ceper, Kabupaten Klaten, Jawa Tengah 57465"
            if endCode == "TCBYL091":
                alamat = " Dusun I, Kuwiran, Kec. Banyudono, Kabupaten Boyolali, Jawa Tengah 57373"
            if endCode == "TCSRN061":
                alamat = " Jl. Nasional 15, Kebayanan 1, Purwosuman, Kec. Sidoharjo, Kabupaten Sragen, Jawa Tengah 57281"
            if endCode == "TCKAA071":
                alamat = " Jl. Lawu No.144, RW.11, Bejen, Kec. Karanganyar, Kabupaten Karanganyar, Jawa Tengah 57716"
            if endCode == "TCWGI051":
                alamat = " Jl. Diponegoro No. 75, Pokoh, Wonoboyo, Kec. Wonogiri, Kabupaten Wonogiri, Jawa Tengah 57615"
            img = Image('image4.png')
            wb = load_workbook(filename = 'kota.xlsx')
            sheet= wb['Sheet1']
            
            sheet["A6"] = jdl
            sheet["D7"] = maintgl
            sheet["D8"] = jamber
            sheet["D9"] = plateNumber
            sheet["D10"] = driverName
            sheet["F21"] = driverName
            sheet["D11"] = actualVehicleTypegroup
            sheet["D12"] = f"0{driverContact}"
            sheet["D13"] = maintgl
            sheet["D14"] = f"0{shifts}"
            sheet["H8"] = endCode
            sheet["H9"] = alamat
            sheet["J15"] = shipmentNo
            sheet["A16"] = f"SHUTTLE VENDOR {carrierName}"
            wb.save(filename="kota2.xlsx")
            final = {'No Sj' : jdl,"Tanggal Operasi":rekaptgl,"Nama Rute":endCode,"Nopol":plateNumber,"Jenis Mobil":actualVehicleTypegroup,"Trip":shifts,
                     "Tanggal Keberangkatan":rekaptgl,"Jam":jamber,"Koli":"Koli","Ecer":"Ecer","Jam Cetak":jmctk,"Layanan":"EZ","Admin":"Pamungkas/WIJANARKO","Vendor":carrierName,"KT":shipmentNo}
            path = os.path.join(folder , "kota2.xlsx")
            excel = client.Dispatch("Excel.Application",pythoncom.CoInitialize())
            sheets2 = excel.Workbooks.Open(path)

            pdf_path = os.path.join(folder,f"{endCode} - {shipmentNo}.pdf")
            work_sheets = sheets2.Worksheets[0]
            work_sheets.ExportAsFixedFormat(0, pdf_path)

            sheets2.application.displayalerts = False
            sheets2.Close()
            st.text(f"{kt} - {shipmentNo} DONE")
            rekap.append(final)
            # subprocess.Popen([f"{endCode}.pdf"],shell=True)
            time.sleep(0.7)

    st.caption("Result :")
    df = pd.DataFrame(rekap)
    st.dataframe(df,hide_index=True)
    st.caption(f"{len(df.index)}" + " Data")