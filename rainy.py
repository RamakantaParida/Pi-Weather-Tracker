from machine import Pin, I2C
import ssd1306
import uos
import time

# Create I2C object
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Create lists to hold raindrops and splash particles
raindrops = []
splashes = []

# Constants for physics simulation
GRAVITY = 0.2  # Gravity constant
SPLASH_VELOCITY = 1.5  # Initial velocity for splashes
BASELINE = 63  # Baseline row for raindrops to burst

# Function to create a new raindrop at a random x position
def create_raindrop():
    x = uos.urandom(1)[0] % 128  # Random x position
    raindrops.append({'x': x, 'y': 0, 'velocity': 0})

# Function to create splash particles when a raindrop hits the baseline
def create_splash(x):
    num_splashes = 6  # Number of particles in the splash
    spread = 12  # Horizontal spread
    for i in range(-num_splashes // 2, num_splashes // 2):
        initial_velocity = SPLASH_VELOCITY + (uos.urandom(1)[0] % 5) / 10  # Random additional velocity
        offset = (spread // (num_splashes - 1)) * i
        splashes.append({
            'x': x + offset,
            'y': BASELINE,
            'velocity': -initial_velocity,
            'gravity': GRAVITY
        })

# Function to update the raindrops
def update_raindrops():
    for drop in raindrops.copy():
        drop['velocity'] += GRAVITY  # Apply gravity
        drop['y'] += drop['velocity']  # Move down with velocity
        if drop['y'] >= BASELINE:  # If it hits the baseline, create splash
            raindrops.remove(drop)
            create_splash(drop['x'])

# Function to update splash particles
def update_splashes():
    for splash in splashes.copy():
        splash['velocity'] += splash['gravity']  # Apply gravity
        splash['y'] += splash['velocity']  # Move with velocity
        if splash['y'] > BASELINE:  # Remove if below baseline
            splashes.remove(splash)

# Function to draw the background text "RAIN"
def draw_background_text():
    # Calculate the position to center the text
    text = "RAIN"
    text_width = 7 * len(text)  # Each character is 7 pixels wide
    text_height = 10  # Text height
    x_center = (128 - text_width) // 2  # Center horizontally
    y_center = (64 - text_height) // 2  # Center vertically
    oled.text(text, x_center, y_center, 1)  # Draw the text

# Function to draw the raindrops and splash particles
def draw_raindrops_and_splashes():
    oled.fill(0)  # Clear the screen
    draw_background_text()  # Draw the background text
#    oled.line(0, BASELINE, 127, BASELINE, 1)  # Baseline
    for drop in raindrops:
        oled.pixel(drop['x'], int(drop['y']), 1)  # Draw raindrops
    for splash in splashes:
        oled.pixel(splash['x'], int(splash['y']), 1)  # Draw splash particles
    oled.show()  # Update the display

# Main loop with delay for smooth animation
while True:
    if len(raindrops) < 10 and uos.urandom(1)[0] < 50:
        create_raindrop()  # Create a new drop if fewer than 10
    update_raindrops()  # Update raindrops
    update_splashes()  # Update splash particles
    draw_raindrops_and_splashes()  # Draw both raindrops and splash particles
    time.sleep(0.05)  # Delay to control animation speed

