import React, { useState } from 'react';
import AudioUploader from './components/AudioUploader';
import ImageUploader from './components/ImageUploader';
import VideoPlayer from './components/VideoPlayer';
import StatusPolling from './components/StatusPolling';
import { generateVideo } from './api/client';

function App() {
  const [jobId, setJobId] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [musicUrl, setMusicUrl] = useState('');

  const handleSubmit = async () => {
    if (!audioFile && !musicUrl) {
      alert("Please upload an audio file or provide a music URL");
      return;
    }
    if (!imageFile) {
      alert("Please upload a source image");
      return;
    }
    const id = await generateVideo(audioFile, imageFile, musicUrl);
    setJobId(id);
  };

  return (
    <div style={{ maxWidth: 800, margin: 'auto', padding: 20 }}>
      <h1>🎵 Realistic AI Music Video</h1>
      <AudioUploader onFileSelect={setAudioFile} />
      <input
        type="text"
        placeholder="Or paste Suno/aimusic.so link"
        value={musicUrl}
        onChange={(e) => setMusicUrl(e.target.value)}
        style={{ width: '100%', margin: '10px 0', padding: 8 }}
      />
      <ImageUploader onFileSelect={setImageFile} />
      <button onClick={handleSubmit} style={{ padding: '10px 20px', marginTop: 20 }}>
        Generate Video
      </button>
      {jobId && <StatusPolling jobId={jobId} onComplete={setVideoUrl} />}
      {videoUrl && <VideoPlayer src={videoUrl} />}
    </div>
  );
}

export default App;
