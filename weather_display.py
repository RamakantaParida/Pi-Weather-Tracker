import time
import urequests
from machine import Pin, I2C
import ssd1306
import lcd1602
import network
import socket

def read_url_from_response(response_text):
    try:
        # Extract the URL from the response text
        url_info = response_text.split("URL:")[1].split(",")[0].strip().replace("\\", "")
        return url_info
    except Exception as e:
        print(f"Error extracting URL: {e}")
        return None

def get_weather(url):
    try:
        response = urequests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_air_pollution(lat, lon, api_key):
    try:
        aqi = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=babb2568d2f0a307fa4023b8ffd9a7ac&units=metric"
        responses = urequests.get(aqi)
        return responses.json()
    except Exception as e:
        print(f"Error fetching air pollution data: {e}")
        return None


def get_wind_direction(degrees):
    directions = ["North", "North East", "East", "South East", "South", "South West", "West", "North West"]
    index = round(degrees / 45) % 8
    return directions[index]

def print_weather(weather_data):
    print(f'\nCountry: {weather_data["sys"]["country"]}')
    print(f'City: {weather_data["name"]}')
    print(f'Coordinates: [{weather_data["coord"]["lon"]}, {weather_data["coord"]["lat"]}]')
    print(f'Visibility: {weather_data["visibility"]}m')
    print(f'Weather: {weather_data["weather"][0]["description"]}'.upper)
    print(f'Temperature: {weather_data["main"]["temp"]}°C')
    print(f'Feels Like: {weather_data["main"]["feels_like"]}°C')
    print(f'Minimum Temperature: {weather_data["main"]["temp_min"]}°C')
    print(f'Maximum Temperature: {weather_data["main"]["temp_max"]}°C')
    print(f'Pressure: {weather_data["main"]["pressure"]}hPa')
    print(f'Humidity: {weather_data["main"]["humidity"]}%')
    print(f'Wind Speed: {weather_data["wind"]["speed"]}m/s')
    print(f'Wind Direction: {get_wind_direction(weather_data["wind"]["deg"])}')
    
def print_air_pollution(air_pollution_data):    
    print("\nAir Pollution Data:")
    aqi = air_pollution_data['list'][0]['main']['aqi']
    print("Components:")
    components = air_pollution_data['list'][0]['components']
    for component, value in components.items():
        print(f"{component}: {value}")
    aqi_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
    turn_on_single_led(aqi)
    if 1 <= aqi <= 5:
        print(f"Air Quality: {aqi_levels[aqi-1]}")
    else:
        print("Unknown AQI value")

            
def turn_on_single_led(led_number):
    # Define LED pins
    led_pins = {
        1: Pin(8, Pin.OUT),
        2: Pin(11, Pin.OUT),
        3: Pin(13, Pin.OUT),
        4: Pin(14, Pin.OUT),
        5: Pin(15, Pin.OUT),
    }
    # Turn off all LEDs
    for pin in led_pins.values():
        pin.value(0)
    # Turn on the specified LED
    if led_number in led_pins:
        led_pins[led_number].value(1)

def main():
    

    # Initialize LCD
    lcd = lcd1602.LCD()  # Replace with your LCD initialization

    # Initialize OLED
    i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

    def display_weather_lcd(weather_data):
        
        lcd.message("Welcome to \nPi Weather Tracker")
        time.sleep(3.5)
        for i in range(3):
            lcd.clear()
            lcd.message("City: " + weather_data["name"])
            time.sleep(3.5)  # Display for 3 seconds
            lcd.clear()
            
            lcd.message("Temp: " + str(weather_data["main"]["temp"]) + "C")
            lcd.message("\nFeels Like: " + str(weather_data["main"]["feels_like"]) + "C")
            time.sleep(3.5)  # Display for 3 seconds
            lcd.clear()
            
            lcd.message("Min Temp: " + str(weather_data["main"]["temp_min"]) + "C")
            lcd.message("\nMax Temp: " + str(weather_data["main"]["temp_max"]) + "C")
            time.sleep(3.5)  # Display for 3 seconds
            lcd.clear()
            
            lcd.message("Pressure: " + str(weather_data["main"]["pressure"]) + "hPa")
            lcd.message("\nHumidity: " + str(weather_data["main"]["humidity"]) + "%")
            time.sleep(3.5)  # Display for 3 seconds
            lcd.clear()
            
            lcd.message("Wind: " + str(weather_data["wind"]["speed"]) + "m/s")
            lcd.message("\nDirection: " + get_wind_direction(weather_data["wind"]["deg"]))
            time.sleep(3.5)  # Display for 3 seconds
            lcd.clear()
            aqi = air_pollution_data['list'][0]['main']['aqi']
            aqi_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
            aqi_level = aqi_levels[aqi - 1]
            lcd.message(f"AQI: {aqi_level}")
            time.sleep(3.5)  # Display for 3 seconds

        

    def display_weather_oled(weather_data, air_pollution_data):
        oled.fill(0)  # Clear OLED display
        if weather_data:
            oled.text(f"City: {weather_data['name']}", 0, 0)
            oled.text(f"Temp: {weather_data['main']['temp']}C", 0, 10)
            oled.text(f"Weather: {weather_data['weather'][0]['description']}", 0, 20)
            oled.text(f"Wind: {weather_data['wind']['speed']} m/s", 0, 30)
            oled.text(f"Humidity: {weather_data['main']['humidity']}%", 0, 40)
        else:
            oled.text("Weather data unavailable", 0, 0)

        if air_pollution_data:
            aqi = air_pollution_data['list'][0]['main']['aqi']
            aqi_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
            aqi_level = aqi_levels[aqi - 1]
            oled.text(f"AQI: {aqi_level}", 0, 50)
        else:
            oled.text("Air pollution data unavailable", 0, 50)

        oled.show()  # Update OLED display

    # Your OpenWeatherMap API key
    api_key = "babb2568d2f0a307fa4023b8ffd9a7ac"
    while True:
        # Get weather data
        # Fetch the URL from the server
        data = {"tag": "URL-adsxx"}
        data = "tag=" + data["tag"]  # Manually format the data as a URL-encoded string
        data = data.encode('utf-8')  # Encode the string into bytes
        url = "http://tinywebdb.appinventor.mit.edu/getvalue"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}  # Set the appropriate Content-Type header
        response = urequests.post(url, data=data, headers=headers)
        response_text = response.text

        # Extract the weather URL
        weather_url = read_url_from_response(response_text)
        if weather_url:
            weather_data = get_weather(weather_url)
            if weather_data:
                lat = weather_data["coord"]["lat"]
                lon = weather_data["coord"]["lon"]
                air_pollution_data = get_air_pollution(lat, lon, api_key)
                print_weather(weather_data)
                print_air_pollution(air_pollution_data)
                display_weather_oled(weather_data, air_pollution_data)
                display_weather_lcd(weather_data)
            else:
                print("Failed to get weather data")
        else:
            print("No valid weather URL found")

        time.sleep(3)


if __name__ == "__main__":
    main()






