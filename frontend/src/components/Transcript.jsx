import React, { useEffect, useRef } from 'react'
import { Volume2 } from 'lucide-react'

export default function Transcript({ messages = [], sessionId }) {
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="space-y-6">

      {/* Transcript Display */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Volume2 className="w-6 h-6 text-indigo-600" />
          Transcript Overview
        </h2>

        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-gray-600">
            <p>No transcript available yet. Start a conversation first.</p>
          </div>
        ) : (
          <div className="min-h-[400px] max-h-[500px] overflow-y-auto space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-lg animate-fadeIn ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-blue-50 to-blue-100 ml-[15%] border-l-4 border-blue-500'
                    : msg.role === 'assistant'
                    ? 'bg-gradient-to-r from-gray-50 to-gray-100 mr-[15%] border-l-4 border-purple-500'
                    : 'bg-yellow-50 border-l-4 border-yellow-500'
                }`}
              >
                <p className="font-semibold text-sm mb-1">
                  {msg.role === 'user'
                    ? '🗣️ You'
                    : msg.role === 'assistant'
                    ? '🤖 Sarah'
                    : '⚠️ System'}
                </p>
                <p className="text-gray-800">{msg.content}</p>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Session Info */}
      <div className="text-center">
        <p className="text-xs text-gray-500">Session: {sessionId?.slice(0, 8)}...</p>
      </div>

      {/* Animations */}
      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.4s ease-out;
        }
      `}</style>
    </div>
  )
}
