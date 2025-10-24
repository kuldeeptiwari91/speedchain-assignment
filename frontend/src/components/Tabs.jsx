import React from 'react'

const tabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'calls', label: 'Calls' },
  { id: 'appointments', label: 'Appointments' },
  { id: 'transcript', label: 'Transcript' }, 
]

export default function Tabs({ activeTab, setActiveTab }) {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex gap-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-2 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  )
}