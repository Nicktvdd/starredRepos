import os

github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

def get_params(code: str):
    return {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }