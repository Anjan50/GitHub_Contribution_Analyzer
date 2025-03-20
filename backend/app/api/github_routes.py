from flask import Blueprint, jsonify, request
# Import service methods
from backend.app.services.github_graphql_services import get_current_user_login, get_specific_user_login

from backend.app.services.github_query.queries.comments import user_commit_comments
from backend.app.services.github_query.queries.comments import user_gist_comments
from backend.app.services.github_query.queries.comments import user_issue_comments
from backend.app.services.github_query.queries.comments import user_repository_discussion_comments
from backend.app.services.github_query.queries.comments.user_commit_comments import UserCommitComments
from backend.app.services.github_query.queries.comments.user_gist_comments import UserGistComments
from backend.app.services.github_query.queries.comments.user_issue_comments import UserIssueComments
from backend.app.services.github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments
from backend.app.services.github_query.queries.contributions.user_gists import UserGists
from backend.app.services.github_query.queries.contributions.user_issues import UserIssues
from backend.app.services.github_query.queries.contributions.user_pull_requests import UserPullRequests
from backend.app.services.github_query.queries.contributions.user_repositories import UserRepositories
from backend.app.services.github_query.queries.contributions.user_repository_discussions import UserRepositoryDiscussions
from backend.app.services.github_query.queries.profiles.user_profile_stats import UserProfileStats
from backend.app.services.github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection

github_bp = Blueprint('api', __name__)

@github_bp.route('/graphql/current-user-login', methods=['GET'])
def current_user_login():
    data = get_current_user_login()
    return jsonify(data)

@github_bp.route('/graphql/user-login/<username>', methods=['GET'])
def specific_user_login(username):
    data = get_specific_user_login(username)
    return jsonify(data)

# @github_bp.route('/graphql/comments/commit/<raw_data>', methods=['GET'])
# def get_user_commit_comments(raw_data):
#     data = user_commit_comments(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/comments/gist/<raw_data>', methods=['GET'])
# def get_user_gist_comments(raw_data):
#     data = user_gist_comments(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/comments/issue/<raw_data>', methods=['GET'])
# def get_user_issue_comments(raw_data):
#     data = user_issue_comments(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/comments/repo-discussion/<raw_data>', methods=['GET'])
# def get_user_repository_discussion_comments(raw_data):
#     data = user_repository_discussion_comments(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/contributions/gists/<raw_data>', methods=['GET'])
# def get_user_gists(raw_data):
#     data = user_gists(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/contributions/issues/<raw_data>', methods=['GET'])
# def get_user_issues(raw_data):
#     data = user_issues(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/contributions/pull-requests/<raw_data>', methods=['GET'])
# def get_user_pull_requests(raw_data):
#     data = user_pull_requests(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/contributions/repositories/<raw_data>', methods=['GET'])
# def get_user_repositories(raw_data):
#     data = user_repositories(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/contributions/repo-discussion/<raw_data>', methods=['GET'])
# def get_user_repository_discussions(raw_data):
#     data = user_repository_discussions(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/profiles/stats/<raw_data>', methods=['GET'])
# def get_profile_stats(raw_data):
#     data = profile_stats(raw_data)
#     return jsonify(data)

# @github_bp.route('/graphql/time-range-contributions/user-collection/<raw_data>', methods=['GET'])
# def get_user_contributions_collection(raw_data):
#     data = user_contributions_collection(raw_data)
#     return jsonify(data)
