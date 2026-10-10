"""
Export Formats (V2 API)
=========================
Get timestamped segments, paragraphs, or word-level timings, then save
the transcript as plain text and as SRT subtitles.

All times in the API are in milliseconds.

Get your free API key at: https://youtubetranscript.dev

Requirements:
    pip install requests
"""

import requests
import sys

API_KEY = "your_api_key_here"  # Get yours at https://youtubetranscript.dev
BASE_URL = "https://www.youtubetranscript.dev/api/v2"


def transcribe(video: str, timestamp=True, paragraphs=False, words=False) -> dict:
    response = requests.post(
        f"{BASE_URL}/transcribe",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "video": video,
            # format is an object of on/off switches
            "format": {"timestamp": timestamp, "paragraphs": paragraphs, "words": words},
        },
    )
    response.raise_for_status()
    return response.json()


def srt_time(ms: int) -> str:
    """Milliseconds to SRT time (HH:MM:SS,mmm)."""
    hours, ms = divmod(ms, 3_600_000)
    mins, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{mins:02d}:{secs:02d},{ms:03d}"


def to_srt(segments: list) -> str:
    blocks = []
    for i, seg in enumerate(segments, start=1):
        blocks.append(f"{i}\n{srt_time(seg['start'])} --> {srt_time(seg['end'])}\n{seg['text']}\n")
    return "\n".join(blocks)


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"

    result = transcribe(video, timestamp=True, paragraphs=True)
    if result.get("status") != "completed":
        print(f"Status: {result.get('status')} {result.get('error', '')}")
        return

    data = result["data"]
    transcript = data["transcript"]
    video_id = data["video_id"]

    # 1. Plain text
    with open(f"{video_id}.txt", "w", encoding="utf-8") as f:
        f.write(transcript["text"])

    # 2. SRT subtitles from timed segments
    segments = transcript.get("segments") or []
    with open(f"{video_id}.srt", "w", encoding="utf-8") as f:
        f.write(to_srt(segments))

    # 3. Paragraphs (same {text, start, end} shape as segments)
    paragraphs = transcript.get("paragraphs") or []

    print(f"Title: {data.get('video_title')}")
    print(f"Saved {video_id}.txt and {video_id}.srt ({len(segments)} segments)")
    print(f"Paragraphs: {len(paragraphs)}")
    if paragraphs:
        print(f"First paragraph: {paragraphs[0]['text'][:200]}...")


if __name__ == "__main__":
    main()
