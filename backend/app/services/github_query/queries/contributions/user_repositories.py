"""The module defines the UserRepositories class, which formulates the GraphQL query string
to extract repositories created by the user based on a given user ID."""

import backend.app.services.github_query.utils.helper as helper
from typing import Dict, Any, List
from backend.app.services.github_query.github_graphql.query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from backend.app.services.github_query.queries.constants import (
    NODE_USER,
    FIELD_CREATED_AT,
    FIELD_NAME,
    FIELD_TOTAL_COUNT,
    FIELD_TOTAL_SIZE,
    FIELD_SIZE,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    FIELD_WATCHERS,
    FIELD_STARGAZER_COUNT,
    FIELD_FORK_COUNT,
    NODE_REPOSITORIES,
    NODE_LANGUAGES,
    NODE_EDGES,
    NODE_NODE,
    NODE_NODES,
    NODE_PAGE_INFO,
    ARG_LOGIN,
    ARG_FIRST,
    ARG_IS_FORK,
    ARG_OWNER_AFFILIATIONS,
    ARG_ORDER_BY,
    ARG_FIELD,
    ARG_DIRECTION,
)


class UserRepositories(PaginatedQuery):
    """
    UserRepositories is a class for querying a user's repositories including details like language statistics,
    fork count, stargazer count, etc. It extends PaginatedQuery to handle potentially large numbers of repositories.
    """

    def __init__(
        self,
        login: str,
        is_fork: bool = False,
        ownership: str = "[OWNER]",
        pg_size: int = 10,
        repo_order_field: str = "CREATED_AT",
        repo_order_dir: str = "DESC",
        lag_order_field: str = "SIZE",
        lag_order_dir: str = "DESC",
    ) -> None:
        """
        Initializes a query for a user's repositories with various filtering and ordering options.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        QueryNodePaginator(
                            NODE_REPOSITORIES,
                            args={
                                ARG_FIRST: pg_size,
                                ARG_IS_FORK: is_fork,
                                ARG_OWNER_AFFILIATIONS: ownership,
                                ARG_ORDER_BY: {
                                    ARG_FIELD: repo_order_field,
                                    ARG_DIRECTION: repo_order_dir,
                                },
                            },
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[
                                        QueryNode(
                                            NODE_LANGUAGES,
                                            args={
                                                ARG_FIRST: 100,
                                                ARG_ORDER_BY: {
                                                    ARG_FIELD: lag_order_field,
                                                    ARG_DIRECTION: lag_order_dir,
                                                },
                                            },
                                            fields=[
                                                FIELD_TOTAL_COUNT,
                                                QueryNode(
                                                    NODE_EDGES,
                                                    fields=[
                                                        FIELD_SIZE,
                                                        QueryNode(
                                                            NODE_NODE,
                                                            fields=[FIELD_NAME],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                QueryNode(
                                    NODE_PAGE_INFO,
                                    fields=[FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE],
                                ),
                            ],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def user_repositories(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the list of repositories from the raw GraphQL query response data.

        Args:
            raw_data: The raw data returned by the GraphQL query.

        Returns:
            A list of dictionaries, each containing data about a single repository.
        """
        repositories = raw_data.get(NODE_USER, {}).get(NODE_REPOSITORIES, {}).get(NODE_NODES, [])
        return repositories

    @staticmethod
    def cumulated_repository_stats(
        repo_list: List[Dict[str, Any]],
        repo_stats: Dict[str, int],
        lang_stats: Dict[str, int],
        start: str,
        end: str,
        direction: str,
    ) -> None:
        """
        Aggregates statistics for repositories created before, after a certain time or in between a time range.

        Args:
            repo_list: List of repositories to be analyzed.
            repo_stats: Dictionary accumulating various statistics like total count, fork count, etc.
            lang_stats: Dictionary accumulating language usage statistics.
            start: String representing the start time for consideration of repositories.
            end: String representing the end time for consideration of repositories.
            direction: Specify whether to aggregates statistics for repositories created before,
                       after a certain time or in between a time range.

        Returns:
            None: Modifies the repo_stats and lang_stats dictionaries in place.
        """
        for repo in repo_list:
            if direction == "before" and not helper.created_before(
                repo[FIELD_CREATED_AT], start
            ):
                continue
            elif direction == "after" and not helper.created_after(
                repo[FIELD_CREATED_AT], start
            ):
                continue
            elif direction == "between" and not helper.in_time_period(
                repo[FIELD_CREATED_AT], start, end
            ):
                continue

            if repo[NODE_LANGUAGES][FIELD_TOTAL_SIZE] == 0:
                continue
            repo_stats["total_count"] += 1
            repo_stats["fork_count"] += repo[FIELD_FORK_COUNT]
            repo_stats["stargazer_count"] += repo[FIELD_STARGAZER_COUNT]
            repo_stats["watchers_count"] += repo[FIELD_WATCHERS][FIELD_TOTAL_COUNT]
            repo_stats["total_size"] += repo[NODE_LANGUAGES][FIELD_TOTAL_SIZE]
            language_list_sorted = sorted(
                repo[NODE_LANGUAGES][NODE_EDGES], key=lambda s: s[FIELD_SIZE], reverse=True
            )
            if language_list_sorted:
                for language in language_list_sorted:
                    name = language[NODE_NODE][FIELD_NAME]
                    size = language[FIELD_SIZE]
                    if name not in lang_stats:
                        lang_stats[name] = int(size)
                    else:
                        lang_stats[name] += int(size)
