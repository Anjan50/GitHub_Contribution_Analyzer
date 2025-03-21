from typing import List, Dict, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
from backend.app.services.github_query.queries.constants import (
    NODE_USER,
    NODE_LOGIN,
    NODE_GISTS,
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

class UserGists(PaginatedQuery):
    def __init__(self,user:str,pg_size:int) -> None:
        """Initializes a query for User Gists as a paginated query.

        This query is used to fetch a list of gists for a specific user,
        including pagination support to handle large numbers of gists.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: user},
                    fields=[
                        NODE_LOGIN,
                        QueryNodePaginator(
                            NODE_GISTS,
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
    def user_gists(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processes raw data to extract user gists information.

        Args:
            raw_data: The raw data returned by the query, structured as a dictionary.

        Returns:
            A list of dictionaries, each containing data about a single gist.
        """
        gists = raw_data.get(NODE_USER, {}).get(NODE_GISTS, {}).get(NODE_NODES, [])
        return gists

    @staticmethod
    def created_before_time(gists: Dict[str, Any], time: str) -> int:
        """Counts the gists created before a specified time.

        Args:
            gists: A list of gist dictionaries returned by the query.
            time: The time string to compare against, in ISO format.

        Returns:
            The count of gists created before the specified time.
        """
        counter = 0
        for gist in gists:
            if helper.created_before(gist.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
