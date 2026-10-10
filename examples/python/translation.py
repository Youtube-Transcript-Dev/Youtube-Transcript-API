"""
Translation (V2 API)
======================
Get transcripts translated to any language.

In V2, translation only happens when you explicitly request a language.
No surprises — omit the language parameter to get the original captions.

Cost: 1 credit per 2,500 characters.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import sys

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def transcribe_with_translation(video: str, language: str) -> dict:
    """
    Extract transcript and translate to the specified language.

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

    print(f"Translating transcript to {languages.get(target, target)}...\n")

    result = transcribe_with_translation(video, language=target)

    if result.get("success"):
        data = result["data"]
        print(f"Title: {data['title']}")
        print(f"Original language: {data.get('original_language', 'N/A')}")
        print(f"Translated to: {target}")
        print("-" * 50)

        for segment in data["transcript"][:10]:
            print(f"  {segment['text']}")

        if len(data["transcript"]) > 10:
            print(f"\n  ... and {len(data['transcript']) - 10} more segments")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
