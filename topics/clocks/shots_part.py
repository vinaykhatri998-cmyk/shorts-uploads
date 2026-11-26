
# ---------------------------------------------------------------- clock shots
FACE = mat("face", "#F4EFE2", rough=0.5)
HAND = mat("hand", "#1C1D21", rough=0.4)
WATER_C = mat("water_c", "#4E9BD0", rough=0.1, alpha=0.8)
EARTH = mat("earth", "#3E7FB0", noise=("#5E9B4A", 2.5))
PANEL = mat("panel", "#22406E", rough=0.2, metal=0.6)
ATOM = mat("atom", "#5CD8FF", emit=4.0)


def applied(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def sun_obj():
    return next(o for o in bpy.data.objects if o.type == "LIGHT" and o.data.type == "SUN")


def spin(o, axis, turns, f0=1, f1=None, base=(0, 0, 0)):
    f1 = f1 or N
    r0 = list(base)
    r1 = list(base)
    r1[axis] += turns * math.tau
    key(o, "rotation_euler", f0, tuple(r0))
    key(o, "rotation_euler", f1, tuple(r1))
    for fc in o.animation_data.action.fcurves:
        if fc.data_path == "rotation_euler":
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def hand(length, width, loc, rot_axis_y=True, m=HAND):
    """A clock hand on a face lying in the x-z plane, pivot at loc; returns a pivot empty to rotate around y."""
    bpy.ops.object.empty_add(location=loc)
    piv = bpy.context.object
    h = applied(box((width, 0.03, length), (0, 0, 0), m))
    h.parent = piv
    h.location = (0, -0.02, length / 2 - 0.05)
    return piv


def clock_face(loc, R, hands=2, numerals=True):
    x, y, z = loc
    cyl(R, 0.08, loc, FACE, rot=(math.radians(90), 0, 0), verts=48)
    torus(R, 0.06, loc, BRASS, rot=(math.radians(90), 0, 0))
    for i in range(12):
        a = math.tau * i / 12
        box((0.04 * R, 0.02, 0.14 * R), (x + 0.82 * R * math.sin(a), y - 0.05, z + 0.82 * R * math.cos(a)), HAND,
            rot=(0, a, 0))
    ps = [hand(0.6 * R, 0.06 * R, (x, y - 0.06, z))]
    if hands > 1:
        ps.append(hand(0.85 * R, 0.04 * R, (x, y - 0.08, z)))
    return ps


def shot_sundial():
    m2 = MARKS[2]
    ground()
    scatter_rocks(14, (-6, 6), (2, 12), seed=4)
    for x, y, s in ((-6, 14, 3), (5, 18, 4)):
        prism(2 * s, 2 * s, 1.6 * s, (x, y, 0), SANDSTONE)
    cyl(1.6, 0.25, (0, 0.5, 0.125), STONE, verts=40)
    for i in range(13):
        a = math.pi * i / 12
        box((0.05, 0.25, 0.02), (1.35 * math.cos(a), 0.5 + 1.35 * math.sin(a) * -1 + 0.0, 0.26), HAND,
            rot=(0, 0, a + math.pi / 2))
    g = prism(1.3, 0.06, 0.9, (0, 0.5, 0.25), BRASS)
    g.rotation_euler = (0, 0, math.radians(60))
    g2 = box((0.06, 1.2, 0.06), (0, 0.5, 0.26), BRASS)
    sun = sun_obj()
    sun.data.energy = 4.0
    key(sun, "rotation_euler", 1, (math.radians(45), 0, math.radians(-60)))
    key(sun, "rotation_euler", N, (math.radians(45), 0, math.radians(60)))
    sunb = ball(1.2, (-30, 40, 25), mat("sunball", "#FFE7A0", emit=5.0), seg=16)
    key(sunb, "location", 1, (-30, 40, 22))
    key(sunb, "location", N, (30, 40, 22))
    camera((0, -6.5, 4.5), (0, 0.8, 0.3), lens=30, moves=[(m2 / N, (1.5, -5.0, 3.6), None), (1.0, (0.8, -3.5, 3.4), (0, 0.4, 0.2))])


def shot_water():
    night(0.15)
    box((400, 400, 0.02), (0, 0, -0.01), mat("floorw", "#3A3530"))
    ball(1.0, (-6, 30, 14), mat("moon", "#F4F1DE", emit=2.0), seg=24)
    box((4, 2, 0.15), (0, 0.6, 2.4), DARK_WOOD)
    for x in (-1.8, 1.8):
        box((0.15, 1.8, 2.4), (x, 0.6, 1.2), DARK_WOOD)
    top = cyl(0.55, 0.9, (0, 0.6, 2.95), mat("clayc", "#B5643A", noise=("#9A5230", 5)), r2=0.75, verts=24)
    cyl(0.05, 0.25, (0, 0.6, 2.35), BRASS, verts=8)
    cyl(0.75, 1.9, (0, 0.6, 0.95), GLASS, verts=32)
    lvl = cyl(0.72, 0.1, (0, 0.6, 0.05), WATER_C, verts=32)
    key(lvl, "scale", 1, (1, 1, 1))
    key(lvl, "location", 1, (0, 0.6, 0.1))
    key(lvl, "scale", N, (1, 1, 17))
    key(lvl, "location", N, (0, 0.6, 0.9))
    for k in range(7):
        box((0.3, 0.02, 0.03), (0, 0.6 - 0.76, 0.3 + k * 0.22), mat("mark", "#F2C14E", emit=1.0))
    for i in range(14):
        d = ball(0.05, (0, 0.6, 2.2), WATER_C, seg=8, squash=1.4)
        t0 = 4 + i * 11
        if t0 + 10 >= N:
            break
        pop_in(d, t0, 2)
        key(d, "location", t0, (0, 0.6, 2.2))
        key(d, "location", t0 + 10, (0, 0.6, 0.3 + 0.8 * t0 / N))
        pop_out(d, t0 + 9, 2)
    point_light((-1.5, -1.5, 3.0), 150, color=(1.0, 0.75, 0.45), flicker=True)
    camera((1.8, -5.5, 2.2), (0, 0.6, 1.5), lens=32, moves=[(1.0, (1.0, -4.6, 1.8), (0, 0.6, 1.3))])


def gear(r, loc, teeth, m, rot=(math.radians(90), 0, 0), th=0.15):
    g = cyl(r, th, loc, m, rot=rot, verts=max(16, teeth * 2))
    for i in range(teeth):
        a = math.tau * i / teeth
        t = applied(box((0.12, th, 0.14), (0, 0, 0), m))
        t.parent = g
        t.location = ((r + 0.05) * math.cos(a), (r + 0.05) * math.sin(a), 0)
        t.rotation_euler = (0, 0, a)
    return g


def shot_tower():
    ground(m=GRASS)
    H = 11
    box((4, 4, H), (0, 1.5, H / 2), SANDSTONE)
    prism(4.6, 4.6, 3, (0, 1.5, H), mat("roof_t", "#5E6E78"))
    # cut-out window into the works, front side
    box((3.0, 0.1, 3.4), (0, -0.48, 5.5), mat("works_bg", "#2E2722"))
    g1 = gear(0.9, (-0.5, -0.6, 5.3), 16, BRASS)
    g2 = gear(0.5, (0.85, -0.6, 5.85), 10, IRON)
    spin(g1, 1, 0.5, base=(math.radians(90), 0, 0))
    spin(g2, 1, -0.9, base=(math.radians(90), 0, 0))
    rope = cyl(0.02, 3.0, (1.2, -0.75, 4.9), ROPE if "ROPE" in globals() else BLACK, verts=6)
    wgt = cyl(0.25, 0.6, (1.2, -0.75, 3.6), IRON, verts=12)
    key(wgt, "location", 1, (1.2, -0.75, 4.6))
    key(wgt, "location", N, (1.2, -0.75, 3.9))
    ps = clock_face((0, -0.55, 8.6), 1.4, hands=1)
    spin(ps[0], 1, 0.25)
    for x, y in ((-6, 6), (6, 7), (-9, 12), (8, 14)):
        house((x, y), 1.4)
    camera((3.0, -10, 4.0), (0, 0, 7.0), lens=30, moves=[(1.0, (1.5, -8.0, 5.5), (0, 0, 6.6))])


def shot_pendulum():
    box((400, 400, 0.02), (0, 0, -0.01), mat("floorp", "#7A5A3C", noise=("#664A30", 6)))
    box((30, 0.3, 12), (0, 1.5, 6), mat("wallp", "#C9B99A"))
    box((1.4, 0.8, 4.0), (0, 0.6, 2.0), DARK_WOOD, bevel=0.04)
    box((1.1, 0.1, 2.3), (0, 0.18, 1.7), mat("pend_bg", "#3A2718"))
    box((1.6, 0.9, 0.2), (0, 0.6, 4.1), DARK_WOOD, bevel=0.03)
    ps = clock_face((0, 0.15, 3.4), 0.5)
    spin(ps[0], 1, 0.08)
    spin(ps[1], 1, 1.0)
    bpy.ops.object.empty_add(location=(0, 0.1, 2.8))
    piv = bpy.context.object
    rod = applied(box((0.04, 0.03, 1.8), (0, 0, 0), BRASS))
    rod.parent = piv
    rod.location = (0, 0, -0.9)
    bob = cyl(0.22, 0.05, (0, 0, 0), BRASS, rot=(math.radians(90), 0, 0), verts=32)
    bob.parent = piv
    bob.location = (0, -0.02, -1.8)
    per = 30
    for f in range(1, N + 1, per // 2):
        k = (f // (per // 2)) % 2
        key(piv, "rotation_euler", f, (0, math.radians(14 if k else -14), 0))
    yr = text3d("1656", (0, -0.4, 5.0), size=0.55, m=mat("yr_c", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    camera((1.5, -5.5, 2.6), (0, 0.4, 2.8), lens=32, moves=[(1.0, (0.8, -4.6, 2.4), (0, 0.4, 2.6))])


def shot_quartz():
    box((400, 400, 0.02), (0, 0, -0.01), mat("desk", "#2E3440"))
    box((30, 0.3, 12), (0, 2.5, 6), mat("wallq", "#3B4252"))
    wx, wz = -0.9, 1.6
    box((0.8, 0.1, 3.6), (wx, 0.65, wz), mat("strap", "#1C1D21"))
    cyl(0.75, 0.25, (wx, 0.5, wz), STEEL, rot=(math.radians(90), 0, 0), verts=48)
    cyl(0.66, 0.27, (wx, 0.49, wz), mat("dial", "#14161B", rough=0.3), rot=(math.radians(90), 0, 0), verts=48)
    for i in range(12):
        a = math.tau * i / 12
        box((0.04, 0.02, 0.12), (wx + 0.55 * math.sin(a), 0.34, wz + 0.55 * math.cos(a)), mat("tick", "#E8E8E8", emit=0.6), rot=(0, a, 0))
    hs = [hand(0.35, 0.05, (wx, 0.33, wz), m=mat("hw", "#E8E8E8", emit=0.6)), hand(0.5, 0.03, (wx, 0.32, wz), m=mat("hw", "#E8E8E8", emit=0.6))]
    sec = hand(0.55, 0.015, (wx, 0.31, wz), m=mat("hs", "#FF5A3D", emit=1.0))
    for f in range(1, N + 1, 30):
        key(sec, "rotation_euler", f, (0, math.tau * (f // 30) / 60, 0))
        key(sec, "rotation_euler", f + 3, (0, math.tau * (f // 30 + 1) / 60, 0))
    # the tuning-fork crystal
    QZ = mat("quartz", "#CFE8FF", rough=0.05, emit=0.8)
    fork = []
    for x in (-0.16, 0.16):
        fork.append(applied(box((0.12, 0.08, 1.1), (1.0 + x, 0.4, 1.9), QZ)))
    applied(box((0.44, 0.08, 0.3), (1.0, 0.4, 1.2), QZ))
    t0 = int(N * 0.35)
    for i, x in enumerate((-0.16, 0.16)):
        o = fork[i]
        for f in range(t0, N, 2):
            key(o, "location", f, (1.0 + x + (0.025 if (f // 2) % 2 else -0.025) * (1 if i else -1), 0.4, 1.9))
    glow_ramp(QZ, t0, t0 + 10, 4.0)
    hz = text3d("32,768 / SEC", (0.1, 0.2, 3.0), size=0.3, m=mat("hz_t", "#5CD8FF", emit=1.5))
    pop_in(hz, int(N * 0.5), 8)
    yr = text3d("1969", (0.1, 0.2, 3.0), size=0.45, m=mat("yr_q", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    key(yr, "scale", int(N * 0.45), (1, 1, 1))
    key(yr, "scale", int(N * 0.45) + 6, (0, 0, 0))
    point_light((0, -2, 3), 150, color=(1, 1, 1), flicker=False)
    camera((-0.6, -5.0, 2.0), (-0.3, 0.4, 1.9), lens=32, moves=[(0.4, (-0.4, -4.8, 2.0), None), (1.0, (0.6, -4.4, 2.1), (0.4, 0.4, 2.0))])


def shot_atomic():
    m1 = MARKS[1]
    night(0.05, top="#02040A", bottom="#070B18", sun=2.5)
    sun_obj().data.color = (1, 1, 1)
    e = ball(4.0, (0, 6, -2.5), EARTH, seg=48)
    spin(e, 2, 0.05)
    rnd = random.Random(2)
    for i in range(80):
        ball(0.04, (rnd.uniform(-30, 30), 40, rnd.uniform(-10, 30)), mat("star", "#FFFFFF", emit=3.0), seg=6)
    sats = []
    for k in range(3):
        bpy.ops.object.empty_add(location=(0, 6, -2.5))
        orb = bpy.context.object
        s = applied(box((0.4, 0.4, 0.5), (0, 0, 0), GOLD))
        s.parent = orb
        s.location = (5.4, 0, 0)
        for sx in (-1, 1):
            p = applied(box((0.9, 0.05, 0.4), (0, 0, 0), PANEL))
            p.parent = s
            p.location = (sx * 0.65, 0, 0)
        orb.rotation_euler = (math.radians(70 + k * 15), math.radians(k * 50), 0)
        spin(orb, 2, 0.35, base=(math.radians(70 + k * 15), math.radians(k * 50), math.radians(k * 120)))
        sats.append(s)
    # the atom: a glowing nucleus with three orbits
    bpy.ops.object.empty_add(location=(0, -0.5, 4.2))
    at = bpy.context.object
    nuc = ball(0.25, (0, 0, 0), ATOM, seg=16)
    nuc.parent = at
    for k in range(3):
        t = torus(0.75, 0.02, (0, 0, 0), ATOM, rot=(math.radians(90), math.radians(60 * k), 0))
        t.parent = at
    spin(at, 2, 1.2)
    sec = text3d("< 1 SECOND", (0, -0.5, 5.6), size=0.42, m=mat("sec_t", "#5CD8FF", emit=1.5))
    pop_in(sec, 12, 8)
    yrs = text3d("IN MILLIONS OF YEARS", (0, -0.5, 2.8), size=0.26, m=mat("sec_t2", "#FFFFFF", emit=1.2))
    pop_in(yrs, 30, 8)
    camera((0, -9, 4.0), (0, 0, 3.6), lens=30, moves=[(m1 / N, (0, -10, 3.0), (0, 2, 2.6)), (1.0, (0, -13, 2.6), (0, 3, 1.8))])
