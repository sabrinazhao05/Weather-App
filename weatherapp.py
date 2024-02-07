import schedule
import time
import requests
from twilio.rest import Client

def get_coordinates(city_name):
    # Use a geocoding API to get latitude and longitude for the entered city
    # Example: You can use OpenCage Geocoding API, Google Maps Geocoding API, etc.
    # Replace 'YOUR_API_KEY' with your actual API key
    geocoding_url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key=YOUR_API_KEY"
    response = requests.get(geocoding_url)
    data = response.json()
    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        return None, None

def get_weather(latitude, longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(base_url)
    data = response.json()
    return data

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def send_text_message(body):
    # Your Twilio credentials and phone numbers
    account_sid = '[AccountSid]'
    auth_token = '[AuthToken]'
    from_phone_number = "+18336599154"
    to_phone_number = "[number]"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_="+18336599154",
        body=body,
        to="[number]"
    )
    print("Weather Info Sent!")

def send_weather_update(city_name):
    latitude, longitude = get_coordinates(city_name)
    if latitude is not None and longitude is not None:
        weather_data = get_weather(latitude, longitude)
        temperature_celsius = weather_data["hourly"]["temperature_2m"][0]
        relative_humidity = weather_data["hourly"]["relativehumidity_2m"][0]
        wind_speed = weather_data["hourly"]["windspeed_10m"][0]
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

        weather_info = (
            f"Good Morning\n"
            f"Current Weather in {city_name}:\n"
            f"Temperature: {temperature_fahrenheit:.2f}F\n"
            f"Relative Humidity: {relative_humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        send_text_message(weather_info)
    else:
        print("Unable to retrieve coordinates for the entered city.")

def main():
    # Prompt the user to enter the city name
    city_name = input("Enter the name of the city: ")
    schedule.every().day.at("08:00").do(send_weather_update, city_name)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
