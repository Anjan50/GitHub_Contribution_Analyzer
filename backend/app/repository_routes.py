from flask import Blueprint, jsonify, request
from app.services.github_comments_service import (get_user_commit_comments,get_user_gist_comments,get_user_issue_comments)
from app.services.github_contributions import (get_user_gists,get_issues,get_pull_requests,get_repo_discussions)
from app.services.github_contributions_service import (get_user_contributions)
from app.services.github_profile_services import (get_profile_stats,get_profile_login)
repository_bp = Blueprint('repository', __name__)

@repository_bp.route('/graphql/comments/<user>/commitcomments',methods=['GET'])
def commit_comments(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    print(pg_size)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    data=get_user_commit_comments(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/comments/<user>/gistcomments', methods=['GET'])
def gist_comments(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]

    data=get_user_gist_comments(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/comments/<user>/issuecomments', methods=['GET'])
def issue_comments(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    
    data=get_user_issue_comments(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/contributions/<user>/usergists', methods=['GET'])
def contributions_gists(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    data=get_user_gists(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/contributions/<user>/userissues', methods=['GET'])
def contributions_isues(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    data=get_issues(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/contributions/<user>/userpullrequests', methods=['GET'])
def pull_request(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    data=get_pull_requests(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/contributions/<user>/userrepodiscussions', methods=['GET'])
def repo_discussions(user):
    pg_size = request.args.get('pg_size', 100, type=int)
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
    data=get_repo_discussions(user,pg_size)
    data_list = list(data)
    
    # Use jsonify to create a proper JSON response
    return jsonify(data_list)

@repository_bp.route('/graphql/contributions/<user>', methods=['GET'])
def user_contributions(user):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    # print(start_date,end_date)
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    header = request.headers.get('Authorization')
    token = None
    if header and header.startswith('Bearer '):
        token = header.split(' ')[1]

    data = get_user_contributions(user, start_date, end_date, token)
    return jsonify(data)

@repository_bp.route('/graphql/profiles/<user>', methods=['GET'])
def user_profiles(user):
    header = request.headers.get('Authorization')
    token = None
    if header and header.startswith('Bearer '):
        token = header.split(' ')[1]

    data = get_profile_stats(user, token)
    return jsonify(data)

@repository_bp.route('/graphql/profiles/login/<user>', methods=['GET'])
def user_profiles_login(user):
    header = request.headers.get('Authorization')
    token = None
    if header and header.startswith('Bearer '):
        token = header.split(' ')[1]

    data = get_profile_login(user, token)
    return jsonify(data)





    
    