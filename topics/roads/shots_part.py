
# ---------------------------------------------------------------- road shots
MUDM = mat("mudm", "#6B4E32", noise=("#57402A", 5), rough=0.4)
GRAVEL = mat("gravel", "#9A948A", noise=("#7A746A", 14))
SANDL = mat("sandl", "#D8C29A", noise=("#C9B07F", 6))
MORTAR = mat("mortar", "#BDB5A6", noise=("#A79F90", 8))
PAVER = mat("paver", "#A8A296", noise=("#8E887C", 5))
TAR = mat("tar", "#24262A", rough=0.5)
ASPH = mat("asph", "#3B3D42", noise=("#33353A", 20))
WHITE_L = mat("white_l", "#F2F2F2", rough=0.5)
YEL = mat("yel", "#F2D04E", rough=0.5)
RAIN = mat("rain", "#BFE2FF", emit=0.8, alpha=0.6)
LEAF = mat("leaf", "#6E9B4A", noise=("#58823A", 4))


def rain(n=60, area=(-6, 6, -2, 8), top=7, seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        x, y = rnd.uniform(*area[:2]), rnd.uniform(*area[2:])
        d = cyl(0.012, 0.35, (x, y, top), RAIN, verts=4)
        ph = rnd.randint(0, 20)
        for f in range(1 + ph % 20, N + 1, 20):
            key(d, "location", f, (x, y, top))
            key(d, "location", min(N, f + 19), (x, y, 0.0))
        for fc in d.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def cart(loc, s=1.0):
    x, y, z = loc
    bpy.ops.object.empty_add(location=loc)
    r = bpy.context.object
    parts = [box((1.8 * s, 1.1 * s, 0.5 * s), (x, y, z + 0.7 * s), WOOD, bevel=0.03)]
    for sy in (-1, 1):
        w = cyl(0.45 * s, 0.1 * s, (x, y + sy * 0.62 * s, z + 0.45 * s), DARK_WOOD, rot=(math.radians(90), 0, 0), verts=12)
        parts.append(w)
    parts.append(beam((x + 0.9 * s, y, z + 0.6 * s), (x + 2.4 * s, y, z + 0.4 * s), 0.06 * s, WOOD))
    for p in parts:
        p.parent = r
        p.location = p.location - r.location
    return r


def shot_mud():
    night(0.5, top="#6E7A86", bottom="#8E98A2", sun=1.2)
    ground(m=MUDM)
    rnd = random.Random(3)
    for i in range(14):
        ball(rnd.uniform(0.3, 0.9), (rnd.uniform(-8, 8), rnd.uniform(-1, 10), -0.05), mat("puddle", "#5A6E80", rough=0.05), seg=12, squash=0.03)
    for x, y in ((-5, 8), (5, 7), (-7, 3), (7, 12)):
        cyl(0.15, 2.0, (x, y, 1.0), LOG, verts=8)
        ball(1.0, (x, y, 2.4), LEAF, seg=8)
    c = cart((0, 1.5, -0.25), 1.0)
    for f in range(1, N, 16):
        key(c, "rotation_euler", f, (math.radians(4 if (f // 16) % 2 else -3), 0, math.radians(-15)))
    for x in (2.6, 3.0):
        person(x, 1.5, -0.1, 1.0, mat("cloak", "#5A4A3A"))
    rain(90, seed=2)
    camera((3.0, -6.0, 2.0), (0.3, 1.5, 0.6), lens=30, moves=[(1.0, (1.8, -5.0, 1.6), (0.3, 1.5, 0.6))])


def shot_paved():
    ground(m=SANDL)
    M = mat("mudbrick", "#C9A97A", noise=("#B89466", 4))
    for i, x in enumerate((-4.5, 4.5)):
        for k in range(5):
            h = 2.2 + (k % 3) * 0.8
            box((2.6, 2.6, h), (x, k * 3.0, h / 2), M, bevel=0.05)
            box((0.5, 0.1, 0.9), (x - math.copysign(1.31, x), k * 3.0, 0.45), mat("door2", "#4A3322"))
    n = 0
    for j in range(16):
        for i in range(5):
            st = box((0.95, 0.95, 0.12), (-1.6 + i * 0.8 + (0.4 if j % 2 else 0), -1 + j * 0.9, 0.06), PAVER, bevel=0.04)
            pop_in(st, 4 + j * 6 + i, 5)
    person(0.5, 6, 0.12, 1.0, mat("robe", "#7A3E2E"))
    camera((0.5, -6.0, 2.6), (0, 4, 0.6), lens=30, moves=[(1.0, (0.0, -3.5, 2.2), (0, 6, 0.6))])


def side_grass(halfw, L, top=0.0, width=28):
    for sx in (-1, 1):
        box((width, L, 0.06), (sx * (halfw + width / 2), -1 + L / 2, top + 0.03), GRASS)
    box((400, 400, 0.02), (0, L - 1 + 200, top), GRASS)


def shot_roman():
    m1 = MARKS[1]
    side_grass(2.2, 60, 0.1)
    # cross-section of the road, open toward the camera at y = -1
    L = 60
    layers = [(SANDL, 0.35, -1.4), (GRAVEL, 0.45, -1.0), (MORTAR, 0.3, -0.6)]
    t = 4
    for m, h, z in layers:
        o = box((4.4, L, h), (0, -1 + L / 2, z + h / 2), m)
        key(o, "location", 1, (0, -1 + L / 2, z + h / 2 + 6))
        key(o, "location", t, (0, -1 + L / 2, z + h / 2 + 6))
        key(o, "location", t + 10, (0, -1 + L / 2, z + h / 2))
        t += 22
    box((60, L + 20, 2.0), (0, -1 + L / 2, -2.4), SOIL)
    for sx in (-1, 1):
        box((28, L, 1.6), (sx * (2.2 + 14), -1 + L / 2, -0.7), SOIL)
    # fitted stones with a camber (higher in the middle)
    for j in range(40):
        for i in range(6):
            x = -1.85 + i * 0.74 + (0.37 if j % 2 else 0)
            if abs(x) > 2.0:
                continue
            z = -0.3 + 0.18 * (1 - (x / 2.2) ** 2)
            st = box((0.7, 0.7, 0.22), (x, -0.65 + j * 0.72, z + 0.11), PAVER, bevel=0.05)
            pop_in(st, t + j * 2 + i, 4)
    for sx in (-1, 1):
        box((0.3, L, 0.5), (sx * 2.3, -1 + L / 2, -0.05), STONE)
    # rain running off the camber
    for i in range(16):
        d = ball(0.06, (0, -0.8, 0.2), RAIN, seg=6)
        sx = -1 if i % 2 else 1
        t0 = t + 50 + i * 6
        if t0 + 16 >= N:
            break
        pop_in(d, t0, 2)
        key(d, "location", t0, (0, -0.8, 0.0))
        key(d, "location", t0 + 14, (sx * 2.5, -0.8, -0.3))
        pop_out(d, t0 + 13, 3)
    km = text3d("80,000 KM", (0.6, 1.0, 1.4), size=0.42, m=mat("km_r", "#F2C14E", emit=1.2))
    pop_in(km, m1 + 6, 8)
    ms = cyl(0.3, 1.4, (3.0, 6, 0.7), STONE, verts=12)
    camera((1.5, -7.5, 0.9), (0, 0, -0.4), lens=32, moves=[(m1 / N, (1.0, -7.0, 1.2), (0, 0, -0.2)), (1.0, (2.5, -6.0, 4.0), (0, 10, 0))])


def shot_macadam():
    side_grass(2.2, 60, 0.0)
    L = 60
    box((60, L + 20, 2.0), (0, -1 + L / 2, -2.4), SOIL)
    for sx in (-1, 1):
        box((28, L, 1.4), (sx * (2.2 + 14), -1 + L / 2, -0.7), SOIL)
    box((4.4, L, 0.6), (0, -1 + L / 2, -1.1), SOIL)
    rnd = random.Random(2)
    # big stones, then small crushed stones on top
    for j in range(3):
        for i in range(8):
            ball(0.22, (-1.9 + i * 0.54 + rnd.uniform(-0.05, 0.05), -0.75 + j * 0.5, -0.6), GRAVEL, seg=6, squash=0.7)
    box((4.4, L, 0.35), (0, -1 + L / 2 + 0.25, -0.55), GRAVEL)
    top = box((4.4, L, 0.25), (0, -1 + L / 2, -0.2), mat("crushed", "#8E887E", noise=("#6E685E", 30)))
    for k in range(60):
        b = applied(box((0.12, 0.12, 0.1), (rnd.uniform(-2.1, 2.1), rnd.uniform(-0.9, 4), 0.0), mat("chip", "#A8A296")))
        key(b, "location", 1, (b.location.x, b.location.y, 3 + rnd.uniform(0, 2)))
        f = 4 + k
        key(b, "location", f, (b.location.x, b.location.y, 3 + rnd.uniform(0, 2)))
        key(b, "location", f + 12, (b.location.x, b.location.y, -0.05))
    roller = cyl(0.7, 2.0, (0, 0, 0.6), IRON, rot=(0, math.radians(90), 0), verts=24)
    key(roller, "location", int(N * 0.45), (0, 9, 0.6))
    key(roller, "location", N, (0, 1.2, 0.6))
    for sx in (-1, 1):
        beam((sx * 1.1, 0, 0.6), (sx * 0.4, -2.0, 1.4), 0.06, WOOD).parent = roller
    yr = text3d("1820s", (0, -1.5, 2.0), size=0.55, m=mat("yr_m", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    camera((1.8, -7.0, 1.6), (0, 1.0, 0), lens=32, moves=[(1.0, (1.0, -6.0, 1.8), (0, 2.0, 0))])


def shot_tarmac():
    side_grass(2.2, 60, 0.0)
    L = 60
    box((60, L + 20, 2.0), (0, -1 + L / 2, -2.4), SOIL)
    for sx in (-1, 1):
        box((28, L, 1.4), (sx * (2.2 + 14), -1 + L / 2, -0.7), SOIL)
    box((4.4, L, 0.9), (0, -1 + L / 2, -0.85), GRAVEL)
    # tar layer spreads toward the camera
    tar = applied(box((4.4, 1.0, 0.18), (0, 0, 0), TAR))
    key(tar, "scale", 1, (1, 1, 1))
    key(tar, "location", 1, (0, 20, -0.31))
    key(tar, "scale", N, (1, 42, 1))
    key(tar, "location", N, (0, 20, -0.31))
    for fc in tar.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    # the tar edge front: shrink so it reveals from far to near
    tar.scale = (1, 1, 1)
    key(tar, "scale", 1, (1, 1, 1))
    key(tar, "location", 1, (0, 42.5, -0.31))
    key(tar, "scale", N, (1, 44, 1))
    key(tar, "location", N, (0, -1 + 22, -0.31))
    # steam roller
    roller = cyl(0.6, 2.2, (0, 0, 0.5), IRON, rot=(0, math.radians(90), 0), verts=24)
    body = box((1.8, 2.4, 1.2), (0, 0, 0), mat("roller_body", "#2E5E3E"), bevel=0.05)
    body.parent = roller
    body.location = (0, -1.2, -0.3)
    stack = cyl(0.15, 1.2, (0, 0, 0), BLACK, verts=10)
    stack.parent = roller
    stack.location = (0, -1.2, -1.2)
    key(roller, "location", 1, (0, 40, 0.5))
    key(roller, "location", N, (0, 2.0, 0.5))
    for fc in roller.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    for i in range(12):
        s = ball(0.3, (0, 18, 2.0), mat("steam", "#E0E0E0", alpha=0.5), seg=10)
        t0 = 1 + i * 12
        if t0 + 20 >= N:
            break
        x0 = (0, 40 - 38 * t0 / N - 1.2, 2.3)
        pop_in(s, t0, 4)
        key(s, "location", t0, x0)
        key(s, "location", t0 + 20, (0.5, x0[1] + 1, 4.0))
        pop_out(s, t0 + 17, 3)
    yr = text3d("1902", (0.9, -1.5, 2.0), size=0.55, m=mat("yr_t", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    camera((3.0, -7.0, 2.6), (0, 8.0, 0.2), lens=30, moves=[(1.0, (1.5, -6.0, 1.8), (0, 3.0, 0.2))])


def shot_highway():
    m1 = MARKS[1]
    L = 200
    W = 9.0
    side_grass(W / 2, L, 0.0, 40)
    box((W, L, 0.3), (0, -1 + L / 2, -0.15), ASPH)
    box((W, L, 0.5), (0, -1 + L / 2, -0.55), mat("binder", "#55575C", noise=("#45474C", 20)))
    box((W, L, 0.5), (0, -1 + L / 2, -1.05), CONCRETE)
    box((W, L, 0.6), (0, -1 + L / 2, -1.6), GRAVEL)
    box((80, L + 20, 2.0), (0, -1 + L / 2, -2.9), SOIL)
    for sx in (-1, 1):
        box((40, L, 1.9), (sx * (W / 2 + 20), -1 + L / 2, -0.95), SOIL)
    box((0.12, L, 0.02), (0, -1 + L / 2, 0.01), YEL)
    for x in (-2.2, 2.2):
        for j in range(60):
            box((0.1, 1.2, 0.02), (x, j * 3.0, 0.01), WHITE_L)
    box((0.4, L, 0.5), (0, -1 + L / 2, 0.25), CONCRETE)
    rnd = random.Random(7)
    cols = ["#E8E8E8", "#3A6EA5", "#CC3333", "#F2C14E", "#2E8B57", "#555555", "#1C1D21"]
    for i in range(18):
        lane = rnd.choice([-3.3, -1.1, 1.1, 3.3])
        d = 1 if lane > 0 else -1
        c = applied(box((0.9, 1.9, 0.5), (0, 0, 0), mat(f"car{i%7}", cols[i % 7], rough=0.3, metal=0.3)))
        top = applied(box((0.8, 1.0, 0.35), (0, 0, 0), mat("carglass", "#2B3440", rough=0.2)))
        top.parent = c
        top.location = (0, -0.1, 0.4)
        y0 = rnd.uniform(-5, 60)
        span = 70
        key(c, "location", 1, (lane, y0 - d * span * 0, 0.3))
        key(c, "location", N, (lane, y0 + d * span, 0.3))
        for fc in c.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    # overpass
    box((40, 3.0, 0.5), (0, 40, 6.0), CONCRETE)
    for x in (-6, 6):
        box((1.0, 1.5, 6.0), (x, 40, 3.0), CONCRETE)
    camera((4.5, -9.0, 1.0), (0, 2, -0.6), lens=30, moves=[(m1 / N, (6.0, -8.0, 3.5), (0, 8, 0)), (1.0, (8.0, -10.0, 9.0), (0, 20, 0))])
