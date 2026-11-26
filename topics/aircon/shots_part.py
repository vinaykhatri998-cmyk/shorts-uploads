
# ---------------------------------------------------------------- air conditioning shots
HOT = mat("hot", "#FF7A3D", emit=2.5, alpha=0.85)
COOL = mat("cool", "#5CD8FF", emit=2.5, alpha=0.85)
REED = mat("reed", "#7E8C4A", noise=("#5E6B35", 8))
ICE = mat("ice", "#CFEFFF", rough=0.1, alpha=0.75, spec=0.8)
WHITE_P = mat("white_p", "#F2F4F5", rough=0.35)
GRILLE = mat("grille", "#4A4F57", rough=0.4, metal=0.5)


def heat_waves(x, y, z0, n=6, w=3.0):
    for i in range(n):
        p = applied(box((w, 0.02, 0.06), (x, y, z0), mat("wave", "#FFB27A", emit=1.0, alpha=0.35)))
        t0 = 1 + i * 18
        for k in range(0, N, 30):
            pass
        key(p, "location", 1, (x, y, z0 + i * 0.4))
        key(p, "location", N, (x, y, z0 + i * 0.4 + 2.5))


def shot_heat():
    ground()
    sun_obj().data.energy = 5.0
    sb = ball(2.0, (-9, 40, 16), mat("sunb", "#FFD66B", emit=6.0), seg=24)
    house((0, 2), 2.2, "#E9D7B6")
    for x, y in ((-6, 8), (6, 9), (-3, 14)):
        house((x, y), 1.5, "#E2CCA4")
    # thermometer
    cyl(0.18, 3.2, (1.9, -1.5, 1.8), GLASS, verts=16)
    ball(0.3, (1.9, -1.5, 0.25), mat("red", "#E2412E", emit=1.0), seg=16)
    bar = applied(box((0.16, 0.16, 1.0), (1.9, -1.5, 0.3), mat("red2", "#E2412E", emit=1.0)))
    key(bar, "scale", 1, (1, 1, 0.3))
    key(bar, "location", 1, (1.9, -1.5, 0.4))
    key(bar, "scale", MARKS[1], (1, 1, 2.9))
    key(bar, "location", MARKS[1], (1.9, -1.5, 1.7))
    t = text3d("45°C", (1.9, -1.6, 3.8), size=0.55, m=mat("deg", "#FF7A3D", emit=1.5))
    pop_in(t, 30, 8)
    camera((0.5, -8.0, 2.2), (0.6, 0, 2.0), lens=30, moves=[(1.0, (1.2, -6.8, 2.0), (0.9, 0, 2.0))])


def window_wall(y=0.0, W=8, H=4, win=(1.6, 1.6), wz=1.8, m=None):
    m = m or mat("mudwall", "#C9A97A", noise=("#B89466", 4))
    ww, wh = win
    box(((W - ww) / 2, 0.4, H), (-(W + ww) / 4, y, H / 2), m)
    box(((W - ww) / 2, 0.4, H), ((W + ww) / 4, y, H / 2), m)
    box((ww, 0.4, wz - wh / 2), (0, y, (wz - wh / 2) / 2), m)
    box((ww, 0.4, H - wz - wh / 2), (0, y, (H + wz + wh / 2) / 2), m)


def shot_reeds():
    ground()
    sun_obj().data.energy = 4.5
    # wall seen from inside the room (camera inside, looking out through the window)
    window_wall(y=2.0, W=10, H=4)
    box((10, 8, 0.1), (0, -2, 4.05), mat("ceil", "#B89466"))
    for sx in (-1, 1):
        box((0.3, 8, 4), (sx * 5, -2, 2), mat("mudwall2", "#BFA070"))
    for i in range(14):
        x = -0.75 + i * 0.115
        cyl(0.045, 1.7, (x, 1.75, 1.8), REED, verts=6)
    rnd = random.Random(1)
    for i in range(16):
        d = ball(0.035, (0, 0, 0), mat("drop", "#7FC2EA", emit=0.6), seg=6, squash=1.4)
        x = rnd.uniform(-0.7, 0.7)
        t0 = 4 + i * 10
        if t0 + 12 >= N:
            break
        pop_in(d, t0, 2)
        key(d, "location", t0, (x, 1.7, 1.0))
        key(d, "location", t0 + 12, (x, 1.7, 0.1))
        pop_out(d, t0 + 10, 2)
    for k in range(5):
        y0 = 5.0
        x = -0.6 + k * 0.3
        stream([(x, y0, 1.9 + 0.1 * k), (x, 2.4, 1.85)], 30, HOT, t0=1 + k * 2, every=10, travel=18, r=0.06)
        stream([(x, 1.5, 1.85), (x * 1.6, -2.5, 1.3 + 0.1 * k)], 30, COOL, t0=12 + k * 2, every=10, travel=22, r=0.06)
    for x in (-2.5, 2.5):
        person(x, -1.5, 0, 1.0, mat("linen", "#E9E1CF"))
    camera((0.5, -5.0, 1.6), (0, 2, 1.8), lens=28, moves=[(1.0, (0.2, -3.6, 1.6), (0, 2, 1.8))])


def shot_windcatcher():
    section(front=-1.0, half_w=12)
    M = mat("adobe", "#D9B88A", noise=("#C7A576", 4))
    # building, cut open toward the camera: back wall, roof, tower
    box((6, 0.3, 3.0), (0, 2.0, 1.5), M)
    for sx in (-1, 1):
        box((0.3, 3.0, 3.0), (sx * 3, 0.5, 1.5), M)
    box((6.3, 3.0, 0.3), (0, 0.5, 3.15), M)
    box((1.4, 1.4, 4.0), (2.2, 0.8, 5.3), M)
    for sx in (-1, 1):
        box((0.1, 1.42, 0.9), (2.2 + sx * 0.66, 0.8, 6.6), mat("slot", "#3A2E22"))
    # shaft down to a channel of water, then into the room
    box((1.0, 0.1, 3.4), (2.2, 1.8, 3.0), mat("shaftd", "#4A3B2C"))
    box((1.0, 0.1, 2.9), (2.2, -1.05, -1.45), mat("shaftd", "#4A3B2C"))
    box((5.4, 0.1, 0.7), (0, -1.05, -3.1), mat("qanat", "#2B6C9A", emit=0.3))
    box((1.0, 0.1, 2.9), (-2.2, -1.05, -1.45), mat("shaftd", "#4A3B2C"))
    path = [(6.5, 1.0, 6.6), (2.2, 1.0, 6.6), (2.2, 1.6, 3.0), (2.2, -1.2, -0.2), (2.2, -1.2, -2.8), (0.0, -1.2, -3.1),
            (-2.2, -1.2, -2.8), (-2.2, -1.2, -0.2), (-1.0, 0.0, 1.2), (1.0, 0.5, 1.4)]
    for i in range(18):
        s = 1 + i * 8
        if s + 40 >= N:
            break
        hot = ball(0.2, path[0], HOT, seg=8)
        cool = ball(0.2, path[0], COOL, seg=8)
        for q, p in enumerate(path):
            f = s + round(q * 40 / (len(path) - 1))
            key(hot, "location", f, p)
            key(cool, "location", f, p)
        # orange until it passes the water, then blue
        key(hot, "scale", 1, (0, 0, 0))
        key(hot, "scale", s, (1, 1, 1))
        key(hot, "scale", s + 20, (1, 1, 1))
        key(hot, "scale", s + 22, (0, 0, 0))
        key(cool, "scale", 1, (0, 0, 0))
        key(cool, "scale", s + 20, (0, 0, 0))
        key(cool, "scale", s + 22, (1, 1, 1))
        key(cool, "scale", s + 38, (1, 1, 1))
        key(cool, "scale", s + 41, (0, 0, 0))
    person(-0.5, 0.6, 0.02, 1.0, mat("robe", "#7A3E2E"))
    camera((1.2, -14.0, 1.2), (0.5, 0, 1.0), lens=26, moves=[(1.0, (0.2, -12.5, 0.8), (0.5, 0, 0.8))])


def shot_ice():
    box((400, 400, 0.02), (0, 0, -0.01), mat("snow", "#EEF3F6", rough=0.6))
    box((14, 14, 0.04), (0, 4, 0.01), mat("lake", "#B7DDF0", rough=0.1, spec=0.8))
    for x, y in ((-9, 14), (9, 16), (-12, 6), (11, 6)):
        cyl(1.2, 3.0, (x, y, 1.5), mat("pine", "#3E6B4A"), r2=0.0, verts=8)
        cyl(0.2, 0.6, (x, y, 0.3), LOG, verts=6)
    sled = applied(box((2.6, 1.4, 0.2), (0, 0, 0), DARK_WOOD))
    sled.location = (-2.0, -0.5, 0.25)
    blocks = []
    for k in range(6):
        b = applied(box((0.7, 0.7, 0.55), (0, 0, 0), ICE))
        b.parent = sled
        b.location = (-0.85 + (k % 3) * 0.8, 0.0, 0.4 + (k // 3) * 0.58)
        pop_in(b, 8 + k * 12, 6)
    for k in range(5):
        b = box((0.7, 0.7, 0.55), (1.5 + k * 0.85, 3.0, 0.3), ICE)
    for x in (2.5, 3.6):
        person(x, 2.2, 0, 1.0, mat("coat", "#6B2E2E"))
    saw = applied(box((0.05, 0.6, 1.0), (0, 0, 0), STEEL))
    for f in range(1, N, 8):
        key(saw, "location", f, (3.0, 2.8, 0.7 if (f // 8) % 2 else 0.4))
    key(sled, "location", int(N * 0.7), (-2.0, -0.5, 0.25))
    key(sled, "location", N, (-7.0, -0.5, 0.25))
    ship = applied(box((8, 2, 1.4), (0, 0, 0), mat("hull", "#3A3A44")))
    ship.location = (-12, 12, 0.7)
    cyl(0.12, 5, (-12, 12, 3.8), DARK_WOOD, verts=8)
    camera((2.0, -7.5, 3.0), (0, 1.0, 0.8), lens=30, moves=[(1.0, (-1.5, -6.5, 2.8), (-1.5, 1.5, 0.8))])


def shot_carrier():
    box((400, 400, 0.02), (0, 0, -0.01), mat("factory_floor", "#6E6A62"))
    box((40, 0.3, 14), (0, 5, 7), BRICK if "BRICK" in globals() else mat("brick", "#B5654A", noise=("#9A5039", 6)))
    # the machine: housing, coils, fan, pipes
    box((3.0, 1.8, 2.4), (-1.5, 1.5, 1.2), mat("machine", "#4F6A5A", rough=0.5, metal=0.4), bevel=0.05)
    for k in range(8):
        torus(0.55, 0.06, (1.0, 1.5, 0.5 + k * 0.22), COPPER)
    box((1.6, 1.6, 0.2), (1.0, 1.5, 0.3), IRON)
    fan = cyl(0.8, 0.1, (-1.5, 0.55, 1.4), GRILLE, rot=(math.radians(90), 0, 0), verts=24)
    bpy.ops.object.empty_add(location=(-1.5, 0.5, 1.4))
    rot = bpy.context.object
    for k in range(4):
        bl = applied(box((0.18, 0.04, 0.65), (0, 0, 0), STEEL))
        bl.parent = rot
        a = k * math.pi / 2
        bl.location = (0.35 * math.sin(a), 0, 0.35 * math.cos(a))
        bl.rotation_euler = (0, a, 0)
    spin(rot, 1, 12)
    curve_tube([(0.2, 1.5, 2.3), (1.0, 1.5, 3.0), (1.0, 1.5, 2.2)], 0.08, COPPER)
    curve_tube([(-3.0, 1.5, 2.0), (-3.8, 1.5, 3.5), (-6.0, 2.0, 3.5)], 0.12, PIPE)
    # printing press rollers and paper
    for k in range(3):
        r = cyl(0.35, 2.0, (4.5, 1.0 + k * 0.0, 0.6 + k * 0.72), IRON, rot=(math.radians(90), 0, 0), verts=24)
        spin(r, 1, 3 * (1 if k % 2 else -1), base=(math.radians(90), 0, 0))
    box((2.0, 1.8, 0.02), (6.2, 1.0, 1.05), mat("paper", "#F4F1E8"))
    stream([(-1.5, 0.4, 1.4), (-1.0, -1.5, 1.4), (2.5, -1.5, 1.3), (5.0, -0.5, 1.4)], 30, COOL, t0=4, every=6, travel=30, r=0.09)
    yr = text3d("1902", (0.5, -0.5, 4.4), size=0.8, m=mat("yr_a", "#F2C14E", emit=1.2))
    pop_in(yr, 10, 8)
    camera((2.5, -8.0, 3.0), (1.0, 1.0, 1.8), lens=30, moves=[(1.0, (0.0, -7.0, 2.6), (1.0, 1.0, 1.8))])


def ac_unit(loc, w=1.2, d=0.9, h=0.7, m=None):
    x, y, z = loc
    u = box((w, d, h), loc, m or mat("unit", "#D9D4C8", rough=0.4), bevel=0.04)
    for k in range(6):
        box((w * 0.9, 0.02, 0.03), (x, y - d / 2 - 0.01, z - h * 0.35 + k * h * 0.14), GRILLE)
    return u


def shot_window():
    ground(m=GRASS)
    W = mat("siding", "#9FC3D6")
    window_wall(y=0.0, W=12, H=5, win=(1.4, 1.0), wz=2.2, m=W)
    prism(12.5, 6, 2.0, (0, 2.8, 5.0), mat("roof_w", "#7A3E2E"))
    for sx in (-1, 1):
        box((0.3, 6, 5), (sx * 6, 2.8, 2.5), W)
    ac_unit((0, -0.15, 2.05), 1.35, 1.0, 0.7)
    for x in (-3.5, 3.5):
        box((1.2, 0.1, 1.2), (x, -0.22, 2.6), mat("glassw", "#BFE2F2", rough=0.1))
    stream([(0, 0.4, 2.1), (-0.5, 2.5, 1.8), (-1.5, 4.0, 1.5)], 20, COOL, t0=4, every=6, travel=24, r=0.07)
    stream([(0, -0.7, 2.0), (0.3, -2.0, 2.4), (0.6, -3.0, 3.2)], 20, HOT, t0=4, every=6, travel=20, r=0.07)
    camera((3.0, -7.5, 2.0), (0, 0, 2.2), lens=30, moves=[(1.0, (1.5, -5.5, 2.3), (0, 0, 2.1))])


def shot_split():
    m1 = MARKS[1]
    ground(m=GRASS)
    W = mat("modern", "#E8E6E1")
    # room cut open toward the camera
    box((7, 0.3, 3.4), (0, 2.5, 1.7), W)
    box((0.3, 5, 3.4), (3.5, 0.0, 1.7), W)
    box((7, 5, 0.12), (0, 0, 0.06), mat("wood_floor", "#B08A5E", noise=("#9A7650", 6)))
    indoor = box((1.8, 0.4, 0.5), (0, 2.15, 2.8), WHITE_P, bevel=0.08)
    box((1.6, 0.05, 0.06), (0, 1.94, 2.6), mat("led_s", "#5CD8FF", emit=3.0))
    out = box((1.4, 0.6, 1.0), (5.0, 0.5, 0.5), WHITE_P, bevel=0.04)
    fan = cyl(0.38, 0.04, (5.0, 0.18, 0.55), GRILLE, rot=(math.radians(90), 0, 0), verts=24)
    bpy.ops.object.empty_add(location=(5.0, 0.15, 0.55))
    rot = bpy.context.object
    for k in range(3):
        bl = applied(box((0.12, 0.02, 0.32), (0, 0, 0), STEEL))
        bl.parent = rot
        a = k * math.tau / 3
        bl.location = (0.17 * math.sin(a), 0, 0.17 * math.cos(a))
        bl.rotation_euler = (0, a, 0)
    spin(rot, 1, 25)
    curve_tube([(0.9, 2.2, 2.8), (3.4, 2.2, 2.8), (3.8, 1.5, 1.5), (4.3, 0.5, 0.6)], 0.05, COPPER)
    stream([(0, 1.9, 2.55), (0, 0.5, 1.9), (0.5, -1.5, 1.2)], 26, COOL, t0=4, every=6, travel=26, r=0.1)
    stream([(0.5, 0.5, 1.2), (1.8, 2.0, 2.6), (3.6, 2.2, 2.8), (4.4, 0.6, 0.8), (5.0, -1.0, 1.0), (5.5, -2.5, 2.0)], 26, HOT, t0=10, every=6, travel=36, r=0.1)
    sofa = box((2.2, 0.9, 0.5), (-1.2, 1.4, 0.35), mat("sofa", "#3A6EA5"), bevel=0.08)
    person(-1.2, 1.2, 0.55, 0.9)
    camera((1.5, -7.5, 2.6), (1.5, 0.8, 1.6), lens=28, moves=[(m1 / N, (2.5, -6.5, 2.4), None), (1.0, (2.0, -9.5, 3.4), (1.8, 0.8, 1.6))])
