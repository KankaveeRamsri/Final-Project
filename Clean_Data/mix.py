import pandas as pd

# โหลดไฟล์ CSV 2 อัน
df1 = pd.read_csv('mix_info.csv')
df2 = pd.read_csv('ไฟล์.csv')

# รวม DataFrame โดยใช้เงื่อนไขหรือการเชื่อมโยงด้วย merge()
# ตัวอย่างนี้เป็นการรวมโดยใช้คอลัมน์ 'key' เป็นตัวเชื่อมโยง
# สามารถเปลี่ยนแปลงคอลัมน์และเงื่อนไขตามที่ต้องการ
combined_df = pd.merge(df1, df2, on='DATETIMEDATA')

# บันทึกไฟล์ CSV ที่รวมแล้ว
combined_df.to_csv('combined_file.csv', index=False)
