import { useState, useEffect } from 'react'
import { GitPullRequest, Calendar, LineChart, Activity, Download, Filter } from 'lucide-react'

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

interface DateRange {
  startDate: string
  endDate: string
}

interface TimeRangeContributionsProps {
  username: string
}

const TimeRangeContributions = ({ username }: TimeRangeContributionsProps) => {
  const [pullRequests, setPullRequests] = useState<PullRequest[]>([])
  const [filteredPRs, setFilteredPRs] = useState<PullRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [dateRange, setDateRange] = useState<DateRange>({
    startDate: '',
    endDate: new Date().toISOString().split('T')[0] // Today's date as default end date
  })
  const [stats, setStats] = useState({
    total: 0,
    filtered: 0,
    mostActiveDay: '',
    activeMonths: 0
  })

  // Fetch pull requests
  useEffect(() => {
    const fetchContributions = async () => {
      setLoading(true)
      try {
        const response = await fetch(`/api/graphql/contributions/${username}/userpullrequests`, {
          credentials: 'include'
        })
        const data: ApiResponse[] = await response.json()
        
        if (data && data[0]?.user) {
          const prs = data[0].user.pullRequests.nodes
          setPullRequests(prs)
          setStats(prev => ({ ...prev, total: data[0].user.pullRequests.totalCount }))
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

  // Filter and analyze contributions based on date range
  useEffect(() => {
    if (!pullRequests.length) return

    const { startDate, endDate } = dateRange
    
    let filtered = [...pullRequests]
    
    if (startDate && endDate) {
      const start = new Date(startDate).getTime()
      const end = new Date(endDate).getTime()
      
      filtered = pullRequests.filter(pr => {
        const prDate = new Date(pr.createdAt).getTime()
        return prDate >= start && prDate <= end
      })
    }

    // Calculate statistics
    const contributionsByDate = filtered.reduce((acc, pr) => {
      const date = new Date(pr.createdAt).toDateString()
      acc[date] = (acc[date] || 0) + 1
      return acc
    }, {} as Record<string, number>)

    const mostActiveDay = Object.entries(contributionsByDate)
      .sort(([, a], [, b]) => b - a)[0]?.[0] || ''

    const activeMonths = new Set(
      filtered.map(pr => {
        const date = new Date(pr.createdAt)
        return `${date.getFullYear()}-${date.getMonth()}`
      })
    ).size

    setFilteredPRs(filtered)
    setStats(prev => ({
      ...prev,
      filtered: filtered.length,
      mostActiveDay,
      activeMonths
    }))
  }, [pullRequests, dateRange])

  const handleDateRangeChange = (field: keyof DateRange, value: string) => {
    setDateRange(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleExportCSV = () => {
    if (!filteredPRs.length) return

    const csvData = [
      ['Date', 'Time', 'Created At'],
      ...filteredPRs.map(pr => {
        const date = new Date(pr.createdAt)
        return [
          date.toLocaleDateString(),
          date.toLocaleTimeString(),
          pr.createdAt
        ]
      })
    ]

    const csvString = csvData.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n')
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `${username}_contributions_${dateRange.startDate}_${dateRange.endDate}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

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

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!dateRange.startDate || !dateRange.endDate) {
      return
    }

    // Filter pull requests based on date range
    const start = new Date(dateRange.startDate).getTime()
    const end = new Date(dateRange.endDate).getTime()
    
    const filtered = pullRequests.filter(pr => {
      const prDate = new Date(pr.createdAt).getTime()
      return prDate >= start && prDate <= end
    })

    setFilteredPRs(filtered)
    setStats(prev => ({
      ...prev,
      filtered: filtered.length,
      activeMonths: new Set(
        filtered.map(pr => {
          const date = new Date(pr.createdAt)
          return `${date.getFullYear()}-${date.getMonth()}`
        })
      ).size,
      mostActiveDay: getMostActiveDay(filtered)
    }))
  }

  const getMostActiveDay = (prs: PullRequest[]) => {
    const contributionsByDate = prs.reduce((acc, pr) => {
      const date = new Date(pr.createdAt).toDateString()
      acc[date] = (acc[date] || 0) + 1
      return acc
    }, {} as Record<string, number>)

    return Object.entries(contributionsByDate)
      .sort(([, a], [, b]) => b - a)[0]?.[0] || ''
  }

  return (
    <div className="space-y-6">
      {/* Title and Date Range Selection */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <Calendar className="h-6 w-6 mr-2 text-indigo-500" />
              Time Range Contributions
            </h2>
            {filteredPRs.length > 0 && (
              <button
                onClick={handleExportCSV}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                <Download className="h-4 w-4 mr-2" />
                Export Range
              </button>
            )}
          </div>

          {/* Search Form */}
          <form onSubmit={handleSearch} className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-5 w-5 text-gray-400" />
              <span className="text-sm text-gray-500">Select date range:</span>
            </div>
            <input
              type="date"
              value={dateRange.startDate}
              onChange={(e) => handleDateRangeChange('startDate', e.target.value)}
              className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              required
            />
            <span className="text-gray-500">to</span>
            <input
              type="date"
              value={dateRange.endDate}
              onChange={(e) => handleDateRangeChange('endDate', e.target.value)}
              className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              required
            />
            <button
              type="submit"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Search Range
            </button>
          </form>
        </div>
      </div>

      {/* Show results only when search is performed */}
      {filteredPRs.length > 0 ? (
        <>
          {/* Statistics */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
              {/* ... keep existing statistics ... */}
            </div>
          </div>

          {/* Contributions Timeline */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                Pull Requests ({filteredPRs.length})
              </h3>
            </div>
            <div className="p-6">
              <div className="relative px-6">
                <div className="absolute left-[2.60rem] top-0 bottom-0 w-px bg-gray-200" />
                <div className="space-y-6">
                  {filteredPRs.map((pr, index) => (
                    <div key={index} className="flex group">
                      <div className="relative">
                        <div className="h-9 w-9 flex items-center justify-center">
                          <div className="h-4 w-4 bg-indigo-500 rounded-full group-hover:bg-indigo-600 ring-4 ring-white" />
                        </div>
                      </div>
                      <div className="flex-1 ml-4">
                        <div className="bg-gray-50 rounded-lg p-4 group-hover:bg-indigo-50 transition-colors">
                          <div className="flex items-center text-sm text-gray-500">
                            <Calendar className="h-4 w-4 mr-2" />
                            {new Date(pr.createdAt).toLocaleDateString('en-US', {
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
                  ))}
                </div>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="bg-yellow-50 p-4 rounded-md">
          <p className="text-yellow-700">
            Select a date range and click Search to view pull requests.
          </p>
        </div>
      )}

      {/* Summary Footer */}
      <div className="bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-500">
        {filteredPRs.length > 0 ? (
          <>
            Showing {filteredPRs.length} pull requests between
            {' '}{new Date(dateRange.startDate).toLocaleDateString()} and
            {' '}{new Date(dateRange.endDate).toLocaleDateString()}
          </>
        ) : (
          'Use the date range selector above to search for pull requests'
        )}
      </div>
    </div>
  )
}

export default TimeRangeContributions