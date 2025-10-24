import React, { useState, useEffect, useRef } from 'react'
import {
  Mic, Square, Send, Volume2, Loader2, CheckCircle, RefreshCw,
  Play, Pause, User, Bot, MessageCircle
} from 'lucide-react'

// 🎧 Reusable voice bubble with auto-play support
function VoiceMessage({ url, role, timestamp, autoPlay = false, onPlayingChange, messageId, hasBeenPlayed }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [duration, setDuration] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  const audioRef = useRef(null)

  const togglePlay = () => {
    if (!audioRef.current) return
    if (isPlaying) {
      audioRef.current.pause()
    } else {
      audioRef.current.play()
    }
  }

  // Auto-play logic - only if autoPlay is true AND hasn't been played before
  useEffect(() => {
    if (autoPlay && audioRef.current && !hasBeenPlayed) {
      const timer = setTimeout(() => {
        audioRef.current?.play().catch(err => {
          console.log('Auto-play prevented:', err)
        })
      }, 300)
      
      return () => clearTimeout(timer)
    }
  }, [autoPlay, hasBeenPlayed])

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const onLoaded = () => setDuration(audio.duration || 0)
    const onTime = () => setCurrentTime(audio.currentTime)
    const onEnd = () => {
      setIsPlaying(false)
      if (onPlayingChange) onPlayingChange(false)
    }
    const onPlay = () => {
      setIsPlaying(true)
      if (onPlayingChange) onPlayingChange(true, messageId)
    }
    const onPause = () => {
      setIsPlaying(false)
      if (onPlayingChange) onPlayingChange(false)
    }

    audio.addEventListener('loadedmetadata', onLoaded)
    audio.addEventListener('timeupdate', onTime)
    audio.addEventListener('ended', onEnd)
    audio.addEventListener('play', onPlay)
    audio.addEventListener('pause', onPause)

    return () => {
      audio.removeEventListener('loadedmetadata', onLoaded)
      audio.removeEventListener('timeupdate', onTime)
      audio.removeEventListener('ended', onEnd)
      audio.removeEventListener('play', onPlay)
      audio.removeEventListener('pause', onPause)
    }
  }, [onPlayingChange, messageId])

  const progress = duration ? (currentTime / duration) * 100 : 0
  const formatTime = (s) => isNaN(s) ? '0:00' : `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`

  return (
    <div className={`flex items-end gap-2 ${role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
      {role === 'assistant' && (
        <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${
          isPlaying ? 'bg-indigo-500 animate-pulse' : 'bg-gray-200'
        }`}>
          <Bot className={`w-4 h-4 ${isPlaying ? 'text-white' : 'text-gray-600'}`} />
        </div>
      )}

      <div className={`p-3 rounded-2xl shadow-sm w-[250px] sm:w-[300px] transition-all ${
        role === 'user'
          ? 'bg-green-100 rounded-br-none'
          : isPlaying
            ? 'bg-indigo-50 border-2 border-indigo-400 rounded-bl-none shadow-lg'
            : 'bg-white border border-gray-200 rounded-bl-none'
      }`}>

        {/* audio element (hidden) */}
        <audio
          ref={audioRef}
          src={url}
          preload="auto"
        />

        {/* Playing indicator INSIDE bubble - only for assistant */}
        {isPlaying && role === 'assistant' && (
          <div className="mb-2 flex items-center gap-2 bg-indigo-100 rounded-lg px-2 py-1.5">
            <div className="flex gap-0.5">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="w-0.5 bg-indigo-500 rounded-full animate-pulse"
                  style={{
                    height: `${8 + (i % 2) * 4}px`,
                    animationDelay: `${i * 100}ms`
                  }}
                />
              ))}
            </div>
            <span className="text-xs font-medium text-indigo-700">Sarah is speaking...</span>
          </div>
        )}

        {/* controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={togglePlay}
            className={`p-2 rounded-full shadow-sm border transition-all ${
              isPlaying && role === 'assistant'
                ? 'bg-indigo-500 border-indigo-600 hover:bg-indigo-600'
                : 'bg-white hover:bg-gray-100 border-gray-300'
            }`}
          >
            {isPlaying ? (
              <Pause className={`w-4 h-4 ${role === 'assistant' ? 'text-white' : 'text-gray-700'}`} />
            ) : (
              <Play className="w-4 h-4 text-gray-700" />
            )}
          </button>

          <div className="flex-1">
            <div className="h-1 bg-gray-300 rounded-full overflow-hidden">
              <div 
                className={`h-1 transition-all ${
                  isPlaying && role === 'assistant' ? 'bg-indigo-500' : 'bg-green-500'
                }`}
                style={{ width: `${progress}%` }} 
              />
            </div>
            <div className="text-xs text-gray-600 flex justify-between mt-1">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>
        </div>

        <div className="text-[10px] text-gray-500 text-right mt-1">
          {timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>

      {role === 'user' && (
        <div className="w-8 h-8 bg-green-200 rounded-full flex items-center justify-center">
          <User className="w-4 h-4 text-green-700" />
        </div>
      )}
    </div>
  )
}

export default function Calls({ conversationState, setConversationState, onAppointmentBooked }) {
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const messagesEndRef = useRef(null)
  const API_BASE_URL = "http://localhost:8000/api"

  // Extract state values
  const { sessionId, messages, greeted, isRecording, isProcessing, audioBlob, playedMessageIds = new Set() } = conversationState

  // Helper to update conversation state
  const updateState = (updates) => {
    setConversationState(prev => ({ ...prev, ...updates }))
  }

  // Helper to mark message as played
  const markMessageAsPlayed = (messageId) => {
    setConversationState(prev => {
      const newPlayedIds = new Set(prev.playedMessageIds)
      newPlayedIds.add(messageId)
      return { ...prev, playedMessageIds: newPlayedIds }
    })
  }

  // Handle playing state change
  const handlePlayingChange = (isPlaying, messageId) => {
    if (isPlaying && messageId) {
      markMessageAsPlayed(messageId)
    }
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const startConversation = async () => {
    try {
      updateState({ isProcessing: true })
      const res = await fetch(`${API_BASE_URL}/conversation/greeting?session_id=${sessionId}`)
      const data = await res.json()
      
      const messageId = `greeting-${Date.now()}`
      const greetingMsg = {
        id: messageId,
        role: 'assistant',
        audioUrl: `http://localhost:8000${data.audio_url}`,
        content: data.text || 'Hello! How can I help you today?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        autoPlay: true
      }
      
      updateState({
        messages: [greetingMsg],
        greeted: true,
        isProcessing: false
      })
    } catch (err) {
      console.error(err)
      updateState({
        messages: [{ 
          id: `error-${Date.now()}`,
          role: 'system', 
          content: '❌ Cannot connect to backend! Please start the backend server.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }],
        greeted: true,
        isProcessing: false
      })
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const rec = new MediaRecorder(stream)
      mediaRecorderRef.current = rec
      audioChunksRef.current = []
      rec.ondataavailable = e => audioChunksRef.current.push(e.data)
      rec.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        updateState({ audioBlob: blob })
        stream.getTracks().forEach(t => t.stop())
      }
      rec.start()
      updateState({ isRecording: true })
    } catch {
      alert('Please allow microphone access.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      updateState({ isRecording: false })
    }
  }

  const sendAudio = async () => {
    if (!audioBlob) return
    updateState({ isProcessing: true })
    const form = new FormData()
    form.append('audio', audioBlob, 'recording.wav')
    try {
      const res = await fetch(`${API_BASE_URL}/conversation/process-voice?session_id=${sessionId}`, {
        method: 'POST',
        body: form
      })
      const result = await res.json()
      
      const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      const userMessageId = `user-${Date.now()}`
      const assistantMessageId = `assistant-${Date.now()}`
      
      const newMessages = [
        ...messages,
        { 
          id: userMessageId,
          role: 'user', 
          audioUrl: URL.createObjectURL(audioBlob),
          content: result.user_text || 'User message',
          timestamp
        },
        { 
          id: assistantMessageId,
          role: 'assistant', 
          audioUrl: `http://localhost:8000${result.audio_url}`,
          content: result.assistant_text || 'Assistant response',
          timestamp,
          autoPlay: true
        }
      ]
      
      updateState({
        messages: newMessages,
        audioBlob: null,
        isProcessing: false
      })

      // ✅ Check if appointment was booked and refresh
      if (result.intent === 'book_appointment' || result.appointment_booked) {
        setTimeout(() => {
          showEmailNotification(result.metadata?.email || result.email)
          
          // ✅ Refresh appointments if callback provided
          if (onAppointmentBooked) {
            onAppointmentBooked()
          }
        }, 1000)
      }
    } catch (e) {
      console.error(e)
      alert('Error processing audio. Please try again.')
      updateState({ isProcessing: false })
    }
  }

  const showEmailNotification = (email) => {
    const notification = document.createElement('div')
    notification.className = 'fixed top-20 right-4 bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 p-4 rounded-lg shadow-2xl z-50 animate-slideIn max-w-sm'
    notification.innerHTML = `
      <div class="flex items-start gap-3">
        <div class="bg-green-100 p-2 rounded-full">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <div class="flex-1">
          <p class="font-bold text-green-800 mb-1">✅ Appointment Confirmed!</p>
          <p class="text-sm text-green-700">Confirmation email sent to:</p>
          <p class="text-sm font-semibold text-green-900">${email || 'your email'}</p>
        </div>
        <button onclick="this.parentElement.parentElement.remove()" class="text-gray-400 hover:text-gray-600">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>
    `
    document.body.appendChild(notification)
    setTimeout(() => notification.remove(), 7000)
  }

  const resetConversation = () => {
    setConversationState({
      sessionId: crypto.randomUUID(),
      messages: [],
      greeted: false,
      isRecording: false,
      isProcessing: false,
      audioBlob: null,
      playedMessageIds: new Set()
    })
  }

  return (
    <div className="space-y-6">
      {/* Processing Overlay - FIXED */}
      {isProcessing && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[9999] overflow-hidden">
          <div className="bg-white rounded-2xl p-8 flex flex-col items-center gap-4 shadow-2xl max-w-sm mx-4">
            <div className="relative">
              <Loader2 className="w-16 h-16 text-indigo-600 animate-spin" />
              <div className="absolute inset-0 bg-indigo-400 blur-xl opacity-50 animate-pulse"></div>
            </div>
            <div className="text-center">
              <p className="text-xl font-bold text-gray-800">Sarah is thinking...</p>
              <p className="text-sm text-gray-600 mt-2">Processing your request</p>
              <div className="flex gap-1 justify-center mt-4">
                <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Chat section */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        {/* Title + Start/New Conversation Button */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Volume2 className="w-6 h-6 text-indigo-600" />
            Voice Conversation
          </h2>
          
          {/* Dynamic Button - Changes based on conversation state */}
          {!greeted ? (
            <button
              onClick={startConversation}
              disabled={isProcessing}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-colors shadow-md disabled:opacity-50"
            >
              <MessageCircle className="w-4 h-4" />
              Start Conversation
            </button>
          ) : (
            <button
              onClick={resetConversation}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              New Conversation
            </button>
          )}
        </div>

        {/* Welcome Screen - Shows before conversation starts */}
        {!greeted && messages.length === 0 && (
          <div className="min-h-[400px] flex items-center justify-center bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg">
            <div className="text-center max-w-md px-6">
              <div className="mb-6">
                <div className="inline-block bg-gradient-to-br from-purple-600 to-indigo-600 p-6 rounded-full mb-4">
                  <MessageCircle className="w-12 h-12 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  Welcome to SmileCare Dental
                </h3>
                <p className="text-gray-600">
                  Click "Start Conversation" to begin speaking with Sarah, your AI voice receptionist.
                </p>
              </div>
              <div className="space-y-2 text-sm text-gray-600">
                <p>✨ Book appointments in seconds</p>
                <p>🎙️ Natural voice conversation</p>
                <p>📧 Instant email confirmations</p>
              </div>
            </div>
          </div>
        )}

        {/* Chat messages - Only show if conversation started */}
        {messages.length > 0 && (
          <div className="min-h-[400px] max-h-[500px] overflow-y-auto space-y-4 mb-4 flex flex-col">
            {messages.map((msg, i) => (
              msg.audioUrl ? (
                <VoiceMessage 
                  key={msg.id || i}
                  messageId={msg.id}
                  url={msg.audioUrl} 
                  role={msg.role} 
                  timestamp={msg.timestamp}
                  autoPlay={msg.autoPlay}
                  hasBeenPlayed={playedMessageIds.has(msg.id)}
                  onPlayingChange={msg.role === 'assistant' ? handlePlayingChange : undefined}
                />
              ) : (
                <div key={msg.id || i} className="text-sm text-center bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                  <p className="text-yellow-800">{msg.content}</p>
                </div>
              )
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}

        {/* Recording controls - Only show after greeting */}
        {greeted && (
          <div className="text-center space-y-6">
            {!audioBlob && !isRecording && (
              <button
                onClick={startRecording}
                disabled={isProcessing}
                className="px-8 py-4 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-full font-semibold hover:from-red-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50"
              >
                <Mic className="w-6 h-6 inline mr-2" />
                Start Recording
              </button>
            )}

            {isRecording && (
              <button
                onClick={stopRecording}
                className="px-8 py-4 bg-gradient-to-r from-gray-700 to-gray-900 text-white rounded-full font-semibold hover:from-gray-800 hover:to-black transition-all shadow-lg"
              >
                <Square className="w-6 h-6 inline mr-2" />
                Stop Recording
              </button>
            )}

            {audioBlob && !isRecording && (
              <div className="space-y-4">
                <CheckCircle className="w-10 h-10 text-green-500 mx-auto" />
                <audio src={URL.createObjectURL(audioBlob)} controls className="w-full rounded-lg" />
                <div className="flex gap-4 justify-center">
                  <button
                    onClick={sendAudio}
                    disabled={isProcessing}
                    className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-full font-semibold hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="w-6 h-6 inline mr-2 animate-spin" /> Processing...
                      </>
                    ) : (
                      <>
                        <Send className="w-6 h-6 inline mr-2" /> Send
                      </>
                    )}
                  </button>
                  <button
                    onClick={() => updateState({ audioBlob: null })}
                    disabled={isProcessing}
                    className="px-6 py-3 bg-gray-200 text-gray-700 rounded-full font-semibold hover:bg-gray-300 transition-all"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Animation */}
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateX(100%); }
          to { opacity: 1; transform: translateX(0); }
        }
        .animate-fadeIn { animation: fadeIn 0.4s ease-out; }
        .animate-slideIn { animation: slideIn 0.3s ease-out; }
      `}</style>
    </div>
  )
}