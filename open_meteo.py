import requests
from datetime import datetime

# Function to get latitude and longitude for a given location
def get_coordinates(location):
    geocoding_url = "https://geocode.maps.co/search"
    params = {"q": location}
    response = requests.get(geocoding_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            print(f"No results found for location: {location}")
    else:
        print(f"Geocoding API request failed: {response.status_code}")
    return None, None

# Function to fetch weather data
def get_weather(location, hour):
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Get coordinates for the location
    latitude, longitude = get_coordinates(location)
    if latitude is None or longitude is None:
        return

    # Define the API endpoint and parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto",
        "start_date": today,
        "end_date": today
    }

    # Make the API request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Weather Data for {location} at {hour}:00 on {today}:")
        for time, temp, rain in zip(
            data["hourly"]["time"],
            data["hourly"]["temperature_2m"],
            data["hourly"]["precipitation"]
        ):
            # Extract the hour from the time
            time_hour = datetime.fromisoformat(time).strftime("%H")
            if time_hour == hour:
                print(f"Time: {time}, Temp: {temp}°C, Rain: {rain} mm")
                break
        else:
            print(f"No data available for {hour}:00.")
    else:
        print(f"Weather API request failed: {response.status_code}")

# Input for location and hour
location = input("Enter the location: ")
hour = input("Enter the hour (00-23): ")

# Validate hour input
if not hour.isdigit() or not (0 <= int(hour) <= 23):
    print("Invalid hour. Please enter a value between 00 and 23.")
else:
    get_weather(location, hour.zfill(2))  # Pad single-digit hours with a leading zero
