import React from 'react';

export default function ImageUploader({ onFileSelect }) {
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileSelect(file);
  };
  return (
    <div>
      <label>Upload source photo/video: </label>
      <input type="file" accept=".jpg,.jpeg,.png" onChange={handleChange} />
    </div>
  );
}
