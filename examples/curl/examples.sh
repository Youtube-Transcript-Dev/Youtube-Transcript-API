#!/bin/bash
# ================================================
# YouTubeTranscript.dev V2 API — cURL Examples
# ================================================
# Get your free API key at: https://youtubetranscript.dev
#
# Replace YOUR_API_KEY with your actual key

API_KEY="YOUR_API_KEY"
BASE_URL="https://www.youtubetranscript.dev/api/v2"

# ------------------------------------------------
# 1. Basic Transcript Extraction
# ------------------------------------------------
echo "=== Basic Extraction ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ"}' | python3 -m json.tool

# ------------------------------------------------
# 2. With Language Translation
# ------------------------------------------------
echo -e "\n=== Translated to Spanish ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "language": "es"}' | python3 -m json.tool

# ------------------------------------------------
# 3. With Format Options
# ------------------------------------------------
echo -e "\n=== With Timestamps ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "format": "timestamp"}' | python3 -m json.tool

# ------------------------------------------------
# 4. Manual Captions Only
# ------------------------------------------------
echo -e "\n=== Manual Captions Only ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "source": "manual"}' | python3 -m json.tool

# ------------------------------------------------
# 5. Batch Request (up to 100 videos)
# ------------------------------------------------
echo -e "\n=== Batch Request ==="
curl -s -X POST "$BASE_URL/batch" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_ids": [
      "dQw4w9WgXcQ",
      "jNQXAC9IVRw",
      "9bZkp7q19f0"
    ]
  }' | python3 -m json.tool

# ------------------------------------------------
# 6. ASR Transcription with Webhook
# ------------------------------------------------
echo -e "\n=== ASR with Webhook ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video": "VIDEO_ID",
    "source": "asr",
    "webhook_url": "https://yoursite.com/webhook"
  }' | python3 -m json.tool

# ------------------------------------------------
# 7. Check ASR Job Status
# ------------------------------------------------
echo -e "\n=== Check Job Status ==="
curl -s "$BASE_URL/jobs/YOUR_JOB_ID" \
  -H "Authorization: Bearer $API_KEY" | python3 -m json.tool

# ------------------------------------------------
# 8. Check Batch Status
# ------------------------------------------------
echo -e "\n=== Check Batch Status ==="
curl -s "$BASE_URL/batch/YOUR_BATCH_ID" \
  -H "Authorization: Bearer $API_KEY" | python3 -m json.tool
