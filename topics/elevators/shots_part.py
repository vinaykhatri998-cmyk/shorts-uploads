
# ---------------------------------------------------------------- elevator shots
BRICK = mat("brick", "#B5654A", noise=("#9A5039", 6))
GLASS_T = mat("glass_tower", "#7FB2D6", rough=0.15, metal=0.4)
SKIN = mat("skin", "#E0A982")
SHIRT = mat("shirt", "#3A6EA5")
ROPE = mat("rope", "#B89558", noise=("#93743F", 10))
CAGE = mat("cage", "#3B3B40", rough=0.4, metal=0.7)
LION = mat("lion", "#D9A13B")
MANE = mat("mane", "#8A4B1E")
FLASH = mat("flash", "#FFD23F", emit=6.0)


def applied(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def person(x, y, z, s=1.0, shirt=None):
    body = cyl(0.16 * s, 0.6 * s, (x, y, z + 0.3 * s), shirt or SHIRT, verts=12)
    head = ball(0.13 * s, (x, y, z + 0.75 * s), SKIN, seg=12)
    head.parent = body
    head.location = (0, 0, 0.45 * s)
    return body


def cage_box(w, d, h, loc, m=CAGE, bars=5):
    """Open-frame cage: floor, roof and corner/side bars, parented to the floor."""
    x, y, z = loc
    floor = applied(box((w, d, 0.08), (x, y, z), m))
    parts = [box((w, d, 0.06), (x, y, z + h), m)]
    for i in range(bars):
        bx = -w / 2 + w * i / (bars - 1)
        for by in (-d / 2, d / 2):
            parts.append(cyl(0.025, h, (x + bx, y + by, z + h / 2), m, verts=6))
    for by in [-d / 2 + d * i / 3 for i in range(4)]:
        parts.append(cyl(0.025, h, (x + w / 2, y + by, z + h / 2), m, verts=6))
        parts.append(cyl(0.025, h, (x - w / 2, y + by, z + h / 2), m, verts=6))
    for p in parts:
        p.parent = floor
        p.location = p.location - floor.location
    return floor


def shot_stairs():
    ground()
    W, D, FH, NF = 4.0, 3.0, 1.4, 6
    for i in range(NF + 1):
        box((W, D, 0.12), (0, 0, i * FH), CONCRETE)
    box((W, 0.15, NF * FH), (0, D / 2, NF * FH / 2), WALL)
    box((0.15, D, NF * FH), (-W / 2, 0, NF * FH / 2), WALL)
    # zig-zag stairs
    steps = 8
    for f in range(NF):
        for k in range(steps):
            xdir = 1 if f % 2 == 0 else -1
            x = xdir * (-1.2 + k * 0.3)
            box((0.3, 0.9, 0.14), (x, -0.6, f * FH + (k + 1) * FH / steps - 0.07), WOOD)
    # a tired climber
    p = person(-1.3, -0.6, 0.06, 0.9)
    pts = []
    for f in range(4):
        xdir = 1 if f % 2 == 0 else -1
        pts.append((xdir * -1.3, -0.6, f * FH + 0.06))
        pts.append((xdir * 1.1, -0.6, (f + 1) * FH + 0.06))
    for i, pt in enumerate(pts):
        key(p, "location", 1 + round(i * (N - 1) / (len(pts) - 1)), pt)
    sweat = []
    for i in range(6):
        b = ball(0.05, (0, -0.6, 0), mat("sweat", "#8FD3FF", emit=1.0), seg=8)
        b.parent = p
        b.location = (0.18, -0.05, 0.9)
        pop_in(b, 40 + i * 25, 4)
        key(b, "location", 40 + i * 25, (0.18, -0.05, 0.9))
        key(b, "location", 40 + i * 25 + 12, (0.35, -0.1, 0.4))
        pop_out(b, 40 + i * 25 + 12, 3)
    camera((3.5, -7.5, 3.0), (0, 0, 2.2), lens=30, moves=[(1.0, (2.5, -6.5, 6.0), (0, 0, 4.0))])


def shot_colosseum():
    HM = mat("hypo", "#8A7A62", noise=("#76684F", 3))
    box((400, 400, 0.02), (0, 200 + 2.5, -0.01), SAND_TOP)
    box((40, 40, 9), (0, 2.5 + 20, -4.5), HM)
    box((14, 4, 0.2), (0, 0.5, -4.7), mat("pitfloor", "#5E5244"))
    for sx in (-1, 1):
        box((1.0, 4, 4.8), (sx * 7, 0.5, -2.4), HM)
    box((14, 0.2, 4.8), (0, 2.5, -2.4), mat("dark", "#3A3128"))
    # arena floor with a trapdoor hole at x=1.4, y=0.6
    hx, hy, hw, hd = 1.4, 0.6, 1.6, 1.4
    box((14, 3.5, 0.3), (0, 0.75, -0.15), SAND_TOP) if False else None
    yb, yf = -1.0, 2.5
    box((hx - hw / 2 + 7, yf - yb, 0.3), ((-7 + hx - hw / 2) / 2, (yb + yf) / 2, -0.15), SAND_TOP)
    box((7 - hx - hw / 2, yf - yb, 0.3), ((7 + hx + hw / 2) / 2, (yb + yf) / 2, -0.15), SAND_TOP)
    box((hw, hy - hd / 2 - yb, 0.3), (hx, (yb + hy - hd / 2) / 2, -0.15), SAND_TOP)
    box((hw, yf - hy - hd / 2, 0.3), (hx, (yf + hy + hd / 2) / 2, -0.15), SAND_TOP)
    point_light((0, -0.5, -1.2), 120, flicker=True)
    # arena wall ring behind
    for i in range(16):
        a = math.pi * i / 15
        x, y = 9 * math.cos(a), 6 + 3 * math.sin(a)
        box((1.4, 0.6, 3.0), (x, y + 2, 1.5), SANDSTONE, bevel=0.03)
        box((0.5, 0.65, 1.2), (x, y + 1.95, 1.4), mat("archdark", "#5A4A38"))
    # capstan with 4 bars
    cap = cyl(0.25, 1.6, (-1.8, 0.4, -3.2), WOOD, verts=12)
    for k in range(2):
        bar = applied(box((2.4, 0.12, 0.12), (0, 0, 0), WOOD, rot=(0, 0, math.radians(90 * k))))
        bar.parent = cap
        bar.location = (0, 0, 0.3)
    key(cap, "rotation_euler", 1, (0, 0, 0))
    key(cap, "rotation_euler", N, (0, 0, math.radians(540)))
    workers = []
    for k in range(4):
        a = math.radians(90 * k + 45)
        w = person(0, 0, 0, 0.8, mat("tunic", "#8C5A3C"))
        w.parent = cap
        w.location = (1.0 * math.cos(a), 1.0 * math.sin(a), -0.8)
    # cage with a lion rising through a trapdoor
    cg = cage_box(1.4, 1.2, 1.2, (1.4, 0.6, -3.9), m=WOOD, bars=4)
    lion = ball(0.35, (0, 0, 0.4), LION, seg=12, squash=0.75)
    lion.parent = cg
    lion.location = (0, 0, 0.4)
    mane = ball(0.27, (0, 0, 0), MANE, seg=12)
    mane.parent = cg
    mane.location = (-0.35, 0, 0.6)
    head = ball(0.18, (0, 0, 0), LION, seg=10)
    head.parent = cg
    head.location = (-0.45, -0.08, 0.62)
    key(cg, "location", 1, (1.4, 0.6, -3.9))
    key(cg, "location", F(0.2), (1.4, 0.6, -3.9))
    key(cg, "location", F(0.8), (1.4, 0.6, 0.02))
    curve_tube([(-1.8, 0.4, -2.6), (-0.2, 0.5, -0.6), (1.4, 0.6, -0.4)], 0.03, ROPE)
    door = box((1.6, 1.4, 0.08), (1.4, 0.6, 0.02), WOOD)
    key(door, "location", F(0.55), (1.4, 0.6, 0.02))
    key(door, "location", F(0.65), (3.0, 0.6, 0.02))
    camera((2.0, -7.0, -0.8), (0, 0.5, -2.2), lens=30, moves=[(0.5, (1.5, -6.5, 0.0), (0.5, 0.5, -1.6)), (1.0, (1.2, -6.5, 1.6), (1.2, 0.5, -0.2))])


def shot_otis():
    m1, m2 = MARKS[1], MARKS[2]
    box((400, 400, 0.02), (0, 0, -0.01), mat("floor", "#8A7A62", noise=("#76684F", 4)))
    box((30, 0.3, 12), (0, 6, 6), mat("hall", "#CFC6B5"))
    H = 6.5
    for x in (-1.3, 1.3):
        box((0.25, 0.5, H), (x, 0, H / 2), DARK_WOOD)
        for k in range(22):
            prism(0.2, 0.3, 0.12, (x - math.copysign(0.18, x), 0, 0.6 + k * 0.26), STEEL).rotation_euler = (0, math.copysign(math.pi / 2, -x), 0)
    box((3.2, 0.6, 0.3), (0, 0, H), DARK_WOOD)
    plat = applied(box((2.2, 1.6, 0.12), (0, 0, 3.8), DARK_WOOD))
    otis = person(0, 0, 0, 1.0, mat("suit", "#2A2A33"))
    otis.parent = plat
    otis.location = (0.2, 0, 0.06)
    hat = cyl(0.1, 0.28, (0, 0, 0), BLACK, verts=12)
    hat.parent = otis
    hat.location = (0, 0, 0.66)
    # spring arms that catch the teeth
    for sx in (-1, 1):
        arm = box((0.3, 0.12, 0.08), (0, 0, 0), STEEL)
        arm.parent = plat
        arm.location = (sx * 1.05, 0, 0.2)
    rope_top = cyl(0.03, H - 3.95 - 0.15, (0, 0, (H + 3.95) / 2), ROPE, verts=8)
    cut_t = m1 + 40
    # the rope is cut: upper part vanishes, platform drops a little, brake flashes
    key(rope_top, "scale", cut_t, (1, 1, 1))
    key(rope_top, "scale", cut_t + 1, (0, 0, 0))
    key(plat, "location", 1, (0, 0, 3.8))
    key(plat, "location", cut_t, (0, 0, 3.8))
    key(plat, "location", cut_t + 4, (0, 0, 3.5))
    for sx in (-1, 1):
        f = ball(0.25, (sx * 1.15, -0.2, 3.65), FLASH, seg=10)
        key(f, "scale", 1, (0, 0, 0))
        key(f, "scale", cut_t + 4, (0, 0, 0))
        key(f, "scale", cut_t + 7, (1.4, 1.4, 1.4))
        key(f, "scale", cut_t + 16, (0, 0, 0))
    sc = text3d("✂", (0, -0.6, 5.4), size=0.4, m=FLASH) if False else None
    crowd = [person(x, -3 - (i % 2) * 0.6, 0, 0.95, mat(f"cr{i}", c)) for i, (x, c) in
             enumerate([(-3.0, "#6B3A3A"), (-2.2, "#3A4F6B"), (2.4, "#5A6B3A"), (3.2, "#6B5A3A"), (-3.8, "#444455")])]
    yr = text3d("1854", (0, -0.8, 7.1), size=0.8, m=mat("yr_e", "#F2C14E", emit=1.2))
    pop_in(yr, m1 + 4, 8)
    camera((2.5, -9.5, 2.0), (0, 0, 4.0), lens=32, moves=[(m1 / N, (1.8, -8.0, 2.4), None), (m2 / N, (0.8, -5.5, 3.6), (0, 0, 3.7)), (1.0, (0.4, -4.8, 3.8), (0, 0, 3.8))])


def building_cut(floors, W=4.0, D=3.0, FH=1.2, m=BRICK):
    for i in range(floors + 1):
        box((W, D, 0.1), (0, 0, i * FH), CONCRETE)
    box((W, 0.15, floors * FH), (0, D / 2, floors * FH / 2), m)
    for sx in (-1, 1):
        box((0.15, D, floors * FH), (sx * W / 2, 0, floors * FH / 2), m)
    for i in range(floors):
        for x in (-1.2, 1.2):
            box((0.7, 0.05, 0.6), (x, D / 2 - 0.1, i * FH + 0.6), mat("winn", "#F0D99A", emit=0.6))


def shot_passenger():
    ground()
    FH, NF = 1.2, 5
    building_cut(NF, FH=FH, m=mat("castiron", "#D9D2C3"))
    for x in (-0.65, 0.65):
        box((0.08, 0.08, NF * FH), (x, 0.4, NF * FH / 2), IRON)
    car_ = cage_box(1.1, 1.0, 1.0, (0, 0.4, 0.12), m=BRASS, bars=5)
    for k in range(2):
        person(-0.2 + 0.4 * k, 0, 0, 0.75, mat(f"pp{k}", ["#6B3A3A", "#2A2A33"][k])).parent = car_
    for o in car_.children:
        if o.type == "MESH" and o.data.materials and o.data.materials[0].name.startswith("pp"):
            o.location = (o.location.x, 0.0, 0.06)
    key(car_, "location", F(0.1), (0, 0.4, 0.12))
    key(car_, "location", F(0.9), (0, 0.4, 3 * FH + 0.12))
    rope = cyl(0.02, NF * FH, (0, 0.4, NF * FH / 2 + 0.6), STEEL, verts=6)
    yr = text3d("1857", (0, -1.8, NF * FH + 0.5), size=0.6, m=mat("yr_p", "#F2C14E", emit=1.2))
    pop_in(yr, 10, 8)
    for x in (-6, 6):
        box((3, 3, 5), (x, 3, 2.5), BRICK)
    camera((3.0, -9.0, 2.0), (0, 0, 2.6), lens=32, moves=[(1.0, (1.5, -8.0, 4.0), (0, 0, 3.4))])


def shot_electric():
    box((400, 400, 0.02), (0, 0, -0.01), mat("floor2", "#8C8C8C"))
    box((30, 0.3, 12), (0, 4, 6), mat("hall2", "#C8D3D9"))
    # motor at the top
    motor = cyl(0.55, 0.9, (0, 0.5, 4.8), COPPER, rot=(0, math.radians(90), 0), verts=24)
    for k in range(6):
        torus(0.56, 0.05, (-0.35 + k * 0.14, 0.5, 4.8), IRON, rot=(0, math.radians(90), 0))
    drum = cyl(0.25, 0.7, (0, 0.5, 4.8), IRON, rot=(0, math.radians(90), 0), verts=12)
    key(drum, "rotation_euler", 1, (0, math.radians(90), 0))
    key(drum, "rotation_euler", N, (math.radians(900), math.radians(90), 0))
    for x in (-0.7, 0.7):
        box((0.1, 0.1, 4.4), (x, 0.5, 2.2), IRON)
    car_ = cage_box(1.2, 1.0, 1.1, (0, 0.5, 0.15), m=mat("car_wood", "#8C6239"), bars=4)
    key(car_, "location", F(0.2), (0, 0.5, 0.15))
    key(car_, "location", F(0.85), (0, 0.5, 2.8))
    cyl(0.02, 3.5, (0, 0.5, 3.0), STEEL, verts=6)
    # sparks along the wires
    curve_tube([(0, 0.5, 5.35), (1.5, 0.6, 5.6), (3.0, 0.8, 3.0), (3.5, 1.0, 0.1)], 0.03, BLACK)
    for i in range(10):
        s = ball(0.08, (1.5, 0.6, 5.6), mat("spark", "#9BE0FF", emit=6.0), seg=8)
        t0 = 6 + i * 12
        if t0 + 12 >= N:
            break
        pop_in(s, t0, 2)
        key(s, "location", t0, (3.5, 0.9, 0.3))
        key(s, "location", t0 + 6, (3.0, 0.8, 3.0))
        key(s, "location", t0 + 12, (0.3, 0.5, 5.35))
        pop_out(s, t0 + 11, 2)
    yr = text3d("1880", (0, -0.4, 6.4), size=0.7, m=mat("yr_el", "#5CD8FF", emit=1.5))
    pop_in(yr, 8, 8)
    camera((3.0, -7.0, 2.4), (0.4, 0.5, 2.9), lens=32, moves=[(1.0, (1.8, -6.0, 3.2), (0.4, 0.5, 3.2))])


def shot_skyscraper():
    m1, m2 = MARKS[1], MARKS[2]
    ground(m=CONCRETE)
    H = 60.0
    W = 6.0
    # tower with a glass skin, cut open toward the camera for the shaft
    box((W, W, H), (0, 3.2, H / 2), GLASS_T)
    for i in range(0, int(H), 3):
        box((W + 0.1, W + 0.1, 0.25), (0, 3.2, i), mat("band", "#DDE3E8"))
    shaft = box((1.6, 0.4, H), (0, -0.05, H / 2), mat("shaft", "#30343A"))
    for x in (-0.6, 0.6):
        box((0.08, 0.1, H), (x, -0.3, H / 2), STEEL)
    cab = applied(box((1.4, 0.5, 1.7), (0, -0.4, 1.0), mat("cabin", "#E9EEF2", rough=0.3, metal=0.4)))
    glow = box((1.3, 0.05, 1.5), (0, -0.66, 1.0), mat("cab_glow", "#5CD8FF", emit=3.0))
    glow.parent = cab
    glow.location = (0, -0.26, 0)
    rnd = random.Random(3)
    for i in range(18):
        x = rnd.choice([-1, 1]) * rnd.uniform(6, 24)
        y = rnd.uniform(3, 30)
        h = rnd.uniform(6, 26)
        box((4, 4, h), (x, y, h / 2), mat(f"cb{i%4}", ["#9AA8B5", "#B7C0C8", "#7F8E9C", "#C9CFD4"][i % 4]))
    # slow ride, then a fast one after "seventy kilometers"
    key(cab, "location", 1, (0, -0.4, 1.0))
    key(cab, "location", m1, (0, -0.4, 8.0))
    key(cab, "location", m2, (0, -0.4, 14.0))
    key(cab, "location", N, (0, -0.4, 54.0))
    speed = text3d("70 KM/H", (0, -3.0, 40), size=2.8, m=mat("sp_t", "#5CD8FF", emit=1.5))
    pop_in(speed, m2 + 20, 8)
    camera((6, -22, 4), (0, 0, 10), lens=30, moves=[(m1 / N, (5, -24, 8), (0, 0, 14)), (m2 / N, (4, -30, 18), (0, 0, 24)), (1.0, (3, -34, 36), (0, 0, 42))])
