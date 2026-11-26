
# ---------------------------------------------------------------- bridge shots
REDSTEEL = mat("redsteel", "#B8432F", rough=0.45, metal=0.5)
GG = mat("gg_orange", "#C0362C", rough=0.5, metal=0.3)
WHITE_C = mat("white_c", "#EDEFF2", rough=0.5)
ROAD = mat("road", "#3B3D42", rough=0.8)
LINE = mat("line_y", "#F2D04E", rough=0.5)
CABLE = mat("cable", "#8E99A6", rough=0.3, metal=0.6)
ROPE = mat("rope", "#B89558", noise=("#93743F", 10))
PLANK = mat("plank", "#8C6239", noise=("#6E4A2A", 8))
LEAF = mat("leaf", "#6E9B4A", noise=("#58823A", 4))


def tree(x, y, s=1.0):
    cyl(0.12 * s, 1.4 * s, (x, y, 0.7 * s + 0.6), LOG, verts=8)
    ball(0.6 * s, (x, y, 1.6 * s + 0.6), LEAF, seg=8)


def car(x, y, z, color, s=1.0):
    c = box((0.9 * s, 0.45 * s, 0.28 * s), (x, y, z + 0.2 * s), mat("car" + color, color, rough=0.3, metal=0.3), bevel=0.03)
    box((0.5 * s, 0.4 * s, 0.2 * s), (x - 0.05 * s, y, z + 0.42 * s), mat("carwin", "#2B3440", rough=0.2))
    return c


def shot_log():
    m1, m2, m3 = MARKS[1], MARKS[2], MARKS[3]
    river(w=3.2)
    for x, y in ((-3.5, 3), (-5, 6), (3.6, 4), (5, 1.5), (4.2, 8), (-4.2, 10)):
        tree(x, y, 1.0)
    scatter_rocks(10, (-4, 4), (-1, 6), seed=3)
    # the fallen log drops across the stream
    lg = cyl(0.2, 4.6, (0, 1.0, 0.85), LOG, rot=(0, math.radians(90), 0), verts=12)
    key(lg, "location", 1, (0, 1.0, 6))
    key(lg, "location", m2, (0, 1.0, 6))
    key(lg, "location", m2 + 12, (0, 1.0, 0.85))
    key(lg, "rotation_euler", m2, (0, math.radians(90), math.radians(30)))
    key(lg, "rotation_euler", m2 + 12, (0, math.radians(90), 0))
    # stacked stones + flat slabs a little upstream
    for i, x in enumerate((-1.0, 0.0, 1.0)):
        for k in range(3):
            st = box((0.55, 0.6, 0.26), (x, 4.0, 0.0 + 0.27 * k), STONE, bevel=0.05)
            pop_in(st, m3 + i * 6 + k * 2, 6)
    for i, x in enumerate((-1.25, -0.5, 0.5, 1.25)):
        sl = box((1.0 if abs(x) < 1 else 0.9, 0.9, 0.12), (x, 4.0, 0.72), STONE, bevel=0.03)
        pop_in(sl, m3 + 24 + i * 5, 6)
    camera((1.5, -5.5, 2.6), (0, 2.0, 0.6), lens=32,
           moves=[(m2 / N, (1.0, -4.2, 2.2), (0, 1.5, 0.6)), (m3 / N, (1.6, -2.5, 2.4), (0, 2.8, 0.6)), (1.0, (2.6, -2.8, 3.2), (0, 4.0, 0.6))])


def arch_ring(cx, R, thick, y0, depth, m, t0, step=1):
    """Semicircular ring of stone blocks centred at x=cx, springing at z=0; blocks pop in from both feet."""
    n = 11
    objs = []
    for i in range(n):
        a = math.pi * (i + 0.5) / n
        x, z = cx + (R + thick / 2) * math.cos(a), (R + thick / 2) * math.sin(a)
        b = box((thick * 0.95, depth, math.pi * R / n * 0.95), (x, y0, z), m, bevel=0.03)
        b.rotation_euler = (0, -a, 0)
        order = min(i, n - 1 - i)
        pop_in(b, t0 + order * step, 5)
        objs.append(b)
    return objs


def shot_arch():
    river(w=12, m_bank=GRASS)
    R, th, dep = 1.7, 0.45, 2.0
    t = 4
    for k, cx in enumerate((-4.0, 0.0, 4.0)):
        arch_ring(cx, R, th, 2.0, dep, SANDSTONE, t + k * 14, step=2)
    # piers between arches and spandrel walls
    for x in (-6.15, -2.0, 2.0, 6.15):
        p = box((0.6, dep, 2.2), (x, 2.0, 1.0), SANDSTONE, bevel=0.03)
        pop_in(p, 2, 6)
    deck = box((13.0, dep + 0.2, 0.35), (0, 2.0, 2.45), SANDSTONE, bevel=0.03)
    pop_in(deck, 50, 8)
    for x in range(-6, 7):
        w = box((0.8, 0.2, 0.3), (x, 1.0, 2.75), STONE, bevel=0.03)
        pop_in(w, 54 + abs(x) * 2, 5)
    # weight arrows: glowing balls running down along the arch to the ground
    for k, cx in enumerate((-4.0, 0.0, 4.0)):
        for side in (-1, 1):
            for j in range(3):
                b = ball(0.12, (cx, 0.9, R + th + 0.2), mat("force", "#5CD8FF", emit=3.0), seg=10)
                t0 = 90 + j * 18 + k * 4
                pts = [(cx + side * (R + th / 2) * math.cos(a), 0.9, (R + th / 2) * math.sin(a))
                       for a in (math.pi / 2, math.pi / 3, math.pi / 6, 0.02)]
                pop_in(b, t0, 4)
                for q, p in enumerate(pts):
                    key(b, "location", t0 + q * 7, p)
                pop_out(b, t0 + 21, 4)
    camera((3.0, -9.5, 3.2), (0, 2.0, 1.5), lens=30, moves=[(1.0, (-1.5, -7.0, 2.0), (0, 2.0, 1.4))])


def shot_rope():
    world = bpy.context.scene.world.node_tree
    for sx in (-1, 1):
        box((8, 14, 12), (sx * 7.0, 3, -6 + 3), ROCK)
        box((8, 14, 0.15), (sx * 7.0, 3, 3.07), GRASS)
    box((40, 40, 0.1), (0, 3, -9), flowing("gorge_river", "#4E9BD0", "#7FC2EA", speed=(0, 1.5, 0)))
    for x, y in ((-5, 6), (-7, 2), (6, 7), (8, 3)):
        cyl(0.1, 1.2, (x, y, 3.6), LOG, verts=8)
        ball(0.5, (x, y, 4.4), LEAF, seg=8)
    # catenary rope bridge across x=-3..3
    def sag(x):
        return 3.0 - 0.9 * (1 - (x / 3.0) ** 2)
    xs = [i * 0.5 - 3.0 for i in range(13)]
    for y in (-0.45, 0.45):
        curve_tube([(x, y, sag(x)) for x in xs], 0.035, ROPE)
        curve_tube([(x, y, sag(x) + 0.9 - 0.1 * (1 - (x / 3) ** 2)) for x in xs], 0.035, ROPE)
        for x in xs[1:-1]:
            beam((x, y, sag(x)), (x, y, sag(x) + 0.9 - 0.1 * (1 - (x / 3) ** 2)), 0.02, ROPE)
    for i in range(24):
        x = -2.9 + i * 0.252
        p = box((0.18, 0.95, 0.05), (x, 0, sag(x) + 0.03), PLANK)
        pop_in(p, 6 + i * 3, 5)
    for sx in (-1, 1):
        for y in (-0.45, 0.45):
            cyl(0.08, 1.3, (sx * 3.15, y, 3.6), LOG, verts=8)
    camera((-1.5, -6.5, 3.2), (0, 0, 2.4), lens=28, moves=[(1.0, (1.8, -5.0, 1.4), (0, 0.5, 2.6))])


def shot_ironbridge():
    river(w=8.0)
    for k, y in enumerate((-0.6, -0.2, 0.2, 0.6)):
        for R in (3.6, 3.2):
            pts = [(R * math.cos(a), y, -0.4 + R * math.sin(a) * 0.85) for a in [math.pi * i / 16 for i in range(17)]]
            o = curve_tube(pts, 0.06, IRON)
            pop_in(o, 4 + k * 6, 8)
        # radial braces
        for i in range(1, 8):
            a = math.pi * i / 8
            b = beam((3.2 * math.cos(a), y, -0.4 + 3.2 * math.sin(a) * 0.85),
                     (3.6 * math.cos(a), y, -0.4 + 3.6 * math.sin(a) * 0.85), 0.05, IRON)
            pop_in(b, 10 + k * 6, 6)
    deck = box((9.5, 1.8, 0.2), (0, 0, 2.75), IRON)
    pop_in(deck, 34, 8)
    for x in [i * 0.5 - 4.5 for i in range(19)]:
        r = box((0.05, 0.05, 0.5), (x, -0.9, 3.05), IRON)
        pop_in(r, 38, 6)
    for sx in (-1, 1):
        box((1.4, 2.2, 3.2), (sx * 4.6, 0, 1.2), SANDSTONE, bevel=0.03)
    yr = text3d("1779", (0, -1.5, 4.7), size=0.9, m=mat("yr_t", "#F2C14E", emit=1.2))
    pop_in(yr, 20, 8)
    camera((1.5, -10.0, 2.0), (0, 0, 2.2), lens=32, moves=[(1.0, (-1.0, -8.5, 1.4), (0, 0, 2.4))])


def shot_truss():
    river(w=14.0)
    z0, H, L = 1.2, 1.6, 12.0
    for y in (-0.7, 0.7):
        for i in range(12):
            x0, x1 = -L / 2 + i, -L / 2 + i + 1
            beam((x0, y, z0), (x1, y, z0), 0.12, REDSTEEL)
            beam((x0, y, z0 + H), (x1, y, z0 + H), 0.12, REDSTEEL)
            if i % 2 == 0:
                beam((x0, y, z0), (x1, y, z0 + H), 0.09, REDSTEEL)
            else:
                beam((x0, y, z0 + H), (x1, y, z0), 0.09, REDSTEEL)
            beam((x1, y, z0), (x1, y, z0 + H), 0.07, REDSTEEL)
    for i in range(13):
        beam((-L / 2 + i, -0.7, z0 + H), (-L / 2 + i, 0.7, z0 + H), 0.06, REDSTEEL)
    box((L, 1.4, 0.12), (0, 0, z0 - 0.06), IRON)
    for y in (-0.3, 0.3):
        box((L + 30, 0.06, 0.06), (0, y, z0 + 0.03), STEEL)
    for x in (-2, 2):
        box((0.8, 1.8, z0), (x * 3, 0, z0 / 2), CONCRETE)
    # train crosses
    train = []
    cols = ["#2F5E8C", "#8C2F2F", "#8C2F2F", "#8C2F2F"]
    for k in range(4):
        c = box((1.5, 0.75, 0.75), (0, 0, z0 + 0.5), mat(f"tr{k}", cols[k], rough=0.4, metal=0.3), bevel=0.05)
        train.append(c)
        key(c, "location", 1, (-16 - k * 1.6, 0, z0 + 0.5))
        key(c, "location", N, (8 - k * 1.6, 0, z0 + 0.5))
        c.animation_data.action.fcurves[0].keyframe_points[0].interpolation = "LINEAR"
    camera((-3.0, -8.5, 2.8), (0, 0, 1.6), lens=30, moves=[(1.0, (2.5, -7.5, 2.2), (0, 0, 1.8))])


def shot_suspension():
    box((300, 300, 0.1), (0, 0, 0.0), flowing("bay", "#3E7FB0", "#6FA9D4", scale=2.0, speed=(1, 1, 0)))
    for sx in (-1, 1):
        box((10, 30, 3.0), (sx * 19, 5, 1.5), GRASS)
    T, H, D = 7.0, 7.5, 2.4
    for x in (-T, T):
        for y in (-0.8, 0.8):
            box((0.45, 0.45, H), (x, y, H / 2), GG)
        for z in (2.6, 4.6, 6.6, H):
            box((0.4, 1.6, 0.35), (x, 0, z), GG)
    deck = box((32, 2.0, 0.35), (0, 0, D), GG)
    box((32, 1.6, 0.05), (0, 0, D + 0.2), ROAD)

    def cab(x):
        if abs(x) <= T:
            return D + 0.5 + (H - D - 0.5) * (x / T) ** 2
        return H - (H - D - 0.2) * (abs(x) - T) / (16 - T)
    xs = [i * 0.5 - 16 for i in range(65)]
    for y in (-0.8, 0.8):
        c = curve_tube([(x, y, cab(x)) for x in xs], 0.07, GG)
        for x in xs[::2]:
            if abs(abs(x) - T) > 0.3:
                beam((x, y, D + 0.15), (x, y, cab(x)), 0.025, GG)
    yr = text3d("1937", (0, -1.8, 9.4), size=1.2, m=mat("yr_t2", "#FFD23F", emit=1.2))
    pop_in(yr, 30, 8)
    for k in range(4):
        cr = car(0, -0.35 if k % 2 else 0.35, D + 0.2, ["#E8E8E8", "#3A6EA5", "#CC3333", "#F2C14E"][k], 0.8)
        d = 1 if k % 2 else -1
        key(cr, "location", 1, (-d * (14 - k * 5), cr.location.y, cr.location.z))
        key(cr, "location", N, (d * (14 + k * 2), cr.location.y, cr.location.z))
    camera((-12, -25, 5.0), (0, 0, 4.5), lens=30, moves=[(1.0, (5, -26, 3.0), (0, 0, 4.8))])


def shot_cablestay():
    box((300, 300, 0.1), (0, 0, 0.0), flowing("bay2", "#3E7FB0", "#6FA9D4", scale=2.0, speed=(1, 1, 0)))
    D = 3.0
    box((60, 2.4, 0.4), (0, 0, D), WHITE_C)
    box((60, 2.0, 0.05), (0, 0, D + 0.22), ROAD)
    box((60, 0.08, 0.06), (0, 0, D + 0.26), LINE)
    for x0 in (-12, 12):
        # A-shaped tower
        for sy in (-1, 1):
            beam((x0, sy * 1.6, 0), (x0, sy * 0.25, 16), 0.5, WHITE_C)
        box((0.6, 2.8, 0.4), (x0, 0, D - 0.3), WHITE_C)
        box((1.6, 3.4, 2.8), (x0, 0, 1.4), CONCRETE)
        for i in range(10):
            for side in (-1, 1):
                xa = x0 + side * (1.6 + i * 1.15)
                zt = 15.6 - i * 0.55
                cb = beam((x0, 0, zt), (xa, 0, D + 0.2), 0.08, CABLE)
                pop_in(cb, 4 + i * 3, 6)
    for k in range(6):
        cr = car(0, -0.45 if k % 2 else 0.45, D + 0.24, ["#E8E8E8", "#3A6EA5", "#CC3333", "#F2C14E", "#2E8B57", "#555555"][k], 0.8)
        d = 1 if k % 2 else -1
        key(cr, "location", 1, (-d * (26 - k * 7), cr.location.y, cr.location.z))
        key(cr, "location", N, (d * (20 + k * 3), cr.location.y, cr.location.z))
    km = text3d("1 KM+", (0, -12.0, 11.5), size=1.4, m=mat("km_t", "#5CD8FF", emit=1.5))
    pop_in(km, MARKS[0] + 40, 8)
    camera((-7, -24, 6.5), (-7, 0, 8), lens=26, moves=[(1.0, (0, -36, 8), (0, 0, 9))])
