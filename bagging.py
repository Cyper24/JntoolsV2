import streamlit as st
import requests
import code128
import qrcode
from PIL import Image
from docxtpl import DocxTemplate,InlineImage
from datetime import datetime, timedelta
import os
import win32com.client
import pythoncom

folder = os.getcwd()
at=(st.session_state.ato).strip(" ")
st.title("Bagging")

dp =[]
tj = st.text_input("Cari Tujuan")

url = "https://jmsgw.jntexpress.id/basicdata/network/select/all"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "cookie": "HWWAFSESID=a00e27f02785ef49ce5; HWWAFSESTIME=1738201375713",
    "Content-Type": "application/json",
    "authtoken": at
}

def listdp():
    querystring = {"current":"1","size":"50","name":tj,"queryLevel":"3"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    r=response.json()
    f = r["data"]["records"]
    for x in f:
        code = x["code"]
        dp.append(code)
    
def prin(jumlah,kodep,enNamep):
    urlp = "https://jmsgw.jntexpress.id/esscustomer/firstPackage/firstPackagePrint"
    payload = {
    "printNumber": jumlah,
    "businessType": "EZ",
    "items": [
                {
                    "centerCode": kodep,
                    "centerName": enNamep
                }
            ],
            "countryId": "1"
            }
    response = requests.request("POST", urlp, json=payload, headers=headers)
    r=response.json()
    f = r["data"]
    for x in f:
        packageNumber=x["packageNumber"]
        centerCodex=x["centerCode"]
        firstName=x["firstName"]

        st.text(packageNumber)

        # barcode gen
        bc_image = code128.image(packageNumber)
        w, h = bc_image.size
        new_width  = int(w/1.7)
        new_height = int(h/2.6)
        img = bc_image.resize((new_width, new_height), Image.LANCZOS)
        img.save('bc.png', 'PNG')

        # qr gen
        qr = qrcode.QRCode(version = 1,
                   box_size =3,
                   border = 1)
        qr.add_data(packageNumber)
        qr.make(fit = True)
        imgqr = qr.make_image(fill_color = 'black',
                            back_color = 'white')
        imgqr.save('qr.png')

        # bgg template
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        doc = DocxTemplate("INCOMING.docx")
        context = {'tujuan' : enNamep,
                'tujuan2': kodep,
                'bagging': packageNumber,
                'tanggal': dt,
                'image': InlineImage(doc, "bc.png"),
                'qr': InlineImage(doc, "qr.png")}
        doc.render(context)
        doc.save("bg.docx")

        # convertpdf
        fn = f"bagging/{packageNumber}.pdf"
        wdFormatPDF = 17
        path = os.path.join(folder , "bg.docx")
        word = win32com.client.Dispatch('Word.Application',pythoncom.CoInitialize())
        doc = word.Documents.Open(path)
        fn = f"bagging/{packageNumber}.pdf"
        pdf_path = os.path.join(folder,fn)
        doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
        st.text("Done")
        doc.Close()

listdp()
options = st.multiselect(
    "Pilih Tujuan",
    dp,
    )

jmlah= st.number_input('Jumlah', min_value=1, value=1, step=1)
if st.button("Exec..."):
    for kode in options:
        querystring = {"current":"1","size":"1","name":kode,"queryLevel":"3"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        r=response.json()
        f = r["data"]["records"]
        for x in f:
            enName = x["enName"]
        prin(jmlah,kode,enName)