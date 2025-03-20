from typing import List, Dict, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
from backend.app.services.github_query.queries.constants import (
    NODE_USER,
    NODE_LOGIN,
    NODE_ISSUES,
    NODE_NODES,
    NODE_PAGE_INFO,
    FIELD_CREATED_AT,
    FIELD_TOTAL_COUNT,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN,
    ARG_FIRST
)
import backend.app.services.github_query.utils.helper as helper

class UserIssues(PaginatedQuery):
    """
    UserIssues extends PaginatedQuery to fetch issues associated with a specific user.
    It is designed to navigate through potentially large sets of issues data.
    """
    
    def __init__(self,user:str,pg_size:int) -> None:
        """
        Initializes the UserIssues query with necessary fields and pagination support.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: user},
                    fields=[
                        NODE_LOGIN,
                        QueryNodePaginator(
                            NODE_ISSUES,
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
    def user_issues(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts issues from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of issues, each represented as a dictionary.
        """
        return raw_data.get(NODE_USER, {}).get(NODE_ISSUES, {}).get(NODE_NODES, [])

    @staticmethod
    def created_before_time(issues: Dict[str, Any], time: str) -> int:
        """
        Counts the number of issues created before a specified time.

        Args:
            issues (List[Dict]): A list of issues, each represented as a dictionary.
            time (str): The time string to compare each issue's creation time against.

        Returns:
            int: The count of issues created before the specified time.
        """
        counter = 0
        for issue in issues:
            if helper.created_before(issue.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
