import { useState, useEffect } from 'react'
import { api } from './../services/api'
import type { User as UserType } from './../types'
import { Search, BarChart2, Users, Activity, FileText } from 'lucide-react'

const FeatureCard = ({ icon: Icon, title, description }: { 
  icon: any, 
  title: string, 
  description: string 
}) => (
  <div className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-center space-x-4 mb-4">
      <div className="bg-indigo-100 p-3 rounded-lg">
        <Icon className="h-6 w-6 text-indigo-600" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
    </div>
    <p className="text-gray-600">{description}</p>
  </div>
)

const Home = () => {
  const [user, setUser] = useState<UserType | null>(null)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await api.auth.getCurrentUser()
        setUser(userData)
      } catch (err) {
        console.log(err)
      }
    }

    fetchUser()
  }, [])

  const features = [
    {
      icon: Search,
      title: "User Analytics",
      description: "Deep dive into GitHub user profiles with comprehensive analytics and insights."
    },
    {
      icon: BarChart2,
      title: "Repository Stats",
      description: "Track repository metrics, including stars, forks, and engagement over time."
    },
    {
      icon: Activity,
      title: "Contribution Analysis",
      description: "Analyze contribution patterns across repositories and organizations."
    },
    {
      icon: Users,
      title: "Bulk Processing",
      description: "Process multiple GitHub profiles simultaneously with CSV upload support."
    },
    {
      icon: FileText,
      title: "Export Reports",
      description: "Generate and export detailed reports in CSV format for further analysis."
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="bg-white rounded-2xl shadow-sm p-8 mb-12">
          <div className="max-w-3xl">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Welcome to GitHub Miner
            </h1>
            {user ? (
              <div className="space-y-4">
                <p className="text-xl text-gray-600">
                  Welcome back, <span className="font-semibold text-indigo-600">{user.name || user.login}</span>!
                </p>
                <p className="text-gray-600">
                  Ready to explore GitHub user activities and contributions? Use the search bar above or upload a CSV file to analyze multiple users at once.
                </p>
                <div className="flex space-x-4 pt-4">
                  <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
                    Start Analysis
                  </button>
                  <button className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-50 transition-colors">
                    View Documentation
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-xl text-gray-600">
                  Discover insights from GitHub profiles and repositories
                </p>
                <p className="text-gray-600">
                  Please login with your GitHub account to start exploring the powerful features of GitHub Miner.
                </p>
                <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors mt-4">
                  Login with GitHub
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Features Grid */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>

        {/* Getting Started Section */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">Get Started Today</h2>
          <p className="text-indigo-100 mb-6">
            Start exploring GitHub analytics with our powerful tools. Upload a CSV file with GitHub usernames or search for individual users.
          </p>
          <div className="flex space-x-4">
            <button className="bg-white text-indigo-600 px-6 py-2 rounded-lg hover:bg-indigo-50 transition-colors">
              Upload CSV
            </button>
            <button className="border border-white text-white px-6 py-2 rounded-lg hover:bg-indigo-500 transition-colors">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home