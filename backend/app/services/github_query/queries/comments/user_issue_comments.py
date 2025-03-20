from typing import Dict, Any, List
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
from backend.app.services.github_query.utils.helper import created_before
from backend.app.services.github_query.queries.constants import (
    NODE_USER, NODE_LOGIN, NODE_ISSUE_COMMENTS, FIELD_TOTAL_COUNT,
    FIELD_CREATED_AT, NODE_NODES, NODE_PAGE_INFO, FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN, ARG_FIRST
)

class UserIssueComments(PaginatedQuery):
    """
    UserIssueComments constructs a paginated GraphQL query specifically for
    retrieving user issue comments. It extends the PaginatedQuery class to handle
    queries that expect a large amount of data that might be delivered in multiple pages.
    """

    def __init__(self,user:str,pg_size:int) -> None:
        """
        Initializes the UserIssueComments query with specific fields and arguments
        to retrieve user issue comments, including pagination handling.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN:user},
                    fields=[
                        NODE_LOGIN,
                        QueryNodePaginator(
                            NODE_ISSUE_COMMENTS,
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
    def user_issue_comments(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the issue comments from the raw query data.

        Args:
            raw_data (dict): The raw data returned by the GraphQL query.
        
        Returns:
            list: A list of dictionaries representing each issue comment's data.
        """
        issue_comments = raw_data[NODE_USER][NODE_ISSUE_COMMENTS][NODE_NODES]
        return issue_comments

    @staticmethod
    def created_before_time(issue_comments: List[Dict[str, Any]], time: str) -> int:
        """
        Counts how many issue comments were created before a specific time.

        Args:
            issue_comments (list): A list of issue comment dictionaries with a "createdAt" field.
            time (str): The cutoff time in string format.
        
        Returns:
            int: The count of issue comments created before the specified time.
        """
        # counter = 0
        # for issue_comment in issue_comments:
        #     if created_before(issue_comment[FIELD_CREATED_AT], time):
        #         counter += 1
        #     # else:
        #     #     break
        # return counter
        return sum(1 for comment in issue_comments if created_before(comment[FIELD_CREATED_AT], time))
