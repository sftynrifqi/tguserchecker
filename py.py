from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
import time

# List of 5 different accounts with API IDs and hashes
accounts = [
    {'api_id': 'your_api_id1', 'api_hash': 'your_api_hash1'},
    {'api_id': 'your_api_id2', 'api_hash': 'your_api_hash2'},
    {'api_id': 'your_api_id3', 'api_hash': 'your_api_hash3'},
    {'api_id': 'your_api_id4', 'api_hash': 'your_api_hash4'},
    {'api_id': 'your_api_id5', 'api_hash': 'your_api_hash5'}
]

# List of usernames to check
usernames = ['username1', 'username2', 'username3', 'username4', 'username5', 'username6']

# Function to check a username
def check_username(client, username):
    try:
        result = client(ResolveUsernameRequest(username))
        print(f"Username @{username} is taken.")
    except:
        print(f"Username @{username} is available.")

# Function to rotate accounts and check usernames
def rotate_accounts(usernames, accounts):
    account_index = 0
    for i, username in enumerate(usernames):
        # Get current account
        current_account = accounts[account_index]

        # Log into the current account
        with TelegramClient(f'session_{account_index}', current_account['api_id'], current_account['api_hash']) as client:
            check_username(client, username)

        # Rotate accounts every 5 checks or if at the last account, reset to the first
        if (i + 1) % 5 == 0:
            account_index = (account_index + 1) % len(accounts)

        # Sleep to avoid rate limiting
        time.sleep(1)  # You can increase this if you still hit limits

# Run the username checking with account rotation
rotate_accounts(usernames, accounts)
