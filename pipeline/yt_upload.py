"""Uploads the next unposted Short from how-it-evolved/ready/QUEUE.md to YouTube (Data API v3).

Needs env YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (OAuth, scope youtube.upload).
Marks the entry posted in QUEUE.md; the workflow commits that change.
Note: until the Google Cloud project passes YouTube's API audit, YouTube locks API uploads to private.
"""
import datetime, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READY = ROOT / "how-it-evolved" / "ready"
QUEUE = READY / "QUEUE.md"


def token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", data) as r:
        return json.loads(r.read())["access_token"]


def upload(tok, mp4, meta):
    body = json.dumps({
        "snippet": {"title": meta["title"][:100], "description": meta["description"], "tags": meta["tags"],
                    "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": os.environ.get("YT_PRIVACY", "public"), "selfDeclaredMadeForKids": False},
    }).encode()
    size = mp4.stat().st_size
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status&notifySubscribers=true",
        data=body, method="POST", headers={
            "Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(req) as r:
        loc = r.headers["Location"]
    req = urllib.request.Request(loc, data=mp4.read_bytes(), method="PUT",
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def main():
    for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"):
        if not os.environ.get(k):
            print(f"::warning::{k} secret is not set; nothing uploaded")
            return 0
    lines = QUEUE.read_text(encoding="utf-8").splitlines()
    idx = next((i for i, l in enumerate(lines) if l.startswith("- [ ] ")), None)
    if idx is None:
        print("Queue is empty; nothing to upload")
        return 0
    slug = lines[idx][6:].split("|")[0].strip()
    meta = json.loads((READY / f"{slug}.json").read_text(encoding="utf-8"))
    res = upload(token(), READY / f"{slug}.mp4", meta)
    vid, priv = res["id"], res["status"]["privacyStatus"]
    day = datetime.date.today().isoformat()
    lines[idx] = lines[idx].replace("- [ ] ", "- [x] ", 1) + f" | {day} https://youtube.com/shorts/{vid} ({priv}, API)"
    QUEUE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Uploaded {slug}: https://youtube.com/shorts/{vid} ({priv})")
    with open(os.environ.get("GITHUB_STEP_SUMMARY", os.devnull), "a") as f:
        f.write(f"Uploaded **{meta['title']}**: https://youtube.com/shorts/{vid} ({priv})\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
