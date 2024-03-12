import pandas as pd

# โหลดข้อมูล CSV
data = pd.read_csv('ไฟล์ใหม่.csv')

# ลบคอลัมน์ที่ไม่ต้องการ
column_to_drop = ['Unnamed: 0']  # แทนที่ด้วยชื่อคอลัมน์ที่ต้องการลบ
data.drop(columns=column_to_drop, inplace=True)

# บันทึกข้อมูลลงในไฟล์ CSV ใหม่
data.to_csv('ไฟล์.csv', index=False)
