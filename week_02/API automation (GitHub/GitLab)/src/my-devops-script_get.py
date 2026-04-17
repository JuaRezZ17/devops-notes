import requests
import os

# 1. We retrieve the token from the environment variable
token = os.getenv("GITHUB_TOKEN")

if not token:
    print("Error: The variable GITHUB_TOKEN was not found")
    exit()

# 2. Configuration of the header (Bearer Token)
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# 3. GET request to the GitHub API
response = requests.get("https://api.github.com/user/repos?type=public", headers=headers)

if response.status_code == 200:
    repos = response.json()
    print(f"You have found {len(repos)} public repositories:")
    for repo in repos:
        print(f"- {repo['name']}")
else:
    print(f"Error {response.status_code}: {response.text}")