
from typing import Dict, Any
from collections import Counter
from backend.app.services.github_query.github_graphql.query import QueryNode, Query
from backend.app.services.github_query.queries.constants import (
    FIELD_LOGIN, FIELD_STARTED_AT, FIELD_ENDED_AT, FIELD_RESTRICTED_CONTRIBUTIONS_COUNT,
    FIELD_TOTAL_COMMIT_CONTRIBUTIONS, FIELD_TOTAL_ISSUE_CONTRIBUTIONS,
    FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS, FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS,
    FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS, NODE_USER, NODE_CONTRIBUTIONS_COLLECTION
)

class UserContributionsCollection(Query):
    def __init__(self, user: str, start_date: str, end_date: str) -> None:
        """
        Initializes a UserContributionsCollection query object.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={
                        FIELD_LOGIN: user  # Remove extra quotes, QueryNode will handle it
                    },
                    fields=[
                        QueryNode(
                            NODE_CONTRIBUTIONS_COLLECTION,
                            args={
                                FIELD_STARTED_AT: start_date,  # Remove extra quotes
                                FIELD_ENDED_AT: end_date,
                            },
                            fields=[
                                FIELD_STARTED_AT,
                                FIELD_ENDED_AT,
                                FIELD_RESTRICTED_CONTRIBUTIONS_COUNT,
                                FIELD_TOTAL_COMMIT_CONTRIBUTIONS,
                                FIELD_TOTAL_ISSUE_CONTRIBUTIONS,
                                FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS,
                                FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS,
                                FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS,
                            ],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def user_contributions_collection(cumulated_contributions_collection: dict) -> Counter:
        """Process the contributions data"""
        try:
            if 'data' in cumulated_contributions_collection:
                cumulated_contributions_collection = cumulated_contributions_collection['data']
                
            raw_data = cumulated_contributions_collection[NODE_USER][NODE_CONTRIBUTIONS_COLLECTION]
            return Counter({
                "res_con": raw_data[FIELD_RESTRICTED_CONTRIBUTIONS_COUNT],
                "commit": raw_data[FIELD_TOTAL_COMMIT_CONTRIBUTIONS],
                "issue": raw_data[FIELD_TOTAL_ISSUE_CONTRIBUTIONS],
                "pr": raw_data[FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS],
                "pr_review": raw_data[FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS],
                "repository": raw_data[FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS],
            })
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            print(f"Raw data: {cumulated_contributions_collection}")
            raise
    def __init__(self, user: str, start_date: str, end_date: str) -> None:
        """
        Initializes a UserContributionsCollection query object.
        """
        # Format the query with proper quotes
        query = f'''
            query {{
                user(login: "{user}") {{
                    contributionsCollection(from: "{start_date}", to: "{end_date}") {{
                        restrictedContributionsCount
                        totalCommitContributions
                        totalIssueContributions
                        totalPullRequestContributions
                        totalPullRequestReviewContributions
                        totalRepositoryContributions
                    }}
                }}
            }}
        '''
        super().__init__(query=query)

    @staticmethod
    def user_contributions_collection(cumulated_contributions_collection: dict) -> Counter:
        raw_data = cumulated_contributions_collection.get('user', {}).get('contributionsCollection', {})
        return Counter({
            "res_con": raw_data.get('restrictedContributionsCount', 0),
            "commit": raw_data.get('totalCommitContributions', 0),
            "issue": raw_data.get('totalIssueContributions', 0),
            "pr": raw_data.get('totalPullRequestContributions', 0),
            "pr_review": raw_data.get('totalPullRequestReviewContributions', 0),
            "repository": raw_data.get('totalRepositoryContributions', 0),
        })
    def __init__(self, user: str, start_date: str, end_date: str) -> None:
        """
        Initializes a UserContributionsCollection query object to fetch detailed contribution information of a user.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={
                        FIELD_LOGIN: f'"{user}"'  # Add quotes around the username
                    },
                    fields=[
                        QueryNode(
                            NODE_CONTRIBUTIONS_COLLECTION,
                            args={
                                FIELD_STARTED_AT: f'"{start_date}"',  # Add quotes around dates
                                FIELD_ENDED_AT: f'"{end_date}"',
                            },
                            fields=[
                                FIELD_STARTED_AT,
                                FIELD_ENDED_AT,
                                FIELD_RESTRICTED_CONTRIBUTIONS_COUNT,
                                FIELD_TOTAL_COMMIT_CONTRIBUTIONS,
                                FIELD_TOTAL_ISSUE_CONTRIBUTIONS,
                                FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS,
                                FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS,
                                FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS,
                            ],
                        ),
                    ],
                )
            ]
        )