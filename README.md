# GitHub Follower Bot

This Python script automates the process of following GitHub users based on a list of usernames stored in text files. It uses the GitHub API and `aiohttp` for asynchronous HTTP requests, allowing for efficient management of API rate limits and network resources.

## Features

- **Load Environment Variables**: The script loads your GitHub API token from a `.env` file.
- **Check Rate Limits**: It checks the GitHub API rate limit before making requests to ensure compliance with GitHub's API usage policies.
- **Follow Users**: The script can follow GitHub users from a list of usernames specified in text files.
- **Asynchronous Operations**: Utilizing Python's `asyncio` and `aiohttp`, the script can perform multiple follow operations concurrently, making it faster and more efficient.

## Installation

1. Clone this repository to your local machine.
2. Ensure you have Python 3.7+ installed.
3. Install the required Python packages:

   ```bash
   pip install aiohttp python-dotenv
   ```

4. Create a `.env` file in the root directory of the project and add your GitHub token:

   ```env
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

1. **Prepare Usernames**: Create a directory named `usernames` in the project root. Inside this directory, create text files where each file contains a list of GitHub usernames, one per line.

2. **Run the Script**: Execute the script by running:

   ```bash
   python your_script_name.py
   ```

3. **Log Output**: The script logs its progress, including rate limit checks, successful follows, and any errors encountered.

## Example

If you have a text file named `usernames.txt` in the `usernames` directory with the following content:

```
octocat
torvalds
mojombo
```

The script will attempt to follow these users on GitHub.

## Importance

### 1. **Connecting with Specific People**
   This script is particularly useful for individuals or organizations looking to build meaningful connections on GitHub. By following specific users, you can connect with influencers, potential collaborators, or contributors in your field.

### 2. **Boosting Profile Activity**
   Following users can boost your GitHub profile activity. It shows engagement within the community and can increase the likelihood of users following you back, thereby expanding your network.

### 3. **Networking Automation**
   Instead of manually following users one by one, this script automates the process, saving time and ensuring consistency in your outreach efforts.

## Note

- Make sure to handle your GitHub API token securely.
- Respect GitHub’s rate limits and API usage policies to avoid being rate-limited or banned.
- This script is intended for personal use; make sure to follow GitHub's terms of service regarding automated interactions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
