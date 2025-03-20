from typing import Dict, Any, Optional
from flask import session

from app.services.github_query.github_graphql.client import (
    Client,
    QueryFailedException,
)
from app.services.github_query.github_graphql.authentication import (
    PersonalAccessTokenAuthenticator,
)

from app.services.github_query.queries.comments.user_commit_comments import (UserCommitComments)
from app.services.github_query.queries.comments.user_gist_comments import (UserGistComments)
from app.services.github_query.queries.comments.user_issue_comments import  (UserIssueComments)
from app.services.github_query.queries.comments.user_repository_discussion_comments import (UserRepositoryDiscussionComments)

def get_user_commit_comments(user:str,pg_size:int=100,token: Optional[str] = None)-> Dict[str, Any]:
    auth_token = token or session.get("access_token")
    print(auth_token)
    if not auth_token:
        return {"error": "User not authenticated"}
    
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=auth_token),
    )

    try:
        query = UserCommitComments(
            user=user,
            pg_size=pg_size
        )
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}

def get_user_gist_comments(user:str,pg_size:int=100)-> Dict[str, Any]:
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserGistComments(user=user,pg_size=pg_size)
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}
    
def get_user_issue_comments(user:str,pg_size:int=100)-> Dict[str, Any]:
    token = session.get("access_token")
    if not token:
        return {"error": "User not authenticated"}
    client = Client(
        host="api.github.com",
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )

    try:
        query = UserIssueComments(user=user,pg_size=pg_size)
        # Execute query and handle pagination
        response = client.execute(query=query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}
    


                             