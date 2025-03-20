from typing import Dict, Any, Optional
from flask import session
from app.services.github_query.github_graphql.client import (
    Client,
    QueryFailedException,
)
from app.services.github_query.github_graphql.authentication import (
    PersonalAccessTokenAuthenticator,
)

from app.services.github_query.queries.profiles.user_profile_stats import (UserProfileStats)
from app.services.github_query.queries.profiles.user_login import (UserLogin)

def get_profile_stats(user: str,token: Optional[str] = None)-> Dict[str, Any]:
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
        query = UserProfileStats(
            user=user,
        )
        response = client.execute(query=query)
        print(response)  # Debugging: Inspect response structure
        return response
    except QueryFailedException as e:
        return {"error": str(e)}
    
def get_profile_login(user: str,token: Optional[str] = None)-> Dict[str, Any]:
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
        query = UserLogin(
            user=user,
        )
        response = client.execute(query=query)
        print(response)  # Debugging: Inspect response structure
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


