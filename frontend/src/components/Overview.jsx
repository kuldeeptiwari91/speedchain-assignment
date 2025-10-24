import React from 'react'
import { Phone, Calendar, Stethoscope, Users, Clock, ThumbsUp, CheckCircle } from 'lucide-react'

export default function Overview({ callStats, appointmentStats, analyticsData, loading }) {
  const services = [
    'General Checkup',
    'Teeth Cleaning',
    'Root Canal',
    'Teeth Whitening',
    'Braces Consultation',
    'Dental Implants'
  ]

  const dentists = [
    { name: 'Dr. Emily Chen', specialty: 'General & Cleaning', color: 'blue' },
    { name: 'Dr. James Wilson', specialty: 'Root Canal', color: 'green' },
    { name: 'Dr. Priya Sharma', specialty: 'Cosmetic', color: 'purple' },
    { name: 'Dr. Mark Johnson', specialty: 'Orthodontics', color: 'orange' }
  ]

  const workingHours = {
    days: 'Monday - Saturday',
    time: '9:00 AM - 6:00 PM'
  }

  return (
    <div className="space-y-6">
      {/* Key Metrics - 4 cards in a row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Total Calls</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {loading ? '...' : callStats.totalCalls}
              </p>
            </div>
            <Phone className="w-12 h-12 text-blue-100" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Appointments Booked</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {loading ? '...' : appointmentStats.booked}
              </p>
            </div>
            <Calendar className="w-12 h-12 text-green-100" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Customer Satisfaction</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {loading ? '...' : analyticsData.customerSatisfaction}
              </p>
            </div>
            <ThumbsUp className="w-12 h-12 text-purple-100" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Booking Success</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {loading ? '...' : analyticsData.bookingRate}
              </p>
            </div>
            <CheckCircle className="w-12 h-12 text-orange-100" />
          </div>
        </div>
      </div>

      {/* Clinic Information Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Our Dentists */}
        <div className="bg-white rounded-lg shadow-lg p-6 border-t-4 border-purple-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-purple-100 p-3 rounded-lg">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">Our Dentists</h3>
          </div>
          <div className="space-y-3">
            {dentists.map((dentist, idx) => (
              <div 
                key={idx} 
                className="p-3 rounded-lg bg-gradient-to-r from-purple-50 to-indigo-50 border-l-4 border-purple-500"
              >
                <p className="font-bold text-gray-900">{dentist.name}</p>
                <p className="text-sm text-gray-600">{dentist.specialty}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Services Available */}
        <div className="bg-white rounded-lg shadow-lg p-6 border-t-4 border-indigo-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-indigo-100 p-3 rounded-lg">
              <Stethoscope className="w-6 h-6 text-indigo-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">Services Available</h3>
          </div>
          <ul className="space-y-2">
            {services.map((service, idx) => (
              <li key={idx} className="flex items-start gap-2 text-gray-700">
                <span className="text-indigo-500 mt-1">✓</span>
                <span>{service}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Working Hours */}
        <div className="bg-white rounded-lg shadow-lg p-6 border-t-4 border-green-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-green-100 p-3 rounded-lg">
              <Clock className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">Working Hours</h3>
          </div>
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-lg border-l-4 border-green-500">
              <p className="text-lg font-bold text-gray-800 mb-2">{workingHours.days}</p>
              <p className="text-2xl font-extrabold text-green-700">{workingHours.time}</p>
            </div>
            <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
              <p className="flex items-center gap-2">
                <span className="text-red-500">●</span>
                <span>Closed on Sundays</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Information */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg shadow-lg p-6 border-l-4 border-blue-500">
        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Phone className="w-5 h-5 text-blue-600" />
          Contact Information
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-gray-700">
          <div className="flex items-start gap-3">
            <span className="font-semibold min-w-[80px]">📍 Address:</span>
            <span>123 Healthcare Ave, Downtown</span>
          </div>
          <div className="flex items-start gap-3">
            <span className="font-semibold min-w-[80px]">📞 Phone:</span>
            <span>(555) 123-4567</span>
          </div>
          <div className="flex items-start gap-3">
            <span className="font-semibold min-w-[80px]">📧 Email:</span>
            <span>info@smilecare.com</span>
          </div>
        </div>
      </div>
    </div>
  )
}