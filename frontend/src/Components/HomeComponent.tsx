import { useState, useRef } from 'react';
import Papa from 'papaparse';
import { Upload, Download, AlertCircle, Mail, Calendar, Hash, GitBranch, MessageSquare } from 'lucide-react';

interface UserProfileData {
  user: {
    createdAt: string;
    email: string;
    id: string;
    login: string;
    name: string;
  }
}

interface UserStatsData {
  user: {
    commitComments: { totalCount: number };
    createdAt: string;
    email: string;
    gistComments: { totalCount: number };
    issueComments: { totalCount: number };
    issues: { totalCount: number };
    login: string;
    name: string;
    pullRequests: { totalCount: number };
    repositories: { totalCount: number };
    repositoryDiscussionComments: { totalCount: number };
  }
}

interface ValidatedUser {
  profileData: UserProfileData;
  statsData: UserStatsData;
}

const UserCard = ({ data }: { data: ValidatedUser }) => {
  const { statsData: { user } } = data;
  const memberSince = new Date(user.createdAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="bg-indigo-600 rounded-lg overflow-hidden shadow-lg">
      <div className="p-6 text-white">
        <div className="flex items-center gap-4">
          <img
            src={`https://github.com/${user.login}.png`}
            alt={user.login}
            className="w-16 h-16 rounded-full border-2 border-white"
          />
          <div>
            <h3 className="text-xl font-bold">{user.name || user.login}</h3>
            <p className="text-indigo-200">@{user.login}</p>
          </div>
        </div>
        
        {user.email && (
          <div className="mt-2 flex items-center text-indigo-200">
            <Mail className="h-4 w-4 mr-2" />
            {user.email}
          </div>
        )}
        
        <div className="flex items-center text-indigo-200 mt-2">
          <Calendar className="h-4 w-4 mr-2" />
          Member since {memberSince}
        </div>
      </div>

      <div className="bg-white p-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900 flex items-center">
              <GitBranch className="h-4 w-4 mr-2 text-indigo-600" />
              Repository Stats
            </h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Repositories</span>
                <span className="font-medium">{user.repositories.totalCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Pull Requests</span>
                <span className="font-medium">{user.pullRequests.totalCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Issues</span>
                <span className="font-medium">{user.issues.totalCount}</span>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="font-medium text-gray-900 flex items-center">
              <MessageSquare className="h-4 w-4 mr-2 text-indigo-600" />
              Comments
            </h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Issues</span>
                <span className="font-medium">{user.issueComments.totalCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Commits</span>
                <span className="font-medium">{user.commitComments.totalCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Discussions</span>
                <span className="font-medium">{user.repositoryDiscussionComments.totalCount}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const HomeComponent = () => {
  const [validUsers, setValidUsers] = useState<ValidatedUser[]>([]);
  const [invalidUsers, setInvalidUsers] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndFetchUserData = async (usernames: string[]) => {
    setIsLoading(true);
    const validatedUsers: ValidatedUser[] = [];
    const invalidUsernames: string[] = [];

    const limitedUsernames = usernames.slice(0, 10);

    for (const username of limitedUsernames) {
      try {
        const [profileResponse, statsResponse] = await Promise.all([
          fetch(`/api/graphql/user-login/${username}`, {
            credentials: 'include',
          }),
          fetch(`/api/graphql/profiles/${username}`, {
            credentials: 'include',
          })
        ]);

        if (profileResponse.ok && statsResponse.ok) {
          const profileData = await profileResponse.json();
          const statsData = await statsResponse.json();
          validatedUsers.push({
            profileData,
            statsData,
          });
        } else {
          invalidUsernames.push(username);
        }
      } catch (error) {
        invalidUsernames.push(username);
      }
    }

    setValidUsers(validatedUsers);
    setInvalidUsers(invalidUsernames);
    setIsLoading(false);
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    Papa.parse(file, {
      complete: (results) => {
        const usernames = results.data
          .flat()
          .filter(username => typeof username === 'string' && username.trim() !== '');
        validateAndFetchUserData(usernames);
      }
    });
  };

  const handleExportAllUsers = () => {
    if (validUsers.length === 0) return;

    const csvData = [
      ['GitHub Username', 'Name', 'Email', 'Member Since', 'Repositories', 'Pull Requests', 
       'Issues', 'Issue Comments', 'Commit Comments', 'Discussion Comments', 'Gist Comments']
    ];

    validUsers.forEach(({ statsData }) => {
      const user = statsData.user;
      csvData.push([
        user.login,
        user.name || '',
        user.email || '',
        new Date(user.createdAt).toLocaleDateString(),
        user.repositories.totalCount,
        user.pullRequests.totalCount,
        user.issues.totalCount,
        user.issueComments.totalCount,
        user.commitComments.totalCount,
        user.repositoryDiscussionComments.totalCount,
        user.gistComments.totalCount,
      ]);
    });

    const csvString = csvData.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'github_users_analytics.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">GitHub User Analytics</h1>
          
          <div className="flex gap-4">
            <button
              onClick={() => fileInputRef.current?.click()}
              className={`inline-flex items-center px-4 py-2 rounded-md text-white ${
                isLoading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
              }`}
              disabled={isLoading}
            >
              <Upload className="h-5 w-5 mr-2" />
              Upload CSV
            </button>

            {validUsers.length > 0 && (
              <button
                onClick={handleExportAllUsers}
                className="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md"
              >
                <Download className="h-5 w-5 mr-2" />
                Export All Users
              </button>
            )}
          </div>

          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            accept=".csv"
            onChange={handleFileUpload}
          />
        </div>

        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
          </div>
        )}

        {invalidUsers.length > 0 && (
          <div className="mb-8 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center text-red-800 mb-2">
              <AlertCircle className="h-5 w-5 mr-2" />
              <h2 className="font-semibold">Invalid Usernames Detected</h2>
            </div>
            <ul className="list-disc list-inside text-red-700 space-y-1">
              {invalidUsers.map((username, index) => (
                <li key={index}>{username}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {validUsers.map((user, index) => (
            <UserCard key={index} data={user} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default HomeComponent;