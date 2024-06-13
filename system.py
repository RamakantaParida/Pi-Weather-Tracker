import machine
import uasyncio as asyncio
import sys
import os

# Configure the onboard LED (on GPIO 25 for Pico)
led = machine.Pin('LED', machine.Pin.OUT)

async def blink_led(duration=0.5):
    """Blink the LED for the specified duration."""
    led.value(1)
    await asyncio.sleep(duration)
    led.value(0)

async def handle_command(command):
    """Handle the received command."""
    if command == '#reset#':
        await reset_file()
    else:
        await save_message(command)

async def reset_file():
    """Reset the message file."""
    try:
        os.remove("user.py")
        print("File removed.")
        await blink_led(3)  # Blink LED for longer duration
    except Exception as e:
        print(f"Error removing file: {e}")

async def save_message(message):
    """Save the received message to a file and blink the LED."""
    try:
        with open("user.py", "w") as file:
            file.write(message)  # write the message to the file
        print("Message saved to user.py")
        await blink_led()  # Blink LED for short duration
    except Exception as e:
        print(f"Error saving message: {e}")

async def read_serial():
    """Read commands from serial input and handle them."""
    while True:
        try:
            command = sys.stdin.readline().strip()  # Read a line from serial input
            if command:
                await handle_command(command)
        except Exception as e:
            print(f"Error reading serial input: {e}")
        await asyncio.sleep(0.1)  # Reduce CPU usage by yielding to other tasks

async def main():
    """Main coroutine to run the read_serial function."""
    await read_serial()

# Run the main coroutine
asyncio.run(main())


