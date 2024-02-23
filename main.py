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
    starred_repos = response.json()
    repos_info = []
    for repo in starred_repos:
        if not repo["private"]:
            repo_info = {"name": repo["name"], "url": repo["html_url"]}
            if repo["license"]:
                repo_info["license"] = repo["license"]["name"]
            if repo["description"]:
                repo_info["description"] = repo["description"]
            if repo["topics"]:
                repo_info["topics"] = repo["topics"]
            repos_info.append(repo_info)
    return {"number_of_starred_repos": len(repos_info), "repos": repos_info}

@app.get("/starred-repos/{username}")
async def other_starred_repos(username: str):
    global access_token
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {access_token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f'https://api.github.com/users/{username}/starred', headers=headers)
    starred_repos = response.json()
    repos_info = []
    for repo in starred_repos:
        repo_info = {"name": repo["name"], "url": repo["html_url"]}
        if repo["license"]:
            repo_info["license"] = repo["license"]["name"]
        if repo["description"]:
            repo_info["description"] = repo["description"]
        if repo["topics"]:
            repo_info["topics"] = repo["topics"]
        repos_info.append(repo_info)
    return {"number_of_starred_repos": len(repos_info), "repos": repos_info}
