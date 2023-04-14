import requests

# API key from OpenWeatherMap
API_KEY = "9ee30c3d4c072a847cde3cc1d93817b5"

# Ask user for latitude and longitude coordinates
lat = input("Enter latitude: ")
lon = input("Enter longitude: ")

# API request URL
url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

# Send API request and get response
response = requests.get(url)

# Parse JSON response into a dictionary
data = response.json()

# Extract weather information from dictionary
temp = data["main"]["temp"]
description = data["weather"][0]["description"]

# Print weather information
print(f"Temperature: {temp:.1f}°C")
print(f"Description: {description.capitalize()}")

