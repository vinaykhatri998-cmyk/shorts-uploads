
# ---------------------------------------------------------------- tunnel shots
MTN = mat("mtn", "#8E8A80", noise=("#76726A", 3))
SNOW = mat("snow", "#F2F4F5", rough=0.6)
DARKT = mat("darkt", "#1E1B18")
LAMP = mat("lamp", "#FFC65A", emit=5.0)
BOOM = mat("boom", "#FF8A2E", emit=6.0, alpha=0.85)
DUST = mat("dust", "#B8A88E", alpha=0.6)
LINING = mat("lining", "#BDBAB3", noise=("#A8A59E", 6))
BRICKT = mat("brickt", "#A8563E", noise=("#8E4530", 8))
TBMY = mat("tbmy", "#E2B13B", rough=0.4, metal=0.5)
LEAF = mat("leaf", "#6E9B4A", noise=("#58823A", 4))


def mountain(x, y, r, h, snow=True, seed=0):
    m = cyl(r, h, (x, y, h / 2), MTN, r2=0.0, verts=9)
    m.rotation_euler = (0, 0, random.Random(seed).uniform(0, 1))
    if snow:
        s = cyl(r * 0.3, h * 0.3, (x, y, h * 0.85 + 0.02), SNOW, r2=0.0, verts=9)
        s.rotation_euler = m.rotation_euler
    return m


def rock_block(front=-1.0, W=24, H=10, D=20, top=None, m=MTN):
    """Rock cross-section, open toward the camera at y = front."""
    return box((W, D, H), (0, front + D / 2, (top if top is not None else 0) - H / 2), m)


def tunnel_cut(block, x0, x1, z, r, f0, f1, l0=0.01):
    """Tunnel shown in section: a dark band on the cut face that grows from x0 toward x1."""
    c = cyl(r, 1.0, (x0, -1.03, z), DARKT, rot=(0, math.radians(90), 0), verts=24)
    sgn = 1 if x1 > x0 else -1
    L = abs(x1 - x0)
    key(c, "scale", 1, (1, 0.02, l0))
    key(c, "location", 1, (x0 + sgn * l0 / 2, -1.03, z))
    key(c, "scale", f0, (1, 0.02, l0))
    key(c, "location", f0, (x0 + sgn * l0 / 2, -1.03, z))
    key(c, "scale", f1, (1, 0.02, L))
    key(c, "location", f1, ((x0 + x1) / 2, -1.03, z))
    return c


def shot_mountain():
    ground(m=GRASS)
    mountain(0, 8, 7, 9, seed=1)
    mountain(-9, 14, 6, 7, seed=2)
    mountain(9, 15, 6, 8, seed=3)
    # long winding path around
    pts = [(-12, -2, 0.03), (-7, 0, 0.03), (-6, 6, 0.03), (-4, 16, 0.03), (4, 18, 0.03), (7, 6, 0.03), (8, 0, 0.03), (12, -2, 0.03)]
    curve_tube(pts, 0.25, mat("pathm", "#C9B07F"))
    cartr = cyl(0.3, 0.6, (0, 0, 0.4), WOOD, verts=8)
    for i, p in enumerate(pts):
        key(cartr, "location", 1 + round(i * (N - 1) / (len(pts) - 1)), (p[0], p[1], 0.4))
    # dashed "shortcut" through the mountain
    for k in range(10):
        d = box((0.6, 0.15, 0.05), (-5 + k * 1.1, 0.0, 0.06), mat("dash", "#5CD8FF", emit=2.0))
        pop_in(d, MARKS[1] + k * 3, 4)
    for x in (-10, -7, 6, 10):
        cyl(0.12, 1.2, (x, -4, 0.6), LOG, verts=8)
        ball(0.7, (x, -4, 1.6), LEAF, seg=8)
    camera((0, -16, 7), (0, 6, 2), lens=28, moves=[(1.0, (2, -14, 9), (0, 6, 2))])


def shot_handdig():
    blk = rock_block(top=6.0, H=30, W=40)
    mountain(0, 8.5, 9, 16, snow=True, seed=4)
    box((40, 0.02, 0.4), (0, -1.01, 5.8), GRASS)
    for z, c in ((4.2, "#9A958A"), (2.6, "#857F74"), (-1.2, "#7A746A"), (-3.0, "#8E897E")):
        box((40, 0.02, 0.5), (0, -1.012, z), mat("strata" + c, c, noise=(c, 4)))
    ground(y0=-1.0, m=GRASS)
    # two crews dig toward each other and meet in the middle
    meet = int(N * 0.8)
    tunnel_cut(blk, -10, 0.15, 0.8, 0.8, 8, meet)
    tunnel_cut(blk, 10, -0.15, 0.8, 0.8, 8, meet)
    for sx in (-1, 1):
        p = person(0, -1.3, 0.0, 0.8, mat(f"crew{sx}", "#8C5A3C"))
        key(p, "location", 8, (sx * 9.4, -1.3, 0.05))
        key(p, "location", meet, (sx * 0.5, -1.3, 0.05))
        pk = beam((0, 0, 0.6), (sx * -0.35, 0, 0.95), 0.04, IRON)
        pk.parent = p
        for f in range(8, meet, 8):
            key(pk, "rotation_euler", f, (0, math.radians(25 if (f // 8) % 2 else -10), 0))
        lmp = ball(0.06, (0, 0, 0), LAMP, seg=8)
        lmp.parent = p
        lmp.location = (sx * -0.25, -0.1, 0.85)
        L = point_light((0, 0, 0), 15, flicker=True, seed=sx + 2)
        L.parent = p
        L.location = (sx * -0.3, -0.3, 0.9)
    star = ball(0.25, (0, -1.1, 0.8), mat("meet", "#FFD23F", emit=6.0), seg=12)
    key(star, "scale", 1, (0, 0, 0))
    key(star, "scale", meet, (0, 0, 0))
    key(star, "scale", meet + 4, (1.6, 1.6, 1.6))
    key(star, "scale", meet + 14, (0, 0, 0))
    t = text3d("1 KM BY HAND", (0, -1.2, 3.6), size=0.6, m=mat("kmh", "#F2C14E", emit=1.2))
    pop_in(t, int(N * 0.3), 8)
    camera((0, -16, 2.5), (0, 0, 1.6), lens=28, moves=[(1.0, (0, -12, 2.0), (0, 0, 1.2))])


def shot_blast():
    box((400, 400, 0.02), (0, 0, -0.01), mat("tfloor", "#5E5244"))
    face = box((10, 4, 8), (0, 3.0, 3.0), MTN)
    for sx in (-1, 1):
        box((4, 10, 8), (sx * 4.5, -2, 3.0), MTN)
    box((10, 10, 3), (0, -2, 5.5), MTN)
    holes = []
    for i in range(3):
        for j in range(3):
            h = cyl(0.06, 0.1, (-0.8 + i * 0.8, 0.98, 0.8 + j * 0.8), DARKT, rot=(math.radians(90), 0, 0), verts=8)
    bt = int(N * 0.4)
    for k in range(6):
        b = ball(0.6, (-0.8 + (k % 3) * 0.8, 0.8, 1.2 + (k // 3) * 0.8), BOOM, seg=12)
        key(b, "scale", 1, (0, 0, 0))
        key(b, "scale", bt + k, (0, 0, 0))
        key(b, "scale", bt + k + 6, (2.2, 2.2, 2.2))
        key(b, "scale", bt + k + 16, (0, 0, 0))
    rnd = random.Random(8)
    for k in range(30):
        c = box((0.25, 0.25, 0.2), (rnd.uniform(-1, 1), 0.8, rnd.uniform(0.6, 2.2)), MTN)
        pop_in(c, bt, 2)
        key(c, "location", bt, c.location.copy())
        key(c, "location", bt + 20, (c.location.x * 3 + rnd.uniform(-1, 1), -2.5 - rnd.uniform(0, 2), 0.12))
        key(c, "rotation_euler", bt, (0, 0, 0))
        key(c, "rotation_euler", bt + 20, (rnd.uniform(0, 6), rnd.uniform(0, 6), 0))
    for k in range(12):
        d = ball(0.5, (rnd.uniform(-1.5, 1.5), 0.0, rnd.uniform(0.5, 2.5)), DUST, seg=8)
        pop_in(d, bt + 6 + k, 8)
        key(d, "location", bt + 6 + k, d.location.copy())
        key(d, "location", N, d.location + Vector((rnd.uniform(-2, 2), -3, 1)))
    # the blasted opening appears after the dust
    hole = cyl(1.4, 0.05, (0, 0.97, 1.4), DARKT, rot=(math.radians(90), 0, 0), verts=16)
    key(hole, "scale", 1, (0, 0, 0))
    key(hole, "scale", bt + 8, (0, 0, 0))
    key(hole, "scale", bt + 14, (1, 1, 1))
    L = point_light((0, -1.5, 2.0), 0, flicker=False)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", bt, 0)
    key(L.data, "energy", bt + 4, 2500)
    key(L.data, "energy", bt + 18, 0)
    point_light((1.5, -3, 3), 200, color=(1, 0.85, 0.6), flicker=True)
    yr = text3d("1600s", (0, 0.5, 4.2), size=0.6, m=mat("yr_g", "#F2C14E", emit=1.2))
    pop_in(yr, 6, 8)
    camera((0.8, -6.0, 1.6), (0, 1, 1.8), lens=28, moves=[(1.0, (0.3, -5.2, 1.5), (0, 1, 1.8))])


def shot_shield():
    # river above, riverbed below, tunnel being dug under it (cross-section)
    blk = rock_block(top=-1.0, H=25, W=40, m=SOIL)
    box((30, 20, 1.0), (0, -1 + 10, -0.5), flowing("thames", "#4E7F9E", "#6E9BB8", speed=(1, 0, 0)))
    for sx in (-1, 1):
        box((10, 20, 1.6), (sx * 20, 9, -0.2), GRASS)
    # brick-lined tunnel behind the shield
    t_end = N
    tunnel_cut(blk, -15, 2.7, -5.0, 1.4, 1, int(N * 0.9), l0=0.8)
    for k in range(16):
        x = -14 + k * 1.0
        r = torus(1.35, 0.1, (x, -0.9, -5.0), BRICKT, rot=(0, math.radians(90), 0))
        pop_in(r, max(1, int((x + 15) / 17.5 * N * 0.9) - 4), 6)
    # the shield: an iron frame with cells, moving forward
    bpy.ops.object.empty_add(location=(-12, -0.9, -5.0))
    sh = bpy.context.object
    for i in range(3):
        for j in range(3):
            cel = applied(box((0.25, 0.1, 0.8), (0, 0, 0), IRON))
            cel.parent = sh
            cel.location = (0, 0, 0)
            cel.location = (0.2, -0.2, -0.85 + j * 0.85)
            wk = person(0, 0, 0, 0.45, mat("wk", "#6B3A3A"))
            wk.parent = sh
            wk.location = (-0.3, -0.4, -1.2 + j * 0.85)
    for j in range(4):
        b = applied(box((0.12, 0.12, 2.6), (0, 0, 0), IRON))
        b.parent = sh
        b.location = (0.3, -0.25, 0)
    key(sh, "location", 1, (-14.5, -0.9, -5.0))
    key(sh, "location", int(N * 0.9), (2.2, -0.9, -5.0))
    # a ship sails over the top
    bpy.ops.object.empty_add(location=(10, 6, 0))
    ship = bpy.context.object
    hb = applied(box((3, 1, 0.6), (0, 0, 0), DARK_WOOD))
    hb.parent = ship
    ms = cyl(0.06, 2.4, (0, 0, 0), WOOD, verts=6)
    ms.parent = ship
    ms.location = (0, 0, 1.4)
    sl = applied(box((0.05, 1.2, 1.4), (0, 0, 0), mat("sailt", "#F1E9D6")))
    sl.parent = ship
    sl.location = (0.1, 0, 1.6)
    key(ship, "location", 1, (10, 6, 0.1))
    key(ship, "location", N, (-8, 6, 0.1))
    yr = text3d("1825", (0, -1.2, 2.5), size=0.8, m=mat("yr_br", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    L = point_light((0, -2.5, -4.6), 400, flicker=True)
    camera((-2, -15, -1.0), (-2, 0, -3.0), lens=28, moves=[(1.0, (1, -13, -1.4), (0, 0, -3.0))])


def shot_tbm():
    m1 = MARKS[1]
    blk = rock_block(top=6.0, H=30, W=50)
    ground(y0=-1.0, m=GRASS)
    R = 2.0
    zc = -2.5
    tunnel_cut(blk, -20, 4.2, zc, R, 1, N, l0=14.4)
    # machine: cutter head + body, moving with the cut
    bpy.ops.object.empty_add(location=(-6, -1.0, zc))
    m = bpy.context.object
    head = cyl(R * 0.97, 0.4, (0, 0, 0), TBMY, rot=(0, math.radians(90), 0), verts=32)
    head.parent = m
    head.location = (0.2, 0, 0)
    for k in range(8):
        a = math.tau * k / 8
        arm = applied(box((0.2, 0.25, R * 1.8), (0, 0, 0), mat("armg", "#5E6269", metal=0.7)))
        arm.parent = head
        arm.location = (0, 0, -0.22)
        arm.rotation_euler = (0, 0, a)
    spin(head, 0, 6, base=(0, math.radians(90), 0))
    body = cyl(R * 0.9, 5.0, (0, 0, 0), mat("tbm_body", "#5E6269", rough=0.4, metal=0.6), rot=(0, math.radians(90), 0), verts=32)
    body.parent = m
    body.location = (-2.7, 0.0, 0)
    key(m, "location", 1, (-6, -1.0, zc))
    key(m, "location", N, (3.8, -1.0, zc))
    # concrete lining rings appear behind the machine
    for k in range(14):
        x = -19 + k * 1.2
        r = torus(R * 0.98, 0.12, (x, -1.0, zc), LINING, rot=(0, math.radians(90), 0))
        f = max(1, int((x + 6 + 5.5) / 9.8 * N))
        pop_in(r, min(N - 1, max(1, f)), 6)
    rnd = random.Random(3)
    for k in range(24):
        c = box((0.18, 0.18, 0.14), (0, 0, 0), MTN)
        t0 = 4 + k * 6
        if t0 + 14 >= N:
            break
        x0 = -6 + 9.8 * t0 / N + 0.4
        pop_in(c, t0, 2)
        key(c, "location", t0, (x0, -1.2, zc + rnd.uniform(-1, 1)))
        key(c, "location", t0 + 14, (x0 - 2.0, -1.2, zc - R + 0.2))
    L = point_light((0, -3, zc + 1), 500, color=(1, 0.9, 0.75), flicker=False)
    # five-story building for scale on the surface
    bld = box((3, 3, 2 * R), (8, 3, R), mat("bld5", "#9AA8B5"))
    for k in range(5):
        box((3.05, 3.05, 0.08), (8, 3, (k + 1) * 2 * R / 5), mat("floorline", "#E8E8E8"))
    pop_in(bld, m1, 10)
    camera((-1, -18, 0.5), (-1, 0, -1.5), lens=28, moves=[(m1 / N, (0, -17, 0.5), (0, 0, -1.2)), (1.0, (3, -19, 2.5), (3, 0, 0.5))])


def shot_gotthard():
    m1 = MARKS[1]
    blk = rock_block(top=0.0, H=40, W=120)
    ground(y0=-1.0, m=GRASS)
    for k, (x, r, h) in enumerate(((-24, 9, 11), (-10, 10, 14), (4, 11, 16), (18, 9, 12), (30, 8, 10))):
        mountain(x, 8, r, h, seed=k + 10)
    # a long, thin tunnel under all of it, glowing as it is revealed
    line = box((60, 0.05, 0.6), (0, -1.02, -1.8), mat("tunnel_line", "#2A2622"))
    lit = applied(box((1.0, 0.05, 0.6), (0, 0, 0), mat("tunnel_glow", "#FFC65A", emit=3.0)))
    key(lit, "location", 1, (-30, -1.04, -1.8))
    key(lit, "scale", 1, (0.01, 1, 1))
    key(lit, "location", int(N * 0.6), (0, -1.04, -1.8))
    key(lit, "scale", int(N * 0.6), (60, 1, 1))
    # the train inside
    tr = applied(box((3.0, 0.1, 0.4), (0, 0, 0), mat("train_w", "#E8E8E8", emit=0.5)))
    key(tr, "location", 1, (-32, -1.08, -1.8))
    key(tr, "location", N, (32, -1.08, -1.8))
    km = text3d("57 KM", (0, -1.4, 8.0), size=2.4, m=mat("km_g", "#5CD8FF", emit=1.5))
    pop_in(km, 12, 8)
    camera((0, -40, 4), (0, 0, 2), lens=28, moves=[(m1 / N, (0, -42, 5), (0, 0, 2.5)), (1.0, (0, -50, 8), (0, 0, 3))])
