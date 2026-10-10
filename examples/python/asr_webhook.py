"""
ASR Audio Transcription (V2 API)
==================================
Transcribe YouTube videos that don't have captions using AI speech recognition.
This runs in the background: get the result by polling the job, or have it
POSTed to your webhook URL.

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

    mode="speech_to_text_only" always uses ASR. Use mode="auto" instead to
    try captions first and fall back to ASR only when there are none.

    Cost: 1 credit per 90 seconds of audio.

    Args:
        video: YouTube URL or 11-character video ID
        webhook_url: Optional URL to receive results when processing completes
    """
    payload = {
        "video": video,
        "mode": "speech_to_text_only",
        "format": {"timestamp": True},
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


def print_transcript(data: dict):
    transcript = data["transcript"]
    print(f"Detected language: {transcript.get('language', 'unknown')}")
    print(f"Segments: {len(transcript.get('segments') or [])}")
    print("-" * 50)
    print(f"\n{transcript['text'][:500]}...")


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"

    # Option 1: With webhook (recommended for production)
    # result = transcribe_audio(video, webhook_url="https://yoursite.com/webhook")

    # Option 2: Poll for results (good for scripts)
    print(f"🎙 Submitting ASR transcription for: {video}")
    print("This may take 2-20 minutes depending on video length...\n")

    result = transcribe_audio(video)

    if result["status"] == "completed":
        # Already transcribed before: no waiting
        print("Transcript already available!")
        print_transcript(result["data"])
        return

    if result["status"] == "requires_asr_confirmation":
        print(f"Needs confirmation: estimated {result.get('estimated_credits')} credits.")
        print(result.get("suggestion", ""))
        return

    job_id = result["job_id"]
    print(f"Job ID: {job_id}")
    print(f"Status: {result['status']}")

    while True:
        time.sleep(10)
        job = check_job_status(job_id)
        print(f"  Status: {job['status']}")

        if job["status"] == "completed":
            print("\n✅ Transcription complete!")
            print_transcript(job["data"])
            break

        if job["status"] == "failed":
            print(f"\n❌ Transcription failed: {job.get('error', 'Unknown error')}")
            break


if __name__ == "__main__":
    main()
