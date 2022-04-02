import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
plt.style.use('ggplot')

st.title('YahooAPI 地図表示＆降水予報')

input_data = st.sidebar.text_area('■住所を入力', '高槻市')

api_key = st.secrets["key"]
Weather_url = "https://map.yahooapis.jp/weather/V1/place?"
geo_url = "https://map.yahooapis.jp/geocode/V1/geoCoder?"
parm1 = "coordinates="
parm2 = "&output=json"
parm3 = "&query="
AREA = input_data

# Yahoo!ジオコーダによる取得したい場所の情報をURLにする
geo = geo_url + api_key + parm2 + parm3 + AREA

# 取得した情報を整形する
geo_info = requests.get(geo)
geo_obj = json.loads(geo_info.text)

# Geometryから座標情報のみ取得する
parm = geo_obj["Feature"][0]["Geometry"]["Coordinates"]

place = [float(i) for i in parm.split(",")[::-1]]

zoom = st.sidebar.slider("■地図の初期ZOOM設定", 1, 20, 10)

# 気象情報APIに渡すための情報（「?」の後ろに「&」で条件を繋いでいく）をURLにする
url = Weather_url + parm1 + parm + parm2 + api_key

# 取得した情報を整形する
url_info = requests.get(url)
obj = json.loads(url_info.text)

# 取得した気象情報7回分のうち10分後のものから表示させる
preds = []
for i in range(1,7):
    pred = {}
    # type = obj['Feature'][0]['Property']['WeatherList']['Weather'][i]['Type']
    pred["time"] = obj['Feature'][0]['Property']['WeatherList']['Weather'][i]['Date'][8:]
    pred["rainfall"] = obj['Feature'][0]['Property']['WeatherList']['Weather'][i]['Rainfall']
    preds.append(pred)

preds = pd.DataFrame(preds)

if st.sidebar.button('検索開始'):
    comment = st.sidebar.empty()
    comment.write('検索を開始します')

    st.write("■ジオコーダAPIより、foliumの地図を表示")
    m = folium.Map(location=place, zoom_start=zoom) # 地図の初期設定
    folium.Marker(location=place, popup=AREA).add_to(m)
    folium_static(m) # 地図情報を表示

    st.write("■気象情報APIより、1時間後までの降水強度を予測")
    fig = plt.figure(figsize=(9,3))
    plt.rcParams["font.size"] = 15
    plt.bar(preds["time"], preds["rainfall"])
    for x, y in zip(preds["time"], preds["rainfall"]):
        plt.text(x, y, y, ha='center', va='bottom', color="blue")
    plt.ylim(0, )
    plt.xlabel("time")
    plt.ylabel("rainfall (mm/h)")
    st.pyplot(fig)
    
    if preds["rainfall"].sum() == 0:
        st.write("ここ1時間は雨は降らないでしょう")
    
    comment.write('完了しました')
