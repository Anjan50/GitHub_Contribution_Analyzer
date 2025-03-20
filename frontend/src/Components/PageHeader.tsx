import type { LucideIcon } from 'lucide-react'

interface PageHeaderProps {
  title: string
  subtitle?: string
  icon?: LucideIcon
  action?: React.ReactNode
}

const PageHeader = ({ title, subtitle, icon: Icon, action }: PageHeaderProps) => {
  return (
    <div className="bg-white shadow">
      <div className="px-4 py-5 sm:px-6 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {Icon && <Icon className="h-6 w-6 text-gray-500" />}
          <div>
            <h1 className="text-lg font-medium leading-6 text-gray-900">{title}</h1>
            {subtitle && (
              <p className="mt-1 max-w-2xl text-sm text-gray-500">{subtitle}</p>
            )}
          </div>
        </div>
        {action && <div>{action}</div>}
      </div>
    </div>
  )
}

export default PageHeader