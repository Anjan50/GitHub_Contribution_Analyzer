from typing import List, Dict, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper
from datetime import datetime

from backend.app.services.github_query.queries.constants import (
    NODE_USER,
    ARG_LOGIN,
    ARG_FIRST,
    FIELD_LOGIN,
    NODE_REPOSITORY_DISCUSSIONS,
    FIELD_TOTAL_COUNT,
    NODE_NODES,
    FIELD_CREATED_AT,
    NODE_PAGE_INFO,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE
)

class UserRepositoryDiscussions(PaginatedQuery):
    def __init__(self,user:str,pg_size:int) -> None:
        """Initializes a paginated query for GitHub user repository discussions."""
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: user},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_REPOSITORY_DISCUSSIONS,
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
    def user_repository_discussions(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts repository discussions from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query, expected to contain user's repository discussions.

        Returns:
            List[Dict]: A list of dictionaries, each containing data about a single repository discussion.
        """
        repository_discussions = raw_data.get(NODE_USER, {}).get(NODE_REPOSITORY_DISCUSSIONS, {}).get(NODE_NODES, [])
        return repository_discussions
    
    @staticmethod
    def created_before(comment_date: str, cutoff_date: str) -> bool:
        """
        Compares the created date of a comment with the cutoff date.

        Args:
            comment_date (str): The creation date of the comment.
            cutoff_date (str): The cutoff date to compare against.

        Returns:
            bool: True if the comment was created before the cutoff date, False otherwise.
        """
        # Convert both strings to datetime objects
        comment_datetime = datetime.fromisoformat(comment_date[:-1])  # Remove the 'Z' and convert
        cutoff_datetime = datetime.fromisoformat(cutoff_date[:-1])
        return comment_datetime < cutoff_datetime

    @staticmethod
    def created_before_time(repository_discussions: Dict[str, Any], time: str) -> int:
        """
        Counts the number of repository discussions created before a specified time.

        Args:
            repository_discussions (List[Dict]): A list of repository discussions dictionaries.
            time (str): The specific time (ISO format) against which to compare the creation dates of the discussions.

        Returns:
            int: The count of repository discussions created before the specified time.
        """
        counter = 0
        cutoff_datetime = datetime.fromisoformat(time[:-1])
        print(f"Cutoff datetime: {cutoff_datetime}")
    
        for comment in repository_discussions:
         comment_datetime = datetime.fromisoformat(comment[FIELD_CREATED_AT][:-1])
         print(f"Comment datetime: {comment_datetime}")
         if comment_datetime < cutoff_datetime:
            counter += 1
            print("Incrementing counter")
         else:
            print("Not incrementing counter")

        print(f"Final counter: {counter}")
        return counter



