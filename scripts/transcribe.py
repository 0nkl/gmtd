#!/usr/bin/env python3
"""transcribe.py — voice memo transcription for GMTD captures.

Stdlib-only. Uses the OpenAI Whisper API (OPENAI_API_KEY env var, or --key).
Input: an audio file path, or base64 data via --b64 (as returned by chat platforms).

Usage:
  transcribe.py <audio-file> [--mime audio/mp4] [--key sk-...]
  transcribe.py --b64 <base64-string> --mime audio/ogg

Prints the transcript to stdout. Exit 2 = no API key; exit 3 = API error.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import uuid

API_URL = "https://api.openai.com/v1/audio/transcriptions"

EXT = {"audio/mp4": "m4a", "audio/mpeg": "mp3", "audio/ogg": "ogg",
       "audio/wav": "wav", "audio/webm": "webm", "audio/x-m4a": "m4a"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="Audio file path")
    ap.add_argument("--b64", help="Base64-encoded audio data instead of a file")
    ap.add_argument("--mime", default="audio/mp4")
    ap.add_argument("--key", default=None)
    args = ap.parse_args()

    key = args.key or os.environ.get("OPENAI_API_KEY")
    if not key:
        print("ERROR: no API key (set OPENAI_API_KEY or pass --key)", file=sys.stderr)
        sys.exit(2)

    if args.b64:
        data = base64.b64decode(args.b64)
        filename = f"memo.{EXT.get(args.mime, 'm4a')}"
    elif args.file:
        with open(args.file, "rb") as f:
            data = f.read()
        filename = os.path.basename(args.file)
    else:
        print("ERROR: provide a file path or --b64", file=sys.stderr)
        sys.exit(1)

    boundary = uuid.uuid4().hex
    body = b""
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n"
             "whisper-1\r\n").encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{filename}\"\r\nContent-Type: {args.mime}\r\n\r\n").encode()
    body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        API_URL, data=body, method="POST",
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            out = json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001 — report any API failure cleanly
        print(f"ERROR: transcription failed: {e}", file=sys.stderr)
        sys.exit(3)

    print(out.get("text", "").strip())


if __name__ == "__main__":
    main()
