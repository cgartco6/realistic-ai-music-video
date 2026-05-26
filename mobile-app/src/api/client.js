import axios from 'axios';

const API_BASE = 'http://your-backend-ip:8000/api'; // Replace with actual IP when testing

export async function generateVideo(audioFile, imageFile, musicUrl) {
  const formData = new FormData();
  formData.append('audio', {
    uri: audioFile.uri,
    name: audioFile.name,
    type: 'audio/mpeg'
  });
  formData.append('source_image', {
    uri: imageFile.uri,
    name: imageFile.fileName,
    type: 'image/jpeg'
  });
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
