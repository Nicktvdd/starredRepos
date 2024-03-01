from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from services.create_repos_response import create_repos_response
from services.get_params import get_params, github_client_id
from services.make_request import make_request

app = FastAPI()
access_token = None

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
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/starred-repos")
async def starred_repos():
    global access_token
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await make_request('get', 'https://api.github.com/user/starred', headers={'Authorization': f'Bearer {access_token}'})
    return create_repos_response(response)

@app.get("/starred-repos/{username}")
async def other_starred_repos(username: str):
    global access_token
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await make_request('get', f'https://api.github.com/users/{username}/starred', headers={'Authorization': f'Bearer {access_token}'})
    return create_repos_response(response)
