import React, { useEffect, useState } from 'react';
import { getJobStatus } from '../api/client';

export default function StatusPolling({ jobId, onComplete }) {
  const [status, setStatus] = useState('queued');

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await getJobStatus(jobId);
      setStatus(data.status);
      if (data.status === 'completed' && data.video_url) {
        clearInterval(interval);
        onComplete(data.video_url);
      } else if (data.status === 'failed') {
        clearInterval(interval);
        alert('Video generation failed: ' + (data.error || 'Unknown error'));
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [jobId, onComplete]);

  return <div>Status: {status} {status === 'processing' && '⏳'}</div>;
}
