import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="今晚我想來點．．．",
    page_icon="random",
    layout="centered",
)

# 今天日期、時間、星期幾
import datetime
import time
from datetime import date
import calendar
current_date = date.today()
current_weekday = calendar.day_name[current_date.weekday()]
localtime = time.localtime()
current_time = time.strftime("%H:%M", localtime)
time_result = current_time + ', ' + current_weekday

# 輸入名字
st.title(time_result + ':sunglasses:')
st.subheader('怎麼稱呼你呢？')
st.caption('盡量少於10個字元')
name = st.text_input('', key = 1)
if not name:
    st.stop()

# 讓使用者選要預定某個時間吃or現在就吃
st.subheader('你是現在要吃嗎')
st.caption('yes/no')
reserve_or_not = st.text_input('', key = 2)
if not reserve_or_not:
    st.stop()
if reserve_or_not == 'no':
    # 讓使用者輸入啥時要吃
    st.subheader('那你想要什麼時候吃呢？')
    st.caption('輸入：西元年,月,日,時,分（24小時制）')
    reserve_time = st.text_input('', key = 3)
    if not reserve_time:
        st.stop()
    reserve_time = reserve_time.split(',')
    for i in range(len(reserve_time)):
        if not reserve_time[i].isdigit():
            e = RuntimeError('請輸入正確的日期格式')
            st.exception(e)
            st.stop()
    yr = int(reserve_time[0])
    mon = int(reserve_time[1])
    day = int(reserve_time[2])
    hr = int(reserve_time[3])
    mn = int(reserve_time[4])
    # 轉換成時間格式
    dt = datetime.datetime(yr, mon, day, hr, mn)
    target_time = dt.strftime('%H:%M')
    target_weekday = calendar.day_name[dt.weekday()]
elif reserve_or_not == 'yes':
    target_time = current_time
    target_weekday = current_weekday
else:
    e = RuntimeError('請重新輸入')
    st.exception(e)
    st.stop()

# 處理時間資訊
wkDict = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
target_weekday = wkDict[target_weekday]
now_in_minutes = int(target_time[0:2]) * 60 + int(target_time[3:5])

# 使用者想要去哪一家吃
st.subheader('你想吃哪個區域的餐廳呢？')
st.caption('(a) 水源、公館 (b) 118巷 (c) 溫州街 (d) 校內')
region = st.text_input('')
if not region:
    st.stop()
if region == 'a':
    file_location = '/Users/dustinlin/Desktop/Final Project/data/gonguan.csv'
elif region == 'b':
    file_location = '/Users/dustinlin/Desktop/Final Project/data/118.csv'
elif region == 'c':
    file_location = '/Users/dustinlin/Desktop/Final Project/data/wenchou.csv'
elif region == 'd':
    file_location = '/Users/dustinlin/Desktop/Final Project/data/ntu.csv'
else:
    e = RuntimeError('請重新輸入')
    st.exception(e)
    st.stop()

# 根據區域去讀檔
readin = open(file_location, mode='r', encoding='utf-8')
lst = []
line = readin.read().splitlines()
for i in line:
    lst.append(i.split(','))

# 使用者想吃什麼類
st.subheader('想要吃哪種食物呢？')
st.caption('0: 早餐, 1: 台式, 2: 港式, 3: 中式, 4: 日式, 5: 韓式, 6: 義式, 7: 美式, 8: 東南亞料理, 9: 飲料, 10: 罪惡的胖胖食物, 11: 其他')
categ = st.text_input('', key = 4)
if not categ:
    st.stop()
if categ != '0' and categ != '1' and categ != '2' and categ != '3' and categ != '4' and categ != '5' and categ != '6' and categ != '7' and categ != '8' and categ != '9' and categ != '10' and categ != '11':
    e = RuntimeError('請重新輸入')
    st.exception(e)
    st.stop()
catDict = {'0':'br', '1':'tw', '2':'hk', '3':'ch', '4':'j', '5':'k', '6':'it', '7':'am', '8':'koh', '9':'dr', '10':'fat', '11':'oth'}
chosen = catDict[categ]
restaurants = []  # [店名, 評分, 評論數, 星期x的營業時間, $數]
for food in lst:
    if food[2] == chosen:
        restaurants.append([food[1], food[3], food[4], food[4 + target_weekday], int(food[-1])])

# 這個時間內是否有符合上述條件的餐廳
qualified = []  # [店名, 評分, 評論數, $數]
for store in restaurants:
    if store[3] == 'x':
        continue
    if '/' in store[3]:
        start1 = int(store[3][0:2]) * 60 + int(store[3][3:5])
        end1 = int(store[3][6:8]) * 60 + int(store[3][9:11])
        start2 = int(store[3][12:14]) * 60 + int(store[3][15:17])
        end2 = int(store[3][18:20]) * 60 + int(store[3][21:23])
        if start1 < now_in_minutes < end1 or start2 < now_in_minutes < end2:
            qualified.append([store[0], store[1], store[2], store[4]])
    else:
        start1 = int(store[3][0:2]) * 60 + int(store[3][3:5])
        end1 = int(store[3][6:8]) * 60 + int(store[3][9:11])
        if start1 < now_in_minutes < end1:
            qualified.append([store[0], store[1], store[2], store[4]])

output = " "
if qualified != []:
    # Random選出一家餐廳
    import random
    output = random.choice(qualified)
    # 輸出
    st.subheader(name + ' 您可以去吃（喝）：')
    st.header(str(output[0]))
    left_col, mid_col, right_col = st.columns(3)
    st.text('Google評分是' + str(output[1]) + '⭐')
    st.text('共有' + str(output[2]) + '則評論')
    st.text('價錢定位是 ' + str('💲' * int(output[-1])))
    st.subheader('祝您用餐愉快')
else:
    st.title('資料庫沒有符合條件的餐廳')
    st.subheader('要不要試著更改搜尋條件呢？')