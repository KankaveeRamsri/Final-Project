# Hatyai

import requests
from pprint import pformat

station_id = "44t"
param = "PM25,WS,TEMP,RH,WD"
data_type = "hr"
start_date = "2024-01-01"
end_date = "2024-03-07"
start_time = "00"
end_time = "23"
url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()
# print(pformat(response_json))

import pandas as pd

Dataframe = pd.DataFrame.from_dict(response_json["stations"][0]["data"])
print(Dataframe)
Dataframe.to_csv(f"PM25_{station_id}_{start_date}_{end_date}.csv")

