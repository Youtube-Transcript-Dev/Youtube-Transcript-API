/**
 * Basic YouTube Transcript Extraction - Node.js (V2 API)
 * ========================================================
 * Extract a transcript from any YouTube video.
 *
 * Get your free API key at: https://youtubetranscript.dev
 *
 * Usage:
 *   node basic.mjs
 *   node basic.mjs "dQw4w9WgXcQ"
 *   node basic.mjs "dQw4w9WgXcQ" "es"
 */

const API_KEY = "your_api_key_here"; // Get yours at https://youtubetranscript.dev
const BASE_URL = "https://www.youtubetranscript.dev/api/v2";

async function transcribe(video, options = {}) {
  const body = { video, ...options };

  const response = await fetch(`${BASE_URL}/transcribe`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`API error ${response.status}: ${error.error_code} — ${error.message}`);
  }

  return response.json();
}

async function batchTranscribe(videoIds) {
  const response = await fetch(`${BASE_URL}/batch`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ video_ids: videoIds }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`API error ${response.status}: ${error.error_code}`);
  }

  return response.json();
}

// --- Main ---

const video = process.argv[2] || "dQw4w9WgXcQ";
const language = process.argv[3]; // optional

console.log(`Extracting transcript for: ${video}\n`);

try {
  const options = {};
  if (language) options.language = language;

  const result = await transcribe(video, options);

  if (result.success) {
    const { title, transcript } = result.data;
    console.log(`Title: ${title}`);
    console.log(`Segments: ${transcript.length}\n`);

    transcript.slice(0, 10).forEach((seg) => {
      const mins = Math.floor(seg.start / 60);
      const secs = Math.floor(seg.start % 60);
      const ts = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
      console.log(`[${ts}] ${seg.text}`);
    });

    if (transcript.length > 10) {
      console.log(`\n... and ${transcript.length - 10} more segments`);
    }
  }
} catch (error) {
  console.error(`Failed: ${error.message}`);
}
