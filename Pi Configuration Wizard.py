import serial
import serial.tools.list_ports
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import tkinter.messagebox as tkMessageBox
import threading
import sys
import time

cap = None
cap_lock = threading.Lock()

def list_serial_ports():
    """ Lists all available serial ports. """
    return [port.device for port in serial.tools.list_ports.comports()]

def send_message():
    """ Sends the message to the selected serial port. """
    port = selected_port.get()
    ssid = ssid_entry.get()
    password = password_entry.get()
    
    if ssid and password:  # Manual mode
        message = f"SSID:{ssid}, Password:{password}$"
        send_to_port(port, message)
    else:
        tkMessageBox.showwarning("Incomplete Input", "Please enter both SSID and password.")

def send_to_port(port, message):
    """ Sends message to the selected serial port. """
    if port and message:
        try:
            with serial.Serial(port, 9600, timeout=1) as ser:
                ser.write((message + "\n").encode())  # Send the message with a newline character
            if message == 'reset':
                status_label.configure(text=" Reconfigure Weather Tracker ", text_color="yellow")
            else:
                status_label.configure(text="Message sent successfully", text_color="green")
        except serial.SerialException as e:
            status_label.configure(text=f"Error: {e}", text_color="red")
    else:
        status_label.configure(text="Please select a serial port and enter a message", text_color="red")

def send_reset():
    """ Sends a reset message to the selected serial port. """
    port = selected_port.get()
    if port:
        message = "#reset#"
        send_to_port(port, message)
    else:
        status_label.configure(text="Please select a serial port", text_color="red")

def scan_qr_code():
    """ Scans a QR code and displays the result. """
    def scan_qr():
        global cap
        with cap_lock:
            cap = cv2.VideoCapture(0)
            start_time = time.time()
            while time.time() - start_time < 20:
                ret, frame = cap.read()
                if not ret:
                    break
                decoded_objects = pyzbar.decode(frame)
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        handle_qr_data(obj.data.decode("utf-8"))
                        return
            if cap.isOpened():
                cap.release()
    
    # Start scanning in a separate thread
    qr_thread = threading.Thread(target=scan_qr)
    qr_thread.start()

def handle_qr_data(data):
    """Handles the scanned QR code data."""
    global cap
    if "S" in data and "P" in data:
        ssid_start = data.find("S:") + 2
        ssid_end = data.find(";", ssid_start)
        password_start = data.find("P:") + 2
        password_end = data.find(";", password_start)

        ssid = data[ssid_start:ssid_end]
        password = data[password_start:password_end]

        ssid_entry.delete(0, ctk.END)
        ssid_entry.insert(0, ssid)
        password_entry.delete(0, ctk.END)
        password_entry.insert(0, password)
        tkMessageBox.showinfo("QR Code Scanned", "SSID and Password filled automatically.")
    else:
        tkMessageBox.showwarning("Invalid QR Code", "The QR Code doesn't include SSID and PASSWORD")
    if cap is not None and cap.isOpened():
        cap.release()

def clear_fields():
    """Clears the content of the SSID and password entry fields."""
    ssid_entry.delete(0, ctk.END)
    password_entry.delete(0, ctk.END)


def on_closing():
    """Handle the close event."""
    global cap
    with cap_lock:
        if cap is not None and cap.isOpened():
            cap.release()
    root.quit()
    
# Create the main window
root = ctk.CTk()
root.title("WiFi Configuration")

# Set the appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Create a frame for the dropdown, entry, and button
frame = ctk.CTkFrame(root, corner_radius=10)
frame.grid(padx=20, pady=20, sticky="nsew")

# Dropdown for serial ports
serial_ports = list_serial_ports()
selected_port = ctk.StringVar()
port_dropdown = ctk.CTkComboBox(frame, variable=selected_port, values=serial_ports)
port_dropdown.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

# Label for dropdown
label = ctk.CTkLabel(frame, text="Select Serial Port:")
label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

# Entry for SSID
ssid_entry = ctk.CTkEntry(frame)
ssid_entry.grid(column=1, row=2, padx=10, pady=10, sticky="ew")

# Label for SSID entry
ssid_label = ctk.CTkLabel(frame, text="Enter SSID:")
ssid_label.grid(column=0, row=2, padx=10, pady=10, sticky="w")

# Entry for password
password_entry = ctk.CTkEntry(frame, show="*")
password_entry.grid(column=1, row=3, padx=10, pady=10, sticky="ew")

# Label for password entry
password_label = ctk.CTkLabel(frame, text="Enter Password:")
password_label.grid(column=0, row=3, padx=10, pady=10, sticky="w")

# Button for manual mode
manual_button = ctk.CTkButton(frame, text="Send Message", command=send_message)
manual_button.grid(column=1, row=4, padx=10, pady=10, sticky="ew")

# Button for automatic mode
auto_button = ctk.CTkButton(frame, text="Automatic Mode", command=scan_qr_code)
auto_button.grid(column=0, row=4, padx=10, pady=10, sticky="ew")

# Button for reset
reset_button = ctk.CTkButton(frame, text="Reset", command=send_reset)
reset_button.grid(column=1, row=5, padx=10, pady=10, sticky="ew")

# Create a button to clear fields
clear_button = ctk.CTkButton(frame, text="Clear Fields", command=clear_fields)
clear_button.grid(column=0, row=5, padx=10, pady=10, sticky="ew")

# Status label
status_label = ctk.CTkLabel(frame, text="")
status_label.grid(column=0, row=6, columnspan=2, padx=10, pady=10, sticky="ew")

# Set the window size fixed and not resizable
root.resizable(width=False, height=False)

# Set the window size
root.geometry("360x320")

# Bind the on_closing function to the WM_DELETE_WINDOW event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()

