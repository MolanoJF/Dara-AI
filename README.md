# ADK + Vertex AI Live API Demo

A demonstration project showcasing how to build real-time, streaming multimodal experiences using Google's Agent Development Kit (ADK) with the Vertex AI Live API.

## Overview

This repository contains a complete implementation of a multimodal assistant that can:

- Process real-time audio input from a microphone
- Analyze video input from webcam or screen sharing
- Stream responses as audio and text
- Showcase function calling capabilities with the ADK

The project demonstrates how to go beyond the standard ADK CLI by creating a custom server implementation that integrates directly with the Live API streaming functionality.

## Repository Structure

```
- adk_audio_to_audio.py      # Standalone ADK audio assistant example
- app/
  - client/                  # Frontend web client
    - audio-client.js        # Audio WebSocket client base class
    - multimodal-client.js   # Extended client with video capabilities
    - multimodal.html        # Web UI for the demo
  - server/                  # Backend server implementation
    - common.py              # Shared utilities and mock functions
    - multimodal_server_adk.py  # ADK integration with WebSockets
    - start_servers.sh       # Server startup script
    - DEPLOYMENT.md          # Deployment instructions
```

## Key Features

- **Bidirectional Audio Streaming**: Real-time voice conversation with the Gemini model
- **Video Analysis**: Process webcam or screen sharing video frames
- **WebSocket Communication**: Low-latency bidirectional communication
- **Function Calling**: Demonstration of ADK tool integration with a mock order status function
- **Google Search Grounding**: Access to current information on the web for up-to-date responses
- **Long-term Memory**: Mem0 integration for persistent memory across conversations
- **Full ADK Integration**: Uses ADK's `LiveRequestQueue` and `Runner` for communication with Gemini

## Getting Started

### Prerequisites

- Google Cloud project with API access
- Python 3.9+
- Google ADK installed (`pip install google-adk`)
- A browser with microphone access (and camera or screen-sharing access for video)

### Installation

1. Clone this repository
   ```
   git clone https://github.com/MolanoJF/Dara-AI.git
   cd Dara-AI
   ```

2. Install server dependencies
   ```
   cd app/server
   pip install -r requirements.txt
   ```

3. Set up environment variables
   The checked-in configuration enables Vertex AI and hard-codes a project ID in `app/server/config/config.py`. Set it to your Google Cloud project, configure application default credentials, and enable the required Vertex AI APIs. The configured preview model may no longer be available. For the alternative developer API endpoint, set `VERTEX_API = False` in that file.

   Create a `.env` file in the `app/server` directory with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   MEM0_API_KEY=your_mem0_api_key_here
   ```

4. Start the server
   ```
   ./start_servers.sh
   ```

5. In a second terminal, serve the client from the repository root:
   ```bash
   python -m http.server 8000 --directory app/client
   ```
   Open [http://localhost:8000/multimodal.html](http://localhost:8000/multimodal.html). The client connects to `ws://localhost:8765`.

## Deployment

This project includes detailed instructions for deploying to Google Cloud Run with WebSocket support and session affinity. See [DEPLOYMENT.md](app/server/DEPLOYMENT.md) for complete deployment instructions.

Key deployment features:
- Cloud Run with WebSocket support via annotations
- Session affinity for stable connections
- Docker container configuration
- Artifact Registry integration

## How It Works

The implementation uses several key technologies:

1. **ADK Integration**: The server uses ADK's `LiveRequestQueue` to stream audio and video to Gemini
2. **WebSockets**: Bidirectional communication between client and server
3. **Media Processing**: Browser APIs capture and process audio/video
4. **Async Processing**: Python's asyncio powers the server-side concurrency

### Server Architecture

The server manages several concurrent tasks:
- WebSocket connection handling
- Audio processing and streaming
- Video frame processing
- Response handling from Gemini
- Google Search grounding for current information
- Long-term memory storage and retrieval using Mem0

### Memory Integration

The assistant now has persistent memory capabilities through Mem0:
- **Conversation Storage**: Automatically saves conversations after each turn
- **Memory Search**: Can search previous conversations for context
- **Personal Details**: Remembers user preferences, family members, and important information
- **Cross-Session**: Memory persists across different chat sessions

### Client Implementation

The client handles:
- Audio recording and playback
- Video capture (webcam and screen sharing)
- WebSocket communication
- UI updates and transcription display

## Additional Resources

- [Original Article: Going Beyond the ADK CLI](https://github.com/SaschaHeyer/gen-ai-livestream/tree/main/agents/agent-development-kit/live-api/app)
- [Full Project with Additional Features](https://github.com/SaschaHeyer/gen-ai-livestream/tree/main/multimodal-live-api/ui)

## License
This project is licensed under the MIT License.
