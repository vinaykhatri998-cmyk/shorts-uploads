"""Turns story.json into timeline.json: beat and word timings plus frames per shot.

Without voiceover, timings are estimated from reading speed.
With voiceover (vo/beat_XX.json from vo.py), the real word timestamps are used.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
WPS = 3.2            # estimated speaking speed, words per second
COMMA, STOP = 0.22, 0.38
TAIL = 0.35          # breath after each beat


def clean(w):
    return re.sub(r"^[^\w#]+|[^\w%]+$", "", w)


def estimate(text):
    words = text.split()
    total_chars = sum(len(clean(w)) + 2 for w in words)
    base = len(words) / WPS
    t, out = 0.0, []
    for w in words:
        d = base * (len(clean(w)) + 2) / total_chars
        out.append({"w": clean(w), "start": round(t, 3), "end": round(t + d, 3)})
        t += d
        if w.endswith(","):
            t += COMMA
        elif w.endswith((".", "?", "!")):
            t += STOP
    return out, t


def main():
    story = json.loads((HERE / "story.json").read_text(encoding="utf-8"))
    fps = story["fps"]
    t0, beats, shots = 0.0, [], []
    for i, b in enumerate(story["beats"]):
        vo = HERE / "vo" / f"beat_{i:02d}.json"
        if vo.exists():
            v = json.loads(vo.read_text())
            words, dur = v["words"], v["duration"]
        else:
            words, dur = estimate(b["text"])
        dur += TAIL
        f0, f1 = round(t0 * fps), round((t0 + dur) * fps)
        beats.append({**b, "i": i, "f0": f0, "f1": f1,
                      "words": [{"w": w["w"], "f0": f0 + round(w["start"] * fps), "f1": f0 + round(w["end"] * fps)} for w in words],
                      "audio": str(HERE / "vo" / f"beat_{i:02d}.mp3") if vo.exists() else None})
        if shots and shots[-1]["shot"] == b["shot"]:
            shots[-1]["f1"] = f1
            shots[-1]["marks"].append(f0 - shots[-1]["f0"])
        else:
            shots.append({"shot": b["shot"], "f0": f0, "f1": f1, "marks": [0]})
        t0 += dur
    for s in shots:
        s["frames"] = s["f1"] - s["f0"]
    tl = {"fps": fps, "frames": round(t0 * fps), "beats": beats, "shots": shots}
    (HERE / "timeline.json").write_text(json.dumps(tl, indent=1))
    print(f"{t0:.1f}s, {tl['frames']} frames")
    for s in shots:
        print(f"  {s['shot']:10s} {s['frames']/fps:5.1f}s marks={s['marks']}")


if __name__ == "__main__":
    main()
