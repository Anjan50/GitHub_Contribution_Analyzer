# import re
# from backend.app.services.github_query.queries.comments.user_gist_comments import UserGistComments

# class TestUserGistComments:
#     def test_user_gist_comments_query_structure(self):
#         # Instantiate the UserGistComments class
#         user_gist_comments_query = UserGistComments()
        
#         # Convert the generated query to a string or the appropriate format
#         query_string = str(user_gist_comments_query)
        
#         # Define what the expected query should look like, including all fields
#         expected_query = '''
#         query {
#             user(login: "$user") {
#                 login
#                 gistComments(first: $pg_size) {
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

#     def test_user_gist_comments_method(self):
#         # Simulated raw data returned by the query
#         raw_data = {
#             "user": {
#                 "gistComments": {
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
#         gist_comments = UserGistComments.user_gist_comments(raw_data)
#         assert gist_comments == expected_comments, "The processed gist comments do not match the expected structure."


#     def test_created_before_time_method(self):
#         gist_comments = [
#             {"createdAt": "2021-01-01T00:00:00Z"},
#             {"createdAt": "2022-01-01T00:00:00Z"}
#         ]
#         time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
#         # Call the created_before_time method and assert it returns the expected count
#         count = UserGistComments.created_before_time(gist_comments, time)
#         assert count == 1, "There should be 1 comment created before 2022."

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
from backend.app.services.github_query.queries.comments.user_gist_comments import UserGistComments
import backend.app.services.github_query.utils.helper as helper
from backend.app.services.github_query.queries.constants import (
    FIELD_LOGIN, FIELD_TOTAL_COUNT, FIELD_CREATED_AT, FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE,
    NODE_USER, NODE_GIST_COMMENTS, NODE_NODES, NODE_PAGE_INFO, ARG_LOGIN, ARG_FIRST
)

@pytest.fixture
def user_gist_comments_query():
    return UserGistComments()

@pytest.fixture
def sample_raw_data():
    return {
        "user": {
            "gistComments": {
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

def test_user_gist_comments_initialization(user_gist_comments_query):
    assert isinstance(user_gist_comments_query, PaginatedQuery)
    assert len(user_gist_comments_query.fields) == 1
    assert isinstance(user_gist_comments_query.fields[0], QueryNode)

def test_user_gist_comments_query_structure(user_gist_comments_query):
    user_node = user_gist_comments_query.fields[0]
    assert user_node.name == NODE_USER
    assert user_node.args == {ARG_LOGIN: "$user"}
    
    assert FIELD_LOGIN in user_node.fields
    assert len(user_node.fields) == 2
    
    gist_comments_node = user_node.fields[1]
    assert isinstance(gist_comments_node, QueryNodePaginator)
    assert gist_comments_node.name == NODE_GIST_COMMENTS
    assert gist_comments_node.args == {ARG_FIRST: "$pg_size"}
    
    assert FIELD_TOTAL_COUNT in gist_comments_node.fields
    assert len(gist_comments_node.fields) == 3

def test_user_gist_comments_extraction(sample_raw_data):
    extracted = UserGistComments.user_gist_comments(sample_raw_data)
    assert len(extracted) == 3
    assert all(FIELD_CREATED_AT in comment for comment in extracted)

def test_created_before_time(mocker):
    gist_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-27T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-26T08:00:00Z"}
    ]
    
    # Mock the helper.created_before function
    mocker.patch('backend.app.services.github_query.utils.helper.created_before', side_effect=[False, True, True])
    
    cutoff_time = "2023-10-27T23:59:59Z"
    count = UserGistComments.created_before_time(gist_comments, cutoff_time)
    assert count == 2

    # Test with all comments after cutoff time
    mocker.patch('backend.app.services.github_query.utils.helper.created_before', return_value=False)
    count = UserGistComments.created_before_time(gist_comments, cutoff_time)
    assert count == 0

    # Test with all comments before cutoff time
    mocker.patch('backend.app.services.github_query.utils.helper.created_before', return_value=True)
    count = UserGistComments.created_before_time(gist_comments, cutoff_time)
    assert count == 3

def test_created_before_time_empty_list():
    assert UserGistComments.created_before_time([], "2023-10-28T10:00:00Z") == 0

def test_user_gist_comments_with_empty_data():
    empty_data = {"user": {"gistComments": {"nodes": []}}}
    assert UserGistComments.user_gist_comments(empty_data) == []

def test_user_gist_comments_missing_data():
    invalid_data = {"user": {}}
    with pytest.raises(KeyError):
        UserGistComments.user_gist_comments(invalid_data)