import pandas as pd 
from pprint import pformat

data = pd.read_csv('Data/PM25_44t_2024-01-01_2024-03-7.csv')
data = data.drop(columns=['Unnamed: 0'])
# print(data)

count_Nan = data.isnull().sum()
# print("A number of NaN in each columns : ")
# print(pformat(count_Nan))

rows_with_nan = data[data.isnull().any(axis=1)]
# print("Rows with NaN_values:")
# print(rows_with_nan)

Mean_PM25 = data['PM25'].mean()
data['PM25'].fillna(round(Mean_PM25),inplace = True)

row = [179,327,328,490,864,865,880,881,952,1004,1005,1161,1162,1280,1281,1378,1379,1542,1543
       ,1544,1545,1546]
# print(data.iloc[row])

count_zeros = (data == 0).sum()
print("A number of zeros in each column:")
print(pformat(count_zeros))

rows_with_zeros = data[(data == 0).sum(axis=1) > 0]
print("Rows with zero values:")
print(rows_with_zeros)


# เลือกคอลัมน์ที่คุณต้องการแทนที่ค่า 0 ด้วยค่าเฉลี่ย
selected_columns = ['WS', 'TEMP', 'RH', 'WD']  # แทนที่ด้วยชื่อคอลัมน์ที่คุณต้องการ

# หาค่าเฉลี่ยของแต่ละคอลัมน์ที่เลือก
mean_values = data[selected_columns].mean()

# วนลูปผ่านแต่ละคอลัมน์และแทนที่ค่า 0 ด้วยค่าเฉลี่ยของแต่ละคอลัมน์ที่เลือก
for column in selected_columns:
    data[column] = data[column].replace(0, mean_values[column])

# count_zeros = (data == 0).sum()
# print("A number of zeros in each column:")
# print(pformat(count_zeros))

print(pformat(data))
data.to_csv(f"Clean_data44t_Hatyai.csv")




