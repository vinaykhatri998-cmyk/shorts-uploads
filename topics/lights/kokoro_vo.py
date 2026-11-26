"""Free offline voiceover with Kokoro (no API key). Same output as vo.py.

    pip install kokoro-onnx soundfile
    (download kokoro-v1.0.onnx and voices-v1.0.bin from
     github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 into this folder)
    python3 kokoro_vo.py && python3 timeline.py && ./render.sh && python3 compose.py
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = Path(__file__).resolve().parent
VOICE, LANG, SPEED = "am_michael", "en-us", 1.12
PRONOUNCE = {"1800s": "eighteen hundreds", "1879": "eighteen seventy-nine", "LEDs": "L E Ds", "90 percent": "ninety percent", "20 years": "twenty years"}
sys.path.insert(0, str(HERE))
from timeline import estimate


def spoken(t):
    for k, v in PRONOUNCE.items():
        t = t.replace(k, v)
    return t


def main():
    k = Kokoro(str(HERE / "kokoro-v1.0.onnx"), str(HERE / "voices-v1.0.bin"))
    story = json.loads((HERE / "story.json").read_text(encoding="utf-8"))
    (HERE / "vo").mkdir(exist_ok=True)
    for i, b in enumerate(story["beats"]):
        a, sr = k.create(spoken(b["text"]), voice=VOICE, speed=SPEED, lang=LANG)
        # trim silence at both ends
        on = np.where(np.abs(a) > 0.01)[0]
        a = a[max(0, on[0] - int(0.03 * sr)): on[-1] + int(0.08 * sr)]
        wav = HERE / "vo" / f"beat_{i:02d}.wav"
        sf.write(wav, a, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5",
                        "-b:a", "192k", str(wav.with_suffix(".mp3"))], check=True)
        dur = len(a) / sr
        # word timings: reading-pace estimate stretched to the real line length
        words, est = estimate(b["text"])
        f = dur / est
        words = [{"w": w["w"], "start": w["start"] * f, "end": w["end"] * f} for w in words]
        wav.with_suffix(".json").write_text(json.dumps({"duration": dur, "words": words}, indent=1))
        print(f"{i:02d} {dur:4.1f}s {b['text']}")


if __name__ == "__main__":
    main()
