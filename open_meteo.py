import requests
from datetime import datetime, timedelta

# Define the API endpoint and parameters
url = "https://api.open-meteo.com/v1/forecast"

# Choose the date range (today or tomorrow)
today = datetime.now().strftime("%Y-%m-%d")  # Today's date
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")  # Tomorrow's date

# Parameters for hourly forecast
params = {
    "latitude": 52.3676,  # Latitude for Amsterdam
    "longitude": 4.9041,  # Longitude for Amsterdam
    "hourly": "temperature_2m,precipitation",  # Add hourly temperature and rain
    "timezone": "auto",  # Automatically adjust timezone
    "start_date": tomorrow,  # Change to `tomorrow` for tomorrow's data
    "end_date": tomorrow  # Use the same date for a single day
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    print(f"Hourly Weather Data for {today}:")
    for time, temp, rain in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["precipitation"]
    ):
        print(f"Time: {time}, Temp: {temp}°C, Rain: {rain} mm")
else:
    print("Failed to retrieve data:", response.status_code)