import pandas as pd 
from pprint import pformat

data = pd.read_csv('Data/PM25_44t_2023-12-01_2024-02-29.csv')

count_Nan = data.isnull().sum()
print("A number of NaN in each columns : ")
print(pformat(count_Nan))

Mean_PM25 = data['PM25'].mean()
data['PM25'].fillna(round(Mean_PM25),inplace = True)

print(pformat(data))
data.to_csv(f"Clean_data44t_Hatyai.csv")