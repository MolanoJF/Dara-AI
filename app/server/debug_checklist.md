# GCP Deployment Debug Checklist

## Pre-Deployment Checks

### 1. Code Issues to Fix
- [x] **Linter Error**: `session_resumption_update` attribute access (lines 254-255) - Fixed with try-catch
- [x] **Import Error**: `mem0` import may fail if package not installed - Fixed with error handling
- [x] **Environment Variables**: Ensure `MEM0_API_KEY` is properly configured - Added to cloudbuild.yaml

### 2. Dependencies
- [ ] **requirements.txt**: `mem0ai>=0.1.0` added ✅
- [ ] **Dockerfile**: Should work with current setup ✅
- [ ] **Cloud Build**: No changes needed ✅

### 3. Environment Variables
- [ ] **Local**: Create `.env` file with `MEM0_API_KEY`
- [ ] **GCP**: Add `MEM0_API_KEY` to Cloud Run environment variables
- [ ] **Vertex AI**: Ensure `GOOGLE_GENAI_USE_VERTEXAI=TRUE` is set

### 4. Memory Integration
- [ ] **search_memory**: Function properly formatted ✅
- [ ] **save_memory**: Function properly formatted ✅
- [ ] **Agent Tools**: Memory tools added to agent ✅
- [ ] **System Instruction**: Updated with memory guidelines ✅

## Deployment Steps

### 1. ✅ Code Issues Fixed
- [x] Added error handling for Mem0 client initialization
- [x] Added graceful degradation when MEM0_API_KEY not set
- [x] Fixed session_resumption_update access with try-catch
- [x] Updated cloudbuild.yaml to include MEM0_API_KEY

### 2. Test Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MEM0_API_KEY="your_mem0_api_key"
export GOOGLE_API_KEY="your_google_api_key"

# Run deployment test
python test_deployment.py

# Test server startup
python multimodal_server_adk.py
```

### 3. Deploy to GCP
```bash
# Build and deploy
gcloud builds submit --config cloudbuild.yaml

# Or manually:
gcloud run deploy adk-audio-assistant \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/adk-audio-assistant/audio-assistant:latest \
  --region=us-central1 \
  --platform=managed \
  --port=8765 \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --min-instances=1 \
  --max-instances=10 \
  --session-affinity \
  --set-env-vars=GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,MEM0_API_KEY=$MEM0_API_KEY
```

## Potential Issues

### 1. Memory Client Initialization
- **Issue**: `mem0_client` initialized at module level
- **Risk**: May fail if `MEM0_API_KEY` not set
- **Solution**: ✅ Added error handling and graceful degradation

### 2. Session Resumption
- **Issue**: Linter errors on `session_resumption_update`
- **Risk**: Runtime errors if attribute doesn't exist
- **Solution**: ✅ Added try-catch with AttributeError handling

### 3. Memory API Errors
- **Issue**: Network calls to Mem0 API may fail
- **Risk**: Server crashes on memory operations
- **Solution**: Already have try-catch blocks ✅

## Testing Checklist

- [ ] **Local Import Test**: `python -c "from mem0 import MemoryClient"`
- [ ] **Local Server Test**: Start server without errors
- [ ] **Memory Search Test**: Test `search_memory` function
- [ ] **Memory Save Test**: Test `save_memory` function
- [ ] **WebSocket Test**: Test client connection
- [ ] **GCP Deployment Test**: Deploy and test in Cloud Run 