/**
 * Basic YouTube Transcript Extraction - Node.js (V2 API)
 * ========================================================
 * Extract a timestamped transcript from any YouTube video.
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
  const body = {
    video,
    format: { timestamp: true }, // include timed segments
    ...options,
  };

  const response = await fetch(`${BASE_URL}/transcribe`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(`API error ${response.status}: ${error.error} — ${error.message}`);
  }

  return response.json();
}

// Segment times are in milliseconds.
function formatTimestamp(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

// --- Main ---

const video = process.argv[2] || "dQw4w9WgXcQ";
const language = process.argv[3]; // optional

console.log(`Extracting transcript for: ${video}\n`);

try {
  const options = {};
  if (language) options.language = language;

  const result = await transcribe(video, options);

  if (result.status === "completed") {
    const { video_title, transcript } = result.data;
    const segments = transcript.segments ?? [];
    console.log(`Title: ${video_title}`);
    console.log(`Language: ${transcript.language} (${transcript.source})`);
    console.log(`Segments: ${segments.length}\n`);

    segments.slice(0, 10).forEach((seg) => {
      console.log(`[${formatTimestamp(seg.start)}] ${seg.text}`);
    });

    if (segments.length > 10) {
      console.log(`\n... and ${segments.length - 10} more segments`);
    }
  } else {
    console.log(`Status: ${result.status}`, result.error ?? "");
  }
} catch (error) {
  console.error(`Failed: ${error.message}`);
}
