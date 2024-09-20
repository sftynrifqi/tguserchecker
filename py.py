from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
import time

# List of 5 different accounts with API IDs and hashes
accounts = [
    {'api_id': 'api_id1', 'api_hash': 'api_hash1'},
    {'api_id': 'api_id2', 'api_hash': 'api_hash2'},
    {'api_id': 'api_id3', 'api_hash': 'api_hash3'},
    {'api_id': 'api_id4', 'api_hash': 'api_hash4'},
    {'api_id': 'api_id5', 'api_hash': 'api_hash5'}
]

# Load usernames from an external file
def load_usernames(filename):
    with open(filename, 'r') as file:
        usernames = file.read().splitlines()
    return usernames

# Function to check a username and log result to a file
def check_username(client, username, result_file):
    try:
        result = client(ResolveUsernameRequest(username))
        result_text = f"Username @{username} is taken."
    except:
        result_text = f"Username @{username} is available."

    # Log the result to the console and the result file
    print(result_text)
    with open(result_file, 'a') as file:
        file.write(result_text + '\n')

# Function to rotate accounts and check usernames
def rotate_accounts(usernames, accounts, result_file):
    account_index = 0  # Start with the first account
    for i, username in enumerate(usernames):
        # Get current account
        current_account = accounts[account_index]

        # Log into the current account
        with TelegramClient(f'session_{account_index}', current_account['api_id'], current_account['api_hash']) as client:
            check_username(client, username, result_file)

        # Rotate accounts every 5 checks or if at the last account, reset to the first
        if (i + 1) % 5 == 0:  # Switch account every 5 usernames
            account_index = (account_index + 1) % len(accounts)  # Cycle through accounts

        # Sleep to avoid rate limiting
        time.sleep(1)  # Adjust this delay if needed

# Load usernames from the file and start the checking process
if __name__ == "__main__":
    username_list = load_usernames('usernames.txt')  # Load usernames from file
    result_file = 'result.txt'  # File to store results
    # Clear previous results in result.txt
    open(result_file, 'w').close()  # Clear the file before writing new results
    rotate_accounts(username_list, accounts, result_file)  # Start checking with account rotation
