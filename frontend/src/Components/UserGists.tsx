import { useState, useEffect } from 'react'
import { Code, Calendar, Clock, GitBranch, ExternalLink, Download } from 'lucide-react'

interface GistResponse {
  user: {
    gists: {
      nodes: Array<{
        createdAt: string;
      }>;
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
      totalCount: number;
    };
    login: string;
  };
}

interface UserGistsProps {
  username: string;
}

const UserGists = ({ username }: UserGistsProps) => {
  const [gistsData, setGistsData] = useState<GistResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchGists = async () => {
      try {
        const response = await fetch(`/api/graphql/contributions/${username}/usergists`, {
          credentials: 'include'
        })
        const data = await response.json()
        setGistsData(data)
      } catch (err) {
        setError('Failed to fetch user gists')
      } finally {
        setLoading(false)
      }
    }

    if (username) {
      fetchGists()
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

  if (!gistsData.length || !gistsData[0].user.gists.nodes.length) {
    return (
      <div className="bg-yellow-50 p-4 rounded-md">
        <p className="text-yellow-700">No gists found for this user.</p>
      </div>
    )
  }

  const { user } = gistsData[0]
  const gistsByYear = user.gists.nodes.reduce((acc, gist) => {
    const year = new Date(gist.createdAt).getFullYear()
    if (!acc[year]) {
      acc[year] = []
    }
    acc[year].push(gist)
    return acc
  }, {} as Record<number, typeof user.gists.nodes>)

  const years = Object.keys(gistsByYear).sort((a, b) => Number(b) - Number(a))


  const handleExportCSV = () => {
    if (!gistsData.length) return;

    const { user } = gistsData[0];
    const gists = user.gists.nodes;

    // Prepare CSV data
    const csvData = [
      ['Created At', 'Year'],
      ...gists.map(gist => [
        new Date(gist.createdAt).toLocaleString('en-US'),
        new Date(gist.createdAt).getFullYear().toString()
      ])
    ];

    // Convert to CSV string
    const csvString = csvData
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    // Create and download the file
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${username}_gists.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-8">
      {/* Title and Export Button */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center">
            <Code className="h-6 w-6 mr-2 text-indigo-500" />
            Gists
          </h2>
          {gistsData.length > 0 && (
            <button
              onClick={handleExportCSV}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Download className="h-4 w-4 mr-2" />
              Export Profile
            </button>
          )}
        </div>
      </div>
      {/* Header Stats */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-center space-x-3">
            <Code className="h-8 w-8 text-indigo-500" />
            <div>
              <p className="text-sm text-gray-500">Total Gists</p>
              <p className="text-2xl font-bold text-gray-900">{user.gists.totalCount}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Calendar className="h-8 w-8 text-green-500" />
            <div>
              <p className="text-sm text-gray-500">Years Active</p>
              <p className="text-2xl font-bold text-gray-900">{years.length}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <GitBranch className="h-8 w-8 text-blue-500" />
            <div>
              <p className="text-sm text-gray-500">First Gist</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(user.gists.nodes[user.gists.nodes.length - 1].createdAt).getFullYear()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Timeline View */}
      <div className="space-y-6">
        {years.map(year => (
          <div key={year} className="bg-white rounded-lg shadow-sm">
            <div className="px-6 py-3 border-b border-gray-200 bg-gray-50">
              <h3 className="text-lg font-semibold text-gray-900">{year}</h3>
            </div>
            <div className="relative py-6">
              <div className="absolute left-[2.60rem] top-0 bottom-0 w-px bg-indigo-200"></div>
              <div className="space-y-6 relative">
                {gistsByYear[Number(year)].map((gist, index) => {
                  const date = new Date(gist.createdAt)
                  return (
                    <button
                      key={index}
                      onClick={() => window.open(`https://gist.github.com/${user.login}`, '_blank')}
                      className="w-full text-left group focus:outline-none"
                    >
                      <div className="flex items-center px-6">
                        <div className="relative">
                          <div className="h-9 w-9 flex items-center justify-center">
                            <div className="h-4 w-4 bg-indigo-500 rounded-full group-hover:bg-indigo-600 ring-4 ring-white transition-all duration-200"></div>
                          </div>
                        </div>
                        <div className="ml-4 flex-1">
                          <div className="bg-gray-50 rounded-lg p-3 group-hover:bg-indigo-50 transition-all duration-200">
                            <div className="flex items-center text-sm text-gray-600">
                              <Clock className="h-4 w-4 mr-2 text-gray-400" />
                              {date.toLocaleDateString('en-US', {
                                month: 'long',
                                day: 'numeric',
                                year: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                              <ExternalLink className="h-4 w-4 ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 text-indigo-500" />
                            </div>
                          </div>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer Stats */}
      <div className="bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-500">
        Showing all {user.gists.totalCount} gists for {user.login}
      </div>
    </div>
  )
}

export default UserGists