# ---------------------------------------------------------------- fridge shots
ICE = mat("ice", "#BFE6F7", rough=0.08, alpha=0.85, spec=0.8)
MEAT = mat("meat", "#B5453C", rough=0.5)
APPLE = mat("apple", "#D8352A", rough=0.35)
GREEN_F = mat("greens", "#5FA34A", rough=0.6)
FLY = mat("fly", "#151515", rough=0.4)
SALT = mat("salt", "#F4F2EC", rough=0.9)
JAR = mat("jar", "#B4673E", noise=("#9A5532", 6))
MUD_DOME = mat("mud_dome", "#C9A574", noise=("#B48F5F", 3))
COLD = mat("cold_air", "#8FD3FF", emit=1.5, alpha=0.7)
HOT = mat("hot_gas", "#FF7A45", emit=2.0)
WHITE_ENAMEL = mat("enamel", "#F2F0EA", rough=0.25, spec=0.5)
TOXIC = mat("toxic", "#9BE36A", alpha=0.5, emit=0.9)
OCEAN = mat("ocean", "#2F80ED", rough=0.4)
LANDM = mat("land", "#3DBE6B")
OZONE = mat("ozone", "#7FD8FF", alpha=0.25, emit=0.6)
FRIDGE_LIGHT = mat("fridge_light", "#FFF6DA", emit=2.5)


def food_table(x, y):
    box((2.4, 1.2, 0.12), (x, y, 0.9), WOOD, bevel=0.02)
    for dx in (-1.05, 1.05):
        for dy in (-0.5, 0.5):
            box((0.1, 0.1, 0.9), (x + dx, y + dy, 0.45), WOOD)
    items = []
    items.append(box((0.6, 0.4, 0.22), (x - 0.6, y - 0.1, 1.07), MEAT, bevel=0.06))
    for i in range(5):
        items.append(ball(0.13, (x + 0.2 + 0.22 * (i % 3), y - 0.2 + 0.25 * (i // 3), 1.1), APPLE, seg=12))
    items.append(ball(0.22, (x + 0.75, y + 0.25, 1.12), GREEN_F, seg=10, squash=0.7))
    return items


def flies(center, n, start, seed=1, radius=0.6):
    rnd = random.Random(seed)
    for i in range(n):
        f = ball(0.04, center, FLY, seg=8)
        t0 = start + i * 3
        pop_in(f, t0, 3)
        ph = rnd.uniform(0, math.tau)
        for k, fr in enumerate(range(t0, N + 1, 6)):
            a = ph + k * 0.9
            f.location = Vector(center) + Vector((radius * math.cos(a), radius * 0.5 * math.sin(a), 0.25 + 0.15 * math.sin(k)))
            f.keyframe_insert("location", frame=fr)


def shot_market():
    ground()
    items = food_table(0, 2)
    flies((0, 2, 1.2), 12, F(0.12), seed=4)
    # food darkens as it spoils
    for o in items:
        m = o.data.materials[0]
    sun = ball(0.8, (2.2, 9, 5.5), mat("sun_disc", "#FFC850", emit=6), seg=20)
    hut((-3.2, 6), 0.9)
    hut((3.4, 8), 1.0)
    scatter_rocks(20, (-5, 5), (-1, 10), seed=6)
    camera((0.8, -3.2, 2.4), (0, 2, 1.1), lens=30, moves=[(1.0, (0.3, -2.2, 2.0), (0, 2, 1.1))])


def shot_cellar():
    front = -1.0
    layers = section(front)
    room = box((3.6, 3.0, 2.0), (0, front + 1.2, -1.45))
    for l in layers[:2]:
        cut(l, room)
    box((3.6, 0.1, 2.0), (0, front + 2.75, -1.45), mat("cellar_back", "#6E4A2E"))
    for i, x in enumerate((-1.2, -0.4, 0.4, 1.2)):
        j = cyl(0.28, 0.75, (x, front + 1.6, -2.07), JAR, r2=0.18, verts=20)
    box((3.2, 0.5, 0.08), (0, front + 2.3, -1.2), WOOD)
    box((0.7, 0.4, 0.25), (-0.9, front + 2.3, -1.03), MEAT, bevel=0.05)
    for k in range(6):
        ball(0.06, (-0.6 + 0.05 * k, front + 2.2, -0.88), SALT, seg=8)
    # stairs down
    for s in range(5):
        box((0.6, 0.6, 0.18), (1.5, front + 1.2 - 0.0, -0.45 - 0.38 * s), STONE)
    # the sun bakes the ground: heat shimmer balls
    sun = ball(0.7, (-2.0, front + 12, 4.5), mat("sun2", "#FFB547", emit=6), seg=20)
    rnd = random.Random(3)
    for i in range(14):
        h = ball(0.12, (rnd.uniform(-3, 3), front + 1.2, 0.2), mat("heat", "#FF8A4C", emit=2, alpha=0.6), seg=10)
        t0 = F(0.5 + 0.035 * i)
        pop_in(h, t0, 4)
        key(h, "location", t0, h.location.copy())
        key(h, "location", min(N, t0 + 22), h.location + Vector((0, 0, -1.6)))
        pop_out(h, min(N - 1, t0 + 18), 5)
    hut((-3, 8), 0.9)
    camera((0, front - 8.5, 1.4), (0, front + 1, -1.0), lens=32, moves=[(1.0, (0.3, front - 7.6, 1.2), None)])


def shot_yakhchal():
    front = -1.0
    layers = section(front, layers=[(0.0, -0.35, SAND_TOP), (-0.35, -4.5, SOIL), (-4.5, -9, ROCK)])
    pit = cyl(2.0, 4.0, (0, front + 2.0, -2.0), smooth=False, verts=48)
    for l in layers[:2]:
        cut(l, pit)
    cut(layers[1], box((4.0, 2.0, 4.0), (0, front + 0.9, -2.0)))
    # dome (cut in half to show the inside)
    dome = cyl(2.6, 5.0, (0, front + 2.0, 2.5), MUD_DOME, r2=0.25, verts=48)
    cut(dome, cyl(2.2, 4.6, (0, front + 2.0, 2.2), smooth=False, r2=0.1, verts=48))
    cut(dome, box((7, 3.0, 7), (0, front + 0.5, 2.5)))
    # ice blocks stacked in the pit
    for r in range(3):
        for c in range(3):
            b = box((0.9, 0.9, 0.75), (-1.0 + c * 1.0, front + 2.4, -3.6 + r * 0.8), ICE, bevel=0.04)
            pop_in(b, F(0.18) + 3 * (r * 3 + c), 6)
    # shading wall beside it
    box((0.6, 6, 3.2), (-4.2, front + 6, 1.6), MUD_DOME, bevel=0.05)
    sun = ball(0.7, (3.0, front + 14, 6.0), mat("sun3", "#FFB547", emit=6), seg=20)
    camera((0.4, front - 10.5, 1.8), (0, front + 1.5, -0.4), lens=30, moves=[(1.0, (-0.3, front - 9.0, 1.4), None)])


def shot_icebox():
    box((10, 8, 0.1), (0, 1, -0.05), mat("kitchen_floor", "#9C7A55", noise=("#86664A", 5)))
    box((10, 0.3, 6), (0, 1.6, 3), mat("kitchen_wall", "#E5D7BE"))
    cab = box((1.6, 1.0, 2.2), (0, 0.6, 1.1), DARK_WOOD, bevel=0.04)
    cut(cab, box((1.3, 1.0, 0.75), (0, 0.15, 1.75)))
    cut(cab, box((1.3, 1.0, 0.95), (0, 0.15, 0.7)))
    for z in (1.75, 0.7):
        box((0.06, 0.06, 0.3), (0.72, 0.05, z), BRASS)
    ice = box((1.1, 0.7, 0.6), (0, 0.6, 1.72), ICE, bevel=0.05)
    key(ice, "location", 1, (0, -2.5, 3.2))
    key(ice, "location", F(0.2), (0, -2.5, 3.2))
    key(ice, "location", F(0.38), (0, 0.6, 1.72))
    food = [box((0.45, 0.35, 0.22), (-0.35, 0.55, 0.36), MEAT, bevel=0.05),
            ball(0.13, (0.25, 0.5, 0.38), APPLE, seg=12), ball(0.13, (0.48, 0.55, 0.38), APPLE, seg=12),
            cyl(0.14, 0.4, (0.1, 0.75, 0.45), mat("milk", "#F7F7F2"), verts=20)]
    rnd = random.Random(7)
    for i in range(22):
        c = ball(0.05, (rnd.uniform(-0.55, 0.55), 0.3, 1.4), COLD, seg=8)
        t0 = F(0.42 + 0.022 * i)
        pop_in(c, t0, 3)
        key(c, "location", t0, c.location.copy())
        key(c, "location", min(N, t0 + 26), c.location + Vector((rnd.uniform(-0.1, 0.1), 0, -1.0)))
        pop_out(c, min(N - 1, t0 + 22), 4)
    camera((1.0, -3.8, 2.0), (0, 0.6, 1.2), lens=30, moves=[(0.4, (0.6, -3.4, 2.1), None), (1.0, (0.2, -2.9, 1.6), None)])


def shot_perkins():
    box((10, 8, 0.1), (0, 1, -0.05), mat("workshop", "#6F5B45", noise=("#5E4B37", 5)))
    box((10, 0.3, 6), (0, 2.2, 3), mat("brick_wall", "#9A5A40", noise=("#84492F", 8)))
    comp = cyl(0.55, 1.0, (-1.4, 0.8, 0.9), IRON, verts=32)
    box((1.4, 1.0, 0.3), (-1.4, 0.8, 0.2), IRON, bevel=0.04)
    wheel = torus(0.6, 0.08, (-2.4, 0.8, 1.0), IRON, rot=(math.radians(90), 0, 0))
    key(wheel, "rotation_euler", 1, (math.radians(90), 0, 0))
    key(wheel, "rotation_euler", N, (math.radians(90), math.radians(720), 0))
    linear(wheel)
    # closed loop of pipe: compressor -> hot coil (top) -> valve -> cold coil (bottom)
    pts = [(-1.4, 0.8, 1.45), (-1.4, 0.8, 2.6), (0.0, 0.8, 2.9), (1.5, 0.8, 2.6), (1.7, 0.8, 1.6),
           (1.5, 0.8, 0.5), (0.2, 0.8, 0.35), (-0.9, 0.8, 0.5)]
    curve_tube(pts + [pts[0]], 0.09, PIPE)
    tank = box((1.3, 0.9, 0.9), (0.9, 0.5, 0.6), mat("cold_tank", "#5C88A8", rough=0.3), bevel=0.05)
    frost = box((1.32, 0.92, 0.2), (0.9, 0.5, 1.05), ICE, bevel=0.05)
    pop_in(frost, F(0.6), 10)
    # gas particles flowing round the loop: hot (orange) on top, cold (blue) on the bottom
    path = [Vector(p) for p in pts] + [Vector(pts[0])]
    seglen = [(path[i + 1] - path[i]).length for i in range(len(path) - 1)]
    total = sum(seglen)

    def at(u):
        d = (u % 1.0) * total
        for i, s in enumerate(seglen):
            if d <= s:
                return path[i] + (path[i + 1] - path[i]) * (d / s)
            d -= s
        return path[-1]
    for j in range(16):
        dot = ball(0.09, at(j / 16), HOT if (j / 16) < 0.5 else COLD, seg=8)
        for fr in range(1, N + 1, 3):
            u = j / 16 + fr / 120
            dot.location = at(u) + Vector((0, -0.12, 0))
            dot.keyframe_insert("location", frame=fr)
            dot.data.materials[0] = HOT if (u % 1.0) < 0.5 else COLD
    camera((0.2, -5.6, 1.8), (0.1, 0.8, 1.5), lens=30, moves=[(1.0, (-0.2, -4.8, 1.7), None)])


def shot_oldfridge():
    box((10, 8, 0.1), (0, 1, -0.05), mat("checker", "#D9D2C3"))
    box((10, 0.3, 6), (0, 1.6, 3), mat("wall_1920", "#B9D3C2"))
    body = box((1.3, 1.0, 1.8), (0, 0.6, 1.15), WHITE_ENAMEL, bevel=0.06)
    for dx in (-0.5, 0.5):
        box((0.12, 0.12, 0.25), (dx, 0.6, 0.12), IRON)
    top = cyl(0.42, 0.6, (0, 0.6, 2.35), WHITE_ENAMEL, verts=32)
    box((0.08, 0.06, 0.4), (0.5, 0.08, 1.4), CHROME)
    rnd = random.Random(2)
    for i in range(16):
        g = ball(rnd.uniform(0.12, 0.22), (rnd.uniform(-0.3, 0.3), 0.5, 2.5), TOXIC, seg=12)
        t0 = F(0.55 + 0.025 * i)
        pop_in(g, t0, 5)
        key(g, "location", t0, g.location.copy())
        key(g, "location", min(N, t0 + 30), g.location + Vector((rnd.uniform(-1.2, 1.2), rnd.uniform(-0.8, 0), 0.8)))
    warn = ball(0.2, (0.9, 0.05, 2.6), GLOW_RED, seg=12)
    pop_in(warn, F(0.62), 4)
    camera((0.9, -4.0, 1.9), (0, 0.6, 1.5), lens=30, moves=[(1.0, (0.3, -3.3, 1.8), None)])


def shot_ozone():
    bpy.context.scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.05
    e = ball(1.6, (0, 0, 1.6), OCEAN, seg=48)
    for (x, z, s) in [(-0.6, 2.4, 0.8), (0.5, 1.2, 0.7), (-0.2, 0.6, 0.5)]:
        bl = ball(s, (x, -1.0, z), LANDM, seg=24, squash=0.5)
        bl.rotation_euler = (math.radians(90), 0, 0)
        cut(bl, cyl(4, 4, (0, 0, 1.6), smooth=False))
        bl.modifiers[-1].operation = "INTERSECT"
    shell = ball(2.0, (0, 0, 1.6), OZONE, seg=48)
    hole = ball(0.9, (0, 0, 3.55), mat("hole_dark", "#0A0F20", alpha=0.85), seg=24, squash=0.25)
    key(hole, "scale", 1, (0, 0, 0))
    key(hole, "scale", F(0.45), (0, 0, 0))
    key(hole, "scale", F(0.75), (1, 1, 0.25))
    rnd = random.Random(1)
    for _ in range(80):
        ball(rnd.uniform(0.01, 0.03), (rnd.uniform(-5, 5), 6, rnd.uniform(-4, 8)), mat("star", "#FFFFFF", emit=3), seg=6)
    for o in (e, shell):
        key(o, "rotation_euler", 1, (0, 0, 0))
        key(o, "rotation_euler", N, (0, 0, math.radians(40)))
    camera((0, -7.5, 4.2), (0, 0, 1.8), lens=32, moves=[(1.0, (0, -6.5, 4.6), None)])


def shot_modern():
    m2 = MARKS[1] if len(MARKS) > 1 else int(N * 0.6)
    box((10, 8, 0.1), (0, 1, -0.05), TILE)
    box((10, 0.3, 6), (0, 1.6, 3), mat("kitchen2", "#EEF1F3"))
    body = box((1.8, 1.1, 2.6), (0, 0.85, 1.3), STEEL, bevel=0.04)
    cut(body, box((1.6, 1.2, 2.4), (0, 0.1, 1.3)))
    box((1.6, 0.05, 2.4), (0, 1.35, 1.3), FRIDGE_LIGHT)
    for z in (0.8, 1.4, 2.0):
        box((1.6, 0.9, 0.04), (0, 0.85, z), GLASS)
    ball(0.13, (-0.4, 0.8, 0.95), APPLE, seg=12); ball(0.13, (-0.15, 0.8, 0.95), APPLE, seg=12)
    cyl(0.12, 0.45, (0.4, 0.8, 1.65), mat("milk2", "#F7F7F2"), verts=20)
    box((0.5, 0.4, 0.2), (0.3, 0.8, 0.95), MEAT, bevel=0.05)
    ball(0.22, (-0.4, 0.8, 1.6), GREEN_F, seg=10, squash=0.7)
    dl = hinge_door(-0.9, 0.28, 0.9, 2.5, STEEL, angle=-110)
    dr_pivot = hinge_door(0.9, 0.28, -0.9, 2.5, STEEL, angle=110)
    t_open = F(0.12)
    for d, ang in ((dl, -110), (dr_pivot, 110)):
        key(d, "rotation_euler", 1, (0, 0, 0))
        key(d, "rotation_euler", t_open, (0, 0, 0))
        key(d, "rotation_euler", t_open + 20, (0, 0, math.radians(ang)))
    badge = text3d("A+++", (1.25, 0.2, 2.3), size=0.3, m=mat("eco", "#3BE37A", emit=2.0))
    pop_in(badge, F(0.35), 6)
    camera((0.6, -3.6, 1.8), (0, 0.8, 1.35), lens=30,
           moves=[(m2 / N, (0.2, -2.9, 1.7), None), (1.0, (0.4, -4.4, 2.0), None)])


