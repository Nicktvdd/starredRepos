from fastapi.testclient import TestClient
from unittest.mock import patch
from .main import app, create_repos_response, get_params, make_request, github_client_id, github_client_secret

client = TestClient(app)

def test_github_login():
    response = client.get("/github-login")
    assert response.status_code == 302
    assert "https://github.com/login/oauth/authorize?client_id=9a7876c6aef4703c61b2" in response.headers["location"]

@patch('starredRepos.main.make_request')
def test_github_code(mock_make_request):
    mock_make_request.return_value = {'access_token': 'mock_token'}
    response = client.get("/github-code?code=test_code")
    assert response.status_code == 200
    assert 'access_token' in response.json()

@patch('starredRepos.main.make_request')
def test_starred_repos(mock_make_request):
    mock_make_request.return_value = [{'name': 'repo1', 'html_url': 'url1', 'license': None, 'description': 'desc1', 'topics': ['topic1']}]
    response = client.get("/starred-repos")
    assert response.status_code == 200
    assert response.json() == create_repos_response(mock_make_request.return_value)

@patch('starredRepos.main.make_request')
def test_other_starred_repos(mock_make_request):
    mock_make_request.return_value = [{'name': 'repo2', 'html_url': 'url1', 'license': None, 'description': 'desc1', 'topics': ['topic1']}]
    response = client.get("/starred-repos/test_user")
    assert response.status_code == 200
    assert response.json() == create_repos_response(mock_make_request.return_value)

@patch('starredRepos.main.make_request')
def test_make_request(mock_make_request):
    mock_make_request.return_value = {'status': 'success'}
    response = make_request('GET', 'https://api.github.com/repos/test_user/test_repo')
    assert response == {'status': 'success'}

def test_create_repos_response():
    repos = [{'name': 'repo1', 'html_url': 'url1', 'license': None, 'description': 'desc1', 'topics': ['topic1']}]
    response = create_repos_response(repos)
    assert response == {"number_of_repos": 1, "repos": [{'name': 'repo1', 'url': 'url1', 'license': None, 'description': 'desc1', 'topics': ['topic1']}]}
    
def test_get_params():
    code = 'test_code'
    params = get_params(code)
    assert params == {'client_id': github_client_id, 'client_secret': github_client_secret, 'code': code}
