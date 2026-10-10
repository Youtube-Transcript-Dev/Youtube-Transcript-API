"""
ASR Audio Transcription with Webhook (V2 API)
================================================
Transcribe YouTube videos that don't have captions using AI speech recognition.
Results are delivered asynchronously to your webhook URL.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import time
import sys

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def transcribe_audio(video: str, webhook_url: str = None) -> dict:
    """
    Transcribe a YouTube video from its audio track.

    Uses ASR (Automatic Speech Recognition) for videos without captions.
    This is an async operation — results are delivered via webhook or polling.

    Cost: 1 credit per 90 seconds of audio.

    Args:
        video: YouTube URL or 11-character video ID
        webhook_url: URL to receive results when processing completes
    """
    payload = {
        "video": video,
        "source": "asr",
    }
    if webhook_url:
        payload["webhook_url"] = webhook_url

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


def check_job_status(job_id: str) -> dict:
    """Poll for ASR job completion."""
    response = requests.get(
        f"{BASE_URL}/jobs/{job_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    response.raise_for_status()
    return response.json()


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"

    # Option 1: With webhook (recommended for production)
    # result = transcribe_audio(video, webhook_url="https://yoursite.com/webhook")
    # print(f"Job submitted! Results will be delivered to your webhook.")

    # Option 2: Poll for results (good for scripts)
    print(f"🎙 Submitting ASR transcription for: {video}")
    print("This may take 2-20 minutes depending on video length...\n")

    result = transcribe_audio(video)
    job_id = result.get("job_id")

    if not job_id:
        # Transcript was already cached
        print("Transcript already available (cached)!")
        return

    print(f"Job ID: {job_id}")
    print(f"Status: {result['status']}")

    # Poll until complete
    while True:
        time.sleep(10)
        status = check_job_status(job_id)
        print(f"  Status: {status['status']}")

        if status["status"] == "completed":
            data = status["data"]
            print(f"\n✅ Transcription complete!")
            print(f"Detected language: {data.get('detected_language', 'unknown')}")
            print(f"Segments: {len(data['transcript'])}")
            print("-" * 50)

            full_text = " ".join(seg["text"] for seg in data["transcript"])
            print(f"\n{full_text[:500]}...")
            break

        elif status["status"] == "failed":
            print(f"\n❌ Transcription failed: {status.get('error', 'Unknown error')}")
            break


if __name__ == "__main__":
    main()
