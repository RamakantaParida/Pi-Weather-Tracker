# Import required modules
from machine import Pin, I2C  # Pin and I2C setup
import ssd1306  # SSD1306 OLED driver
import random  # For random numbers
import time  # For time-based operations

# Constants for OLED display dimensions
WIDTH = 128  # Display width
HEIGHT = 64  # Display height

# Constants for star physics
NUM_STARS = 10  # Number of stars
GRAVITY = 1  # Falling speed (gravity)
WIND = 1  # Horizontal drift (wind)

# I2C setup for SSD1306 (adjust sda and scl pins if needed)
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)  # I2C frequency set to 400kHz
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)  # OLED initialization

# Define a function to draw a smaller star pattern
def draw_star(x, y):
    # Draw a smaller star centered at (x, y) with a 3x3 size
    size = 4  # Smaller star size (3x3)
    oled.pixel(x, y - size, 1)  # Top point
    oled.pixel(x, y + size, 1)  # Bottom point
    oled.pixel(x - size, y, 1)  # Left point
    oled.pixel(x + size, y, 1)  # Right point
    oled.pixel(x, y, 1)  # Center point

# Star class for physics and reset behavior
class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        # Start from a random position at the top
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(-HEIGHT, 0)  # Start above the top
        self.vx = random.uniform(-WIND, WIND)  # Horizontal drift
        self.vy = GRAVITY  # Falling speed

    def update(self):
        # Update position based on velocities
        self.x += self.vx  # Horizontal movement
        self.y += self.vy  # Vertical movement

        # Apply wind drift occasionally
        if random.random() < 0.2:
            self.vx += random.uniform(-WIND / 2, WIND / 2)

        # Keep star within display boundaries
        if self.x < 0:
            self.x = 0
            self.vx *= -1  # Bounce back at left edge
        elif self.x >= WIDTH:
            self.x = WIDTH - 1
            self.vx *= -1  # Bounce back at right edge

        # Reset if it falls out of view
        if self.y >= HEIGHT:
            self.reset()

# Create multiple star objects
stars = [Star() for _ in range(NUM_STARS)]

# Main loop to simulate falling stars and display the text
while True:
    # Clear the display
    oled.fill(0)

    # Draw the text "SNOW" at the center
    text = "SNOW"  # Text to display
    text_width = len(text) * 8  # Approximate width (8 pixels per character)
    x_pos = (WIDTH - text_width) // 2  # Centered horizontally
    y_pos = (HEIGHT - 8) // 2  # Centered vertically (approximate character height is 8)
    oled.text(text, x_pos, y_pos)  # Display the text "SNOW"

    # Update and draw the stars
    for star in stars:
        star.update()  # Update position
        draw_star(int(star.x), int(star.y))  # Draw the smaller star pattern

    # Refresh the display
    oled.show()  # Display the updated content

    # Pause to control animation speed
    time.sleep(0.05)  # Adjust to control speed

