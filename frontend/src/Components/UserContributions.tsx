import { useState, useEffect } from 'react'
import { GitPullRequest, Calendar, LineChart, Activity, Download } from 'lucide-react'

interface PullRequest {
  createdAt: string
}

interface ApiResponse {
  user: {
    login: string
    pullRequests: {
      nodes: PullRequest[]
      pageInfo: {
        endCursor: string
        hasNextPage: boolean
      }
      totalCount: number
    }
  }
}

interface UserContributionsProps {
  username: string
}

const UserContributions = ({ username }: UserContributionsProps) => {
  const [pullRequests, setPullRequests] = useState<PullRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [stats, setStats] = useState({ total: 0 })

  useEffect(() => {
    const fetchContributions = async () => {
      setLoading(true)
      try {
        const response = await fetch(`/api/graphql/contributions/${username}/userpullrequests`, {
          credentials: 'include'
        })
        const data: ApiResponse[] = await response.json()
        
        if (data && data[0]?.user) {
          setPullRequests(data[0].user.pullRequests.nodes)
          setStats({ total: data[0].user.pullRequests.totalCount })
        }
      } catch (err) {
        setError('Failed to fetch contributions')
      } finally {
        setLoading(false)
      }
    }

    if (username) {
      fetchContributions()
    }
  }, [username])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <p className="text-red-700">{error}</p>
      </div>
    )
  }

  // Group PRs by year and month
  const groupedPRs = pullRequests.reduce((acc, pr) => {
    const date = new Date(pr.createdAt)
    const year = date.getFullYear()
    const month = date.toLocaleString('default', { month: 'long' })
    
    if (!acc[year]) {
      acc[year] = {}
    }
    if (!acc[year][month]) {
      acc[year][month] = []
    }
    acc[year][month].push(pr)
    return acc
  }, {} as Record<number, Record<string, PullRequest[]>>)

  const years = Object.keys(groupedPRs).sort((a, b) => Number(b) - Number(a))

  const handleExportCSV = () => {
    if (!pullRequests.length) return;

    // Prepare CSV data
    const csvData = [
      ['Created At', 'Year', 'Month', 'Date', 'Time'],
      ...pullRequests.map(pr => {
        const date = new Date(pr.createdAt);
        return [
          pr.createdAt,
          date.getFullYear(),
          date.toLocaleString('default', { month: 'long' }),
          date.toLocaleDateString('en-US'),
          date.toLocaleTimeString('en-US')
        ];
      })
    ];

    // Convert to CSV string
    const csvString = csvData
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    // Create and download file
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${username}_contributions.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };


  return (
    <div className="space-y-6">
       {/* Title and Export Button */}
       <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center">
            <GitPullRequest className="h-6 w-6 mr-2 text-purple-500" />
            Contributions
          </h2>
          {pullRequests.length > 0 && (
            <button
              onClick={handleExportCSV}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Download className="h-4 w-4 mr-2" />
              Export Contributions
            </button>
          )}
        </div>
      </div>
      {/* Stats Overview */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-3 gap-6">
          <div className="flex items-center space-x-3">
            <GitPullRequest className="h-8 w-8 text-purple-500" />
            <div>
              <p className="text-sm text-gray-500">Total Pull Requests</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Activity className="h-8 w-8 text-green-500" />
            <div>
              <p className="text-sm text-gray-500">Active Years</p>
              <p className="text-2xl font-bold text-gray-900">{years.length}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <LineChart className="h-8 w-8 text-blue-500" />
            <div>
              <p className="text-sm text-gray-500">Most Active Year</p>
              <p className="text-2xl font-bold text-gray-900">
                {years[0] || 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Timeline View */}
      <div className="space-y-6">
        {years.map(year => (
          <div key={year} className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">{year}</h3>
            </div>
            <div className="p-6">
              {Object.entries(groupedPRs[year]).map(([month, prs]) => (
                <div key={month} className="mb-8 last:mb-0">
                  <h4 className="text-md font-medium text-gray-700 mb-4">{month}</h4>
                  <div className="relative px-6">
                    <div className="absolute left-[2.60rem] top-0 bottom-0 w-px bg-gray-200"></div>
                    <div className="space-y-6">
                      {prs.map((pr, index) => {
                        const date = new Date(pr.createdAt)
                        return (
                          <div key={index} className="flex group">
                            <div className="relative">
                              <div className="h-9 w-9 flex items-center justify-center">
                                <div className="h-4 w-4 bg-purple-500 rounded-full group-hover:bg-purple-600 ring-4 ring-white" />
                              </div>
                            </div>
                            <div className="flex-1 ml-4">
                              <div className="bg-gray-50 rounded-lg p-4 group-hover:bg-purple-50 transition-colors">
                                <div className="flex items-center text-sm text-gray-500">
                                  <Calendar className="h-4 w-4 mr-2" />
                                  {date.toLocaleDateString('en-US', {
                                    weekday: 'long',
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric',
                                    hour: '2-digit',
                                    minute: '2-digit'
                                  })}
                                </div>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Summary Footer */}
      <div className="bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-500">
        Showing all {stats.total} pull requests by {username}
      </div>
    </div>
  )
}

export default UserContributions