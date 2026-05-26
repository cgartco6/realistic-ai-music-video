#!/bin/bash
# check-files.sh – verifies all required files exist

required_files=(
    ".env.example"
    ".gitignore"
    "docker-compose.yml"
    "Dockerfile.backend"
    "Dockerfile.frontend"
    "README.md"
    "backend/requirements.txt"
    "backend/app/__init__.py"
    "backend/app/main.py"
    "backend/app/config.py"
    "backend/app/models.py"
    "backend/app/tasks.py"
    "backend/app/api/__init__.py"
    "backend/app/api/videos.py"
    "backend/app/api/webhooks.py"
    "backend/app/services/__init__.py"
    "backend/app/services/music_source.py"
    "backend/app/services/avatar_animation.py"
    "backend/app/services/lipsync.py"
    "backend/app/services/storage.py"
    "backend/app/utils/__init__.py"
    "backend/app/utils/file_helpers.py"
    "backend/celery_worker.py"
    "backend/scripts/download_models.sh"
    "frontend-web/package.json"
    "frontend-web/public/index.html"
    "frontend-web/src/index.js"
    "frontend-web/src/App.js"
    "frontend-web/src/components/AudioUploader.js"
    "frontend-web/src/components/ImageUploader.js"
    "frontend-web/src/components/VideoPlayer.js"
    "frontend-web/src/components/StatusPolling.js"
    "frontend-web/src/api/client.js"
    "frontend-web/Dockerfile"
    "mobile-app/package.json"
    "mobile-app/App.js"
    "mobile-app/app.json"
    "mobile-app/src/screens/HomeScreen.js"
    "mobile-app/src/screens/PlayerScreen.js"
    "mobile-app/src/components/AudioPicker.js"
    "mobile-app/src/components/VideoView.js"
    "mobile-app/src/api/client.js"
    "mobile-app/Dockerfile"
    "nginx/nginx.conf"
)

missing=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        missing=1
    fi
done

if [ $missing -eq 0 ]; then
    echo "✅ All required files present. Module locked."
else
    echo "⚠️ Some files missing – check the list above."
fi
