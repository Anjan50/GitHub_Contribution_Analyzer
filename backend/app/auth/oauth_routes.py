from flask import Blueprint, redirect, url_for, session
from .oauth import oauth  # Import the OAuth object configured for GitHub integration.

oauth_bp = Blueprint("oauth", __name__)


@oauth_bp.route("/login")
def login():
    """
    Route to initiate the OAuth login process with GitHub.

    This endpoint constructs the OAuth authorization URL and redirects the user to GitHub's
    authorization page, where the user can grant or deny access to their GitHub account for this application.

    Returns:
        A redirection response to GitHub's OAuth authorization page.
    """
    # Dynamically generate the callback URL to be used after GitHub authorization.
    redirect_uri = url_for("oauth.authorize", _external=True)

    # Redirect the user to GitHub's authorization page, passing along the callback URL.
    return oauth.github.authorize_redirect(redirect_uri)


@oauth_bp.route("/authorize")
def authorize():
    try:
        # Exchange the authorization code for an access token
        token = oauth.github.authorize_access_token()
        print("Token received:", token)
        
        # Get user info
        resp = oauth.github.get("user", token=token)
        user_info = resp.json()
        print("User info:", user_info)
        
        # Store in session
        session["access_token"] = token["access_token"]
        session["login"] = user_info["login"]
        
        # Redirect to index page
        return redirect(url_for("index"))
        
    except Exception as e:
        print(f"Authorization error: {str(e)}")
        # Redirect to login page or show error
        return redirect(url_for("oauth.login"))

# @oauth_bp.route("/authorize")
# def authorize():
#     """
#     OAuth callback route for handling the response from GitHub after user authorization.

#     This endpoint exchanges the authorization code provided by GitHub for an access token,
#     fetches the user's profile information using the access token, and stores essential
#     information in the session.

#     Returns:
#         A redirection response to the index page of the application after successful authorization.
#     """
#     # Exchange the authorization code for an access token.
#     token = oauth.github.authorize_access_token()
#     print(token)

#     # Use the access token to fetch the user's GitHub profile information.
#     resp = oauth.github.get("user", token=token)
#     user_info = resp.json()  # Convert the response to JSON to extract user details.

#     # Store the access token and GitHub login in the session for future use.
#     session["access_token"] = token["access_token"]
#     session["login"] = user_info["login"]

#     # Redirect the user to the application's index page after successful authorization.
#     return redirect(url_for("index"))


@oauth_bp.route("/logout")
def logout():
    """
    Route to log the user out of the application.

    This endpoint clears all data from the session, effectively logging the user out,
    and redirects them back to the index page.

    Returns:
        A redirection response to the index page.
    """
    # Clear all data from the session to log the user out.
    session.clear()

    # Redirect the user back to the index page.
    return redirect(url_for("index"))

