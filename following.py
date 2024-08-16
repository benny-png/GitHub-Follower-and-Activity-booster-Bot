import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set it in the .env file.")

# URL for following a user
FOLLOW_URL = 'https://api.github.com/user/following/'

# Function to follow a user
def follow_user(username):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.put(FOLLOW_URL + username, headers=headers)

    # Check for rate limiting
    rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
    rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
    
    if response.status_code == 204:
        print(f'Successfully followed {username}')
    else:
        try:
            print(f'Failed to follow {username}: {response.json()}')
        except ValueError:
            print(f'Failed to follow {username}: {response.text}')
    
    # If rate limit is low, wait until it resets
    if rate_limit_remaining < 5:
        wait_time = max(rate_limit_reset - time.time(), 0)
        print(f"Rate limit almost reached. Waiting for {wait_time} seconds.")
        time.sleep(wait_time)

# Function to follow users from a file
def follow_users_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    for username in usernames:
        follow_user(username)
        # Sleep between requests to avoid rate limits
        time.sleep(2)

# Function to iterate through all text files in the project folder
def follow_users_from_all_text_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                follow_users_from_file(file_path)

if __name__ == "__main__":
    # Replace with the path to your project folder
    project_folder_path = './'
    follow_users_from_all_text_files(project_folder_path)
