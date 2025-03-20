import os

class Config(object):
    DEBUG = True  # Ensure debug is enabled in your configuration for development
    SECRET_KEY = "your_secret_key_here"  # Consider using environment variables

class AuthConfig(Config):
    GITHUB_OAUTH_CLIENT_ID = "your_github_oauth_client_id_here"
    GITHUB_OAUTH_CLIENT_SECRET = "your_github_oauth_client_secret_here"



class DBConfig(Config):
    MYSQL_DATABASE_USER = "tester"
    MYSQL_DATABASE_PASSWORD = "password"
    MYSQL_DATABASE_DB = "github_graphql"
    MYSQL_DATABASE_HOST = "localhost"  # or your MySQL server address
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_HOST}/{MYSQL_DATABASE_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
