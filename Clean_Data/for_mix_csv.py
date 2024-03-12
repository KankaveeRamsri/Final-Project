import pandas as pd

# อ่านข้อมูลจากไฟล์ CSV
data1 = pd.read_csv('predict_PM25.csv')
data2 = pd.read_csv('predict_WD.csv')

# รวมข้อมูลโดยใช้ฟังก์ชัน merge() โดยระบุคีย์ที่ใช้ในการรวมข้อมูล
merged_data = pd.merge(data1, data2, on='DATETIMEDATA')

# บันทึกข้อมูลลงในไฟล์ CSV ใหม่
merged_data.to_csv('predict_WD_PM25.csv', index=False)