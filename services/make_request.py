import httpx

client = httpx.AsyncClient(headers={'Accept': 'application/vnd.github.v3+json'})

async def make_request(method, url, **kwargs):
    response = await client.request(method, url, **kwargs)
    return response.json()