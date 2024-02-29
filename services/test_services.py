from .create_repos_response import create_repos_response
from .get_params import github_client_id, github_client_secret, get_params
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_repos_response_unlicensed():
    repos = [{'name': 'repo1', 'html_url': 'url1', 'license': None, 'description': 'desc1', 'topics': ['topic1']}]
    response = create_repos_response(repos)
    assert response == {"number_of_repos": 1, "repos": [{'name': 'repo1', 'url': 'url1', 'description': 'desc1', 'topics': ['topic1']}]}

def test_create_repos_response_private():
    repos = [{'name': 'repo1', 'html_url': 'url1', 'license': None, 'description': 'desc1', 'topics': ['topic1'], 'private': True}]
    response = create_repos_response(repos)
    print(response)
    assert response == {'number_of_repos': 0, 'repos': []}
    
def test_create_repos_response_licensed():
    repos = [{'name': 'repo1', 'html_url': 'url1', 'license': {"name": "MIT license"}, 'description': 'desc1', 'topics': ['topic1']}]
    response = create_repos_response(repos)
    assert response == {"number_of_repos": 1, "repos": [{'name': 'repo1', 'url': 'url1', 'license': "MIT license", 'description': 'desc1', 'topics': ['topic1']}]}

def test_get_params():
    code = 'test_code'
    params = get_params(code)
    assert params == {'client_id': github_client_id, 'client_secret': github_client_secret, 'code': code}