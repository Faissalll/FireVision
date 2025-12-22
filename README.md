---
title: FireVision AI
emoji: 🔥
colorFrom: red
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# FireVision AI Service

Fire detection API service using YOLOv8.

## Endpoints

- `GET /` - Health check
- `GET /api/health` - API health status
- `POST /api/start-detection` - Start fire detection session
- `POST /api/stop-detection` - Stop detection session
- `GET /api/video-feed?session=<id>` - Video stream feed
