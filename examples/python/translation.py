"""
Transcripts in Another Language (V2 API)
==========================================
Ask for a transcript in a specific language.

In V2, you only get a different language when you ask for one.
Omit the language parameter to get the original captions.
If the requested language isn't available, the API may return another
language, so always check transcript.language in the response.

Cost: translation is 1 credit per 2,500 characters.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import sys

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def transcribe_in_language(video: str, language: str) -> dict:
    """
    Extract a transcript in the specified language.

    Args:
        video: YouTube URL or 11-character video ID
        language: ISO 639-1 code (e.g., "es", "fr", "ja", "de")
    """
    response = requests.post(
        f"{BASE_URL}/transcribe",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "video": video,
            "language": language,
            "format": {"timestamp": True},
        },
    )
    response.raise_for_status()
    return response.json()


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"

    languages = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "pt": "Portuguese",
    }

    target = sys.argv[2] if len(sys.argv) > 2 else "es"

    print(f"Requesting transcript in {languages.get(target, target)}...\n")

    result = transcribe_in_language(video, language=target)

    if result.get("status") == "completed":
        data = result["data"]
        transcript = data["transcript"]
        segments = transcript.get("segments") or []
        print(f"Title: {data.get('video_title')}")
        print(f"Requested: {target}")
        print(f"Returned: {transcript.get('language')}")
        print(f"Credits used: {result.get('credits_used')}")
        print("-" * 50)

        for segment in segments[:10]:
            print(f"  {segment['text']}")

        if len(segments) > 10:
            print(f"\n  ... and {len(segments) - 10} more segments")
    else:
        print(f"Status: {result.get('status')} {result.get('error', '')}")


if __name__ == "__main__":
    main()
