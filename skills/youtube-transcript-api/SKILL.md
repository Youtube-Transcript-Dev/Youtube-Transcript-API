---
name: youtube-transcript-api
description: Extract, transcribe, and translate YouTube video transcripts using the YouTubeTranscript.dev V2 API. Supports captions, ASR audio transcription, batch processing (up to 3,000 videos, depending on plan), translation to 100+ languages, and multiple output formats. Use when working with YouTube videos, subtitles, captions, or video-to-text conversion.
license: MIT
compatibility: Requires network access to youtubetranscript.dev API. Works with any language or runtime that can make HTTP requests.
metadata:
  author: YouTubeTranscript.dev
  version: "2.0"
---

# YouTube Transcript API Skill

Use this skill when the user wants to extract transcripts from YouTube videos, transcribe videos without captions, translate video content, or process multiple videos in batch.

## When to Use

- User asks to get a transcript/subtitles/captions from a YouTube video
- User wants to transcribe a YouTube video that has no captions (ASR)
- User wants to translate a YouTube video transcript to another language
- User needs to process multiple YouTube videos at once
- User wants to build an AI/LLM pipeline that uses YouTube video content
- User wants to repurpose video content into text (blog posts, summaries, etc.)

## API Overview

**Base URL:** `https://www.youtubetranscript.dev/api/v2`

**Authentication:** Bearer token via `Authorization: Bearer YOUR_API_KEY`

Users can get a free API key at [youtubetranscript.dev](https://youtubetranscript.dev).

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v2/transcribe` | Extract transcript from a single video |
| `POST` | `/api/v2/batch` | Extract transcripts from many videos (Free 10, Basic 500, Pro 1,500, Business 3,000) |
| `GET`  | `/api/v2/jobs/{job_id}` | Check status of an ASR job |
| `GET`  | `/api/v2/batch/{batch_id}` | Check status of a batch request |

### Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| `video` | Yes (single) | YouTube URL or 11-character video ID |
| `video_ids` | Yes (batch) | Array of IDs or URLs. Per request: Free 10 · Basic 500 · Pro 1,500 · Business 3,000 |
| `language` | No | ISO 639-1 code (e.g., `"es"`, `"fr"`). Omit to get the original language. Check `transcript.language` for what you got |
| `format` | No | Object of switches: `{"timestamp": true, "paragraphs": true, "words": true}`. `timestamp` adds `segments` |
| `mode` | No | `auto` (captions, then ASR if none), `captions_only`, `human_captions_only`, or `speech_to_text_only` (always ASR). When omitted, your account default from the dashboard applies |
| `webhook_url` | No | URL that receives ASR results. Optional with `mode`: you can poll `GET /jobs/{job_id}` instead |
| `source` / `allow_asr` | No | Legacy, still supported. Use `mode` instead (don't combine them) |

### Response Shape

```json
{
  "request_id": "80230632-…",
  "status": "completed",
  "data": {
    "video_id": "UF8uR6Z6KLc",
    "video_title": "Steve Jobs' 2005 Stanford Commencement Address",
    "transcript": {
      "text": "This program is brought to you by Stanford University. …",
      "language": "en",
      "source": "manual",
      "segments": [
        { "text": "This program is brought to you by Stanford University.", "start": 7470, "end": 10369 }
      ]
    }
  },
  "credits_used": 1
}
```

- The transcript lives at `data.transcript`. It's an object, not a list.
- `data.transcript.text` is the full text, always included.
- `data.transcript.segments` is only included when you send `"format": {"timestamp": true}`.
- ⚠️ **`start` and `end` are in milliseconds.** Divide by 1000 for seconds (`7470` → 0:07).
- `transcript.language` is the language you actually got. `transcript.source` is `manual`, `auto`, or `asr`.
- `status` is `completed`, `processing` (async ASR: poll `job_id`), `failed`, or `requires_asr_confirmation`.

### Credit Costs

| Method | Cost | Speed |
|--------|------|-------|
| Native Captions | 1 credit | 5–10 seconds |
| Translation | 1 credit per 2,500 chars | 5–10 seconds |
| ASR (Audio) | 1 credit per 90 seconds | 2–20 minutes (async) |

## Examples

### Basic Transcript Extraction (Python)

```python
import requests

API_KEY = "your_api_key"

response = requests.post(
    "https://www.youtubetranscript.dev/api/v2/transcribe",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={"video": "dQw4w9WgXcQ", "format": {"timestamp": True}},
)

transcript = response.json()["data"]["transcript"]
for segment in transcript["segments"]:
    seconds = segment["start"] / 1000  # start is in milliseconds
    print(f"[{seconds:.1f}s] {segment['text']}")
```

### Basic Transcript Extraction (JavaScript/Node.js)

```javascript
const response = await fetch("https://www.youtubetranscript.dev/api/v2/transcribe", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ video: "dQw4w9WgXcQ" }),
});

const { data } = await response.json();
console.log(data.transcript.text);
```

### Using the Node.js SDK

```bash
npm install youtube-audio-transcript-api
```

```javascript
import { YouTubeTranscript } from "youtube-audio-transcript-api";

const yt = new YouTubeTranscript({ apiKey: "your_api_key" });

// Simple extraction
const result = await yt.getTranscript("dQw4w9WgXcQ");

// With translation
const translated = await yt.transcribe({
  video: "dQw4w9WgXcQ",
  language: "es",
});

// Batch (many videos in one request)
const batch = await yt.batch({
  video_ids: ["dQw4w9WgXcQ", "jNQXAC9IVRw", "9bZkp7q19f0"],
});
```

### Basic Transcript Extraction (cURL)

```bash
curl -X POST https://www.youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ"}'
```

### Batch Processing

```bash
curl -X POST https://www.youtubetranscript.dev/api/v2/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video_ids": ["dQw4w9WgXcQ", "jNQXAC9IVRw", "9bZkp7q19f0"]}'
```

### Translation

Add `"language": "es"` (or any ISO 639-1 code) to get the transcript translated:

```bash
curl -X POST https://www.youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "dQw4w9WgXcQ", "language": "es"}'
```

### ASR Transcription (videos without captions)

For videos that don't have captions, use ASR:

```bash
curl -X POST https://www.youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "VIDEO_ID", "mode": "speech_to_text_only"}'
```

This returns immediately with `status: "processing"` and a `job_id`. Poll `GET /api/v2/jobs/{job_id}` until `status` is `completed`, or add `"webhook_url"` to have the result POSTed to you.

## Error Handling

Errors return JSON like `{"error": "invalid_api_key", "message": "…"}`.

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `invalid_request` | Invalid JSON or missing required fields |
| 401 | `invalid_api_key` | Missing or invalid API key |
| 402 | `payment_required` | Insufficient credits |
| 404 | `no_captions` | No captions available and ASR not used |
| 429 | `rate_limit_exceeded` | Too many requests — check `Retry-After` header |

## Important Notes

- Always ask the user for their API key if they haven't provided one. Free keys are available at [youtubetranscript.dev](https://youtubetranscript.dev).
- Omitting the `language` parameter returns the best available transcript without translation (saves credits).
- Segment `start` and `end` are in **milliseconds**. Divide by 1000 before showing timestamps or building YouTube `?t=` links.
- Timed segments only come back when you send `"format": {"timestamp": true}`. Otherwise use `data.transcript.text`.
- ASR is async — poll the jobs endpoint or use a webhook URL.
- `mode: "auto"` and `mode: "speech_to_text_only"` can charge ASR credits. Use `"mode": "captions_only"` to make sure a request never does.
- Batch endpoint accepts both YouTube URLs and 11-character video IDs.
- Re-fetching an already-owned transcript costs 0 credits.

## Resources

- [Website](https://youtubetranscript.dev)
- [Full API Docs & OpenAPI Spec](https://youtubetranscript.dev/api-docs)
- [npm SDK](https://www.npmjs.com/package/youtube-audio-transcript-api)
- [Pricing](https://youtubetranscript.dev/pricing)
