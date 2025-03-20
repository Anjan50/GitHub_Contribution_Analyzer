# import re
# from backend.app.services.github_query.queries.comments.user_commit_comments import UserCommitComments

# class TestUserCommitComments:
#     def test_user_commit_comments_query_structure(self):
#         # Instantiate the UserCommitComments class
#         user_commit_comments_query = UserCommitComments()
#         # Convert the generated query to a string or the appropriate format
#         query_string = str(user_commit_comments_query)
#         # Define what the expected query should look like, including all fields
#         expected_query = '''
#         query {
#             user(login: "$user") {
#                 login
#                 commitComments(first: $pg_size) {
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
#         assert query_string == expected_query, "The UserCommitComments query does not match the expected structure."

    
#     def test_user_commit_comments_method(self):
#         # Simulated raw data returned by the query
#         raw_data = {
#             "user": {
#                 "commitComments": {
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
        
#         # Call the user_commit_comments method and assert it returns the expected result
#         commit_comments = UserCommitComments.user_commit_comments(raw_data)
#         assert commit_comments == expected_comments, "The processed commit comments do not match the expected structure."


#     def test_created_before_time_method(self):
#         commit_comments = [
#             {"createdAt": "2021-01-01T00:00:00Z"},
#             {"createdAt": "2022-01-01T00:00:00Z"}
#         ]
#         time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
#         # Call the created_before_time method and assert it returns the expected count
#         count = UserCommitComments.created_before_time(commit_comments, time)
#         assert count == 1, "There should be 1 comment created before 2022."

import pytest
from backend.app.services.github_query.queries.comments.user_commit_comments import UserCommitComments
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
from backend.app.services.github_query.queries.constants import (
     FIELD_LOGIN, FIELD_TOTAL_COUNT, FIELD_CREATED_AT, FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE,
    NODE_USER, NODE_COMMIT_COMMENTS, NODE_NODES, NODE_PAGE_INFO, ARG_LOGIN, ARG_FIRST
)
import backend.app.services.github_query.utils.helper as helper

@pytest.fixture
def user_commit_comments_query():
    return UserCommitComments()

@pytest.fixture
def sample_raw_data():
    return {
        "user": {
            "commitComments": {
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

def test_user_commit_comments_initialization(user_commit_comments_query):
    assert isinstance(user_commit_comments_query, PaginatedQuery)
    assert len(user_commit_comments_query.fields) == 1
    assert isinstance(user_commit_comments_query.fields[0], QueryNode)

def test_user_commit_comments_query_structure(user_commit_comments_query):
    user_node = user_commit_comments_query.fields[0]
    assert user_node.name == NODE_USER
    assert user_node.args == {ARG_LOGIN: "$user"}
    
    assert FIELD_LOGIN in user_node.fields
    assert len(user_node.fields) == 2
    
    commit_comments_node = user_node.fields[1]
    assert isinstance(commit_comments_node, QueryNodePaginator)
    assert commit_comments_node.name == NODE_COMMIT_COMMENTS
    assert commit_comments_node.args == {ARG_FIRST: "$pg_size"}
    
    assert FIELD_TOTAL_COUNT in commit_comments_node.fields
    assert len(commit_comments_node.fields) == 3

def test_user_commit_comments_extraction(sample_raw_data):
    extracted = UserCommitComments.user_commit_comments(sample_raw_data)
    assert len(extracted) == 3
    assert all(FIELD_CREATED_AT in comment for comment in extracted)

def test_created_before_time():
    commit_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-27T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-26T08:00:00Z"}
    ]
    
    cutoff_time = "2023-10-27T23:59:59Z"
    count = UserCommitComments.created_before_time(commit_comments, cutoff_time)
    assert count == 2

    earlier_cutoff = "2023-10-26T07:59:59Z"
    count = UserCommitComments.created_before_time(commit_comments, earlier_cutoff)
    assert count == 0

    later_cutoff = "2023-10-29T00:00:00Z"
    count = UserCommitComments.created_before_time(commit_comments, later_cutoff)
    assert count == 3

def test_created_before_time_empty_list():
    assert UserCommitComments.created_before_time([], "2023-10-28T10:00:00Z") == 0

def test_created_before_time_all_before():
    commit_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-27T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-26T08:00:00Z"}
    ]
    cutoff_time = "2023-10-29T00:00:00Z"
    assert UserCommitComments.created_before_time(commit_comments, cutoff_time) == 3

def test_created_before_time_none_before():
    commit_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-27T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-26T08:00:00Z"}
    ]
    cutoff_time = "2023-10-25T00:00:00Z"
    assert UserCommitComments.created_before_time(commit_comments, cutoff_time) == 0

def test_user_commit_comments_with_empty_data():
    empty_data = {"user": {"commitComments": {"nodes": []}}}
    assert UserCommitComments.user_commit_comments(empty_data) == []

def test_user_commit_comments_missing_data():
    invalid_data = {"user": {}}
    with pytest.raises(KeyError):
        UserCommitComments.user_commit_comments(invalid_data)