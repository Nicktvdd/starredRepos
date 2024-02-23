import os
from fastapi import FastAPI
from starlette.responses import RedirectResponse
import httpx

github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

app = FastAPI()

# Global variable to store the access token
access_token = None

@app.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@app.get("/github-code")
async def github_code(code: str):
    global access_token
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }
    headers = {
        'Accept': 'application/json'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
    response_json = response.json()
    print(response_json)
    access_token = response_json['access_token']
    headers.update({'Authorization': f'Bearer {access_token}'})
    async with httpx.AsyncClient() as client:
        response = await client.get(url='https://api.github.com/user', headers=headers)
    return response.json()

@app.get("/starred-repos")
async def starred_repos():
    global access_token
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {access_token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url='https://api.github.com/user/starred', headers=headers)
    return response.json()