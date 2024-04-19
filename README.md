# Email Monitoring Script

This project is a Python script that provides an alternative way to monitor email accounts without the need for configuring IMAP (Internet Message Access Protocol). Instead, it utilizes the Gmail web interface and requires only cookies to access the email accounts.

## Description

The script uses the `requests` library to make HTTP requests to the Gmail web interface, simulating a user's interaction with the interface. It retrieves email data by parsing the JSON response from the Gmail API.

### Main Components

- **EmailManager class**: This class encapsulates the functionality of the script. It handles the connection to the SQLite database, sends Telegram notifications, and manages the email processing logic.
- **gmail_load method**: This method sends a POST request to the Gmail web interface with the necessary cookies and headers to fetch email data in JSON format.
- **catch_emails method**: This method processes the email data received from the `gmail_load` method. It checks for new emails by comparing the email content and recipient address with the existing entries in the SQLite database. If a new email is found, it stores the email content and recipient address in the database and sends a notification to a Telegram chat.
- **process_account method**: This method handles the processing of a single email account. It reads the account cookies and headers from a file and calls the `gmail_load` and `catch_emails` methods.
- **run method**: This method orchestrates the processing of multiple email accounts concurrently using threads. It creates a new thread for each account and waits for all threads to complete before closing the database connection.

The script is designed to run continuously, monitoring multiple email accounts and sending notifications to a Telegram chat when new emails arrive. It provides an alternative solution for email monitoring without the need to configure IMAP, which can be useful in certain scenarios where IMAP access is not available or desired.

## Usage

1. Install the required dependencies by running:
pip install requests
2. Provide the necessary cookies and headers for each email account you want to monitor in separate files (e.g., `account1.txt`, `account2.txt`).
3. Update the `accounts` dictionary in the script with the email addresses and corresponding file paths.
4. Update the `chat_id` and `BOTID` variables in the `send_telegram_message` method with your Telegram chat ID and bot token, respectively.
5. Run the script using:


The script will continuously monitor the specified email accounts and send notifications to the Telegram chat whenever a new email arrives.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
