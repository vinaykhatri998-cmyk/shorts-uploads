"""Makes the voiceover with ElevenLabs and saves word timings, one file per beat.

    export ELEVENLABS_API_KEY=...        (Windows: set ELEVENLABS_API_KEY=...)
    python3 vo.py
    python3 timeline.py                  # re-times every shot and caption to the real voice
    ./render.sh                          # re-render the 3D shots at the new lengths
    python3 compose.py --music bg.mp3    # final video with voice and captions

Writes vo/beat_XX.mp3 and vo/beat_XX.json ({"duration": s, "words": [{"w", "start", "end"}]}).
Existing beats are skipped, so delete a beat's files to redo just that line.
"""
import base64, json, os, re, subprocess, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "MxBoOtR6LujW2R8SMOm4")   # swap for the channel's voice
MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
SETTINGS = {"stability": 0.45, "similarity_boost": 0.75, "style": 0.3, "speed": 1.1}

# Say these differently from how they are written.
PRONOUNCE = {"5,000": "five thousand", "1596": "fifteen ninety-six", "1775": "seventeen seventy-five",
             "Harington": "Harrington"}


def spoken(text):
    for k, v in PRONOUNCE.items():
        text = text.replace(k, v)
    return text


def words_from_alignment(al, shown_text):
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    spoken_words, cur = [], None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                spoken_words.append(cur)
            cur = None
        else:
            cur = cur or {"start": s, "end": e}
            cur["end"] = e
    if cur:
        spoken_words.append(cur)
    shown = shown_text.split()
    # map shown words onto spoken words (pronunciation swaps can change word counts)
    out = []
    for i, w in enumerate(shown):
        j0 = round(i * len(spoken_words) / len(shown))
        j1 = max(j0, round((i + 1) * len(spoken_words) / len(shown)) - 1)
        out.append({"w": re.sub(r"^[^\w#]+|[^\w%]+$", "", w),
                    "start": spoken_words[j0]["start"], "end": spoken_words[j1]["end"]})
    return out


def main():
    key = os.environ["ELEVENLABS_API_KEY"]
    story = json.loads((HERE / "story.json").read_text(encoding="utf-8"))
    (HERE / "vo").mkdir(exist_ok=True)
    for i, b in enumerate(story["beats"]):
        mp3, js = HERE / "vo" / f"beat_{i:02d}.mp3", HERE / "vo" / f"beat_{i:02d}.json"
        if mp3.exists() and js.exists():
            continue
        body = json.dumps({"text": spoken(b["text"]), "model_id": MODEL, "voice_settings": SETTINGS}).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps",
            data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            res = json.loads(r.read())
        mp3.write_bytes(base64.b64decode(res["audio_base64"]))
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", str(mp3)]).decode())
        words = words_from_alignment(res["alignment"], b["text"])
        js.write_text(json.dumps({"duration": dur, "words": words}, indent=1))
        print(f"beat {i:02d}: {dur:.1f}s  {b['text']}")


if __name__ == "__main__":
    main()
