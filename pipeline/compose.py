"""Joins the rendered shots, burns in one-word captions, adds voice (and optional music).

    python3 compose.py                 -> how_toilets_evolved.mp4
    python3 compose.py --music bg.mp3  -> also mixes background music at low volume

Needs: Pillow, ffmpeg. Reads timeline.json and frames/<shot>/NNNN.png.
"""
import argparse, json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1080, 1920
FONT = str(HERE / "LilitaOne.ttf")
CAPTION_Y = 0.60          # word centre, as a share of the height (matches your earlier Shorts)
SIZE = 150
MAX_W = 940
WHITE = (255, 255, 255, 255)
HIGHLIGHT = (92, 216, 255, 255)   # cyan, like "groundwater"
STROKE = 12
POP = [0.72, 0.95, 1.08, 1.03, 1.0]  # per-frame scale when a word appears


_cache = {}


def word_image(word, hl):
    k = (word, hl)
    if k not in _cache:
        size = SIZE
        while True:
            f = ImageFont.truetype(FONT, size)
            l, t, r, b = f.getbbox(word, stroke_width=STROKE)
            if r - l <= MAX_W or size < 60:
                break
            size -= 6
        im = Image.new("RGBA", (r - l + 20, b - t + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        # soft drop shadow, then the outlined word
        d.text((10 - l + 4, 10 - t + 7), word, font=f, fill=(0, 0, 0, 120), stroke_width=STROKE, stroke_fill=(0, 0, 0, 120))
        d.text((10 - l, 10 - t), word, font=f, fill=HIGHLIGHT if hl else WHITE, stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
        _cache[k] = im
    return _cache[k]


def norm(w):
    return re.sub(r"[^\w]", "", w).lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--music")
    ap.add_argument("--out", default=str(HERE / "how_toilets_evolved.mp4"))
    a = ap.parse_args()
    tl = json.loads((HERE / "timeline.json").read_text())
    fps, total = tl["fps"], tl["frames"]

    # frame -> (word, highlighted, frame index within the word)
    cap = {}
    for b in tl["beats"]:
        hl = {norm(h) for h in b["hl"]}
        ws = b["words"]
        for i, w in enumerate(ws):
            end = ws[i + 1]["f0"] if i + 1 < len(ws) else min(b["f1"], w["f1"] + 6)
            for f in range(w["f0"], end):
                cap[f] = (w["w"], norm(w["w"]) in hl, f - w["f0"])

    frames = []
    for s in tl["shots"]:
        d = HERE / "frames" / s["shot"]
        frames += [d / f"{i:04d}.png" for i in range(1, s["frames"] + 1)]

    silent = HERE / "_video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", str(silent)], stdin=subprocess.PIPE)
    last = None
    for n in range(total):
        p = frames[n] if n < len(frames) else frames[-1]
        if p.exists():
            last = p
        im = Image.open(last).convert("RGBA")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        if n in cap:
            word, hl, k = cap[n]
            wi = word_image(word, hl)
            sc = POP[k] if k < len(POP) else 1.0
            if sc != 1.0:
                wi = wi.resize((max(1, int(wi.width * sc)), max(1, int(wi.height * sc))), Image.LANCZOS)
            im.alpha_composite(wi, (W // 2 - wi.width // 2, int(H * CAPTION_Y) - wi.height // 2))
        enc.stdin.write(im.convert("RGB").tobytes())
    enc.stdin.close()
    enc.wait()

    # audio: each beat's voice line at its start time, plus optional music
    inputs, filters, labels = [], [], []
    for b in tl["beats"]:
        if b.get("audio") and Path(b["audio"]).exists():
            idx = len(inputs) // 2 + 1
            inputs += ["-i", b["audio"]]
            ms = round(b["f0"] / fps * 1000)
            filters.append(f"[{idx}:a]adelay={ms}|{ms}[v{idx}]")
            labels.append(f"[v{idx}]")
    if a.music:
        idx = len(inputs) // 2 + 1
        inputs += ["-stream_loop", "-1", "-i", a.music]
        filters.append(f"[{idx}:a]volume=0.12[m]")
        labels.append("[m]")
    if labels:
        fc = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest[a]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), *inputs, "-filter_complex", fc,
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-t", f"{total / fps:.3f}", a.out], check=True)
    else:
        silent.replace(a.out)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
