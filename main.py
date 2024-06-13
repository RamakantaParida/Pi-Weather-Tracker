import network
import socket
import time
import weather_display


# Read Wifi Credentials
def read_wifi_credentials():
    try:
        with open("user.py", "r") as file:
            content = file.read()
            SSID = content.split("SSID:")[1].split(",")[0].strip()
            PASSWORD = content.split("Password:")[1].strip()
        return SSID, PASSWORD
    except IndexError:
        print("Error: Incorrect file format.")
        return None, None

    
SSID, PASSWORD = read_wifi_credentials()

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print("Connecting to Wi-Fi...", end="")
    
    while not wlan.isconnected() and wlan.status() >= 0:
        print(".", end="")
        time.sleep(1)
    
    if wlan.isconnected():
        print("\nConnected to Wi-Fi.")
        print("Network config:", wlan.ifconfig())
        return wlan.ifconfig()[0]  # Return the IP address
    else:
        print("\nFailed to connect to Wi-Fi.")
        return None



# Main execution
while True:
    ip_address = connect_to_wifi(SSID, PASSWORD)  
    if ip_address:
        weather_display.main()
    else:
        print("Failed to connect to Wi-Fi. Exiting.")





