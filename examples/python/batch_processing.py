"""
Batch Transcript Extraction (V2 API)
======================================
Extract transcripts from up to 100 videos in a single request.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import json
import time

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def batch_transcribe(video_ids: list) -> dict:
    """
    Extract transcripts from multiple videos (up to 100).

    Args:
        video_ids: List of YouTube URLs or 11-character video IDs
    """
    response = requests.post(
        f"{BASE_URL}/batch",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"video_ids": video_ids},
    )
    response.raise_for_status()
    return response.json()


def check_batch_status(batch_id: str) -> dict:
    """Check the status of a batch request."""
    response = requests.get(
        f"{BASE_URL}/batch/{batch_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    response.raise_for_status()
    return response.json()


def main():
    # Example: batch of 5 videos
    video_ids = [
        "dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "9bZkp7q19f0",
    ]

    print(f"Submitting batch of {len(video_ids)} videos...\n")

    result = batch_transcribe(video_ids)

    if result.get("batch_id"):
        # Some results may be cached (returned immediately),
        # others may need processing
        batch_id = result["batch_id"]
        print(f"Batch ID: {batch_id}")

        # Check for immediately available results
        if result.get("completed"):
            for video in result["completed"]:
                text_preview = " ".join(
                    seg["text"] for seg in video["transcript"][:3]
                )
                print(f"  ✅ {video['video_id']}: {text_preview}...")

        # Poll for remaining results if needed
        if result.get("status") == "processing":
            print("\nWaiting for remaining videos...")
            while True:
                time.sleep(5)
                status = check_batch_status(batch_id)
                print(f"  Status: {status['status']} ({status.get('completed_count', 0)}/{len(video_ids)})")
                if status["status"] == "completed":
                    break

            print("\nAll transcripts ready!")
    else:
        # All results returned immediately (all cached)
        for video in result.get("data", []):
            word_count = sum(len(seg["text"].split()) for seg in video["transcript"])
            print(f"  ✅ {video['video_id']}: {word_count} words")

    print("\nDone!")


if __name__ == "__main__":
    main()
