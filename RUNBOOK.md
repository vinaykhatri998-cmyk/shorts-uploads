# Daily Short run (How It Evolved)

Each run makes ONE new Short and uploads it. Two runs a day.

1. `bash pipeline/setup.sh` (fresh container).
2. Pick the first topic under "Up next" in topics.md.
3. `cp -r pipeline work && cd work && ln -s /opt/kokoro/*.onnx /opt/kokoro/*.bin .`
4. Write `story.json`: 10 to 13 beats, 45 to 55 s total, hook first ("X years ago..."), then
   the problem, each fix with real names/years, and today; last beat "Follow to see how everything evolved."
   Facts must be correct; keep claims conservative. One "shot" per 1 or 2 beats.
5. In `scenes.py`, replace the toilet `shot_*` functions with new low-poly shots for this topic
   (reuse helpers: box, cyl, ball, torus, prism, section, ground, camera, flowing, pop_in, key).
   Shots must match the existing look: sand ground, cross-sections, soft sky, slow camera moves.
   Check every shot with `--still <frame> --preview` and look at the PNGs before the full render.
6. `/opt/shorts-venv/bin/python kokoro_vo.py && python3 timeline.py && ./render.sh && /opt/shorts-venv/bin/python compose.py --out ../out.mp4`
   (render.sh: run two copies in parallel on halves of the shot list to save time).
7. Watch-check: extract ~12 frames with ffmpeg and look at them; confirm audio is present and length < 60 s.
8. Commit the mp4 to `how-it-evolved/YYYY-MM-DD_<slug>.mp4` on the `videos` branch and push.
9. Upload with Zapier `youtube_upload_video`, connection 02e88359-9432-8b04-9cb1-2e44e11b10ff (How It Evolved ONLY),
   video = raw.githubusercontent.com URL of that file, category 27, public, made_for_kids false,
   title "How <X> Evolved <emoji> <hook> #shorts #engineering", description of 2 to 3 sentences plus hashtags.
   Before retrying any failed upload, check the channel's video count so nothing is posted twice.
10. Move the topic to "Posted" in topics.md, commit, push.
