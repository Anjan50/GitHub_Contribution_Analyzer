# import re
# from backend.app.services.github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection

# class TestUserContributionsCollection:
#     def test_user_contributions_collection_query_structure(self):
#         # Instantiate the query class
#         contributions_query = UserContributionsCollection()
        
#         # Convert the generated query to a string or the appropriate format
#         query_string = str(contributions_query)
        
#         # Define what the expected query should look like, including all fields
#         expected_query = '''
#         query {
#             user(login: "$user") {
#                 contributionsCollection(from: $start, to: $end) {
#                     startedAt
#                     endedAt
#                     restrictedContributionsCount
#                     totalCommitContributions
#                     totalIssueContributions
#                     totalPullRequestContributions
#                     totalPullRequestReviewContributions
#                     totalRepositoryContributions
#                 }
#             }
#         }
#         '''.strip()
#         # Remove all newlines
#         expected_query = expected_query.replace("\n", "")
#         # Remove extra spaces using regex
#         expected_query = re.sub(' +', ' ', expected_query)
#         # Assert that the generated query matches the expected query
#         assert query_string == expected_query, "The UserContributionsCollection query does not match the expected structure."

#     def test_user_contributions_collection_processing(self):
#         # Simulated raw data returned by the query
#         raw_data = {
#             "user": {
#                 "contributionsCollection": {
#                     "startedAt": "2020-01-01T00:00:00Z",
#                     "endedAt": "2020-12-31T23:59:59Z",
#                     "restrictedContributionsCount": 5,
#                     "totalCommitContributions": 150,
#                     "totalIssueContributions": 45,
#                     "totalPullRequestContributions": 30,
#                     "totalPullRequestReviewContributions": 20,
#                     "totalRepositoryContributions": 10,
#                 }
#             }
#         }

#         # Expected processed data structure
#         expected_contributions = {
#             "res_con": 5,
#             "commit": 150,
#             "issue": 45,
#             "pr": 30,
#             "pr_review": 20,
#             "repository": 10,
#         }
        
#         # Call the user_contributions_collection method and assert it returns the expected result
#         processed_contributions = UserContributionsCollection.user_contributions_collection(raw_data)
#         assert processed_contributions == expected_contributions, "Processed user contributions do not match the expected structure."

# test_user_contributions_collection.py

import pytest
from collections import Counter
from backend.app.services.github_query.github_graphql.query import QueryNode
from backend.app.services.github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection
from backend.app.services.github_query.queries.constants import (
    FIELD_RESTRICTED_CONTRIBUTIONS_COUNT,
    FIELD_TOTAL_COMMIT_CONTRIBUTIONS,
    FIELD_TOTAL_ISSUE_CONTRIBUTIONS,
    FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS,
    FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS,
    FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS,
    NODE_USER,
    NODE_CONTRIBUTIONS_COLLECTION
)

# Define test data
@pytest.fixture
def mock_raw_data():
    return {
        NODE_USER: {
            NODE_CONTRIBUTIONS_COLLECTION: {
                FIELD_RESTRICTED_CONTRIBUTIONS_COUNT: 5,
                FIELD_TOTAL_COMMIT_CONTRIBUTIONS: 30,
                FIELD_TOTAL_ISSUE_CONTRIBUTIONS: 12,
                FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS: 7,
                FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS: 15,
                FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS: 3
            }
        }
    }

def test_user_contributions_collection(mock_raw_data):
    # Expected result based on the mock data
    expected_result = Counter({
        "res_con": 5,
        "commit": 30,
        "issue": 12,
        "pr": 7,
        "pr_review": 15,
        "repository": 3
    })
    
    # Call the static method with mock data
    result = UserContributionsCollection.user_contributions_collection(mock_raw_data)
    
    # Assert that the result matches the expected result
    assert result == expected_result, "The contribution counts do not match the expected output."

# Additional test cases can be added below, such as handling empty data or missing fields
def test_user_contributions_collection_empty_data():
    empty_data = {NODE_USER: {NODE_CONTRIBUTIONS_COLLECTION: {}}}
    expected_result = Counter({
        "res_con": 0,
        "commit": 0,
        "issue": 0,
        "pr": 0,
        "pr_review": 0,
        "repository": 0
    })
    result = UserContributionsCollection.user_contributions_collection(empty_data)
    assert result == expected_result, "The contribution counts for empty data should be zeroed."

def test_user_contributions_collection_partial_data():
    partial_data = {
        NODE_USER: {
            NODE_CONTRIBUTIONS_COLLECTION: {
                FIELD_TOTAL_COMMIT_CONTRIBUTIONS: 20,
                FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS: 10
            }
        }
    }
    expected_result = Counter({
        "res_con": 0,
        "commit": 20,
        "issue": 0,
        "pr": 10,
        "pr_review": 0,
        "repository": 0
    })
    result = UserContributionsCollection.user_contributions_collection(partial_data)
    assert result == expected_result, "The contribution counts with partial data should fill missing fields with zero."

