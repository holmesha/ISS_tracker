from machine import Pin
import network
import time
import urequests
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
from pngdec import PNG
from secrets import secrets
from pong import pong  # Import Pong module

# Set up the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)

# Define colors
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)
GREY = display.create_pen(90, 90, 90)

# Set up buttons with PULL_UP
button_A = Pin(12, Pin.IN, Pin.PULL_UP)  # Toggle Grid
button_B = Pin(13, Pin.IN, Pin.PULL_UP)  # Toggle Path
button_X = Pin(14, Pin.IN, Pin.PULL_UP)  # Switch to Pong
button_Y = Pin(15, Pin.IN, Pin.PULL_UP)  # Placeholder for future feature

# Variables
show_grid = True
show_path = False
iss_path = []        # Stores past coordinates
path_counter = 0     # Saves every 10th position

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets["ssid"], secrets["password"])

    print("Connecting to Wi-Fi...")
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("\nConnected! IP:", wlan.ifconfig()[0])
        return True
    else:
        print("\nFailed to connect to Wi-Fi.")
        return False

# Fetch ISS position
def get_iss_position():
    try:
        response = urequests.get("http://api.wheretheiss.at/v1/satellites/25544")
        data = response.json()
        response.close()
        return float(data['latitude']), float(data['longitude'])
    except:
        return None, None

# Map lat/lon to screen coordinates
def map_coords(lat, lon, width=320, height=240):
    x = int((lon + 180) * (width / 360))  # Longitude (-180 to 180)
    y = int((90 - lat) * (height / 180))  # Latitude (90 to -90)
    return x, y

# Draw the world map
def draw_world_map():
    try:
        png = PNG(display)
        png.open_file("worldmap.png")
        png.decode(0, 0)
    except:
        display.set_pen(BLACK)
        display.clear()
        display.text("Map Load Error!", 10, 10, scale=2)

# Draw the grid
def draw_grid():
    display.set_pen(GREY)
    for x in range(0, 320, 20):
        display.line(x, 0, x, 240)  # Vertical lines
    for y in range(0, 240, 20):
        display.line(0, y, 320, y)  # Horizontal lines

# Draw the ISS path (connect saved points)
def draw_path():
    display.set_pen(RED)
    for i in range(1, len(iss_path)):
        x1, y1 = iss_path[i - 1]
        x2, y2 = iss_path[i]
        display.line(x1, y1, x2, y2)

# Handle button inputs
def handle_buttons():
    global show_grid, show_path

    # Toggle Grid (Button A)
    if button_A.value() == 0:
        show_grid = not show_grid
        time.sleep(0.1)
        print("grid toggled")

    # Toggle Path (Button B)
    if button_B.value() == 0:
        show_path = not show_path
        time.sleep(0.1)
        print("ISS path toggled")

    # Switch to Pong (Button X)
    if button_X.value() == 0:
        pong()  # Run Pong game

    # Placeholder for Y Button (ISS mode)
    if button_Y.value() == 0:
        time.sleep(0.1)

# Update ISS position and path
def update_iss():
    global path_counter

    while True:
        # Get ISS position
        lat, lon = get_iss_position()
        if lat is not None and lon is not None:
            # Map coordinates
            x, y = map_coords(lat, lon)

            # Save every 10th point for path
            path_counter += 1
            if path_counter % 10 == 0:
                iss_path.append((x, y))
                if len(iss_path) > 50:  # Limit to 50 points
                    iss_path.pop(0)

            # Draw map, grid, and path
            draw_world_map()
            if show_grid:
                draw_grid()
            if show_path:
                draw_path()

            # Draw ISS position
            display.set_pen(RED)
            display.circle(x, y, 5)

            # Display coordinates
            display.set_pen(BLACK)
            display.text(f"Lat: {lat:.2f}", 10, 200, scale=2)
            display.text(f"Lon: {lon:.2f}", 10, 220, scale=2)
            
            # Title text
            display.set_pen(BLACK)
            display.text("ISS Tracker", 10, 10, scale=2)

            display.update()
            print(f"ISS Position: Lat {lat}, Lon {lon}")
        else:
            print("Unable to fetch ISS position.")

        # Handle button inputs
        handle_buttons()
        time.sleep(0.1)

# Main program
try:
    if connect_wifi():
        display.set_backlight(1.0)  # Turn on backlight
        update_iss()  # Start tracking ISS
except KeyboardInterrupt:
    pass
