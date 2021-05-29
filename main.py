import time
import requests
import datetime as dt

AGE = 20
PINCODE = "201014"
DATE = ""
API_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

dates_future = 4
dates = []
today = dt.datetime.today()

for i in range(1, dates_future+1):
    # print(i)
    new_date = today + dt.timedelta(i)
    # print(new_date)
    formatted_date = new_date.strftime("%d-%m-%Y")
    # print(formatted_date)
    dates.append(formatted_date)


print(dates)

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

while True:
    time.sleep(5)
    for date in dates:
        parameters = {
            "pincode": PINCODE,
            "date": date,
            "Accept-Language": "Accept-Language: en-US"
        }
        api_response = requests.get(API_URL, params=parameters, headers=header)
        api_response.raise_for_status()
        center_data = api_response.json()["centers"]
        for center in center_data:
            min_age_limit = center["sessions"][0]["min_age_limit"]
            available_capacity = center["sessions"][0]["available_capacity"]
            center_name = center["name"]
            address = center["address"]
            time_from = dt.datetime.strptime(center["from"], "%H:%M:%S").strftime("%I:%M %p")
            time_to = dt.datetime.strptime(center["to"], "%H:%M:%S").strftime("%I:%M %p")
            price = center["fee_type"]
            vaccine_name = center["sessions"][0]["vaccine"]

            if min_age_limit <= AGE and available_capacity > 0:
                formatted_message = f"💉 {vaccine_name} Vaccine Slot Available at {center_name}, {address} " \
                                    f"for age {min_age_limit} and above on {date}" \
                                    f"\nCurrently Available Capacity: {available_capacity}" \
                                    f"\nPrice: {price}" \
                                    f"\nCenter timings: {time_from} to {time_to}"

                print(formatted_message)
                break
