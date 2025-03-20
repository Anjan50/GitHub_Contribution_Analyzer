export interface User {
    login: string;
    name: string;
    avatar_url: string;
    bio: string;
    public_repos: number;
    followers: number;
    following: number;
  }
  
  export interface Commit {
    message: string;
    author: {
      name: string;
      email: string;
      user: {
        login: string;
      }
    };
    authoredDate: string;
    additions: number;
    deletions: number;
    changedFilesIfAvailable: number;
  }
  
  export interface RepoStats {
    stars: number;
    forks: number;
    watchers: number;
    issues: number;
  }
  
  export interface Contributor {
    login: string;
    avatar_url: string;
    html_url: string;
    contributions?: number;
    role_name: string;
    type: string;
    permissions: {
      admin: boolean;
      maintain: boolean;
      push: boolean;
      triage: boolean;
      pull: boolean;
    }
  }