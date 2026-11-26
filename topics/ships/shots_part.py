
# ---------------------------------------------------------------- ship shots
SAILC = mat("sailc", "#F1E9D6", rough=0.8)
REED = mat("reedb", "#C9A85E", noise=("#A8893F", 8))
HULL_B = mat("hull_b", "#6B4426", noise=("#563519", 6))
SMOKE = mat("smoke", "#6E6E6E", alpha=0.5)
RED_H = mat("red_h", "#A8322B", rough=0.5)
NAVY = mat("navy", "#24364F", rough=0.5)
CCOLS = ["#C0392B", "#2E86C1", "#27AE60", "#F39C12", "#7D3C98", "#D35400", "#1F618D", "#E5E7E9"]


def sea(color="#2F6E9E", color2="#4F92C4"):
    return box((600, 600, 0.1), (0, 0, -0.05), flowing("sea", color, color2, scale=2.5, speed=(0.6, 0.8, 0)))


def hull(L, W, H, loc, m):
    """Ellipsoid hull; the lower half hides under the water."""
    o = ball(1.0, loc, m, seg=24)
    o.scale = (L / 2, W / 2, H)
    return applied(o)


def bob(o, amp=0.04, rot=3.0, period=48, seed=0):
    base = o.location.copy()
    ph = random.Random(seed).uniform(0, 6.28)
    for f in range(1, N + 1, period // 4):
        s = math.sin(ph + f / period * math.tau)
        c = math.cos(ph + f / period * math.tau)
        key(o, "location", f, (base.x, base.y, base.z + amp * s))
        key(o, "rotation_euler", f, (math.radians(rot * c), math.radians(rot * 0.5 * s), o.rotation_euler.z))


def root(loc):
    bpy.ops.object.empty_add(location=loc)
    return bpy.context.object


def attach(r, objs):
    for o in objs:
        o.parent = r
        o.location = o.location - r.location


def shot_sea():
    sea()
    box((60, 20, 0.6), (0, -14, 0.2), SAND)
    for i in range(10):
        r = random.Random(i)
        ball(r.uniform(0.6, 1.4), (r.uniform(-12, 12), -6 - r.uniform(0, 4), 0.1), ROCK, seg=8, squash=0.5)
    person(2.0, -4.8, 0.45, 1.0, mat("hide", "#8C5A3C"))
    ball(0.9, (8, 60, 2.4), mat("isle", "#6E8B4A"), seg=12, squash=0.5)
    prism(6, 3, 2.4, (8, 60, 0), mat("isle2", "#6E8B4A"))
    camera((1.5, -9.5, 2.0), (0.5, 10, 1.2), lens=30, moves=[(1.0, (0.8, -8.0, 1.6), (0.5, 20, 1.6))])


def shot_canoe():
    sea("#3E7FA8", "#5E9CC4")
    box((60, 20, 0.6), (0, 16, 0.2), GRASS)
    for x in (-6, -2, 3, 7):
        cyl(0.15, 2.0, (x, 12, 1.4), LOG, verts=8)
        ball(0.9, (x, 12, 2.8), mat("leaf", "#6E9B4A"), seg=8)
    r = root((0, 1.5, 0))
    h = hull(3.6, 0.7, 0.45, (0, 1.5, 0.05), HULL_B)
    inner = ball(1.0, (0, 1.5, 0.28), mat("hollow", "#3E2716"), seg=16)
    inner.scale = (1.55, 0.25, 0.12)
    p = person(0.5, 1.5, 0.15, 0.9, mat("hide2", "#8C5A3C"))
    paddle = beam((0.9, 1.0, 0.1), (0.5, 1.2, 1.1), 0.05, WOOD)
    attach(r, [h, inner, p, paddle])
    key(r, "location", 1, (-2.0, 1.5, 0))
    key(r, "location", N, (2.0, 1.5, 0))
    for f in range(1, N, 20):
        key(paddle, "rotation_euler", f, (math.radians(-20 if (f // 20) % 2 else 15), 0, 0))
    yrs = text3d("10,000 YEARS", (1.0, 0, 2.8), size=0.36, m=mat("yrs_t", "#F2C14E", emit=1.2))
    pop_in(yrs, int(N * 0.55), 8)
    camera((2.5, -5.5, 1.8), (0, 1.5, 0.8), lens=30, moves=[(1.0, (1.0, -4.8, 1.8), (1.0, 1.5, 1.0))])


def shot_sail():
    sea("#3E7FA8", "#5E9CC4")
    box((80, 30, 0.6), (0, 30, 0.2), SAND)
    for x in (-14, 12):
        prism(8, 6, 6, (x, 28, 0.5), SANDSTONE)
    r = root((0, 2, 0))
    h = hull(5.0, 1.3, 0.6, (0, 2, 0.05), REED)
    for k in range(5):
        torus(0.5, 0.05, (-2 + k, 2, 0.3), mat("tie", "#8A6A30"), rot=(0, math.radians(90), 0))
    mast = cyl(0.06, 3.6, (0, 2, 1.9), WOOD, verts=8)
    sail = box((2.4, 0.05, 2.2), (0.05, 2.05, 2.3), SAILC)
    yard = cyl(0.05, 2.8, (0, 2, 3.45), WOOD, rot=(0, math.radians(90), 0), verts=8)
    ppl = [person(x, 2, 0.35, 0.7, mat("lin", "#E9E1CF")) for x in (-1.5, 1.5)]
    attach(r, [h, mast, sail, yard] + ppl)
    key(r, "location", 1, (-2.5, 2, 0))
    key(r, "location", N, (2.0, 2, 0))
    key(sail, "scale", 1, (2.4, 0.05, 2.2))
    for f in range(1, N, 16):
        key(sail, "scale", f, (2.4, 0.05 + (0.25 if (f // 16) % 2 else 0.12), 2.2))
    stream([(-8, -1, 2.5), (8, 1, 2.5)], 20, mat("wind", "#FFFFFF", emit=1.5, alpha=0.6), t0=1, every=5, travel=24, r=0.06)
    camera((2.0, -8.0, 2.4), (0, 2, 1.8), lens=30, moves=[(1.0, (0.5, -7.0, 2.2), (0.5, 2, 1.8))])


def shot_galleon():
    sea("#2F6E9E", "#4F92C4")
    r = root((0, 3, 0))
    parts = [hull(9.0, 2.4, 1.6, (0, 3, 0.0), HULL_B)]
    parts.append(box((2.2, 2.0, 1.6), (-3.4, 3, 1.4), HULL_B, bevel=0.05))
    parts.append(box((1.4, 1.6, 0.9), (3.6, 3, 1.0), HULL_B, bevel=0.05))
    parts.append(box((8, 1.9, 0.12), (0, 3, 1.05), mat("deck", "#8C6239")))
    for x, h in ((-1.8, 6.5), (0.6, 7.5), (2.9, 5.5)):
        parts.append(cyl(0.1, h, (x, 3, 1 + h / 2), WOOD, verts=8))
        for k, (w, z) in enumerate(((2.6, 1 + h * 0.45), (2.0, 1 + h * 0.75))):
            parts.append(box((0.06, w, h * 0.26), (x + 0.15, 3, z), SAILC))
            parts.append(cyl(0.04, w + 0.3, (x + 0.1, 3, z + h * 0.13), WOOD, rot=(math.radians(90), 0, 0), verts=6))
    for k in range(5):
        parts.append(box((0.3, 0.05, 0.22), (-2.4 + k * 1.1, 1.85, 0.75), mat("port", "#2A1A10")))
    parts.append(box((0.04, 0.8, 0.5), (0.6, 3, 8.8), mat("flag", "#C0392B")))
    attach(r, parts)
    r.rotation_euler = (0, 0, math.radians(-25))
    bob(r, 0.08, 2.5, 60)
    camera((7, -11, 3.0), (0, 3, 3.5), lens=30, moves=[(1.0, (2, -12, 2.4), (0, 3, 3.6))])


def shot_steam():
    m1 = MARKS[1]
    sea("#3E6F8C", "#5C8DA8")
    box((80, 30, 0.6), (0, 26, 0.2), GRASS)
    for x in (-10, -4, 5, 11):
        house((x, 22), 1.6)
    r = root((0, 2, 0))
    parts = [hull(7.0, 1.6, 0.7, (0, 2, 0.0), mat("steamhull", "#2B2B30")),
             box((6.2, 1.4, 0.1), (0, 2, 0.55), mat("deck2", "#8C6239")),
             box((2.0, 1.0, 0.8), (0.6, 2, 1.0), mat("cabin2", "#E9E1CF"), bevel=0.04),
             cyl(0.22, 2.6, (0.4, 2, 2.2), BLACK, verts=12)]
    wheel = cyl(1.0, 0.3, (0.6, 1.1, 0.6), RED_H, rot=(math.radians(90), 0, 0), verts=20)
    for k in range(6):
        sp = applied(box((1.9, 0.3, 0.36), (0, 0, 0), WOOD))
        sp.parent = wheel
        sp.rotation_euler = (0, 0, math.radians(30 * k))
    attach(r, parts + [wheel])
    spin(wheel, 2, -3, base=(math.radians(90), 0, 0))
    for i in range(16):
        s = ball(0.35, (0.4, 2, 3.6), SMOKE, seg=10)
        t0 = 1 + i * 9
        if t0 + 30 >= N:
            break
        pop_in(s, t0, 4)
        key(s, "location", t0, (0.4, 2, 3.6))
        key(s, "location", t0 + 30, (-2.5, 2.5, 6.0))
        pop_out(s, t0 + 26, 4)
    key(r, "location", 1, (-2, 2, 0))
    key(r, "location", m1, (3, 2, 0))
    yr = text3d("1807", (0, 0, 5.0), size=0.8, m=mat("yr_s", "#F2C14E", emit=1.2))
    pop_in(yr, 6, 8)
    key(yr, "scale", m1 - 8, (1, 1, 1))
    key(yr, "scale", m1, (0, 0, 0))
    # a steel liner sails in for the second line
    lr = root((-30, 6, 0))
    lp = [hull(20, 3.2, 1.8, (-30, 6, 0), mat("liner", "#1C1D21")),
          box((14, 2.6, 1.4), (-30, 6, 2.0), mat("liner_w", "#F2F2F2"), bevel=0.05)]
    for k in range(3):
        lp.append(cyl(0.6, 2.6, (-33 + k * 3, 6, 3.8), RED_H, verts=16))
    attach(lr, lp)
    key(lr, "location", m1, (-34, 7, 0))
    key(lr, "location", N, (-2, 7, 0))
    camera((3, -9, 2.6), (0.5, 2, 1.6), lens=30, moves=[(m1 / N, (2, -9, 2.6), (1.5, 2, 1.6)), (1.0, (6, -16, 4), (-2, 5, 2.4))])


def container_ship(loc, L=24, rows=10, cols=4, tiers=4, seed=1):
    x0, y0, z0 = loc
    r = root(loc)
    parts = [box((L, 4.4, 1.6), (x0, y0, z0 + 0.2), NAVY, bevel=0.1),
             box((L, 4.45, 0.6), (x0, y0, z0 - 0.3), RED_H)]
    parts.append(box((2.0, 4.4, 3.2), (x0 - L / 2 + 1.4, y0, z0 + 2.6), mat("bridge_w", "#F2F2F2"), bevel=0.05))
    parts.append(box((2.6, 4.6, 0.3), (x0 - L / 2 + 1.4, y0, z0 + 4.25), mat("bridge_w", "#F2F2F2")))
    rnd = random.Random(seed)
    cm = [mat(f"cont{i}", c, rough=0.5) for i, c in enumerate(CCOLS)]
    for i in range(rows):
        for j in range(cols):
            for k in range(rnd.randint(2, tiers)):
                parts.append(box((1.8, 0.98, 0.95), (x0 - L / 2 + 3.6 + i * 1.95, y0 - 1.5 + j * 1.0, z0 + 1.5 + k * 0.97),
                                 cm[rnd.randrange(len(cm))]))
    attach(r, parts)
    return r


def shot_container():
    m1, m2 = MARKS[1], MARKS[2]
    sea("#2F6E9E", "#4F92C4")
    first = container_ship((0, 4, 0), L=12, rows=4, cols=2, tiers=2, seed=2)
    yr = text3d("1956", (0, 0, 6.5), size=1.2, m=mat("yr_c", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    key(yr, "scale", m1 - 6, (1, 1, 1))
    key(yr, "scale", m1, (0, 0, 0))
    key(first, "location", 1, (-4, 4, 0))
    key(first, "location", m1, (8, 4, 0))
    key(first, "location", m1 + 20, (60, 4, 0))
    big = container_ship((0, 4, 0), L=60, rows=28, cols=4, tiers=6, seed=5)
    big.scale = (1, 1.8, 1)
    key(big, "location", 1, (-140, 30, 0))
    key(big, "location", m1, (-70, 22, 0))
    key(big, "location", N, (-6, 12, 0))
    tx = text3d("20,000+", (0, -4, 11), size=2.4, m=mat("tx_c", "#5CD8FF", emit=1.5))
    pop_in(tx, m1 + 40, 8)
    camera((4, -16, 3.5), (0, 4, 2.5), lens=30, moves=[(m1 / N, (4, -18, 4), (2, 4, 2.5)), (1.0, (6, -30, 8), (-6, 12, 4))])
