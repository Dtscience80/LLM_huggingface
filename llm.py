#import openai
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import pandas as pd
import datetime as dt
from pycaret.classification import ClassificationExperiment
from openai import OpenAI
import folium
from streamlit_folium import st_folium
from together import Together



st.set_page_config(page_title='ELV', page_icon='👨‍💻', layout="centered", initial_sidebar_state="auto", menu_items={'About': "#v1tr4!"})
st.session_state["home_viewed"] = True
#st.sidebar.image("Picture/logo.jpeg", width=100)

# Gunakan secrets dari Streamlit, bukan hardcoded key

#openai.api_key = st.secrets["OPENAI_API_KEY"]
#client = Together(api_key=st.secrets["TOGETHER_API_KEY"])
#st.write(st.secrets['TOGETHER_API_KEY'])
#st.write(st.secrets['OPENAI_API_KEY'])
#st.write(st.secrets['DEEPSEEK_API_KEY'])


if not (
    st.session_state.get("home_viewed") 
):
    st.toast("Silakan Cek prediksi Uji Emisi, Rating dan ELV berbasis Machine Learning !", icon="🔥")

def regresi(rating, opasitas):
    if opasitas >= 65:
        reg = (opasitas - 65) / (100 - 65)
        hasil = round(reg + rating, 3)
    elif opasitas >= 40 and opasitas < 65:
        reg = (opasitas - 40) / (65 - 40)
        hasil = round(reg + rating, 3)
    elif opasitas >= 30 and opasitas < 40:
        reg = (opasitas - 30) / (40 - 30)
        hasil = round(reg + rating, 3)
    else:
        reg = (opasitas - 0) / (30 - 0)
        hasil = round(reg + rating, 3)
    return hasil


def tambahnilai(nilai, opasitas):
    if opasitas >= 65:
        nilai = round(nilai + 3, 3)
    elif opasitas >= 40 and opasitas < 65:
        nilai = round(nilai + 2, 3)
    elif opasitas >= 30 and opasitas < 40:
        nilai = round(nilai + 2, 3)
    else:
        nilai = round(nilai, 3)
    return regresi(nilai, opasitas)

def ratinggas(tahun, co, hc):
    nilaico = 0
    nilaihc = 0

    if tahun >= 2018:
        nilai = 0
    elif tahun >= 2007 and tahun < 2018:
        nilai = 1
    else:
        nilai = 2
    
    if co >= 4:
        nilaico = nilai + 3
        regco = (co - 4) / (10 - 4)
    elif co >= 1 and co < 4:
        nilaico = nilai + 2
        regco = (co - 1) / (4 - 1)
    elif co >= 0.5 and co < 1:
        nilaico = nilai + 1
        regco = (co - 0.5) / (1 - 0.5)
    else:
        nilaico = nilai
        regco = (co - 0) / (0.5 - 0)
    
    if hc >= 1000:
        nilaihc = nilai + 3
        reghc = (hc - 1000) / (10000 - 1000)
    elif hc >= 150 and hc < 1000:
        nilaihc = nilai + 2
        reghc = (hc - 150) / (1000 - 150)
    elif hc >= 100 and hc < 150:
        nilaihc = nilai + 1
        reghc = (hc - 100) / (150 - 100)
    else:
        nilaihc = nilai
        reghc = (hc - 0) / (99 - 0)

    rating = (regco + nilaico) + (reghc + nilaihc)
    return rating


#navigasi
with st.sidebar:

    selected = option_menu("MENU 📝 ", ["🏡 Home", '🛃 Prediksi Rating', '🌏 Prediksi UjiEmisi & ELV', '📖 ReadMe', '🗺️ Maps', '💬 Chat Me', '📙 About Me'])
    selected

if (selected == '🏡 Home'):
    
    image = Image.open('Picture/3.jpg')
    st.image(image, caption='')
    st.subheader(":rainbow[Prediksi Uji Emisi, Koef pajak, ELV Web Application berbasis machine learning berdasar data emisi kendaraan ] 🚗")
    
    
if (selected == '🛃 Prediksi Rating'):
    # horizontal Menu
    st.subheader(':rainbow[Tax Rating Predictor: Web App] 💸', divider='rainbow')
    st.subheader(" ⛽ Pilih :blue[bahan bakar kendaraan Anda ]")
    selected2 = option_menu(None, ["Diesel", "Gasoline"],  
    orientation="horizontal")
    st.subheader('Bahan bakar 🚘 anda adalah: ' + str(selected2))
    
    if (selected2 == "Diesel"):
        tahun = st.text_input('Tahun Pembuatan kendaraan (s/d 2023):', value='', key='tahun')   
        opasitas = st.text_input('Opasitas [%] kendaraan  (angka 0 - 100):', value='', key='opasitas')    

        if st.button('Hitung Rating'):
            try:
                if opasitas and tahun:
                    opasitas = min(float(opasitas), 100)
                    tahun = min(int(tahun), 2023)
                    koef = 0
                    if int(tahun) >= 2021:
                        koef = tambahnilai(0, opasitas)
                    elif int(tahun) >= 2010 and int(tahun) < 2021:
                        koef = tambahnilai(1, opasitas)
                    else:
                        koef = tambahnilai(2, opasitas)
                    st.subheader("Koefisien pajak anda adalah " + str(koef))
                else:
                    st.subheader("Masukkan nilai opasitas dan tahun terlebih dahulu!")
            except ValueError:
                st.subheader("Nilai opasitas dan tahun harus berupa angka!")


    if (selected2 == "Gasoline"):
        tahun = st.text_input('Tahun Pembuatan kendaraan (s/d 2023):', value='')
        co = st.text_input('Nilai CO [gr/km] kendaraan (0 - 10):', value='')
        hc = st.text_input('Nilai HC [ppm] kendaraan (0 - 10000):', value='')
        
        # Konversi input ke tipe data yang sesuai
        tahun = int(tahun) if tahun.isdigit() else 0
        tahun = min(int(tahun), 2023)
        co = float(co) if co.replace('.', '', 1).isdigit() else 0.0
        co = min(float(co), 10)
        hc = float(hc) if hc.replace('.', '', 1).isdigit() else 0.0
        hc = min(float(hc), 10000)

        if st.button('Hitung Rating'):
            try:
                if co and hc and tahun:
                    rating = round(ratinggas(tahun, co, hc) / 2, 3)
                    st.subheader("Koefisien pajak anda adalah " + str(rating))
                else:
                    st.subheader("Masukkan semua nilai parameter terlebih dahulu!")
            except ValueError:
                st.subheader("Nilai parameter harus berupa angka!")
       


if (selected == '🌏 Prediksi UjiEmisi & ELV'):
    d = ClassificationExperiment()
    st.subheader(':rainbow[Emission & ELV Predictor: Machine Learning Web App] 🔥', divider='rainbow')
    st.subheader(" ⛽ Pilih :blue[bahan bakar kendaraan Anda ]")
    selected3 = option_menu(None, ["Diesel", "Gasoline"],  
    orientation="horizontal")
    st.subheader('Bahan bakar 🚗 anda adalah: ' + str(selected3))

    if (selected3 == "Diesel"):
       
        CC1 = st.text_input("Besar CC kendaraan (1000 - 10000): ", value='')
        opasitas1 = st.text_input("Nilai Opasitas [%] kendaraan (0 - 100): ", value='')
        umur1 = st.text_input("Usia kendaraan saat Uji Emisi (0 - 100): ", value='')

        # Konversi input ke tipe data yang sesuai
        CC1 = int(CC1) if CC1.isdigit() else 0
        CC1 = min(int(CC1), 10000)
        opasitas1 = float(opasitas1) if opasitas1.replace('.', '', 1).isdigit() else 0.0
        opasitas1 = min(float(opasitas1), 100)
        umur1 = float(umur1) if umur1.replace('.', '', 1).isdigit() else 0.0
        umur1 = min(float(umur1), 10000)
        #Buat data frame dari data input
        df1 = pd.DataFrame({'CC': CC1, 'Opasitas [%HSU]': opasitas1, 'Umur Uji': umur1}, index= [0])
        
        if st.button('Cek Hasil Uji'):
            try:
                if CC1 and opasitas1 and umur1:
                    #Load Model 
                    Diesel_model1 = d.load_model('Model_Diesel_KelulusanEmisi')
                    #prediksi data 
                    dieselpr1 = d.predict_model(Diesel_model1, data=df1)
                    if dieselpr1['prediction_label'].iloc[0] == 1:
                        st.subheader('Selamat, :green[Kendaraan anda Lulus Uji Emisi] ✔️')
                    else:
                        st.subheader('Maaf, :blue[Kendaraan anda tidak lulus uji Emisi], :red[Perbaiki Emisi kendaraan anda] 👩‍🔧')
                else:
                    st.subheader("Masukkan semua nilai parameter terlebih dahulu!")
            except ValueError:
                st.subheader("Nilai parameter harus berupa angka!")

            try:
                if CC1 and opasitas1 and umur1:
                    #Load Model 
                    Diesel_model2 = d.load_model('Model_Diesel_ELV')
                    #prediksi data 
                    dieselpr2 = d.predict_model(Diesel_model2, data=df1)
                    if dieselpr2['prediction_label'].iloc[0] == 1:
                        st.subheader('Selamat, :green[Kendaraan anda Lulus Uji ELV] ✔️')
                    else:
                        st.subheader('Maaf, :blue[Kendaraan anda masuk masa ELV], :red[Silakan perbaiki kendaraan anda] 👨‍🔧')
                else:
                    st.subheader("Masukkan semua nilai parameter terlebih dahulu!")
            except ValueError:
                st.subheader("Nilai parameter harus berupa angka!")
            if (dieselpr1['prediction_label'].iloc[0] == 1 and dieselpr2['prediction_label'].iloc[0] == 1):
                st.balloons()

    if (selected3 == "Gasoline"):
       
        CC2 = st.text_input("Besar CC kendaraan (800 - 10000): ", value='')
        co2 = st.text_input("Nilai CO [gr/km] kendaraan (0 - 10): ", value='')
        hc2 = st.text_input("Nilai HC [ppm] kendaraan (0 - 10000): ", value='')
        umur2 = st.text_input("Usia kendaraan saat Uji Emisi (0 - 100): ", value='')

        # Konversi input ke tipe data yang sesuai
        CC2 = int(CC2) if CC2.isdigit() else 0
        CC2 = min(int(CC2), 10000)
        co2 = float(co2) if co2.replace('.', '', 1).isdigit() else 0.0
        co2 = min(float(co2), 10)
        hc2 = float(hc2) if hc2.replace('.', '', 1).isdigit() else 0.0
        hc2 = min(float(hc2), 10000)
        umur2 = float(umur2) if umur2.replace('.', '', 1).isdigit() else 0.0
        umur2 = min(float(umur2), 100)
        #Buat data frame dari data input
        df2 = pd.DataFrame({'CC': CC2, 'CO [%]': co2, 'HC [ppm]' : hc2, 'umur uji': umur2}, index= [0])

        if st.button('Cek Hasil Uji'):
            try:
                if CC2 and co2 and hc2 and umur2:
                    #Load Model 
                    Gasoline_model1 = d.load_model('Model_Gasoline_KelulusanEmisi')
                    #prediksi data 
                    gasolinepr1 = d.predict_model(Gasoline_model1, data=df2)
                    if gasolinepr1['prediction_label'].iloc[0] == 1:
                        st.subheader('Selamat, :green[Kendaraan anda Lulus Uji Emisi] ✔️')
                    else:
                        st.subheader('Maaf, :blue[Kendaraan anda tidak lulus uji Emisi], :red[Perbaiki Emisi kendaraan anda] 👩‍🔧')
                else:
                    st.subheader("Masukkan semua nilai parameter terlebih dahulu!")
            except ValueError:
                st.subheader("Nilai parameter harus berupa angka!")

            try:
                if CC2 and co2 and hc2 and umur2:
                    #Load Model 
                    Gasoline_model2 = d.load_model('Model_Gasoline_ELV')
                    #prediksi data 
                    gasolinepr2 = d.predict_model(Gasoline_model2, data=df2)
                    if gasolinepr2['prediction_label'].iloc[0] == 1:
                        st.subheader('Selamat, :green[Kendaraan anda Lulus Uji ELV] ✔️')
                    else:
                        st.subheader('Maaf, :blue[Kendaraan anda masuk masa ELV], :red[Silakan perbaiki kendaraan anda] 👨‍🔧')
                else:
                    st.subheader("Masukkan semua nilai parameter terlebih dahulu!")
            except ValueError:
                st.subheader("Nilai parameter harus berupa angka!")
            if (gasolinepr1['prediction_label'].iloc[0] == 1 and gasolinepr2['prediction_label'].iloc[0] == 1):
                st.balloons()

if (selected == '📙 About Me'):
    st.subheader(":rainbow[─ ⊹ ⊱ ⋆˚࿔ PSTB - BRIN team 𝜗𝜚˚⋆ ⊰ ⊹ ─] ")
    image1 = Image.open('Picture/1.JPG')
    st.image(image1, caption='')


if (selected == '📖 ReadMe'):
    st.subheader("📖 :rainbow[ReadMe]")
    sections = (
    "🏛️ About BRIN",
    "💻 PSTB",
    "📋 Peraturan Uji Emisi",
    "⚠️ Standart Uji Emisi EURO",
    "🤔 Author Member",
    )
    tabs = st.tabs(sections)

    readme1 = """
    **Badan Riset dan Inovasi Nasional (BRIN)**, disingkat **BRIN**, adalah **lembaga pemerintah nonkementerian** yang berada di bawah
    dan bertanggung jawab kepada **Presiden Indonesia**. Tugas utamanya adalah **menyelenggarakan penelitian, pengembangan, 
    pengkajian, dan penerapan**, serta **invensi dan inovasi**. Selain itu, BRIN juga bertanggung jawab atas **penyelenggaraan 
    ketenaganukliran** dan **keantariksaan yang terintegrasi**³45.

    Berikut beberapa poin penting mengenai BRIN:

    1. **Tujuan**: BRIN bertujuan untuk **mendorong inovasi**, **pengembangan teknologi**, dan **peningkatan daya saing nasional** 
    melalui riset dan pengembangan.
    2. **Fokus**: BRIN fokus pada **penelitian multidisiplin** dan **kolaborasi antarlembaga** untuk menghasilkan solusi inovatif.
    3. **Bidang Kajian**: BRIN mengkaji berbagai bidang, termasuk **sains**, **teknologi**, **kesehatan**, **pertanian**, dan 
    **energi**.
    4. **Integrasi**: BRIN berperan dalam mengintegrasikan upaya riset dan inovasi di seluruh sektor pemerintahan.

    Lebih lanjut, BRIN juga memiliki tanggung jawab dalam **penyelenggaraan ketenaganukliran** dan **keantariksaan**. 
    Ini mencakup pengembangan teknologi nuklir dan eksplorasi luar angkasa.

    Anda dapat memperoleh informasi lebih lanjut mengenai BRIN di [situs resmi BRIN](https://www.brin.go.id/) ²7. 

    Source: Conversation with Bing, 4/19/2024

    (1) Badan Riset dan Inovasi Nasional - Wikiwand. https://www.wikiwand.com/id/Badan_Riset_dan_Inovasi_Nasional.
    (2) Badan Riset dan Inovasi Nasional (BRIN) – Kompaspedia. 
    https://kompaspedia.kompas.id/baca/profil/lembaga/badan-riset-dan-inovasi-nasional.
    (3) Mengenal Apa itu BRIN: Sejarah Berdirinya, Tugas, dan Fungsi - Suara.com.   
    https://www.suara.com/news/2022/01/03/145232/mengenal-apa-itu-brin-sejarah-berdirinya-tugas-dan-fungsi.
    (4) BRIN (Badan Riset dan Inovasi Nasional). https://www.brin.go.id/.
    (5) BRIN - Badan Riset dan Inovasi Nasional. https://www.brin.go.id/en.
    (6) . https://bing.com/search?q=berikan+deskripsi+lengkap+tentang+badan+riset+dan+inovasi+nasional+%28BRIN%29+indonesia.\
    (7) . https://bing.com/search?q=badan+riset+dan+inovasi+nasional+%28BRIN%29+indonesia.
    (8) Badan Riset dan Inovasi Nasional - JDIH BPK RI. https://peraturan.bpk.go.id/Home/Details/178084/perpres-no-78-tahun-2021.


    """ 
    tabs[0].subheader(sections[0])
    tabs[0].info(readme1)

    readme2 = """
    Kelompok Riset Pemodelan Sarana Transportasi Berkelanjutan (KST) di Badan Riset dan Inovasi Nasional (BRIN) 
    berfokus pada pengembangan pemodelan dan teknologi yang mendukung transportasi berkelanjutan. 
    Berikut adalah beberapa informasi mengenai KST:
    
    1. Beberapa Kegiatan Riset:
       - PSTB melakukan riset pemanfaatan IoT berbasis mikrokontroller untuk membangun sistem monitoring kualitas udara secara real-time dengan biaya rendah.
       - Topik kegiatan riset meliputi pemantauan kualitas udara menggunakan teknologi IoT.
       - Berupaya membangun prototipe sistem pemantauan kualitas udara berbiaya rendah dengan menggunakan mikrokontroller.
       - Riset bidang Bio Lubricant, untuk mesin diesel
       - Riset yang bekerjasama dengan kementrian Lingkungan Hidup dan Kehutanan antara lain untuk penentuan rating koefisien pajak, End of Live Vehicle (ELV), dll
       - Riset pembuatan Sistem Monitoring Operasional dan Optimasi Kinerja Mesin Kapal Secara Real Time Menggunakan Teknik Machine Learning
       - Riset pembuatan Analisa cofiring menggunakan machine learning
       - Riset penggunaan wifi sebagai alternatif pengganti gps, dll.
       
    2. Lokasi Pelaksanaan:
       - KST BJ Habibie - Setu, Serpong.
    
    KST ini berperan penting dalam mengembangkan solusi transportasi yang ramah lingkungan dan efisien. 
   
    
    """
    tabs[1].subheader(sections[1])
    tabs[1].success(readme2)
    
    readme3 = """
    Peraturan UjiEmisi Indonesia:
    1. Uji emisi menjadi syarat penting untuk kendaraan beroperasi di jalan raya.
    2. Indonesia menerapkan aturan uji emisi untuk kendaraan baru sejak 2005 berdasarkan Keputusan Menteri Negara Lingkungan Hidup nomor 141 tahun 2003 tentang Ambang Emisi Gas Buang Kendaraan Bermotor Tipe Baru.
    3. Produsen kendaraan bermotor harus memproduksi kendaraan yang ramah lingkungan.
    4. Pada 2013, pemerintah mengetatkan peraturan emisi untuk kendaraan roda 2 menjadi Euro 3.
    5. Pada 2017, ambang batas kendaraan tipe baru ditetapkan menjadi Euro 4.
    6. Implementasi Euro 4 sempat tertunda hingga 2022.
    7. Kendaraan di Indonesia wajib memenuhi baku mutu emisi Euro 4 sejak 2022.
    8. Kementrian Lingkungan Hidup dan Kehutanan mengatur emisi gas buang kendaraan beroperasi di jalan raya dengan umur di atas 3 tahun.
    9. Peraturan emisi gas buang tertuang dalam Peraturan Menteri Lingkungan Hidup dan Kehutanan Nomor 5 tahun 2006.
    10. Pada 2023, terjadi pembaruan peraturan emisi gas buang menjadi Peraturan Menteri Lingkungan Hidup dan Kehutanan nomor 8 tahun 2023.
    """
    tabs[2].subheader(sections[2])
    tabs[2].info(readme3)
    
    readme4 = """
    Standar emisi Euro adalah serangkaian regulasi yang ditetapkan oleh Uni Eropa untuk mengatur emisi kendaraan bermotor baru. 
    Berikut adalah ringkasan tentang penerapan setiap standar emisi Euro dari Euro 1 hingga yang terakhir:
    
    1. **Euro 1 (1992):**
       - Euro 1 merupakan standar emisi pertama yang diperkenalkan pada tahun 1992.
       - Standar ini mengatur batas emisi untuk oksida nitrogen (NOx), hidrokarbon (HC), karbon monoksida (CO), dan partikulat.
       - Euro 1 menetapkan batas emisi yang lebih rendah dibandingkan dengan standar sebelumnya.
    
    2. **Euro 2 (1996):**
       - Euro 2 diperkenalkan pada tahun 1996 sebagai kelanjutan dari Euro 1.
       - Standar ini mengurangi batas emisi untuk NOx, HC, dan CO.
       - Euro 2 memperkenalkan standar yang lebih ketat dan teknologi pengendalian emisi yang lebih canggih.
    
    3. **Euro 3 (2000):**
       - Euro 3 diperkenalkan pada tahun 2000 dengan batas emisi yang lebih ketat lagi.
       - Standar ini memperkenalkan batas emisi baru untuk partikulat diesel.
       - Euro 3 memperkenalkan teknologi seperti katalisator tiga arah untuk mengurangi emisi gas buang.
    
    4. **Euro 4 (2005):**
       - Euro 4 diperkenalkan pada tahun 2005 sebagai respons terhadap kebutuhan untuk mengurangi emisi kendaraan bermotor.
       - Standar ini menetapkan batas emisi yang lebih rendah untuk NOx dan partikulat diesel.
       - Euro 4 mendorong penggunaan teknologi pengendalian emisi yang lebih maju seperti filter partikulat diesel (DPF).
    
    5. **Euro 5 (2009):**
       - Euro 5 diperkenalkan pada tahun 2009 dengan batas emisi yang lebih ketat lagi, khususnya untuk NOx dan partikulat diesel.
       - Standar ini memperkenalkan batas emisi yang lebih rendah untuk gas buang kendaraan diesel.
       - Euro 5 memperkenalkan teknologi seperti sistem selektif katalitik reduction (SCR) untuk mengurangi NOx.
    
    6. **Euro 6 (2014):**
       - Euro 6 diperkenalkan pada tahun 2014 dengan batas emisi yang lebih ketat untuk NOx, partikulat, dan gas buang lainnya.
       - Standar ini mengharuskan kendaraan diesel memenuhi standar emisi NOx yang sangat ketat di bawah kondisi penggunaan nyata.
       - Euro 6 mendorong penggunaan teknologi emisi yang lebih maju termasuk teknologi SCR dan filter partikulat yang lebih canggih.
    
    7. **Euro 6d (2017) dan Euro 6d-TEMP (2019):**
       - Euro 6d diperkenalkan pada tahun 2017 dengan persyaratan pengujian emisi yang lebih ketat di bawah kondisi penggunaan nyata.
       - Euro 6d-TEMP, yang diperkenalkan pada tahun 2019, memperkenalkan batasan sementara pada emisi NOx untuk kendaraan diesel 
       sebelum implementasi penuh Euro 6d.
    
    Perlu dicatat bahwa setiap iterasi Euro standards mengharuskan produsen kendaraan untuk mengembangkan dan menerapkan teknologi 
    pengendalian emisi yang lebih canggih guna memenuhi batas emisi yang ditetapkan. Standar emisi Euro terus berkembang untuk 
    mengurangi dampak negatif kendaraan bermotor terhadap lingkungan dan kesehatan manusia.
    
    """
    tabs[3].subheader(sections[3])
    tabs[3].error(readme4)
    
    readme5 = """
    Member dari Riset yang bekerja sama dengan Kementrian Lingkungan Hidup dan kehutanan (KLHK) ini antara lain:
    
    BRIN :
    * Rizqon Fajar 
    * Fitra Hidiyanto
    * Kurnia Fajar Adhi Sukra
    * Dhani Avianto Sugeng
    * Nilam Sari Octaviani
    
    KLHK :
    * Noor Rahmaniah 
    * Ratna Kartikasari
    * Isa Ansyori 
    * Reza Irvano Irawan
     
    
    """ 
    tabs[4].subheader(sections[4]) 
    tabs[4].success(readme5)

if (selected == '🗺️ Maps'):
    st.subheader(" Lokasi :rainbow[ Pemodelan Sarana Transportasi Berkelanjutan ]")             
                                                                                            
    # center on Liberty Bell, add marker                                                        
    m = folium.Map(location=[-6.34749, 106.66219], zoom_start=17)                               
    folium.Marker([-6.34749, 106.66219], popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)
                                                                                            
    # call to render Folium map in Streamlit                                                    
    st_data = st_folium(m, width=725)                                                           

if (selected == '💬 Chat Me'):

    #st.set_page_config(page_title="💬 Together AI Chat", layout="centered")
    st.title("💬 PSTB AI Chat")

    # Inisialisasi Together Client
    client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

    # Inisialisasi pesan chat dalam session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input pengguna
    if prompt := st.chat_input("Tanyakan sesuatu..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Menunggu jawaban..."):
                try:
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="meta-llama/Llama-3-70b-chat-hf",
                        max_tokens=1024,
                        temperature=0.5,
                        stream=False,
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"⚠️ Terjadi kesalahan: {e}"

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

    # Tombol untuk membersihkan chat
    if st.button("🗑️ Bersihkan Chat"):
        st.session_state.messages = []
