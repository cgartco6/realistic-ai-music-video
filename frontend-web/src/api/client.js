import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export async function generateVideo(audioFile, imageFile, musicUrl) {
  const formData = new FormData();
  formData.append('audio', audioFile);
  formData.append('source_image', imageFile);
  if (musicUrl) formData.append('music_url', musicUrl);
  
  const response = await axios.post(`${API_BASE}/videos/generate`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data.job_id;
}

export async function getJobStatus(jobId) {
  const response = await axios.get(`${API_BASE}/videos/status/${jobId}`);
  return response.data;
}
