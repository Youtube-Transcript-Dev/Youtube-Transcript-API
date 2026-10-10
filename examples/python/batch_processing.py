"""
Batch Transcript Extraction (V2 API)
======================================
Extract transcripts from many videos in a single request.

Batch size depends on your plan: Free 10, Basic 500, Pro 1,500,
Business 3,000 videos per request.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import time

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def batch_transcribe(video_ids: list) -> dict:
    """
    Submit a batch of videos.

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
    video_ids = [
        "dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "9bZkp7q19f0",
    ]

    print(f"Submitting batch of {len(video_ids)} videos...\n")

    batch = batch_transcribe(video_ids)
    print(f"Batch ID: {batch['batch_id']}")

    # Cached videos come back right away; the rest finish in the background.
    while batch["status"] == "processing":
        summary = batch.get("summary", {})
        print(f"  Processing... {summary.get('succeeded', 0)}/{summary.get('total', len(video_ids))} done")
        time.sleep(5)
        batch = check_batch_status(batch["batch_id"])

    print(f"\nBatch {batch['status']}\n")

    # Each result has the same shape as a single /transcribe response.
    for item in batch.get("results", []):
        if item["status"] == "completed":
            text = item["data"]["transcript"]["text"]
            print(f"  ✅ {item['video_id']}: {len(text.split())} words")
        else:
            print(f"  ❌ {item['video_id']}: {item['status']} {item.get('error') or ''}")

    print(f"\nCredits used: {batch.get('credits_used')}")


if __name__ == "__main__":
    main()
