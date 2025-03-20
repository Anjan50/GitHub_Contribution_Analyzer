# 📌 Students' Pre-class GitHub Contribution Research

This project investigates students' pre-class GitHub contributions and their impact on in-class performance. It involves refactoring the GraphQL API endpoints for contribution metrics, integrating them into a Python Flask framework, and making these queries accessible via URL-based API endpoints.

🔗 **Wiki Documentation**: [Expertiza Wiki](https://wiki.expertiza.ncsu.edu/index.php?title=CSC/ECE_517_Fall_2024_-_G2401_Refactor_Graphql_API_endpoint_for_contribution_metrics)

📺 Watch the video here: [GraphQL API Overview](https://www.youtube.com/watch?v=71kupocbLWg)


## 🚀 Project Overview

### 🔹 G2401 - Refactor GraphQL API Endpoint for Contribution Metrics

This project refactors the GraphQL API endpoints in an existing codebase that gathers user GitHub contribution data, ensuring improved modularity and maintainability.

### 🔹 Key Objectives

✅ **API Endpoint Development** - Integrate existing GraphQL queries into Flask as API endpoints.
✅ **Code Refactoring** - Replace hard-coded strings with reusable constants for better maintainability.
✅ **Testing & Validation** - Conduct unit and integration tests to validate functionality.
✅ **Documentation** - Provide usage details for each endpoint.

## 🏗 API Refactoring Overview

### 🔹 Queries Refactored

#### 🔸 `/comments`
- `user_commit_comments`
- `user_gist_comments`
- `user_issue_comments`
- `user_repository_discussion_comments`

#### 🔸 `/contributions`
- `user_gists`
- `user_issues`
- `user_pull_requests`

#### 🔸 `/time_range_contributions`
- `user_contributions_collection`

### 🔹 Constants

🔹 **Field Constants** - Frequently referenced fields in GraphQL queries.
🔹 **Node Constants** - Standardized query node names.
🔹 **Argument Constants** - Common argument names for GraphQL queries.

## 🌐 Flask API Endpoints

- **`/comments`** - Fetch user comments data.
- **`/contributions`** - Retrieve user contributions (gists, issues, pull requests).
- **`/profiles`** - Get user profile statistics.
- **`/time_range_contributions`** - Fetch contributions within a specified time range.

## 🧪 Testing

Each endpoint was tested extensively for:
- Accuracy of responses
- Pagination handling
- Error management

## 🖥 Python Version & Setup

### ⚙️ Prerequisites

🔹 **GitHub Personal Access Token (PAT)** - Stored in a `.env` file.
🔹 **Python Version** - Ensure Python 3.8+ is installed.

### 📥 Installation

1️⃣ Clone the repository:
```sh
cd path/to/your/project/directory
git clone <repo_url>
```

2️⃣ Set up a virtual environment:
```sh
python -m venv venv
```

3️⃣ Activate the virtual environment:
- On macOS/Linux:
```sh
source venv/bin/activate
```
- On Windows (Command Prompt):
```sh
.\venv\Scripts\activate
```
- On Windows (PowerShell):
```sh
.\venv\Scripts\Activate.ps1
```

4️⃣ Install dependencies:
```sh
pip install -r requirements.txt
```

### 🚀 Running the Project

TBD

## 🔐 Authentication

**GitHub API requires authentication.**

- **Set up a `.env` file**:
```sh
GITHUB_TOKEN='yourGitHubPAT'
```
- The API uses [dotenv](https://pypi.org/project/python-dotenv/) to manage environment variables.

## 🛠 Project Structure

📁 `github_graphql/authentication.py` - Handles GitHub API authentication.
📁 `github_graphql/query.py` - Constructs GraphQL queries using Python classes.
📁 `github_graphql/client.py` - Manages API requests and rate limits.
📁 `queries/` - Contains predefined GraphQL queries for contributions, profiles, commits, and more.

## 📊 GraphQL Queries Implemented

### 📌 User Information Queries
- **`UserLoginViewer`** - Fetch authenticated user's login info.
- **`UserProfileStats`** - Get detailed GitHub profile statistics.

### 📌 Contribution Queries
- **`UserContributions`** - Fetch user contributions like issues and PRs.
- **`UserComments`** - Retrieve user comments on repositories.
- **`UserCommits`** - Fetch commit-related contributions within a time range.

---

# Python Version

We provide a convenient tool to query a user's GitHub metrics.

**IN ORDER TO USE THIS TOOL, YOU NEED TO PROVIDE YOUR OWN .env FILE.**
Because we use the [dotenv](https://pypi.org/project/python-dotenv/) package to load environment variable.
**YOU ALSO NEED TO PROVIDE YOUR GITHUB PERSONAL ACCESS TOKEN(PAT) IN YOUR .env FILE**
i.e. GITHUB_TOKEN = 'yourGitHubPAT'

## Installation

We recommend using virtual environment.

```shell
cd path/to/your/project/directory
python -m venv venv
```

On macOS and Linux:

```shell
source venv/bin/activate
```

On Windows (Command Prompt):

```shell
.\venv\Scripts\activate
```

On Windows (PowerShell):

```shell
.\venv\Scripts\Activate.ps1
```

then you can

```shell
pip -r requirements.txt
```

## Execution

TBD

### authentication — Basic authenticator class

Source code: [github_graphql/authentication.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/authentication.py)

This module provides the basic authentication mechanism. User needs to provide a valid GitHub PAT with correct scope to run queries.
A PersonalAccessTokenAuthenticator object will be created with the PAT that user provided. get_authorization_header method will return an
authentication header that will be used when send request to GitHub GraphQL server.

<span style="font-size: larger;">Authenticator Objects</span>

Parent class of PersonalAccessTokenAuthenticator. Serve as base class of any authenticators.

<span style="font-size: larger;">PersonalAccessTokenAuthenticator Objects</span>

Handles personal access token authentication method for GitHub clients.

`class PersonalAccessTokenAuthenticator(token)`

- The `token` argument is required. This is the user's GitHub personal access token with the necessary scope to execute the queries that the user required.

Instance methods:

`get_authorization_header()`

- Returns the authentication header as a dictionary i.e. {"Authorization": "your_access_token"}.


### 📌 Repository Queries
- **`UserRepositories`** - Fetch user-owned or contributed repositories.
- **`RepositoryContributors`** - Fetch contributors for a repository.
- **`RepositoryCommits`** - Retrieve commits from a repository's default branch.

### 📌 API Rate Limit Query
- **`RateLimit`** - Fetch remaining API request limits.

## 💡 Future Enhancements

📌 Expand the API with more contribution-related metrics.
📌 Optimize GraphQL query performance.
📌 Add front-end visualization for contribution tracking.

---

📢 **Developed by:** Anjan Diyora 👨‍💻
