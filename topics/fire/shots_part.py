
# ---------------------------------------------------------------- fire-starting shots
EMBER = mat("ember", "#FF5A1F", emit=0.0)
TINDER = mat("tinder", "#C9A85E", noise=("#A8893F", 10))
SPARKM = mat("sparkm", "#FFC65A", emit=10.0)
FLINT = mat("flint", "#5E5A55", rough=0.3)
MATCHW = mat("matchw", "#E8CF9A", noise=("#D4B97E", 8))
MHEAD = mat("mhead", "#B8322B", rough=0.5)
BLUEF = mat("bluef", "#4FA3FF", emit=8.0, alpha=0.8)
GLASSB = mat("glassb", "#121317", rough=0.08, spec=0.9)
RINGG = mat("ringg", "#FF4D2E", emit=0.0)


def show_flame(objs, f0, length=6, parent=None, offset=(0, 0, 0.02)):
    c = sum((o.location for o in objs), Vector()) / len(objs)
    c.z = min(o.location.z for o in objs)
    bpy.ops.object.empty_add(location=c)
    e = bpy.context.object
    for o in objs:
        o.parent = e
        o.location = o.location - c
    if parent is not None:
        e.parent = parent
        e.location = offset
    key(e, "scale", 1, (0, 0, 0))
    key(e, "scale", f0, (0, 0, 0))
    key(e, "scale", f0 + length, (1, 1, 1))
    return e


def smoke_puffs(loc, f0, f1, every=8, s=0.15, rise=1.6):
    for i in range(40):
        t0 = f0 + i * every
        if t0 + 24 >= f1:
            break
        b = ball(s, loc, SMOKE, seg=8)
        pop_in(b, t0, 4)
        key(b, "location", t0, loc)
        key(b, "location", t0 + 24, (loc[0] + 0.3, loc[1] + 0.2, loc[2] + rise))
        pop_out(b, t0 + 20, 4)


def shot_friction():
    m2 = MARKS[2]
    night(0.2)
    ground(m=mat("dirtn", "#5A4632", noise=("#4A3828", 4)))
    board = box((1.4, 0.4, 0.1), (0, 0.5, 0.05), LOG)
    stick = cyl(0.04, 1.2, (0, 0.5, 0.7), mat("stick", "#9B6B3D"), verts=8)
    spin(stick, 2, 30, 1, N)
    p1 = person(-0.15, 0.95, 0.0, 1.0, mat("hide", "#8C5A3C"))
    for side in (-1, 1):
        arm = beam((side * 0.25, 0.85, 0.8), (side * 0.06, 0.5, 1.0), 0.06, mat("skin", "#E0A982"))
        for f in range(1, N, 6):
            key(arm, "location", f, (side * 0.155 + (0.05 if (f // 6) % 2 else -0.05), 0.675, 0.9))
    tinder = ball(0.25, (0.45, 0.45, 0.12), TINDER, seg=10, squash=0.5)
    ember = ball(0.07, (0.02, 0.4, 0.12), EMBER, seg=10)
    glow_ramp(EMBER, m2 - 30, m2 + 10, 8.0)
    smoke_puffs((0.0, 0.45, 0.2), 30, N, every=10, s=0.08, rise=1.2)
    fl = flame((0.45, 0.45, 0.15), 1.0, seed=3)
    show_flame(fl, m2 + 60, 8)
    L = point_light((0.3, 0.2, 0.6), 0, flicker=False)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", m2 - 20, 8)
    key(L.data, "energy", m2 + 60, 15)
    key(L.data, "energy", m2 + 68, 120)
    camera((1.2, -2.6, 1.1), (0.1, 0.5, 0.45), lens=34, moves=[(1.0, (0.7, -1.9, 0.8), (0.2, 0.5, 0.3))])


def shot_flint():
    night(0.15)
    ground(m=mat("dirtn2", "#5A4632", noise=("#4A3828", 4)))
    fl = ball(0.18, (0.0, 0.5, 0.7), FLINT, seg=6, squash=0.8)
    st = torus(0.2, 0.04, (0.3, 0.5, 0.8), IRON, rot=(math.radians(90), 0, 0))
    for f in range(1, N, 20):
        key(st, "location", f, (0.35, 0.5, 0.95))
        key(st, "location", f + 6, (0.1, 0.5, 0.65))
        key(st, "location", f + 12, (0.35, 0.5, 0.95))
    rnd = random.Random(2)
    for k in range(int(N / 20)):
        for j in range(6):
            sp = ball(0.025, (0.15, 0.45, 0.72), SPARKM, seg=6)
            t0 = 1 + k * 20 + 6
            if t0 + 12 >= N:
                continue
            pop_in(sp, t0, 1)
            key(sp, "location", t0, (0.15, 0.45, 0.72))
            key(sp, "location", t0 + 12, (0.4 + rnd.uniform(-0.15, 0.15), 0.45 + rnd.uniform(-0.1, 0.1), 0.1))
            pop_out(sp, t0 + 10, 2)
    tinder = ball(0.3, (0.4, 0.45, 0.08), TINDER, seg=10, squash=0.45)
    fl2 = flame((0.4, 0.45, 0.1), 1.1, seed=5)
    show_flame(fl2, int(N * 0.35), 8)
    L = point_light((0.3, 0.1, 0.7), 0, flicker=False)
    key(L.data, "energy", 1, 5)
    key(L.data, "energy", int(N * 0.35), 5)
    key(L.data, "energy", int(N * 0.35) + 8, 120)
    # the Iceman's kit: pouch and fungus beside
    box((0.4, 0.25, 0.3), (-0.6, 0.6, 0.15), mat("pouch", "#6B4426"), bevel=0.05)
    ball(0.12, (-0.3, 0.3, 0.06), mat("fungus", "#8C6239"), seg=8, squash=0.5)
    yr = text3d("5,300 YEARS AGO", (0.0, 0.3, 1.5), size=0.12, m=mat("yr_f", "#F2C14E", emit=1.5))
    pop_in(yr, int(N * 0.5), 8)
    camera((0.8, -2.0, 1.1), (0.1, 0.5, 0.65), lens=34, moves=[(1.0, (0.4, -1.8, 1.0), (0.1, 0.5, 0.6))])


def match_stick(loc, rot_y=0.0):
    bpy.ops.object.empty_add(location=loc)
    r = bpy.context.object
    s = applied(box((0.9, 0.06, 0.06), (0, 0, 0), MATCHW))
    s.parent = r
    h = ball(0.06, (0, 0, 0), MHEAD, seg=10)
    h.parent = r
    h.location = (0.47, 0, 0)
    h.scale = (1.4, 1, 1)
    r.rotation_euler = (0, rot_y, 0)
    return r, h


def shot_match():
    m1 = MARKS[1]
    box((400, 400, 0.02), (0, 0, -0.01), mat("table", "#6B4426", noise=("#563519", 6)))
    box((40, 0.3, 14), (0, 3, 7), mat("wallm", "#3B3A40"))
    # 1826: a match scraped on sandpaper
    box((1.0, 0.5, 0.02), (-0.4, 0.5, 0.01), mat("sandp", "#B8A27A", noise=("#9A845C", 30)))
    r, h = match_stick((-0.8, 0.5, 0.12))
    key(r, "location", 1, (-1.0, 0.5, 0.12))
    key(r, "location", 30, (-1.0, 0.5, 0.12))
    key(r, "location", 40, (-0.2, 0.5, 0.12))
    key(r, "location", 48, (0.0, 0.5, 0.6))
    key(r, "rotation_euler", 40, (0, 0, 0))
    key(r, "rotation_euler", 48, (0, math.radians(-40), 0))
    fo, fc = flame((0, 0, 0), 0.9, seed=1)
    show_flame([fo, fc], 40, 4, parent=h)
    yr = text3d("1826", (0, 0.5, 1.6), size=0.4, m=mat("yr_m", "#F2C14E", emit=1.2))
    pop_in(yr, 10, 8)
    key(yr, "scale", m1 - 6, (1, 1, 1))
    key(yr, "scale", m1, (0, 0, 0))
    L = point_light((0.0, 0.2, 1.0), 0, flicker=False)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", 40, 0)
    key(L.data, "energy", 44, 40)
    # move the first match away for the safety box
    key(r, "location", m1 - 6, (0.0, 0.5, 0.6))
    key(r, "location", m1, (-3.0, 0.5, 0.6))
    # safety matchbox with red striking strip
    bx = box((0.9, 0.55, 0.22), (0.4, 0.3, 0.11), mat("mbox", "#2E6EB5"), bevel=0.02)
    strip = box((0.86, 0.02, 0.16), (0.4, 0.02, 0.11), mat("strip", "#7A2E22", noise=("#5A1E18", 30)))
    for p in (bx, strip):
        pop_in(p, m1, 8)
    r2, h2 = match_stick((0.0, -0.05, 0.11))
    r2.rotation_euler = (0, 0, math.radians(0))
    pop_in(r2, m1 + 4, 6)
    key(r2, "location", m1 + 4, (-0.6, -0.05, 0.11))
    key(r2, "location", m1 + 24, (-0.6, -0.05, 0.11))
    key(r2, "location", m1 + 32, (0.3, -0.05, 0.11))
    key(r2, "location", m1 + 42, (0.3, -0.2, 0.6))
    f2o, f2c = flame((0, 0, 0), 0.9, seed=2)
    show_flame([f2o, f2c], m1 + 32, 4, parent=h2)
    key(L.data, "energy", m1 + 32, 40)
    camera((0.3, -3.0, 1.3), (-0.1, 0.4, 0.5), lens=34, moves=[(1.0, (0.4, -2.6, 1.2), (0.1, 0.3, 0.45))])


def shot_lighter():
    box((400, 400, 0.02), (0, 0, -0.01), mat("table2", "#2E3440"))
    box((40, 0.3, 14), (0, 3, 7), mat("walll", "#3B4252"))
    body = box((0.5, 0.25, 1.2), (0, 0.5, 0.6), mat("lighter_b", "#C0392B", rough=0.25, metal=0.3), bevel=0.04)
    box((0.5, 0.27, 0.15), (0, 0.5, 1.28), CHROME)
    wheel = cyl(0.09, 0.12, (0.12, 0.5, 1.45), mat("wheel", "#5E6269", rough=0.4, metal=0.8), rot=(math.radians(90), 0, 0), verts=16)
    spin(wheel, 1, -1, 20, 30, base=(math.radians(90), 0, 0))
    sp = ball(0.05, (0.0, 0.45, 1.45), SPARKM, seg=6)
    key(sp, "scale", 1, (0, 0, 0))
    key(sp, "scale", 26, (0, 0, 0))
    key(sp, "scale", 28, (1.5, 1.5, 1.5))
    key(sp, "scale", 32, (0, 0, 0))
    fl = flame((-0.05, 0.5, 1.38), 0.75, seed=4)
    show_flame(fl, 28, 5)
    L = point_light((0, 0.0, 1.8), 0, flicker=False)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", 28, 0)
    key(L.data, "energy", 33, 60)
    point_light((-2, -2, 3), 40, color=(0.8, 0.85, 1.0), flicker=False)
    camera((0.8, -2.6, 1.6), (0, 0.5, 1.2), lens=34, moves=[(1.0, (0.4, -2.2, 1.6), (0, 0.5, 1.3))])


def shot_stove():
    m1 = MARKS[1]
    box((400, 400, 0.02), (0, 0, -0.01), mat("kfloor", "#C9C2B4"))
    box((40, 0.3, 14), (0, 2.5, 7), mat("kwall", "#E8E6E1"))
    box((6, 1.6, 0.9), (0, 1.5, 0.45), mat("cab", "#F2F2F2"), bevel=0.03)
    box((6, 1.7, 0.06), (0, 1.5, 0.93), mat("counter", "#3A3A44"))
    # gas burner, left
    gx = -1.3
    torus(0.32, 0.05, (gx, 1.3, 1.0), IRON)
    for k in range(4):
        a = k * math.pi / 2
        beam((gx + 0.5 * math.cos(a), 1.3 + 0.5 * math.sin(a), 1.08), (gx + 0.15 * math.cos(a), 1.3 + 0.15 * math.sin(a), 1.08), 0.04, IRON)
    fls = []
    for k in range(16):
        a = math.tau * k / 16
        f = cyl(0.04, 0.16, (gx + 0.32 * math.cos(a), 1.3 + 0.32 * math.sin(a), 1.1), BLUEF, r2=0.0, verts=8)
        fls.append(f)
    show_flame(fls, 20, 3)
    clk = ball(0.06, (gx + 0.32, 1.0, 1.05), SPARKM, seg=6)
    key(clk, "scale", 1, (0, 0, 0))
    key(clk, "scale", 16, (0, 0, 0))
    key(clk, "scale", 18, (1.5, 1.5, 1.5))
    key(clk, "scale", 21, (0, 0, 0))
    # induction hob, right
    ix = 1.3
    box((1.6, 1.4, 0.04), (ix, 1.4, 0.97), GLASSB)
    ring = torus(0.35, 0.015, (ix, 1.3, 0.995), RINGG)
    glow_ramp(RINGG, m1 - 70, m1 - 60, 2.0)
    pan = cyl(0.36, 0.18, (ix, 1.3, 1.1), mat("pan", "#2B2D33", rough=0.3, metal=0.7), verts=32)
    beam((ix + 0.35, 1.3, 1.15), (ix + 1.0, 1.0, 1.2), 0.05, BLACK)
    water = cyl(0.33, 0.02, (ix, 1.3, 1.17), mat("water_p", "#5CA8D8", rough=0.1), verts=32)
    smoke_puffs((ix, 1.3, 1.25), m1 - 50, N, every=8, s=0.08, rise=1.0)
    nf = text3d("NO FLAME", (0.7, 0.5, 2.0), size=0.22, m=mat("nf", "#5CD8FF", emit=1.5))
    pop_in(nf, m1 - 40, 8)
    camera((-1.0, -2.5, 2.4), (gx, 1.3, 1.0), lens=32, moves=[(0.25, (-0.8, -2.4, 2.3), (gx, 1.3, 1.0)), (0.45, (0.8, -2.5, 2.4), (ix, 1.3, 1.1)), (1.0, (0.2, -3.6, 2.6), (0, 1.3, 1.1))])
