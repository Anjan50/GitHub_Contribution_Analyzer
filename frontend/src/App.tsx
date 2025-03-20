import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom'
import { Search, User, GitCommit, Users, Github, Code } from 'lucide-react'
import UserInfo from './Components/UserInfo'
import UserGists from './Components/UserGists'
import UserComments from './Components/UserComments'
import UserContributions from './Components/UserContributions'
import PageHeader from './Components/PageHeader'
import { api, createErrorMessage } from './services/api'
import type { User as UserType } from './types'
import Home from './Components/Home'
import HomeComponent from './Components/HomeComponent'
import TimeRangeContributions from './Components/TimeRangeContributions'


interface SearchFormProps {
  username: string
  setUsername: (value: string) => void
  onSearch: () => void
  searchPerformed: boolean
}

const SearchForm = ({ 
  username, 
  setUsername,
  onSearch,
  searchPerformed
}: SearchFormProps) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (username.trim()) {
      onSearch()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center space-x-4">
      <input
        type="text"
        placeholder="GitHub Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
      />
      <button
        type="submit"
        className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
          searchPerformed ? 'bg-green-600 hover:bg-green-700' : 'bg-indigo-600 hover:bg-indigo-700'
        }`}
      >
        <Search className="h-4 w-4 mr-2" />
        {searchPerformed ? 'Update Search' : 'Search'}
      </button>
    </form>
  )
}

const AuthButton = () => {
  const [user, setUser] = useState<UserType | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await api.auth.getCurrentUser()
        setUser(userData)
      } catch (_err) {
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const handleLogin = () => {
    api.auth.login()
  }

  const handleLogout = async () => {
    try {
      await api.auth.logout()
      setUser(null)
    } catch (_err) {
      // Handle logout error silently
    }
  }

  if (loading) {
    return <div className="animate-pulse">Loading...</div>
  }

  if (user) {
    return (
      <div className="flex items-center space-x-4">
        <img
          src={`https://github.com/${user.login}.png`}
          alt={user.login}
          className="h-8 w-8 rounded-full"
        />
        <span className="text-sm font-medium text-gray-700">{user.login}</span>
        <button
          onClick={handleLogout}
          className="text-sm text-gray-600 hover:text-gray-900"
        >
          Logout
        </button>
      </div>
    )
  }

  return (
    <button
      onClick={handleLogin}
      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 hover:bg-gray-700"
    >
      <Github className="h-4 w-4 mr-2" />
      Login with GitHub
    </button>
  )
}

interface ProtectedRouteProps {
  children: React.ReactNode
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await api.auth.getCurrentUser()
        setIsAuthenticated(true)
      } catch (_err) {
        setIsAuthenticated(false)
      }
    }

    checkAuth()
  }, [])

  if (isAuthenticated === null) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

const App = () => {
  const [username, setUsername] = useState('')
  const [searchPerformed, setSearchPerformed] = useState(false)

  const handleSearch = () => {
    if (username.trim()) {
      setSearchPerformed(true)
    }
  }

  const ContentWrapper = ({ children }: { children: React.ReactNode }) => {
    if (!searchPerformed) {
      return (
        <div className="bg-yellow-50 p-4 rounded-md">
          <p className="text-yellow-700">
            Please search for a GitHub username to view their information.
          </p>
        </div>
      )
    }
    return <>{children}</>
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-2xl font-bold text-gray-900">GitHub Miner</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link to="/" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300">
                    Home
                  </Link>
                  <Link to="/user" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300">
                    User Info
                  </Link>
                  <Link to="/gists" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300">
                    Gists
                  </Link>
                  <Link to="/comments" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300">
                    Comments
                  </Link>
                  <Link to="/contributions" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300">
                    Contributions
                  </Link>
                  <Link to="/time-range-contributions" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300">
                    Time Range
                  </Link>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <SearchForm 
                  username={username}
                  setUsername={setUsername}
                  onSearch={handleSearch}
                  searchPerformed={searchPerformed}
                />
                <AuthButton />
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={
              <>
                <PageHeader 
                  title="GitHub Miner"
                  subtitle="Explore GitHub user activities and data"
                  icon={Search}
                />
                <Home />
                <HomeComponent/>
              </>
            } />
            <Route path="/user" element={
              <ProtectedRoute>
                <PageHeader 
                  title="User Profile"
                  icon={User}
                />
                <ContentWrapper>
                  <UserInfo username={username} />
                </ContentWrapper>
              </ProtectedRoute>
            } />
            <Route path="/gists" element={
              <ProtectedRoute>
                <PageHeader 
                  title="User Gists"
                  icon={Code}
                />
                <ContentWrapper>
                  <UserGists username={username} />
                </ContentWrapper>
              </ProtectedRoute>
            } />
            <Route path="/comments" element={
              <ProtectedRoute>
                <PageHeader 
                  title="User Comments"
                  icon={GitCommit}
                />
                <ContentWrapper>
                  <UserComments username={username} />
                </ContentWrapper>
              </ProtectedRoute>
            } />
            <Route path="/contributions" element={
              <ProtectedRoute>
                <PageHeader 
                  title="User Contributions"
                  icon={Users}
                />
                <ContentWrapper>
                  <UserContributions username={username} />
                </ContentWrapper>
              </ProtectedRoute>
            } />
            <Route path="/time-range-contributions" element={
              <ProtectedRoute>
                <PageHeader 
                  title="Time Range Contributions"
                  icon={Users}
                />
                <ContentWrapper>
                  <TimeRangeContributions username={username} />
                </ContentWrapper>
              </ProtectedRoute>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  )
}



export default App