import pytesseract
import pyautogui
import keyboard
import cv2
import numpy as np
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_tessdata_dir = r'trained_data'
pytesseract.pytesseract.tessdata_dir_config = f'--tessdata-dir "{custom_tessdata_dir}"'

# Initialize variables
capturing = False
dps_sum = 0

# Screen size
screen_width, screen_height = pyautogui.size()

# Define margins
margin_top_bottom = 150
margin_sides= 370 # space from the edge

roi = (
    margin_sides, # x
    margin_top_bottom, # y
    screen_width - 2 * margin_sides,
    screen_height - 2 * margin_top_bottom
)

# Preprocess
def preprocess_image(image):
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color range for yellowish-orange numbers
    lower_color = np.array([15, 100, 100])
    upper_color = np.array([35, 255, 255])

    # Apply color filter
    mask = cv2.inRange(hsv, lower_color, upper_color)
    filtered_image = cv2.bitwise_and(image, image, mask=mask)

    # Convert to grayscale
    gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Use morphological operations to enhance the digits
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return morph

# Capture screen and perform OCR
def capture_screen():
    global dps_sum
    screenshot = pyautogui.screenshot(region=roi)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    preprocessed_image = preprocess_image(screenshot)
    # Debugging
    #cv2.imshow('Captured Region', screenshot)
    #cv2.imshow('Preprocessed Region', preprocessed_image)


    #cv2.imwrite('captured_region.png', screenshot)
    #cv2.imwrite('preprocessed_region.png', preprocessed_image)

    text = pytesseract.image_to_string(preprocessed_image, config='--psm 6')
    print("Captured Text:", text) # Debug
    numbers = [int(s) for s in text.split() if s.isdigit()]
    dps_sum += sum(numbers)
    print("Current DPS Sum:", dps_sum) # Debug:

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Function to handle hotkey press
def on_hotkey_start():
    global capturing
    capturing = True
    print("Capturing started")

def on_hotkey_stop():
    global capturing
    capturing = False
    print("Capturing stopped.")
    print(f"Total DPS: {dps_sum}")

# Bind hotkeys
keyboard.add_hotkey('ctrl+shift+s', on_hotkey_start)
keyboard.add_hotkey('ctrl+shift+e', on_hotkey_stop)

# Main loop
print("Press 'Ctrl+Shift+S' to start capturing and 'Ctrl+Shift+E' to stop.")

def main_loop():
    while True:
        if capturing:
            capture_screen()
        if keyboard.is_pressed('esc'):  # Press 'esc' to exit the program
            break

def debug_loop():
    while True:
        if capturing:
            capture_screen()
            break
        if keyboard.is_pressed('esc'):  # Press 'esc' to exit the program
            break

#debug_loop()
main_loop()
cv2.destroyAllWindows()