"""
Basic YouTube Transcript Extraction (V2 API)
==============================================
Extract a transcript from any YouTube video.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import sys

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def extract_transcript(video: str, language: str = None, format: str = None) -> dict:
    """
    Extract transcript from a YouTube video.

    Args:
        video: YouTube URL or 11-character video ID
        language: Optional ISO 639-1 code (e.g., "es", "fr"). Omit for best available.
        format: Optional - "timestamp", "paragraphs", or "words"
    """
    payload = {"video": video}
    if language:
        payload["language"] = language
    if format:
        payload["format"] = format

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


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"

    print(f"Extracting transcript for: {video}\n")

    result = extract_transcript(video)

    if result.get("success"):
        data = result["data"]
        print(f"Title: {data['title']}")
        print(f"Language: {data.get('language', 'N/A')}")
        print(f"Segments: {len(data['transcript'])}")
        print("-" * 50)

        for segment in data["transcript"]:
            timestamp = format_timestamp(segment["start"])
            print(f"[{timestamp}] {segment['text']}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
