import { useState, useEffect } from 'react'
import { MessageCircle, GitPullRequest, Calendar, Download } from 'lucide-react'

interface UserCommentsProps {
  username: string
}

interface IssueComment {
  createdAt: string
}

interface GistComment {
  createdAt: string
}

interface ApiResponse {
  user: {
    issueComments?: {
      nodes: IssueComment[]
      totalCount: number
    }
    gistComments?: {
      nodes: GistComment[]
      totalCount: number
    }
    login: string
  }
}

const UserComments = ({ username }: UserCommentsProps) => {
  const [activeTab, setActiveTab] = useState<'issue' | 'gist'>('issue')
  const [issueComments, setIssueComments] = useState<IssueComment[]>([])
  const [gistComments, setGistComments] = useState<GistComment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchComments = async () => {
      setLoading(true)
      try {
        const [issueRes, gistRes] = await Promise.all([
          fetch(`/api/graphql/comments/${username}/issuecomments`, {
            credentials: 'include'
          }),
          fetch(`/api/graphql/comments/${username}/gistcomments`, {
            credentials: 'include'
          })
        ])

        const issueData: ApiResponse[] = await issueRes.json()
        const gistData: ApiResponse[] = await gistRes.json()

        setIssueComments(issueData.flatMap(d => d.user.issueComments?.nodes || []))
        setGistComments(gistData.flatMap(d => d.user.gistComments?.nodes || []))
        setError(null)
      } catch (err) {
        setError('Failed to fetch comments')
      } finally {
        setLoading(false)
      }
    }

    if (username) {
      fetchComments()
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

  const comments = activeTab === 'issue' ? issueComments : gistComments
  const totalComments = comments.length

  const handleExportCSV = () => {
    const commentsToExport = activeTab === 'issue' ? issueComments : gistComments;
    
    // Prepare CSV data
    const csvData = [
      ['Type', 'Created At', 'Date'],
      ...commentsToExport.map(comment => [
        activeTab,
        new Date(comment.createdAt).toLocaleString('en-US'),
        new Date(comment.createdAt).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      ])
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
    link.setAttribute('download', `${username}_${activeTab}_comments.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900 flex items-center">
            <MessageCircle className="h-6 w-6 mr-2 text-indigo-500" />
            Comments
          </h2>
          {(issueComments.length > 0 || gistComments.length > 0) && (
            <button
              onClick={handleExportCSV}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Download className="h-4 w-4 mr-2" />
              Export {activeTab === 'issue' ? 'Issue' : 'Gist'} Comments
            </button>
          )}
        </div>
      </div>
      {/* Stats Card */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-2 gap-6">
          <div className="flex items-center space-x-3">
            <GitPullRequest className="h-8 w-8 text-blue-500" />
            <div>
              <p className="text-sm text-gray-500">Issue Comments</p>
              <p className="text-2xl font-bold text-gray-900">{issueComments.length}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <MessageCircle className="h-8 w-8 text-green-500" />
            <div>
              <p className="text-sm text-gray-500">Gist Comments</p>
              <p className="text-2xl font-bold text-gray-900">{gistComments.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tab Selection */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('issue')}
              className={`w-1/2 py-4 px-6 text-center border-b-2 font-medium text-sm ${
                activeTab === 'issue'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <GitPullRequest className="inline-block h-5 w-5 mr-2" />
              Issue Comments
            </button>
            <button
              onClick={() => setActiveTab('gist')}
              className={`w-1/2 py-4 px-6 text-center border-b-2 font-medium text-sm ${
                activeTab === 'gist'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <MessageCircle className="inline-block h-5 w-5 mr-2" />
              Gist Comments
            </button>
          </nav>
        </div>

        <div className="p-6">
          {!totalComments ? (
            <div className="text-center text-gray-500 py-12">
              No {activeTab} comments found
            </div>
          ) : (
            <div className="relative px-6">
              <div className="absolute left-[2.60rem] top-0 bottom-0 w-px bg-gray-200"></div>
              <div className="space-y-6 relative">
                {comments.map((comment, index) => (
                  <div key={index} className="flex group">
                    <div className="relative">
                      <div className="h-9 w-9 flex items-center justify-center">
                        <div className="h-4 w-4 bg-indigo-500 rounded-full group-hover:bg-indigo-600 ring-4 ring-white" />
                      </div>
                    </div>
                    <div className="flex-1 ml-4">
                      <div className="bg-gray-50 rounded-lg p-4 group-hover:bg-gray-100 transition-colors">
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="h-4 w-4 mr-2" />
                          {new Date(comment.createdAt).toLocaleDateString('en-US', {
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
          )}
        </div>
      </div>

      {/* Footer Stats */}
      <div className="bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-500">
        Showing {totalComments} {activeTab} comments
      </div>
    </div>
  )
}

export default UserComments