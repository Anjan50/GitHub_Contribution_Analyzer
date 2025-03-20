from typing import Dict, Any, Optional
from flask import session

from app.services.github_query.github_graphql.client import (
    Client,
    QueryFailedException,
)
from app.services.github_query.github_graphql.authentication import (
    PersonalAccessTokenAuthenticator,
)

from app.services.github_query.queries.contributions.user_gists import (UserGists)
from app.services.github_query.queries.contributions.user_issues import (UserIssues)
from app.services.github_query.queries.contributions.user_pull_requests import (UserPullRequests)
from app.services.github_query.queries.contributions.user_repositories import (UserRepositories)
from app.services.github_query.queries.contributions.user_repository_discussions import (UserRepositoryDiscussions)

def get_user_gists(user:str,pg_size:int=100)-> Dict[str, Any]:
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserGists(user=user,pg_size=pg_size)
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}

def get_issues(user:str,pg_size:int=100)-> Dict[str, Any]:
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserIssues(user=user,pg_size=pg_size)
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}

def get_pull_requests(user:str,pg_size:int=100)-> Dict[str, Any]:
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserPullRequests(user=user,pg_size=pg_size)
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}

def get_repo_discussions(user:str,pg_size:int=100)->Dict[str, Any]:
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserRepositoryDiscussions(user=user,pg_size=pg_size)
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}









    