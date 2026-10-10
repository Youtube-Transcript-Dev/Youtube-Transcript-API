"""
Basic YouTube Transcript Extraction (V2 API)
==============================================
Extract a timestamped transcript from any YouTube video.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import sys

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def extract_transcript(video: str, language: str = None) -> dict:
    """
    Extract a transcript from a YouTube video.

    Args:
        video: YouTube URL or 11-character video ID
        language: Optional ISO 639-1 code (e.g., "es", "fr"). Omit for best available.
    """
    payload = {
        "video": video,
        "format": {"timestamp": True},  # include timed segments
    }
    if language:
        payload["language"] = language

    response = requests.post(
        f"{BASE_URL}/transcribe",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def format_timestamp(ms: int) -> str:
    """Convert milliseconds to MM:SS format."""
    mins, secs = divmod(ms // 1000, 60)
    return f"{mins:02d}:{secs:02d}"


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"

    print(f"Extracting transcript for: {video}\n")

    result = extract_transcript(video)

    if result.get("status") == "completed":
        data = result["data"]
        transcript = data["transcript"]
        segments = transcript.get("segments") or []
        print(f"Title: {data.get('video_title')}")
        print(f"Language: {transcript.get('language', 'N/A')} ({transcript.get('source')})")
        print(f"Segments: {len(segments)}")
        print("-" * 50)

        for segment in segments:
            timestamp = format_timestamp(segment["start"])
            print(f"[{timestamp}] {segment['text']}")
    else:
        print(f"Status: {result.get('status')} {result.get('error', '')}")


if __name__ == "__main__":
    main()
