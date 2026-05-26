import React from 'react';

export default function VideoPlayer({ src }) {
  return (
    <div style={{ marginTop: 20 }}>
      <h3>Your AI Music Video</h3>
      <video src={src} controls width="100%" />
    </div>
  );
}
