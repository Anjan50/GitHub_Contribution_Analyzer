// We don't need BASE_URL or FRONTEND_URL since we're using Vite's proxy
export const api = {
    auth: {
      getCurrentUser: async () => {
        try {
          const response = await fetch('/api/graphql/current-user-login', {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            }
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch user data');
          }
          
          const data = await response.json();
          return data.viewer;
        } catch (error) {
          console.error('Error fetching current user:', error);
          throw error;
        }
      },
      
      login: () => {
        window.location.href = '/oauth/login';
      },
      
      logout: async () => {
        try {
          const response = await fetch('/oauth/logout', {
            method: 'POST',
            credentials: 'include',
          });
          return response.ok;
        } catch (error) {
          console.error('Error during logout:', error);
          throw error;
        }
      }
    },
    
    github: {
      getCommits: async (owner: string, repo: string) => {
        try {
          const response = await fetch(
            `/api/graphql/specific-user-commits/${owner}/${repo}`,
            {
              method: 'GET',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              }
            }
          );
          
          if (!response.ok) {
            throw new Error('Failed to fetch commits');
          }
          
          return response.json();
        } catch (error) {
          console.error('Error fetching commits:', error);
          throw error;
        }
      },
      
      getContributors: async (owner: string, repo: string) => {
        try {
          const response = await fetch(
            `/api/rest/repository-contributors/${owner}/${repo}`,
            {
              method: 'GET',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              }
            }
          );
          
          if (!response.ok) {
            throw new Error('Failed to fetch contributors');
          }
          
          return response.json();
        } catch (error) {
          console.error('Error fetching contributors:', error);
          throw error;
        }
      }
    }
  };
  
  export const createErrorMessage = (error: unknown): string => {
    if (error instanceof Error) {
      return error.message;
    }
    return 'An unexpected error occurred';
  };