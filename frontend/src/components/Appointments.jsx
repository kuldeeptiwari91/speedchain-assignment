import React from 'react'
import { Calendar, User, Stethoscope, RefreshCw, Loader2 } from 'lucide-react'

export default function Appointments({ appointments, loading, onRefresh }) {
  return (
    <div className="space-y-6">
      {/* Summary Stats - At the Top */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
          <p className="text-gray-600 text-sm font-medium">Total Appointments</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {loading ? '...' : appointments.length}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
          <p className="text-gray-600 text-sm font-medium">Confirmed</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {loading ? '...' : appointments.filter(apt => apt.status === 'Confirmed').length}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-500">
          <p className="text-gray-600 text-sm font-medium">Pending</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {loading ? '...' : appointments.filter(apt => apt.status === 'Pending').length}
          </p>
        </div>
      </div>

      {/* Booked Appointments List */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Calendar className="w-8 h-8 text-indigo-600" /> 
            Booked Appointments
          </h2>
          
          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <RefreshCw className="w-4 h-4" />
            )}
            Refresh
          </button>
        </div>
        
        {loading ? (
          <div className="text-center py-12">
            <Loader2 className="w-12 h-12 text-indigo-600 mx-auto mb-4 animate-spin" />
            <p className="text-gray-500">Loading appointments...</p>
          </div>
        ) : appointments.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No appointments scheduled yet</p>
            <p className="text-gray-400 text-sm mt-2">Appointments will appear here once booked via voice chat</p>
          </div>
        ) : (
          <div className="space-y-4">
            {appointments.map((apt, index) => (
              <div 
                key={apt.id} 
                className="bg-gradient-to-r from-amber-50 to-yellow-50 border-l-4 border-amber-500 rounded-lg p-5 shadow-md hover:shadow-lg transition-shadow"
              >
                <div className="space-y-2">
                  {/* Appointment Number */}
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-bold text-gray-900">
                      Appointment #{index + 1}
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      apt.status === 'Confirmed' 
                        ? 'bg-green-100 text-green-700' 
                        : apt.status === 'Pending'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}>
                      {apt.status}
                    </span>
                  </div>

                  {/* Service */}
                  <div className="mb-3">
                    <p className="text-xl font-bold text-gray-800 flex items-center gap-2">
                      <Stethoscope className="w-5 h-5 text-indigo-600" />
                      {apt.service}
                    </p>
                  </div>

                  {/* Date and Time */}
                  <div className="flex items-center gap-2 text-gray-700">
                    <span className="text-lg">📅</span>
                    <span className="font-medium">{apt.date} at {apt.time}</span>
                  </div>

                  {/* Dentist */}
                  <div className="flex items-center gap-2 text-gray-700">
                    <span className="text-lg">👨‍⚕️</span>
                    <span className="font-medium">{apt.dentist}</span>
                  </div>

                  {/* Client Name */}
                  <div className="flex items-center gap-2 text-gray-700">
                    <User className="w-4 h-4 text-gray-500" />
                    <span className="font-medium">{apt.clientName}</span>
                  </div>

                  {/* Email */}
                  <div className="flex items-center gap-2 text-gray-700">
                    <span className="text-lg">📧</span>
                    <span className="font-medium">{apt.email}</span>
                  </div>

                  {/* Booked timestamp */}
                  <div className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-200">
                    Booked: {new Date(apt.bookedAt).toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}