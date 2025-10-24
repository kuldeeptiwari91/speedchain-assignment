import React from 'react'
import { Volume2 } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-purple-600 to-indigo-600 text-white p-3 rounded-lg shadow-md">
              <span className="text-3xl">🦷</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">SmileCare Dental</h1>
              <p className="text-sm text-gray-500">AI Voice Receptionist - Sarah</p>
            </div>
          </div>
          <div className="flex items-center gap-2 bg-green-50 px-4 py-2 rounded-lg border border-green-200">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-green-700">System Active</span>
          </div>
        </div>
      </div>
    </header>
  )
}