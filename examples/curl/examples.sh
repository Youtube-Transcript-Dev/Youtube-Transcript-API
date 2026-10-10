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
# Response: {"status": "completed", "data": {"video_id", "video_title",
#   "transcript": {"text", "language", "source"}}, "credits_used": ...}

# ------------------------------------------------
# 2. With Language Translation
# ------------------------------------------------
echo -e "\n=== Translated to Spanish ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "language": "es"}' | python3 -m json.tool

# ------------------------------------------------
# 3. With Timestamps
# ------------------------------------------------
# Adds data.transcript.segments: [{"text", "start", "end"}]
# start and end are in milliseconds.
echo -e "\n=== With Timestamps ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "format": {"timestamp": true}}' | python3 -m json.tool

# ------------------------------------------------
# 4. Human-Made Captions Only (never uses ASR)
# ------------------------------------------------
echo -e "\n=== Manual Captions Only ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "mode": "human_captions_only"}' | python3 -m json.tool

# ------------------------------------------------
# 5. Batch Request (Free 10 · Basic 500 · Pro 1,500 · Business 3,000 videos)
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
# 6. ASR Transcription (videos without captions)
# ------------------------------------------------
# Returns status "processing" and a job_id. Poll /jobs/{job_id} (step 7),
# or add webhook_url to have the result POSTed to you.
echo -e "\n=== ASR with Webhook ==="
curl -s -X POST "$BASE_URL/transcribe" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video": "VIDEO_ID",
    "mode": "speech_to_text_only",
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
