import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

class AppointmentAPI {
  /**
   * Fetch all appointments from backend
   */
  async getAllAppointments() {
    try {
      const response = await axios.get(`${API_BASE_URL}/appointments/list`);
      return response.data.appointments || [];
    } catch (error) {
      console.error('[AppointmentAPI] Error fetching appointments:', error);
      return [];
    }
  }

  /**
   * Fetch appointments for a specific session
   */
  async getSessionAppointments(sessionId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/appointments/${sessionId}`);
      return response.data.appointments || [];
    } catch (error) {
      console.error('[AppointmentAPI] Error fetching session appointments:', error);
      return [];
    }
  }

  /**
   * Fetch conversation history (includes metadata)
   */
  async getConversationHistory(sessionId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/conversation/history/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('[AppointmentAPI] Error fetching history:', error);
      return null;
    }
  }
}

export const appointmentAPI = new AppointmentAPI();