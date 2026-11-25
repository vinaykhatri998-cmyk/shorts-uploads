# ---------------------------------------------------------------- main
world_setup()
globals()["shot_" + SHOT]()
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action and o.name.startswith("tube") is False:
        pass

if STILL is not None:
    sc = bpy.context.scene
    sc.frame_set(STILL)
    sc.render.filepath = str(HERE / "stills" / f"{SHOT}_{STILL:04d}.png")
    bpy.ops.render.render(write_still=True)
else:
    if "--range" in ARGS:
        a, b = ARGS[ARGS.index("--range") + 1].split("-")
        bpy.context.scene.frame_start, bpy.context.scene.frame_end = int(a), int(b)
    bpy.ops.render.render(animation=True)
