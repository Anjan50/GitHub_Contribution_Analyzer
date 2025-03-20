import { useState, useEffect } from 'react'
import { User as UserIcon, Mail, Calendar, Download, GitBranch, MessageSquare, GitPullRequest, Hash } from 'lucide-react'

interface UserProfileData {
  user: {
    createdAt: string
    email: string
    id: string
    login: string
    name: string
  }
}

interface UserStatsData {
  user: {
    commitComments: { totalCount: number }
    createdAt: string
    email: string
    gistComments: { totalCount: number }
    issueComments: { totalCount: number }
    issues: { totalCount: number }
    login: string
    name: string
    pullRequests: { totalCount: number }
    repositories: { totalCount: number }
    repositoryDiscussionComments: { totalCount: number }
  }
}

interface UserInfoProps {
  username?: string
}

const UserInfo = ({ username }: UserInfoProps) => {
  const [profileData, setProfileData] = useState<UserProfileData | null>(null)
  const [statsData, setStatsData] = useState<UserStatsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        // Fetch basic profile data
        const profileResponse = await fetch(`/api/graphql/user-login/${username}`, {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          }
        });

        // Fetch detailed stats data
        const statsResponse = await fetch(`/api/graphql/profiles/${username}`, {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          }
        });

        if (!profileResponse.ok || !statsResponse.ok) {
          throw new Error('Failed to fetch user data');
        }

        const profileData = await profileResponse.json();
        const statsData = await statsResponse.json();

        setProfileData(profileData);
        setStatsData(statsData);
        setError(null);
      } catch (err) {
        setError('Failed to fetch user data');
        setProfileData(null);
        setStatsData(null);
      } finally {
        setLoading(false);
      }
    };

    if (username) {
      fetchData();
    }
  }, [username]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 p-4 rounded-md">
        <div className="text-red-700">{error}</div>
      </div>
    );
  }

  const user = statsData?.user;
  const profile = profileData?.user;

  if (!user || !profile) {
    return (
      <div className="bg-yellow-50 p-4 rounded-md">
        <div className="text-yellow-700">
          {username ? `No data found for user ${username}` : 'No user data available'}
        </div>
      </div>
    );
  }

  const handleExportCSV = () => {
    const csvData = [
      ['GitHub Profile Information'],
      ['Basic Information'],
      ['Field', 'Value'],
      ['Name', user.name || ''],
      ['Username', user.login],
      ['Email', user.email || 'Not available'],
      ['GitHub ID', profile.id],
      ['Member Since', new Date(user.createdAt).toLocaleDateString()],
      [''],
      ['Activity Statistics'],
      ['Repositories', user.repositories.totalCount],
      ['Pull Requests', user.pullRequests.totalCount],
      ['Issues Created', user.issues.totalCount],
      [''],
      ['Comments Activity'],
      ['Issue Comments', user.issueComments.totalCount],
      ['Commit Comments', user.commitComments.totalCount],
      ['Discussion Comments', user.repositoryDiscussionComments.totalCount],
      ['Gist Comments', user.gistComments.totalCount],
    ];

    const csvString = csvData
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${user.login}_github_profile_stats.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-4">
      {/* Main Profile Card */}
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Profile Header */}
        <div className="px-6 py-8 bg-gradient-to-r from-indigo-600 to-purple-600">
          <div className="flex justify-between items-start mb-6">
            <div className="flex items-center space-x-4">
              <img
                src={`https://github.com/${user.login}.png`}
                alt={user.login}
                className="h-24 w-24 rounded-full ring-4 ring-white"
              />
              <div className="text-white">
                <h1 className="text-2xl font-bold">{user.name || user.login}</h1>
                <p className="text-indigo-100">@{user.login}</p>
                {user.email && (
                  <p className="text-indigo-100 flex items-center mt-2">
                    <Mail className="h-4 w-4 mr-2" />
                    {user.email}
                  </p>
                )}
              </div>
            </div>
            <button
              onClick={handleExportCSV}
              className="bg-white text-indigo-600 px-4 py-2 rounded-md flex items-center hover:bg-indigo-50 transition-colors"
            >
              <Download className="h-4 w-4 mr-2" />
              Export Profile
            </button>
          </div>
          
          <div className="flex items-center text-indigo-100">
            <Calendar className="h-4 w-4 mr-2" />
            Member since {new Date(user.createdAt).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </div>
        </div>

        {/* GitHub ID */}
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center text-gray-600">
            <Hash className="h-4 w-4 mr-2" />
            GitHub ID: {profile.id}
          </div>
        </div>

        {/* Statistics Grid */}
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Repository Stats */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center mb-4">
              <GitBranch className="h-5 w-5 mr-2 text-indigo-600" />
              Repository Statistics
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Total Repositories</span>
                <span className="font-semibold text-gray-900">{user.repositories.totalCount}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Pull Requests</span>
                <span className="font-semibold text-gray-900">{user.pullRequests.totalCount}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Issues Created</span>
                <span className="font-semibold text-gray-900">{user.issues.totalCount}</span>
              </div>
            </div>
          </div>

          {/* Comments Stats */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center mb-4">
              <MessageSquare className="h-5 w-5 mr-2 text-indigo-600" />
              Comment Activity
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Issue Comments</span>
                <span className="font-semibold text-gray-900">{user.issueComments.totalCount}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Commit Comments</span>
                <span className="font-semibold text-gray-900">{user.commitComments.totalCount}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Discussion Comments</span>
                <span className="font-semibold text-gray-900">{user.repositoryDiscussionComments.totalCount}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Gist Comments</span>
                <span className="font-semibold text-gray-900">{user.gistComments.totalCount}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserInfo;