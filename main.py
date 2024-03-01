from fastapi import FastAPI, Cookie, HTTPException, Response
from starlette.responses import RedirectResponse
from services.create_repos_response import create_repos_response
from services.get_params import get_params, github_client_id
from services.make_request import make_request

app = FastAPI()

@app.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@app.get("/github-code")
async def github_code(response: Response, code: str):
    params = get_params(code)
    response_data = await make_request('post', 'https://github.com/login/oauth/access_token', params=params, headers={'Accept': 'application/json'})
    if 'access_token' in response_data:
        response.set_cookie(key="access_token", value=response_data['access_token'], httponly=True)
        user_data = await make_request('get', 'https://api.github.com/user', headers={'Authorization': f'Bearer {response_data["access_token"]}'})
        return user_data
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/starred-repos")
async def starred_repos(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await make_request('get', 'https://api.github.com/user/starred', headers={'Authorization': f'Bearer {access_token}'})
    return create_repos_response(response)

@app.get("/starred-repos/{username}")
async def other_starred_repos(username: str, access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = await make_request('get', f'https://api.github.com/users/{username}/starred', headers={'Authorization': f'Bearer {access_token}'})
    return create_repos_response(response)