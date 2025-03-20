from typing import Dict, Any, Optional
from flask import session
from app.services.github_query.github_graphql.client import (
    Client,
    QueryFailedException,
)
from app.services.github_query.github_graphql.authentication import (
    PersonalAccessTokenAuthenticator,
)

from app.services.github_query.queries.time_range_contributions.user_contributions_collection import (UserContributionsCollection)
def get_user_contributions(user: str, start_date: str, end_date: str, token: Optional[str] = None) -> Dict[str, Any]:
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
        query = UserContributionsCollection(
            user=user,
            start_date=start_date,
            end_date=end_date
        )
        response = client.execute(query=query)
        print(response)  # Debugging: Inspect response structure
        return response
    except QueryFailedException as e:
        return {"error": str(e)}