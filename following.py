import aiohttp
import asyncio
import time
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Please set it in the .env file.")

BASE_URL = 'https://api.github.com'
FOLLOW_URL = f'{BASE_URL}/user/following/'
RATE_LIMIT_URL = f'{BASE_URL}/rate_limit'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GithubFollower:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.session = None

    async def create_session(self):
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def close_session(self):
        if self.session:
            await self.session.close()

    async def check_rate_limit(self):
        async with self.session.get(RATE_LIMIT_URL) as response:
            if response.status == 200:
                data = await response.json()
                remaining = data['resources']['core']['remaining']
                reset_time = data['resources']['core']['reset']
                if remaining < 5:
                    wait_time = max(reset_time - time.time(), 0)
                    logger.info(f"Rate limit almost reached. Waiting for {wait_time:.2f} seconds.")
                    await asyncio.sleep(wait_time)
            else:
                logger.error(f"Failed to check rate limit: {response.status}")

    async def follow_user(self, username):
        await self.check_rate_limit()
        
        # First, check if the user exists
        user_url = f'{BASE_URL}/users/{username}'
        async with self.session.get(user_url) as response:
            if response.status != 200:
                logger.warning(f"User {username} does not exist or is not accessible.")
                return

        async with self.session.put(FOLLOW_URL + username) as response:
            if response.status == 204:
                logger.info(f'Successfully followed {username}')
            else:
                error_msg = await response.text()
                logger.error(f'Failed to follow {username}: {error_msg}')

    async def follow_users_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                usernames = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return

        for username in usernames:
            await self.follow_user(username)
            await asyncio.sleep(1)  # Small delay between requests

    async def follow_users_from_all_text_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    logger.info(f"Processing file: {file_path}")
                    await self.follow_users_from_file(file_path)

async def main():
    follower = GithubFollower(GITHUB_TOKEN)
    await follower.create_session()
    try:
        project_folder_path = './'
        await follower.follow_users_from_all_text_files(project_folder_path)
    finally:
        await follower.close_session()

if __name__ == "__main__":
    asyncio.run(main())
