import math
import time
from machine import Pin, I2C
import ssd1306

# Initialize I2C for OLED display (pin setup may vary)
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)



# Sun parameters
center_x = 32  # Center x-position for the sun (to keep it on the left side)
center_y = oled.height // 2  # Center y-position (middle of the screen)
sun_radius = 10  # Radius of the sun
ray_count = 18  # Number of rays
base_ray_length = 15  # Base length of the rays
oscillation_frequency = 1.0  # Frequency of oscillation
oscillation_amplitude = 1.5  # Maximum length change during oscillation
t = 0.5  # Time variable for oscillation

# Function to draw a filled circle (for the sun)
def draw_filled_circle(cx, cy, r):
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x * x + y * y <= r * r:
                oled.pixel(cx + x, cy + y, 1)

# Function to smooth oscillation for the rays
def smooth_oscillation(t, frequency, amplitude):
    return amplitude * math.sin(t * frequency)

# Main animation loop
while True:
    oled.fill(0)  # Clear the display
    
    # Increment time for oscillation
    t += 0.1
    
    # Draw the sun
    draw_filled_circle(center_x, center_y, sun_radius)

    # Draw rays with smooth oscillation
    for i in range(ray_count):
        angle = 2 * math.pi * i / ray_count
        ray_length = base_ray_length + smooth_oscillation(t, oscillation_frequency, oscillation_amplitude)

        ray_end_x = int(center_x + math.cos(angle) * ray_length)
        ray_end_y = int(center_y + math.sin(angle) * ray_length)

        # Draw the rays
        oled.line(center_x, center_y, ray_end_x, ray_end_y, 1)

    # Write text on the right side
    oled.text("Sunny", 70, center_y - 5)  # Position text on the right side
    
    # Refresh display
    oled.show()

    # Add a slight delay to smooth the animation
    time.sleep(0.1)  
