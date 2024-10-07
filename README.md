# Python Keylogger with Encryption and Anomaly Detection

This project is a **Python-based keylogger** that records keypresses, saves them to a log file, and offers encryption for secure log storage. The keylogger also includes **basic anomaly detection** for monitoring unusual typing patterns, like rapid typing or excessive key repetitions.

## Features

- **Keypress Logging**: Captures all key presses and stores them in a log file.
- **Log Encryption**: Uses `Fernet` symmetric encryption to secure the log file. The encryption key is generated and stored locally.
- **Log Decryption**: Decrypts the encrypted log file for viewing the raw keypress logs.
- **Anomaly Detection**:
  - **Typing Speed**: Detects and alerts when keys are pressed too quickly (average time between key presses).
  - **Character Frequency**: Detects repeated excessive keystrokes (e.g., holding a key).
- **CLI Interface**: Allows users to start/stop the keylogger, view decrypted logs, clear logs, and configure file paths.
- **Environment Configuration**: Log and encryption file paths are configurable through environment variables.

## How It Works

### 1. Keypress Logging
The keylogger captures every key press, including special keys (e.g., Enter, Backspace, Tab) and stores them in a log file. It uses the `pynput` library to listen for keyboard events.

### 2. Encryption and Decryption
- **Encryption**: When logging is stopped (via pressing the `ESC` key), the program encrypts the log file using `Fernet` encryption. The raw log file is deleted after encryption, and the encrypted version is saved in a separate file.
- **Decryption**: The user can decrypt the log file through the CLI and view its contents if the file is encrypted.

### 3. Anomaly Detection
- **Typing Speed**: The program measures the time intervals between consecutive key presses. If the average interval between key presses is too low (e.g., less than 0.05 seconds), it flags a potential anomaly.
- **Character Frequency**: The program tracks how often each character is pressed. If a character is pressed more than 100 times, it flags a potential anomaly for repeated key usage.

## Prerequisites

Before running the keylogger, you need to set the paths for your log and encrypted files. This is done through environment variables stored in a `.env` file.

### `.env` Example:

- `log_file`: The path where raw logs will be stored.
- `encrypted_file`: The path where encrypted logs will be saved.

## Key Files

- **`key.key`**: The generated encryption key for encrypting and decrypting the log file. It is created when the program runs for the first time if it doesn't already exist.
- **Log File**: The file where keystrokes are stored.
- **Encrypted File**: The encrypted version of the log file.

## How to Use the Keylogger

### 1. Run the Program
To start the program, execute the following command:
```bash
python keylogger.py
```
### CLI Menu

Keylogger Menu:
1. Start logging
2. Decrypt logs
3. View logs (must decrypt first)
4. Clear logs
5. Configure file paths
6. Exit

### Keylogging

- Choose option `1` to start logging.
- Press `ESC` to stop logging, which will automatically encrypt the log file.

### Decryption 

- After stopping the keylogger, choose option `2` to decrypt the logs.
- You can then choose option `3` to view the decrypted logs.

### Clearing Logs

- Choose option 4 to clear the logs if needed.

### Configuring File Paths

- Use option `5` to change the paths of the log and encrypted files during runtime.

## Code Breakdown

### Key Functions

- `generate_key()`: Generates a new `Fernet` encryption key and saves it in `key.key`.
- `load_key()`: Loads the encryption key from `key.key`. If the key does not exist, it generates a new one.
- `encrypt_log_file()`: Encrypts the contents of the log file and saves the encrypted data to the encrypted file.
- `decrypt_log_file()`: Decrypts the encrypted file and saves the result in the log file for viewing.
- `on_press()`: Captures keypress events and logs them to the log file.
- `on_release()`: Stops the keylogger when the ESC key is pressed and triggers encryption of the logs.
- `detect_anomalies()`: Detects anomalies based on typing speed and character frequency.

### Anomaly Detection

The program monitors typing patterns and flags:

- Fast Typing: If the average time between key presses is less than 0.05 seconds.
- Frequent Characters: If a character is pressed more than 100 times.

## Usage warning

This project is for educational purposes only. Unauthorized use of keyloggers is illegal and unethical. Always seek permission before using this tool.