import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import pandas as pd 

# df = pd.read_csv('predict_day.csv') 

# # ข้อมูลจาก DATETIMEDATA และ prediction_label
# datetimes = df['DATETIMEDATA'].tolist()
# prediction_labels = df['PREDICTION_PM25'].tolist()

# # แปลงข้อมูล datetimes เป็นรูปแบบ datetime
# datetimes = [datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") for dt in datetimes]

# # สร้างกราฟ
# plt.figure(figsize=(10, 6))
# plt.plot(datetimes, prediction_labels, marker='o', color='b', linestyle='-')

# # กำหนดรายละเอียดกราฟ
# plt.title('Prediction Labels Over Time')
# plt.xlabel('Date and Time')
# plt.ylabel('Prediction Label')
# plt.grid(True)
# plt.xticks(rotation=45)

# # กำหนดรูปแบบแกน X
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
# plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))

# # แสดงกราฟ
# plt.tight_layout()
# plt.show()

print("-------------------------------------")

# df = pd.read_csv('predict_hour.csv') 

# # ดึงข้อมูลจาก DataFrame
# DATETIMEDATA = df['DATETIMEDATA'].tolist()
# PM25 = df['PREDICTION_PM25'].tolist()
    
# # พล็อตกราฟ
# plt.plot(DATETIMEDATA, PM25, color='blue', marker='o', linestyle='-')

# # กำหนดชื่อแกน
# plt.xlabel('Date Time')
# plt.ylabel('Temperature (°C)')
# plt.title('Temperature Variation')

# # แสดงกราฟ
# plt.xticks(rotation=45)  # หมุนข้อมูลในแกน x 45 องศาเพื่อป้องกันการซ้อนทับ
# plt.tight_layout()  # ปรับแต่งเล็บของกราฟ
# plt.show()

import matplotlib.pyplot as plt
import pandas as pd

# อ่านข้อมูลจากไฟล์ CSV
df = pd.read_csv('predict_day.csv')

# สร้างกราฟ
plt.figure(figsize=(10, 6))
plt.plot(df['DATETIMEDATA'], df['PREDICTION_PM25'], marker='o', color='b', linestyle='-')

# กำหนดรายละเอียดกราฟ
plt.title('Prediction Labels Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Prediction Label')
plt.grid(True)
plt.xticks(rotation=45)

# แสดงกราฟ
plt.tight_layout()
plt.show()
