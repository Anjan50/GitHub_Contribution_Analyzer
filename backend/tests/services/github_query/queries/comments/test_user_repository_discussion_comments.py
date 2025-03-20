# import re
# from backend.app.services.github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments

# class TestUserRepositoryDiscussionComments:
#     def test_user_repository_discussion_comments_query_structure(self):
#         # Instantiate the UserRepositoryDiscussionComments class
#         user_repository_discussion_comments_query = UserRepositoryDiscussionComments()
        
#         # Convert the generated query to a string or the appropriate format
#         query_string = str(user_repository_discussion_comments_query)
        
#         # Define what the expected query should look like, including all fields
#         expected_query = '''
#         query {
#             user(login: "$user") {
#                 login
#                 repositoryDiscussionComments(first: $pg_size) {
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
#         assert query_string == expected_query, "The UserRepositoryDiscussionComments query does not match the expected structure."

#     def test_user_repository_discussion_comments_method(self):
#         # Simulated raw data returned by the query
#         raw_data = {
#             "user": {
#                 "repositoryDiscussionComments": {
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
#         repository_discussion_comments = UserRepositoryDiscussionComments.user_repository_discussion_comments(raw_data)
#         assert repository_discussion_comments == expected_comments, "The processed repository discussion comments comments do not match the expected structure."


#     def test_created_before_time_method(self):
#         user_repository_discussion_comments = [
#             {"createdAt": "2021-01-01T00:00:00Z"},
#             {"createdAt": "2022-01-01T00:00:00Z"}
#         ]
#         time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
#         # Call the created_before_time method and assert it returns the expected count
#         count = UserRepositoryDiscussionComments.created_before_time(user_repository_discussion_comments, time)
#         assert count == 1, "There should be 1 comment created before 2022."

import pytest
from typing import Dict, Any, List
from backend.app.services.github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments
from backend.app.services.github_query.queries.constants import (
    NODE_USER,
    NODE_LOGIN,
    NODE_REPOSITORY_DISCUSSION_COMMENTS,
    FIELD_CREATED_AT,
    FIELD_TOTAL_COUNT,
    NODE_NODES,
    NODE_PAGE_INFO,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN,
    ARG_FIRST
)

@pytest.fixture
def user_repository_discussion_comments_query():
    return UserRepositoryDiscussionComments()

@pytest.fixture
def sample_raw_data():
    return {
        "user": {
            "repositoryDiscussionComments": {
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

def test_user_repository_discussion_comments_initialization(user_repository_discussion_comments_query):
    assert isinstance(user_repository_discussion_comments_query, UserRepositoryDiscussionComments)
    assert len(user_repository_discussion_comments_query.fields) == 1

def test_user_repository_discussion_comments_query_structure(user_repository_discussion_comments_query):
    user_node = user_repository_discussion_comments_query.fields[0]
    assert user_node.name == NODE_USER
    assert user_node.args == {ARG_LOGIN: "$user"}

    assert NODE_LOGIN in user_node.fields
    assert len(user_node.fields) == 2

    discussion_comments_node = user_node.fields[1]
    assert discussion_comments_node.name == NODE_REPOSITORY_DISCUSSION_COMMENTS
    assert discussion_comments_node.args == {ARG_FIRST: "$pg_size"}
    
    assert FIELD_TOTAL_COUNT in discussion_comments_node.fields
    assert len(discussion_comments_node.fields) == 3

def test_user_repository_discussion_comments_extraction(sample_raw_data):
    extracted = UserRepositoryDiscussionComments.user_repository_discussion_comments(sample_raw_data)
    assert len(extracted) == 3
    assert all(FIELD_CREATED_AT in comment for comment in extracted)

def test_created_before_time():
    repository_discussion_comments = [
        {FIELD_CREATED_AT: "2023-10-28T10:00:00Z"},  # After cutoff
        {FIELD_CREATED_AT: "2023-10-27T09:00:00Z"},  # Before cutoff
        {FIELD_CREATED_AT: "2023-10-26T08:00:00Z"}   # Before cutoff
    ]
    cutoff_time = "2023-10-27T23:59:59Z"

    # Debug print
    print(f"Cutoff time: {cutoff_time}")
    for comment in repository_discussion_comments:
        print(f"Comment time: {comment[FIELD_CREATED_AT]}")

    # Test with some comments before cutoff time
    count = UserRepositoryDiscussionComments.created_before_time(repository_discussion_comments, cutoff_time)
    
    # Debug print
    print(f"Returned count: {count}")

    assert count == 2, f"Expected 2, got {count}"

    # Test with all comments before cutoff time
    repository_discussion_comments = [
        {FIELD_CREATED_AT: "2023-10-26T10:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-25T09:00:00Z"},
        {FIELD_CREATED_AT: "2023-10-24T08:00:00Z"}
    ]
    count = UserRepositoryDiscussionComments.created_before_time(repository_discussion_comments, cutoff_time)
    assert count == 3, f"Expected 3, got {count}"

def test_created_before_time_empty_list():
    assert UserRepositoryDiscussionComments.created_before_time([], "2023-10-28T10:00:00Z") == 0


def test_created_before_time_empty_list():
    assert UserRepositoryDiscussionComments.created_before_time([], "2023-10-28T10:00:00Z") == 0

def test_user_repository_discussion_comments_with_empty_data():
    empty_data = {"user": {"repositoryDiscussionComments": {"nodes": []}}}
    assert UserRepositoryDiscussionComments.user_repository_discussion_comments(empty_data) == []

def test_user_repository_discussion_comments_missing_data():
    invalid_data = {"user": {}}
    with pytest.raises(KeyError):
        UserRepositoryDiscussionComments.user_repository_discussion_comments(invalid_data)
