import React from 'react';

export default function AudioUploader({ onFileSelect }) {
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileSelect(file);
  };
  return (
    <div>
      <label>Upload audio (MP3, WAV): </label>
      <input type="file" accept=".mp3,.wav,.m4a" onChange={handleChange} />
    </div>
  );
}
