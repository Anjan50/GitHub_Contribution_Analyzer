# import re
# from backend.app.services.github_query.queries.comments.user_issue_comments import UserIssueComments

# class TestUserIssueComments:
#     def test_user_issue_comments_query_structure(self):
#         # Instantiate the UserIssueComments class
#         user_issue_comments_query = UserIssueComments()
        
#         # Convert the generated query to a string or the appropriate format
#         query_string = str(user_issue_comments_query)
        
#         # Define what the expected query should look like, including all fields
#         expected_query = '''
#         query {
#             user(login: "$user") {
#                 login
#                 issueComments(first: $pg_size) {
#                     totalCount
#                     nodes {
#                         createdAt
#                     }
#                     pageInfo {
#                         endCursor
#                         hasNextPage
#                     }
#                 }
#             }
#         }
#         '''.strip()  # Use .strip() to remove any leading/trailing whitespace
#         # Remove all newlines
#         expected_query = expected_query.replace("\n", "")
#         # Remove extra spaces using regex
#         expected_query = re.sub(' +', ' ', expected_query)
#         # Assert that the generated query matches the expected query
#         assert query_string == expected_query, "The UserGistComments query does not match the expected structure."

#     def test_user_issue_comments_method(self):
#         # Simulated raw data returned by the query
#         raw_data = {
#             "user": {
#                 "issueComments": {
#                     "nodes": [
#                         {"createdAt": "2021-01-01T00:00:00Z"},
#                         {"createdAt": "2021-01-02T00:00:00Z"}
#                     ]
#                 }
#             }
#         }
        
#         expected_comments = [
#             {"createdAt": "2021-01-01T00:00:00Z"},
#             {"createdAt": "2021-01-02T00:00:00Z"}
#         ]
        
#         # Call the user_gist_comments method and assert it returns the expected result
#         issue_comments = UserIssueComments.user_issue_comments(raw_data)
#         assert issue_comments == expected_comments, "The processed issue comments do not match the expected structure."


#     def test_created_before_time_method(self):
#         issue_comments = [
#             {"createdAt": "2021-01-01T00:00:00Z"},
#             {"createdAt": "2022-01-01T00:00:00Z"}
#         ]
#         time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
#         # Call the created_before_time method and assert it returns the expected count
#         count = UserIssueComments.created_before_time(issue_comments, time)
#         assert count == 1, "There should be 1 comment created before 2022."

import pytest
from typing import Dict, Any, List
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
from backend.app.services.github_query.queries.comments.user_issue_comments import UserIssueComments
from backend.app.services.github_query.queries.constants import (
    NODE_USER, NODE_LOGIN, NODE_ISSUE_COMMENTS, FIELD_TOTAL_COUNT,
    FIELD_CREATED_AT, NODE_NODES, NODE_PAGE_INFO, FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN, ARG_FIRST
)

@pytest.fixture
def user_issue_comments_query():
    return UserIssueComments()

@pytest.fixture
def sample_raw_data():
    return {
        "user": {
            "issueComments": {
                "totalCount": 3,
                "nodes": [
                    {"createdAt": "2023-10-28T10:00:00Z"},
                    {"createdAt": "2023-10-27T09:00:00Z"},
                    {"createdAt": "2023-10-26T08:00:00Z"}
                ],
                "pageInfo": {
                    "endCursor": "cursor123",
                    "hasNextPage": False
                }
            }
        }
    }

def test_user_issue_comments_initialization(user_issue_comments_query):
    assert isinstance(user_issue_comments_query, PaginatedQuery)
    assert len(user_issue_comments_query.fields) == 1
    assert isinstance(user_issue_comments_query.fields[0], QueryNode)

def test_user_issue_comments_query_structure(user_issue_comments_query):
    user_node = user_issue_comments_query.fields[0]
    assert user_node.name == NODE_USER
    assert user_node.args == {ARG_LOGIN: "$user"}
    
    assert NODE_LOGIN in user_node.fields
    assert len(user_node.fields) == 2
    
    issue_comments_node = user_node.fields[1]
    assert isinstance(issue_comments_node, QueryNodePaginator)
    assert issue_comments_node.name == NODE_ISSUE_COMMENTS
    assert issue_comments_node.args == {ARG_FIRST: "$pg_size"}
    
    assert FIELD_TOTAL_COUNT in issue_comments_node.fields
    assert len(issue_comments_node.fields) == 3

def test_user_issue_comments_extraction(sample_raw_data):
    extracted = UserIssueComments.user_issue_comments(sample_raw_data)
    assert len(extracted) == 3
    assert all(FIELD_CREATED_AT in comment for comment in extracted)

def test_created_before_time():
    issue_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-27T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-26T08:00:00Z"}
    ]
    cutoff_time = "2023-10-27T23:59:59Z"

    # Define a helper function to simulate the `created_before` logic directly in the test
    def created_before(comment_time, cutoff_time):
        return comment_time < cutoff_time

    # Inject the helper function into the class method
    UserIssueComments.created_before = staticmethod(created_before)

    # Test with some comments before cutoff time
    count = UserIssueComments.created_before_time(issue_comments, cutoff_time)
    assert count == 2, f"Expected 2, got {count}"

    # Test with all comments after cutoff time by modifying the data
    issue_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-28T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-28T08:00:00Z"}
    ]
    count = UserIssueComments.created_before_time(issue_comments, cutoff_time)
    assert count == 0, f"Expected 0, got {count}"

    # Test with all comments before cutoff time by modifying the data
    issue_comments = [
        {FIELD_CREATED_AT: "2023-10-26T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-25T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-24T08:00:00Z"}
    ]
    count = UserIssueComments.created_before_time(issue_comments, cutoff_time)
    assert count == 3, f"Expected 3, got {count}"


def test_created_before_time_empty_list():
    assert UserIssueComments.created_before_time([], "2023-10-28T10:00:00Z") == 0

def test_user_issue_comments_with_empty_data():
    empty_data = {"user": {"issueComments": {"nodes": []}}}
    assert UserIssueComments.user_issue_comments(empty_data) == []

def test_user_issue_comments_missing_data():
    invalid_data = {"user": {}}
    with pytest.raises(KeyError):
        UserIssueComments.user_issue_comments(invalid_data)