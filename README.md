<p align="center">
  <img src="https://www.youtubetranscript.dev/logo.svg" alt="YouTubeTranscript.dev" width="80" />
</p>

<h1 align="center">YouTube Transcript API</h1>

<p align="center">
  <strong>The fastest YouTube transcript API — extract, transcribe, and transform video content at scale.</strong>
</p>

<p align="center">
  <a href="https://www.youtubetranscript.dev">Website</a> •
  <a href="https://www.youtubetranscript.dev/api-docs">Full API Docs</a> •
  <a href="https://www.youtubetranscript.dev/pricing">Pricing</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#examples">Examples</a>
</p>

<p align="center">
  <a href="https://www.youtubetranscript.dev"><img src="https://img.shields.io/badge/API-v2-brightgreen" alt="API Version" /></a>
  <a href="https://www.youtubetranscript.dev"><img src="https://img.shields.io/badge/uptime-99.9%25-brightgreen" alt="Uptime" /></a>
  <a href="https://www.youtubetranscript.dev"><img src="https://img.shields.io/badge/response_time-<200ms-blue" alt="Response Time" /></a>
  <a href="https://www.youtubetranscript.dev/pricing"><img src="https://img.shields.io/badge/free_tier-available-orange" alt="Free Tier" /></a>
  <a href="https://www.youtubetranscript.dev"><img src="https://img.shields.io/badge/languages-100+-purple" alt="Languages" /></a>
  <a href="https://www.npmjs.com/package/youtube-audio-transcript-api"><img src="https://img.shields.io/npm/v/youtube-audio-transcript-api?label=npm" alt="npm" /></a>
</p>

---

## Why YouTubeTranscript.dev?

Most YouTube transcript tools break when videos don't have captions. **We don't.** Our API extracts existing captions *and* transcribes directly from audio using AI speech recognition — covering 100% of YouTube videos.

- ⚡ **Lightning fast** — Cached transcripts return in under 2 seconds
- 🎙 **Audio transcription (ASR)** — No captions? We transcribe from the audio track
- 🌍 **100+ languages** — Multilingual support with on-demand translation
- 📤 **Multiple formats** — Timestamps, paragraphs, word-level output
- 📚 **Batch processing** — Up to 100 videos per request
- 🔔 **Webhooks** — Async processing with delivery to your endpoint
- 💰 **Predictable pricing** — 1 credit per transcript, no surprises
- 🔒 **Production ready** — 99.9% uptime SLA

**→ [Get your free API key](https://www.youtubetranscript.dev)**

---

## API V2 Overview

V2 is the streamlined, user-owned transcript model. It prioritizes fast cache hits, consistent responses, and no surprise translations unless you explicitly request a language.

### How V2 Works

1. **Check your owned transcripts** (0 credits) — if you've already fetched it, it's free
2. **Fetch captions** (1 credit) — if not owned yet
3. **Translate** (1 credit per 2,500 chars) — only when you request a specific language
4. **ASR transcription** (1 credit per 90 seconds) — async via webhook, for videos without captions

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v2/transcribe` | Extract transcript from a single video |
| `POST` | `/api/v2/batch` | Extract transcripts from up to 100 videos |
| `GET` | `/api/v2/jobs/{job_id}` | Check status of an ASR job |
| `GET` | `/api/v2/batch/{batch_id}` | Check status of a batch request |

### Credit Costs

| Method | Cost | Speed | Notes |
|--------|------|-------|-------|
| Native Captions | 1 credit | 5–10 seconds | Best quality, exact language |
| Translation | 1 credit per 2,500 chars | 5–10 seconds | Only when `language` is requested |
| ASR (Audio) | 1 credit per 90 seconds | 2–20 minutes | Async via webhook |

---

## Quick Start

### 1. Get Your API Key

Sign up at [youtubetranscript.dev](https://www.youtubetranscript.dev) and grab your API key from the [Dashboard](https://www.youtubetranscript.dev/dashboard).

### 2. Extract a Transcript

```bash
curl -X POST https://youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### 3. With Options

```bash
curl -X POST https://youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video": "dQw4w9WgXcQ",
    "language": "es",
    "format": "timestamp"
  }'
```

### 4. Batch Request (up to 100 videos)

```bash
curl -X POST https://youtubetranscript.dev/api/v2/batch \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_ids": [
      "dQw4w9WgXcQ",
      "https://www.youtube.com/watch?v=VIDEO_ID_2",
      "VIDEO_ID_3"
    ]
  }'
```

### 5. ASR with Webhook (videos without captions)

```bash
curl -X POST https://youtubetranscript.dev/api/v2/transcribe \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video": "VIDEO_ID",
    "source": "asr",
    "webhook_url": "https://yoursite.com/webhook"
  }'
```

Returns immediately with `status: "processing"`. Results are delivered to your webhook when ready.

---

## Request Reference

### Headers

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | Yes | `Bearer YOUR_API_KEY` |
| `Content-Type` | Yes | `application/json` |

### Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| `video` | Yes (single) | YouTube URL or 11-character video ID |
| `video_ids` | Yes (batch) | Array of IDs or URLs. Up to 100 per request |
| `language` | No | ISO 639-1 code (e.g., `"es"`, `"fr"`). Omit to get best available without translation |
| `source` | No | `auto` (default), `manual`, or `asr` |
| `format` | No | `timestamp`, `paragraphs`, or `words` |
| `webhook_url` | No | URL for async delivery. **Required** for `source="asr"` |

### Webhook Behavior

- Requests with `webhook_url` return immediately with `status: "processing"`
- Batch requests return cached results immediately and queue only the missing items
- Your webhook receives the final results when processing completes

### Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `invalid_request` | Invalid JSON or missing required fields |
| 400 | `invalid_parameter` | Invalid video ID or parameter value |
| 401 | `invalid_api_key` | Missing or invalid API key |
| 402 | `payment_required` | Insufficient credits |
| 404 | `no_captions` | No captions available and ASR not used |
| 429 | `rate_limit_exceeded` | Too many requests, check `Retry-After` |
| 500 | `internal_error` | Server error, retry with backoff |

**→ [Full API Documentation & OpenAPI Spec](https://www.youtubetranscript.dev/api-docs)**

---

## Examples

### Install the SDK (Node.js / TypeScript)

```bash
npm install youtube-audio-transcript-api
```

### Node.js / TypeScript (SDK)

```typescript
import { YouTubeTranscript } from "youtube-audio-transcript-api";

const yt = new YouTubeTranscript({ apiKey: "your_api_key" });

// Simple — one line
const result = await yt.getTranscript("dQw4w9WgXcQ");
console.log(result.data?.transcript.text);

// With options
const translated = await yt.transcribe({
  video: "dQw4w9WgXcQ",
  language: "es",
  format: { timestamp: true },
});

// Batch — up to 100 videos
const batch = await yt.batch({
  video_ids: ["dQw4w9WgXcQ", "jNQXAC9IVRw", "9bZkp7q19f0"],
});

// ASR for videos without captions
const asr = await yt.transcribe({
  video: "VIDEO_ID",
  source: "asr",
  allow_asr: true,
  webhook_url: "https://yoursite.com/webhook",
});
```

**→ [Full SDK documentation](https://www.npmjs.com/package/youtube-audio-transcript-api)**

### Python

```python
import requests

API_KEY = "your_api_key"

# Single video
response = requests.post(
    "https://youtubetranscript.dev/api/v2/transcribe",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={"video": "dQw4w9WgXcQ"}
)

data = response.json()
for segment in data["data"]["transcript"]:
    print(f"[{segment['start']:.1f}s] {segment['text']}")
```

### JavaScript / Node.js (without SDK)

```javascript
const response = await fetch("https://youtubetranscript.dev/api/v2/transcribe", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ video: "dQw4w9WgXcQ" }),
});

const { data } = await response.json();
console.log(data.transcript.text);
```

### More Examples

Check the [`/examples`](./examples) directory for complete, runnable scripts:

| Example | Description |
|---------|-------------|
| [Basic Extraction](./examples/python/basic_extraction.py) | Extract a single video transcript |
| [Batch Processing](./examples/python/batch_processing.py) | Process up to 100 videos at once |
| [ASR + Webhook](./examples/python/asr_webhook.py) | Transcribe videos without captions |
| [Translation](./examples/python/translation.py) | Get transcripts in any language |
| [Export Formats](./examples/python/export_formats.py) | Timestamps, paragraphs, word-level |
| [Node.js Basic](./examples/javascript/basic.mjs) | Node.js extraction example |
| [cURL Examples](./examples/curl/examples.sh) | Ready-to-run cURL commands |

---

## Use Cases

### 🤖 AI & LLM Pipelines
Feed video transcripts into GPT, Claude, or any LLM. Build RAG systems, knowledge bases, and AI assistants powered by YouTube content.

### 🎯 Content Repurposing
Turn YouTube videos into blog posts, social media content, newsletters, and more.

### 🔬 Research & Analysis
Analyze video content at scale — sentiment analysis, topic modeling, trend detection across thousands of videos.

### 📊 SEO & Marketing
Extract competitor video strategies, generate SEO-optimized content from videos, and analyze trends across your niche.

### 🎓 Education
Transcribe lectures, courses, and tutorials. Make video content searchable and accessible.

### ♿ Accessibility
Generate accurate captions and subtitles for videos that don't have them, in 100+ languages.

---

## Comparison with youtube-transcript-api (Python)

The open-source `youtube-transcript-api` Python package is a great tool, but it has limitations:

| | YouTubeTranscript.dev | youtube-transcript-api |
|---|---|---|
| Videos without captions | ✅ ASR audio transcription | ❌ Fails |
| Translation | ✅ On-demand, any language | ⚠️ Limited to YouTube's translations |
| Batch processing | ✅ Up to 100 videos/request | ❌ One at a time |
| Caching | ✅ Owned transcripts, 0 credits on re-fetch | ❌ Fetches every time |
| Webhooks | ✅ Async delivery | ❌ Not available |
| Infrastructure | ✅ Managed API, 99.9% uptime | ❌ Self-hosted, you handle rate limits |
| Rate limit handling | ✅ Managed for you | ❌ YouTube blocks you |

---

## Issues & Feedback

This is the public repository for [YouTubeTranscript.dev](https://www.youtubetranscript.dev). The API is proprietary, but we use this repo to collect feedback from our developer community.

**How you can help:**

- 🐛 **Bug Reports** — Found an issue with the API? [Open an issue](../../issues)
- 💡 **Feature Requests** — Have an idea? [Start a discussion](../../discussions)
- 📖 **Documentation Errors** — Spot something wrong in the docs? Let us know
- ⭐ **Star this repo** — Help other developers find us

---

## Links

- 🌐 [Website](https://www.youtubetranscript.dev)
- 📦 [npm SDK](https://www.npmjs.com/package/youtube-audio-transcript-api)
- 📖 [API Documentation](https://www.youtubetranscript.dev/api-docs)
- 📐 [OpenAPI Spec (YAML)](https://www.youtubetranscript.dev/api-docs#openapi)
- 💰 [Pricing](https://www.youtubetranscript.dev/pricing)
- 📧 [support@youtubetranscript.dev](mailto:support@youtubetranscript.dev)
- 💼 [LinkedIn](https://www.linkedin.com/company/youtube-transcript-dev)

---

## License

The code examples and documentation in this repository are licensed under the [MIT License](./LICENSE).

The YouTubeTranscript.dev API is a proprietary service. See [Terms of Service](https://www.youtubetranscript.dev/terms).

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://www.youtubetranscript.dev">YouTubeTranscript.dev</a></strong>
  <br />
  <sub>Trusted by 1,000+ developers worldwide</sub>
</p>
