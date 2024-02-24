import os
from fastapi import FastAPI
from starlette.responses import RedirectResponse
import httpx

github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
app = FastAPI()
access_token = None
client = httpx.AsyncClient(headers={'Accept': 'application/vnd.github.v3+json'})

@app.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@app.get("/github-code")
async def github_code(code: str):
    global access_token
    params = get_params(code)
    response = await make_request('post', 'https://github.com/login/oauth/access_token', params=params, headers={'Accept': 'application/json'})
    if 'access_token' in response:
        access_token = response['access_token']
        response = await make_request('get', 'https://api.github.com/user', headers={'Authorization': f'Bearer {access_token}'})
        return response
    else:
        return {"error": "access_token not found in response", "response": response}

@app.get("/starred-repos")
async def starred_repos():
    global access_token
    response = await make_request('get', 'https://api.github.com/user/starred', headers={'Authorization': f'Bearer {access_token}'})
    return create_repos_response(response)

@app.get("/starred-repos/{username}")
async def other_starred_repos(username: str):
    global access_token
    response = await make_request('get', f'https://api.github.com/users/{username}/starred', headers={'Authorization': f'Bearer {access_token}'})
    return create_repos_response(response)

async def make_request(method, url, **kwargs):
    response = await client.request(method, url, **kwargs)
    return response.json()

def create_repos_response(repos):
    repos_info = [
        {
            "name": repo["name"],
            "url": repo["html_url"],
            "license": repo["license"]["name"] if repo["license"] else None,
            "description": repo.get("description"),
            "topics": repo.get("topics")
        }
        for repo in repos
    ]
    return {"number_of_repos": len(repos_info), "repos": repos_info}

def get_params(code: str):
    return {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }