import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import pandas as pd 

df = pd.read_csv('pm25_predictions_for_next_7_days.csv') 
# print(df)

# ข้อมูลจาก DATETIMEDATA และ prediction_label
datetimes = df['DATETIMEDATA'].tolist()
prediction_labels = df['prediction_label'].tolist()

# แปลงข้อมูล datetimes เป็นรูปแบบ datetime
datetimes = [datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") for dt in datetimes]

# สร้างกราฟ
plt.figure(figsize=(10, 6))
plt.plot(datetimes, prediction_labels, marker='o', color='b', linestyle='-')

# กำหนดรายละเอียดกราฟ
plt.title('Prediction Labels Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Prediction Label')
plt.grid(True)
plt.xticks(rotation=45)

# กำหนดรูปแบบแกน X
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))

# แสดงกราฟ
plt.tight_layout()
plt.show()
