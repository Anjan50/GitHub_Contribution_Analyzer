from typing import List, Dict, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper
from backend.app.services.github_query.queries.constants import (
    NODE_USER, NODE_LOGIN, NODE_PULL_REQUESTS, FIELD_CREATED_AT,
    FIELD_TOTAL_COUNT, FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE, ARG_LOGIN, ARG_FIRST, NODE_NODES, NODE_PAGE_INFO
)

class UserPullRequests(PaginatedQuery):
    """
    UserPullRequests extends PaginatedQuery to fetch pull requests associated with a specific user.
    It navigates through potentially large sets of pull request data with pagination.
    """
    
    def __init__(self,user:str,pg_size:int) -> None:
        """
        Initializes the UserPullRequests query with necessary fields and pagination support.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: user},
                    fields=[
                        NODE_LOGIN,
                        QueryNodePaginator(
                            NODE_PULL_REQUESTS,
                            args={ARG_FIRST: pg_size},
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[FIELD_CREATED_AT]
                                ),
                                QueryNode(
                                    NODE_PAGE_INFO,
                                    fields=[FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    @staticmethod
    def user_pull_requests(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts pull requests from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of pull requests, each represented as a dictionary.
        """
        pull_requests = raw_data.get(NODE_USER, {}).get(NODE_PULL_REQUESTS, {}).get(NODE_NODES, [])
        return pull_requests

    @staticmethod
    def created_before_time(pull_requests: Dict[str, Any], time: str) -> int:
        """
        Counts the number of pull requests created before a specified time.

        Args:
            pull_requests (List[Dict]): A list of pull requests, each represented as a dictionary.
            time (str): The time string to compare each pull request's creation time against.

        Returns:
            int: The count of pull requests created before the specified time.
        """
        counter = 0
        for pull_request in pull_requests:
            if helper.created_before(pull_request.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
