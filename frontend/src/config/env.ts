const getEnvVariable = (key: string): string => {
    const value = import.meta.env[key] 
    
    if (!value) {
      console.warn(`Environment variable ${key} is not set`)
      return ''
    }
    
    return value
  }
  
  export const config = {
    API_URL: getEnvVariable('VITE_API_URL') || 'http://127.0.0.1:5000',
    AUTH_PATH: '/oauth',
    API_PATH: '/api',
    NODE_ENV: getEnvVariable('NODE_ENV') || 'development'
  } as const
  
  // Create URL builders for different endpoints
  export const createAuthUrl = (path: string) => `${config.API_URL}${config.AUTH_PATH}${path}`
  export const createApiUrl = (path: string) => `${config.API_URL}${config.API_PATH}${path}`