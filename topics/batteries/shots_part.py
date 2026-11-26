
# ---------------------------------------------------------------- battery shots
ZINC = mat("zinc", "#B9BEC4", rough=0.35, metal=0.8)
CLOTH = mat("cloth", "#D9C9A3", noise=("#C2B184", 10))
LEAD = mat("lead", "#6E737A", rough=0.5, metal=0.6)
ACID = mat("acid", "#BFE58A", rough=0.1, alpha=0.35)
SPARK = mat("spark", "#9BE0FF", emit=8.0)
ION = mat("ion", "#5CD8FF", emit=4.0)
GLOW_Y = mat("glow_y", "#FFE9A0", emit=6.0, alpha=0.25)
DESK = mat("desk", "#7A5A3C", noise=("#664A30", 6))
CHARGE = mat("charge", "#3BE37A", emit=3.0)


def lab(color="#C9B99A"):
    box((400, 400, 0.02), (0, 0, -0.01), DESK)
    box((40, 0.3, 14), (0, 3.0, 7), mat("labwall", color))


def flicker_spark(loc, f0, f1, every=10, s=0.12):
    sp = ball(s, loc, SPARK, seg=8)
    key(sp, "scale", 1, (0, 0, 0))
    for f in range(f0, f1, every):
        key(sp, "scale", f, (0, 0, 0))
        key(sp, "scale", f + 2, (1.3, 1.3, 1.3))
        key(sp, "scale", f + 5, (0, 0, 0))
    return sp


def shot_pile():
    m2 = MARKS[2]
    lab()
    base = cyl(0.9, 0.15, (0, 0.5, 0.075), DARK_WOOD, verts=32)
    for sx in (-1, 1):
        cyl(0.04, 3.4, (sx * 0.75, 0.5, 1.8), GLASS, verts=8)
    z = 0.2
    k = 0
    for i in range(10):
        for m, h in ((COPPER, 0.07), (ZINC, 0.07), (CLOTH, 0.05)):
            d = cyl(0.55, h, (0, 0.5, z + h / 2), m, verts=32)
            pop_in(d, 4 + k * 3, 4)
            z += h + 0.005
            k += 1
    cyl(0.9, 0.12, (0, 0.5, z + 0.06), DARK_WOOD, verts=32)
    w1 = curve_tube([(0.55, 0.5, z - 0.05), (1.4, 0.3, z + 0.4), (1.6, -0.2, 1.4)], 0.025, COPPER)
    w2 = curve_tube([(0.55, 0.5, 0.25), (1.4, 0.3, 0.3), (1.6, -0.2, 1.25)], 0.025, COPPER)
    flicker_spark((1.6, -0.2, 1.33), m2 + 20, N, 12)
    yr = text3d("1800", (0, 0, z + 0.9), size=0.55, m=mat("yr_v", "#F2C14E", emit=1.2))
    pop_in(yr, m2 + 4, 8)
    camera((1.6, -5.0, 1.6), (0.2, 0.5, 1.4), lens=32, moves=[(m2 / N, (1.2, -4.6, 1.8), (0.3, 0.5, 1.5)), (1.0, (2.2, -3.8, 1.6), (0.8, 0.3, 1.4))])


def car_battery(loc, s=1.0):
    x, y, z = loc
    parts = [box((1.6 * s, 0.9 * s, 0.9 * s), (x, y, z + 0.45 * s), mat("bat_case", "#1C1D21", rough=0.4), bevel=0.04),
             box((1.62 * s, 0.92 * s, 0.12 * s), (x, y, z + 0.86 * s), mat("bat_lid", "#2B2D33"), bevel=0.02),
             cyl(0.08 * s, 0.14 * s, (x - 0.5 * s, y, z + 0.98 * s), mat("term_r", "#CC3333"), verts=12),
             cyl(0.08 * s, 0.14 * s, (x + 0.5 * s, y, z + 0.98 * s), BLACK, verts=12)]
    return parts


def shot_leadacid():
    lab("#BFC7C9")
    tank = box((2.2, 1.0, 1.4), (-0.8, 0.5, 0.72), GLASS)
    liquid = box((2.1, 0.92, 1.1), (-0.8, 0.5, 0.6), ACID)
    for i in range(7):
        pl = box((0.06, 0.8, 1.2), (-1.65 + i * 0.28, 0.5, 0.75), LEAD if i % 2 else mat("leadox", "#7A4A36", rough=0.6))
    for i in range(20):
        b = ball(0.03, (0, 0, 0), mat("bubble", "#FFFFFF", alpha=0.6), seg=6)
        x = -1.6 + (i % 7) * 0.28 + 0.14
        t0 = 2 + i * 9
        if t0 + 30 >= N:
            break
        pop_in(b, t0, 2)
        key(b, "location", t0, (x, 0.2, 0.2))
        key(b, "location", t0 + 30, (x, 0.2, 1.1))
        pop_out(b, t0 + 28, 2)
    for x in (-1.5, -0.1):
        cyl(0.05, 0.4, (x, 0.5, 1.6), LEAD, verts=8)
    yr = text3d("1859", (-0.8, 0.0, 2.3), size=0.55, m=mat("yr_l", "#F2C14E", emit=1.2))
    pop_in(yr, 6, 8)
    cb = car_battery((1.6, 0.5, 0.0), 0.9)
    t0 = int(N * 0.6)
    for p in cb:
        pop_in(p, t0, 8)
    # a little car outline behind the battery
    car = box((3.4, 1.4, 0.8), (2.4, 2.0, 0.6), mat("car_s", "#3A6EA5", rough=0.3, metal=0.3), bevel=0.1)
    pop_in(car, t0 + 6, 8)
    camera((0.0, -5.2, 2.0), (-0.4, 0.5, 1.0), lens=32, moves=[(0.55, (-0.2, -4.8, 2.0), (-0.6, 0.5, 1.0)), (1.0, (1.2, -5.2, 2.2), (1.0, 0.8, 0.9))])


def cell(loc, r=0.25, h=0.9, body="#1C1D21", band="#C9A23B", cut=False):
    x, y, z = loc
    ps = [cyl(r, h, (x, y, z + h / 2), mat("cell_" + body, body, rough=0.3), verts=24),
          cyl(r * 1.01, h * 0.35, (x, y, z + h * 0.82), mat("band_" + band, band, rough=0.3, metal=0.6), verts=24),
          cyl(r * 0.35, 0.06, (x, y, z + h + 0.03), STEEL, verts=16)]
    return ps


def shot_drycell():
    m1 = MARKS[1]
    lab("#C9C2B4")
    # big cut-open dry cell: zinc can, black paste, carbon rod
    can = cyl(0.6, 1.8, (-0.9, 0.6, 0.9), ZINC, verts=32)
    cutter = box((1.4, 1.4, 2.0), (-0.9, -0.05, 0.9))
    cut(can, cutter)
    paste = cyl(0.56, 1.7, (-0.9, 0.65, 0.88), mat("paste", "#2B2B2E"), verts=32)
    cut(paste, box((1.4, 1.4, 2.0), (-0.9, -0.1, 0.9)))
    rod = cyl(0.09, 1.95, (-0.9, 0.6, 0.97), mat("carbon_r", "#1A1A1A", rough=0.4), verts=16)
    cyl(0.12, 0.08, (-0.9, 0.6, 1.98), BRASS, verts=16)
    # flashlight with a beam
    fl = cyl(0.18, 1.0, (1.2, 0.4, 0.25), mat("torch", "#B8322B", rough=0.3, metal=0.3), rot=(0, math.radians(90), 0), verts=20)
    cyl(0.24, 0.25, (1.8, 0.4, 0.25), CHROME, rot=(0, math.radians(90), 0), verts=20)
    beam_ = cyl(0.25, 3.0, (3.4, 0.4, 0.25), GLOW_Y, rot=(0, math.radians(90), 0), r2=1.2, verts=24)
    key(beam_, "scale", 1, (0, 0, 0))
    key(beam_, "scale", 30, (0, 0, 0))
    key(beam_, "scale", 34, (1, 1, 1))
    # alkaline cells for the second line
    for i in range(6):
        for p in cell((-1.6 + i * 0.55, -0.4, 0.0), 0.22, 0.85):
            pop_in(p, m1 + 4 + i * 4, 6)
    rem = box((0.5, 1.4, 0.15), (2.2, -0.6, 0.08), mat("remote", "#2B2D33"), bevel=0.05)
    pop_in(rem, m1 + 30, 8)
    for k in range(6):
        b = cyl(0.07, 0.04, (2.2 - 0.1 + (k % 2) * 0.2, -0.9 + (k // 2) * 0.25, 0.17), mat("rbtn", "#9AA3AD"), verts=10)
        pop_in(b, m1 + 34, 6)
    camera((1.0, -5.8, 2.2), (0.5, 0.5, 0.9), lens=30, moves=[(m1 / N, (0.6, -5.2, 2.2), (0.4, 0.4, 0.9)), (1.0, (0.4, -4.4, 2.6), (0.2, -0.3, 0.4))])


def shot_lithium():
    lab("#B7C0C8")
    # stacked layers of a pouch cell, exploded
    cols = [("#C8743A", "anode_cu"), ("#2B2B2E", "graphite"), ("#E8E8E8", "separator"), ("#5A6E8C", "cathode"), ("#B9BEC4", "alum")]
    z = 0.4
    for rep in range(2):
        for c, n in cols:
            l = box((2.6, 1.6, 0.06), (0, 0.6, z), mat(n, c, rough=0.4), bevel=0.01)
            key(l, "location", 1, (0, 0.6, z + 1.0 + rep * 0.6))
            key(l, "location", 20, (0, 0.6, z + 1.0 + rep * 0.6))
            key(l, "location", 60, (0, 0.6, z))
            z += 0.18
    # ions shuttling between layers
    rnd = random.Random(4)
    for i in range(30):
        b = ball(0.05, (0, 0, 0), ION, seg=8)
        x = rnd.uniform(-1.1, 1.1)
        t0 = 60 + (i % 10) * 6
        pop_in(b, t0, 3)
        key(b, "location", t0, (x, -0.25, 0.55 + 0.18 * (i % 3)))
        key(b, "location", min(N, t0 + 30), (x + 0.2, -0.25, 0.9 + 0.18 * (i % 3)))
    yr = text3d("1991", (0, 0, 2.8), size=0.55, m=mat("yr_li", "#F2C14E", emit=1.2))
    pop_in(yr, 8, 8)
    camera((1.6, -5.0, 2.6), (0, 0.6, 1.0), lens=32, moves=[(1.0, (0.8, -4.2, 2.2), (0, 0.6, 1.0))])


def shot_ev():
    m1 = MARKS[1]
    ground(m=CONCRETE)
    # car body (semi-transparent) with a glowing battery floor
    bpy.ops.object.empty_add(location=(0, 1, 0))
    car = bpy.context.object
    parts = [box((4.2, 1.9, 0.7), (0, 1, 0.75), mat("ev_body", "#E9EEF2", rough=0.25, metal=0.3, alpha=0.55), bevel=0.15),
             box((2.4, 1.7, 0.55), (-0.2, 1, 1.35), mat("ev_glass", "#2B3440", rough=0.1, alpha=0.6), bevel=0.12)]
    CG = mat("cellg", "#3BE37A", emit=0.0)
    for i in range(10):
        for j in range(4):
            c = box((0.3, 0.36, 0.12), (-1.5 + i * 0.33, 0.35 + j * 0.43, 0.42), CG)
            parts.append(c)
    glow_ramp(CG, 10, 40, 3.0)
    for sx in (-1.4, 1.4):
        for sy in (0.0, 2.0):
            parts.append(cyl(0.38, 0.25, (sx, sy, 0.38), BLACK, rot=(math.radians(90), 0, 0), verts=20))
    for p in parts:
        p.parent = car
        p.location = p.location - car.location
    key(car, "location", 1, (-1.5, 1.5, 0))
    key(car, "location", m1, (0.0, 1.5, 0))
    key(car, "location", N, (2.0, 1.5, 0))
    # phone and laptop pop up beside
    ph = applied(box((0.45, 0.06, 0.9), (-1.5, -1.6, 1.0), mat("phone", "#1C1D21", rough=0.2)))
    scr = box((0.38, 0.02, 0.78), (0, -0.04, 0), mat("phscr", "#5CD8FF", emit=1.5))
    scr.parent = ph
    pop_in(ph, 20, 8)
    lt = box((1.4, 0.9, 0.05), (1.5, -1.6, 0.6), mat("laptop", "#B7C0C8", rough=0.3, metal=0.5))
    sc = box((1.4, 0.05, 0.9), (1.5, -1.15, 1.05), mat("lscr", "#5CD8FF", emit=1.2))
    pop_in(lt, 40, 8)
    pop_in(sc, 44, 8)
    pc = text3d("100%", (0, -1.0, 2.6), size=0.55, m=CHARGE)
    pop_in(pc, 60, 8)
    camera((0.3, -7.5, 2.4), (0, 0.5, 1.0), lens=30, moves=[(1.0, (1.0, -8.2, 2.8), (0.8, 0.5, 1.0))])
