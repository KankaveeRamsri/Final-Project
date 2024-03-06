from datetime import datetime, timedelta 

now = datetime.now()

formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

print(formatted_date)



# print ("initial_date", str(ini_time_for_now))

# future_date_after_2yrs = ini_time_for_now + timedelta(days = 730)

# print(future_date_after_2yrs)

# print(timedelta(hours=8) + datetime.now())