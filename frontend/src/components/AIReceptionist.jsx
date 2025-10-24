import React, { useState, useEffect } from 'react'
import Header from './Header'
import Tabs from './Tabs'
import Overview from './Overview'
import Calls from './Calls'
import Appointments from './Appointments'
import Transcript from './Transcript'
import { appointmentAPI } from '../services/appointmentAPI'

export default function AIReceptionist() {
  const [activeTab, setActiveTab] = useState('overview')

  // Conversation state
  const [conversationState, setConversationState] = useState({
    sessionId: crypto.randomUUID(),
    messages: [],
    greeted: false,
    isRecording: false,
    isProcessing: false,
    audioBlob: null,
    playedMessageIds: new Set()
  })

  // Real appointments data
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)

  // Fetch appointments on mount
  useEffect(() => {
    fetchAppointments()
  }, [])

  // Auto-refresh every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchAppointments()
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  // Fetch when switching to appointments or overview tab
  useEffect(() => {
    if (activeTab === 'appointments' || activeTab === 'overview') {
      fetchAppointments()
    }
  }, [activeTab])

  const fetchAppointments = async () => {
    try {
      setLoading(true)
      const data = await appointmentAPI.getAllAppointments()
      
      const formattedAppointments = data.map((apt, index) => ({
        id: apt.session_id || `apt-${index}`,
        clientName: apt.name || 'Unknown',
        service: apt.service || 'N/A',
        date: apt.date || 'N/A',
        time: apt.time || 'N/A',
        dentist: apt.dentist || 'TBA',
        email: apt.email || 'N/A',
        status: apt.status || 'Confirmed',
        bookedAt: apt.booked_at || new Date().toISOString()
      }))

      formattedAppointments.sort((a, b) => new Date(b.bookedAt) - new Date(a.bookedAt))

      setAppointments(formattedAppointments)
    } catch (error) {
      console.error('Error fetching appointments:', error)
    } finally {
      setLoading(false)
    }
  }

  const refreshAppointments = () => {
    fetchAppointments()
  }

  // Calculate stats
  const appointmentStats = {
    booked: appointments.length,
    confirmed: appointments.filter(apt => apt.status === 'Confirmed').length,
    pending: appointments.filter(apt => apt.status === 'Pending').length,
  }

const callStats = {
  totalCalls: conversationState.messages.filter(m => m.role === 'user').length,
  answeredCalls: conversationState.messages.filter(m => m.role === 'assistant').length,
  avgDuration: '3m 24s',
}

  const analyticsData = {
    conversionRate: appointments.length > 0 
      ? `${Math.round((appointments.length / Math.max(callStats.totalCalls, 1)) * 100)}%`
      : '0%',
    responseTime: '15s',
    customerSatisfaction: '88%',
    bookingRate: appointments.length > 0 
      ? `${Math.round((appointmentStats.confirmed / appointments.length) * 100)}%`
      : '0%',
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header />
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <Overview
            callStats={callStats}
            appointmentStats={appointmentStats}
            analyticsData={analyticsData}
            loading={loading}
            // ✅ Removed onRefresh prop
          />
        )}

        {activeTab === 'calls' && (
          <Calls
            conversationState={conversationState}
            setConversationState={setConversationState}
            onAppointmentBooked={refreshAppointments}
          />
        )}

        {activeTab === 'appointments' && (
          <Appointments 
            appointments={appointments}
            loading={loading}
            onRefresh={refreshAppointments}
          />
        )}

        {activeTab === 'transcript' && (
          <Transcript
            messages={conversationState.messages}
            sessionId={conversationState.sessionId}
          />
        )}
      </div>
    </div>
  )
}