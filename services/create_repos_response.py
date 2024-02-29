def create_repos_response(repos):
    repos_info = [
        {
            "name": repo["name"],
            "url": repo["html_url"],
            "license": repo["license"]["name"] if repo.get("license") else None,
            "description": repo.get("description"),
            "topics": repo.get("topics")
        }
        if repo.get("license")
        else
        {
            "name": repo["name"],
            "url": repo["html_url"],
            "description": repo.get("description"),
            "topics": repo.get("topics")
        }
        for repo in repos
        if not repo.get("private")
    ]
    return {"number_of_repos": len(repos_info), "repos": repos_info}