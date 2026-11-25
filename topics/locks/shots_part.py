# ---------------------------------------------------------------- lock shots
BRASS = mat("brass", "#D4A845", rough=0.3, metal=0.9)
BRASS_DK = mat("brass_dk", "#A47E2C", rough=0.4, metal=0.8)
STEEL = mat("steel", "#C9CED3", rough=0.25, metal=1.0)
IRON = mat("iron", "#4A4A4E", rough=0.5, metal=0.7)
COPPER = mat("copper", "#C8743A", rough=0.3, metal=0.9)
GOLD = mat("gold", "#F2C14E", rough=0.2, metal=1.0)
DARK_WOOD = mat("dark_wood", "#6B4426", noise=("#563519", 6))
SANDSTONE = mat("sandstone", "#D9C08F", noise=("#C7AB78", 4))
VELVET = mat("velvet", "#7A1E2E", rough=0.9)
SPRING = mat("spring", "#9EA4AA", rough=0.3, metal=1.0)
GLOW_GREEN = mat("glow_green", "#3BE37A", emit=4.0)
GLOW_RED = mat("glow_red", "#FF4D4D", emit=3.0)
SCREEN = mat("screen", "#5CC8FF", emit=2.5)
BLACK = mat("black", "#1C1D21", rough=0.3)
SHEAR = mat("shear", "#FFD23F", emit=3.0)


def text3d(s, loc, size=0.6, m=None, rot=(math.radians(90), 0, 0), extrude=0.04):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.data.body = s
    o.data.size = size
    o.data.extrude = extrude
    o.data.align_x = "CENTER"
    o.data.align_y = "CENTER"
    o.data.materials.append(m or GOLD)
    return o


def hinge_door(x_hinge, y, w, h, m, open_frame=None, close_frame=None, angle=-100):
    """Door panel rotating about a vertical hinge at x_hinge (opens toward the camera)."""
    bpy.ops.object.empty_add(location=(x_hinge, y, 0))
    piv = bpy.context.object
    d = box((w, 0.12, h), (x_hinge + w / 2, y, h / 2), m, bevel=0.02)
    knob = ball(0.07, (x_hinge + w - 0.15, y - 0.1, h * 0.48), BRASS)
    for o in (d, knob):
        o.parent = piv
        o.location.x -= x_hinge
    if open_frame is not None:
        key(piv, "rotation_euler", 1, (0, 0, 0))
        key(piv, "rotation_euler", open_frame, (0, 0, 0))
        key(piv, "rotation_euler", open_frame + 18, (0, 0, math.radians(angle)))
    return piv


def shot_open_door():
    ground()
    x0, y0 = 0, 3
    body = box((3.4, 2.6, 2.6), (x0, y0, 1.3), mat("wall_h", "#E3D2B4", noise=("#D3BF9D", 4)), bevel=0.03)
    cut(body, box((1.0, 1, 1.9), (x0, y0 - 1.3, 0.95)))
    box((0.98, 0.1, 1.88), (x0, y0 - 1.15, 0.95), mat("dark_in", "#2A2018"))
    prism(3.8, 3.0, 1.3, (x0, y0, 2.6), STRAW)
    hinge_door(x0 - 0.5, y0 - 1.32, 1.0, 1.9, DARK_WOOD, open_frame=F(0.18), angle=-105)
    for x in (-4.5, 4.2):
        hut((x, 9), 0.9)
    scatter_rocks(24, (-5, 5), (-2, 10), seed=11)
    camera((1.2, -6.5, 2.2), (0, 3, 1.2), lens=32, moves=[(1.0, (0.4, -3.6, 1.6), (0, 3, 1.1))])


def shot_bar():
    # inside the house, looking at the door
    wall = box((8, 0.3, 5), (0, 1.2, 2.5), mat("wall_in", "#CDB894", noise=("#BBA47F", 4)))
    cut(wall, box((1.42, 1, 2.42), (0, 1.2, 1.2)))
    box((30, 30, 0.05), (0, 16, -0.02), SAND)                        # outside, seen through the doorway
    box((8, 6, 0.1), (0, -1.5, -0.05), mat("floor_in", "#9C7A55", noise=("#86664A", 5)))
    door = hinge_door(-0.7, 1.0, 1.4, 2.4, DARK_WOOD)
    for x in (-1.05, 1.05):
        box((0.22, 0.35, 0.35), (x, 0.82, 1.3), WOOD, bevel=0.02)
    bar = box((2.6, 0.18, 0.2), (0, 0.78, 3.4), mat("bar", "#8A5A2B", noise=("#70461F", 7)), bevel=0.02)
    drop, lift = F(0.08), F(0.55)
    key(bar, "location", 1, (0, 0.78, 3.4))
    key(bar, "location", drop, (0, 0.78, 3.4))
    key(bar, "location", drop + 10, (0, 0.78, 1.45))
    key(bar, "location", lift, (0, 0.78, 1.45))
    key(bar, "location", lift + 12, (-2.6, 0.2, 1.8))
    key(bar, "rotation_euler", lift, (0, 0, 0))
    key(bar, "rotation_euler", lift + 12, (0, math.radians(70), 0.4))
    key(door, "rotation_euler", 1, (0, 0, 0))
    key(door, "rotation_euler", lift + 10, (0, 0, 0))
    key(door, "rotation_euler", lift + 28, (0, 0, math.radians(-95)))
    # outside light through the open door
    bpy.ops.object.light_add(type="AREA", location=(0, 2.2, 1.4), rotation=(math.radians(-90), 0, 0))
    bpy.context.object.data.energy = 120
    bpy.context.object.data.size = 1.2
    bpy.context.object.data.color = (1.0, 0.92, 0.8)
    ball(0.35, (2.3, 0.4, 0.2), STONE, seg=10, squash=0.7)
    camera((0.5, -3.6, 1.7), (0, 1.0, 1.5), lens=30, moves=[(1.0, (0.2, -3.0, 1.6), None)])


def shot_egypt():
    m2 = MARKS[1] if len(MARKS) > 1 else int(N * 0.7)
    box((10, 0.3, 8), (0, 1.0, 2.5), SANDSTONE)                 # wall behind
    box((10, 6, 0.1), (0, -1.5, -0.6), mat("floor_e", "#C9A97A", noise=("#B89466", 4)))
    W = WOOD
    housing = box((2.6, 0.6, 0.9), (0, 0.3, 2.35), mat("housing", "#A87648", noise=("#8E5F36", 6)), bevel=0.03)
    bolt = box((5.2, 0.6, 0.55), (0, 0.3, 1.55), W, bevel=0.03)
    pins = [box((0.28, 0.4, 0.75), (x, 0.0, 2.35), mat(f"pin{i}", "#E0B070"), bevel=0.02) for i, x in enumerate((-0.8, 0, 0.8))]
    # key: long bar with three pegs, made of two halves so it can crack
    bpy.ops.object.empty_add(location=(4.2, 0.0, 1.2))
    k = bpy.context.object
    halves = []
    for side in (-1, 1):
        bpy.ops.object.empty_add(location=(4.2 + side * 0.9, 0.0, 1.2))
        h = bpy.context.object
        h.parent = k
        h.location = (side * 0.9, 0, 0)
        b = box((1.8, 0.35, 0.22), (0, 0, 0), mat("key_wood", "#C08A50", noise=("#A6723D", 6)), bevel=0.02)
        b.parent = h
        halves.append(h)
    for x in (-0.8, 0, 0.8):
        side = 0 if x < 0 else 1
        p = box((0.22, 0.3, 0.3), (0, 0, 0), mat("key_wood", "#C08A50"), bevel=0.02)
        p.parent = halves[side]
        p.location = (x - (-0.9 if side == 0 else 0.9), 0, 0.26)
    handle = box((0.35, 0.35, 1.2), (0, 0, 0), mat("key_wood", "#C08A50"), bevel=0.03)
    handle.parent = halves[1]
    handle.location = (1.0, 0, -0.45)
    # pins drop into the bolt (locked)
    t1 = F(0.04)
    for p in pins:
        key(p, "location", 1, (p.location.x, 0.0, 2.35))
        key(p, "location", t1, (p.location.x, 0.0, 2.35))
        key(p, "location", t1 + 8, (p.location.x, 0.0, 1.75))
    # key slides in under the pins, lifts them, bolt slides open
    a = round(m2 * 0.35)
    b_ = round(m2 * 0.55)
    c = round(m2 * 0.62)
    d = round(m2 * 0.8)
    key(k, "location", 1, (5.5, 0.0, 1.05))
    key(k, "location", a, (5.5, 0.0, 1.05))
    key(k, "location", b_, (0.0, 0.0, 1.05))
    key(k, "location", c, (0.0, 0.0, 1.38))
    for p in pins:
        key(p, "location", b_, (p.location.x, 0.0, 1.75))
        key(p, "location", c, (p.location.x, 0.0, 2.08))
    key(bolt, "location", c + 3, (0, 0.3, 1.55))
    key(bolt, "location", d, (-1.6, 0.3, 1.55))
    key(k, "location", c + 3, (0.0, 0.0, 1.38))
    key(k, "location", d, (-1.6, 0.0, 1.38))
    # PROBLEM: the key cracks in two
    crack = m2 + 20
    key(k, "location", m2, (-1.6, 0.0, 1.38))
    key(k, "location", m2 + 15, (0.4, -0.6, 0.6))
    for i, h in enumerate(halves):
        key(h, "rotation_euler", crack, (0, 0, 0))
        key(h, "rotation_euler", crack + 14, (0, math.radians(35 if i else -35), 0))
        key(h, "location", crack, h.location.copy())
        key(h, "location", crack + 14, h.location + Vector((0.3 if i else -0.3, 0, -0.5)))
    camera((0.3, -7.6, 1.9), (0.2, 0.3, 1.5), lens=34, moves=[(1.0, (0.0, -6.8, 1.8), None)])


def ring_key(loc, s=1.0):
    bpy.ops.object.empty_add(location=loc)
    e = bpy.context.object
    r = torus(0.35 * s, 0.07 * s, (0, 0, 0), BRASS_DK, rot=(math.radians(90), 0, 0))
    stem = box((0.12 * s, 0.12 * s, 0.6 * s), (0, 0, 0), BRASS_DK, bevel=0.01)
    bit = box((0.25 * s, 0.1 * s, 0.25 * s), (0, 0, 0), BRASS_DK, bevel=0.01)
    r.parent = stem.parent = bit.parent = e
    r.location = (0, 0, 0)
    stem.location = (0, 0, -0.62 * s)
    bit.location = (0.16 * s, 0, -0.75 * s)
    return e


def shot_roman():
    box((12, 8, 0.1), (0, 2, -0.05), mat("stone_floor", "#B9AE9C", noise=("#A39886", 4)))
    box((12, 0.3, 6), (0, 3.5, 3), mat("fresco", "#B0503A", noise=("#9A4231", 3)))
    chest = box((2.6, 1.4, 1.4), (0, 1.5, 0.7), DARK_WOOD, bevel=0.04)
    for x in (-1.2, 1.2):
        box((0.12, 1.45, 1.45), (x, 1.5, 0.7), IRON)
    plate = box((0.7, 0.1, 0.8), (0, 0.78, 0.85), IRON, bevel=0.02)
    box((0.08, 0.05, 0.25), (0, 0.72, 0.82), BLACK)
    rk = ring_key((0.9, 0.2, 2.6), s=1.2)
    key(rk, "location", 1, (0.9, 0.2, 3.6))
    key(rk, "location", F(0.2), (0.6, 0.0, 2.2))
    key(rk, "rotation_euler", 1, (0, 0, 0))
    key(rk, "rotation_euler", N, (0, 0, math.radians(300)))
    linear(rk)
    # a smaller ring key worn on a hand-like stand
    cyl(0.18, 1.2, (-1.5, 0.6, 0.6), mat("stand", "#E8DFCC"), verts=24)
    torus(0.22, 0.05, (-1.5, 0.6, 1.0), BRASS_DK)
    camera((0.8, -4.2, 2.2), (0.1, 1.0, 1.3), lens=32, moves=[(1.0, (-0.2, -3.6, 2.0), None)])


def shot_bramah():
    box((12, 8, 0.1), (0, 2, -0.05), mat("table", "#5A3A22", noise=("#4A2F1B", 5)))
    box((12, 0.3, 6), (0, 3.0, 3), mat("shop_wall", "#2F4A3A"))
    stand = box((2.2, 1.2, 0.3), (0, 0.8, 0.15), VELVET, bevel=0.05)
    lock = cyl(0.42, 1.1, (0, 0.8, 0.75), BRASS, rot=(0, math.radians(90), 0), verts=48)
    face = cyl(0.3, 0.06, (0.57, 0.8, 0.75), BRASS_DK, rot=(0, math.radians(90), 0), verts=48)
    sign = text3d("200 GUINEAS", (0, 2.6, 3.0), size=0.55, m=GOLD)
    sub = text3d("to whoever picks this lock", (0, 2.6, 2.4), size=0.22, m=mat("ivory", "#F3E9D2", emit=0.3))
    pop_in(sign, F(0.25), 8)
    pop_in(sub, F(0.3), 8)
    for i in range(9):
        c = cyl(0.22, 0.06, (-1.4 + 0.12 * (i % 2), 0.4, 0.33 + 0.065 * i), GOLD, verts=32)
        pop_in(c, F(0.32) + 2 * i, 4)
    pick = cyl(0.025, 1.2, (1.4, 0.8, 0.85), STEEL, rot=(0, math.radians(80), 0), verts=8)
    key(pick, "location", 1, (2.5, 0.8, 0.85))
    for j, t in enumerate((0.45, 0.55, 0.65, 0.75, 0.85)):
        key(pick, "location", F(t), (1.2 + 0.08 * (j % 2), 0.8, 0.82 + 0.04 * (j % 2)))
    yrs = text3d("67 YEARS", (0, 0.2, 1.9), size=0.45, m=mat("white_e", "#FFFFFF", emit=1.2))
    pop_in(yrs, F(0.8), 8)
    camera((0.6, -4.6, 2.0), (0, 1.2, 1.4), lens=30, moves=[(1.0, (0.1, -4.0, 1.9), None)])


def shot_yale():
    m2 = MARKS[1] if len(MARKS) > 1 else int(N * 0.6)
    box((14, 0.3, 10), (0, 1.5, 1.5), mat("bg_dark", "#2B3440"))
    housing = box((4.6, 0.3, 2.0), (0, 0.6, 2.3), BRASS_DK, bevel=0.03)       # upper body (behind pins)
    bpy.ops.object.empty_add(location=(0, 0.3, 0.65))
    plug_grp = bpy.context.object
    plug = box((4.6, 0.3, 1.3), (0, 0, 0), BRASS, bevel=0.03)
    plug.parent = plug_grp
    shear = box((4.8, 0.05, 0.035), (0, 0.05, 1.3), SHEAR)
    xs = [-1.6, -0.8, 0.0, 0.8, 1.6]
    L = [0.95, 0.6, 0.8, 0.5, 0.75]           # key pin lengths
    kp, dp, sp = [], [], []
    for x, l in zip(xs, L):
        a = cyl(0.14, l, (x, 0, 0.2 + l / 2), COPPER, verts=20)
        b = cyl(0.14, 0.7, (x, 0, 0.2 + l + 0.35), STEEL, verts=20)
        top = 0.2 + l + 0.7
        s_len = 3.15 - top
        s = cyl(0.09, s_len, (x, 0, top + s_len / 2), SPRING, verts=12)
        kp.append(a); dp.append(b); sp.append(s)
    # key: blade with teeth so each key pin's top lands on the shear line
    bpy.ops.object.empty_add(location=(-6.5, 0, 0))
    k = bpy.context.object
    blade = box((5.0, 0.18, 0.12), (0, 0, 0), STEEL)
    blade.parent = k
    blade.location = (0.2, 0, 0.1)
    for x, l in zip(xs, L):
        h = 1.3 - l - 0.16
        t = box((0.36, 0.18, h), (0, 0, 0), STEEL)
        t.parent = k
        t.location = (x, 0, 0.16 + h / 2)
    bow = cyl(0.55, 0.15, (0, 0, 0), STEEL, rot=(math.radians(90), 0, 0), verts=32)
    bow.parent = k
    bow.location = (-3.0, 0, 0.6)
    ins0, ins1 = F(0.08), round(m2 * 0.55)
    key(k, "location", 1, (-7.5, 0, 0))
    key(k, "location", ins0, (-7.5, 0, 0))
    key(k, "location", ins1, (0, 0, 0))
    lift0 = ins1 - 12
    for x, l, a, b, s in zip(xs, L, kp, dp, sp):
        dz = (1.3 - l) - 0.2
        for o in (a, b):
            key(o, "location", lift0, o.location.copy())
            key(o, "location", ins1, o.location + Vector((0, 0, dz)))
        key(s, "scale", lift0, (1, 1, 1))
        z_top = 3.15
        new_len = z_top - (0.2 + dz + l + 0.7)
        key(s, "scale", ins1, (1, 1, new_len / (z_top - (0.2 + l + 0.7))))
        key(s, "location", lift0, s.location.copy())
        key(s, "location", ins1, (x, 0, z_top - new_len / 2))
    # second beat: shear line lights up, then the plug turns with the key and key pins
    glow0 = m2 + 10
    key(shear, "scale", glow0, (4.8, 0.05, 0.035))
    key(shear, "scale", glow0 + 6, (4.8, 0.2, 0.12))
    key(shear, "scale", glow0 + 14, (4.8, 0.06, 0.06))
    turn0 = m2 + round((N - m2) * 0.45)
    for o in [k] + kp:
        o.parent = plug_grp
        o.matrix_parent_inverse = plug_grp.matrix_world.inverted()
    key(plug_grp, "rotation_euler", 1, (0, 0, 0))
    key(plug_grp, "rotation_euler", turn0, (0, 0, 0))
    key(plug_grp, "rotation_euler", turn0 + 20, (math.radians(-80), 0, 0))
    camera((0.6, -8.2, 1.9), (0, 0.3, 1.5), lens=34, moves=[(0.5, (0.2, -7.6, 1.7), None), (1.0, (-0.2, -7.2, 1.7), None)])


def shot_smart():
    m2 = MARKS[1] if len(MARKS) > 1 else int(N * 0.6)
    box((10, 8, 0.1), (0, 0, -0.05), mat("porch", "#8C8F94", noise=("#7B7E83", 3)))
    wall = box((8, 0.3, 4.2), (0, 1.3, 2.1), mat("modern_wall", "#EDEAE4"))
    cut(wall, box((1.25, 1, 2.45), (0, 1.3, 1.22)))
    door = hinge_door(-0.6, 1.2, 1.2, 2.4, mat("modern_door", "#2F3A44", rough=0.4), angle=-80)
    box((0.15, 0.04, 1.8), (0.25, 1.12, 1.25), mat("glass_strip", "#9FD2F0", rough=0.05, emit=0.3))
    pad = box((0.28, 0.06, 0.45), (0.95, 1.12, 1.3), BLACK, bevel=0.02)
    led = ball(0.035, (0.95, 1.08, 1.47), GLOW_RED, seg=10)
    led_g = ball(0.036, (0.95, 1.079, 1.47), GLOW_GREEN, seg=10)
    for r in range(3):
        for c in range(3):
            box((0.05, 0.02, 0.05), (0.88 + 0.07 * c, 1.085, 1.2 + 0.08 * r), mat("btn", "#7FD8FF", emit=1.5))
    phone = box((0.42, 0.06, 0.82), (0.2, -0.9, 1.35), BLACK, bevel=0.05)
    scr = box((0.36, 0.01, 0.72), (0.2, -0.935, 1.35), SCREEN)
    for o in (phone, scr):
        o.rotation_euler = (0, 0, math.radians(-15))
    t_tap = F(0.32)
    for o, base in ((phone, phone.location.copy()), (scr, scr.location.copy())):
        key(o, "location", 1, base + Vector((0, -0.8, -0.6)))
        key(o, "location", F(0.15), base)
        key(o, "location", t_tap, base + Vector((0.45, 1.2, 0)))
        key(o, "location", t_tap + 12, base + Vector((0.2, 0.4, 0)))
    ring = torus(0.2, 0.02, (0.95, 1.0, 1.3), mat("wave", "#7FD8FF", emit=3, alpha=0.8), rot=(math.radians(90), 0, 0))
    key(ring, "scale", 1, (0, 0, 0))
    key(ring, "scale", t_tap, (0.2, 0.2, 0.2))
    key(ring, "scale", t_tap + 12, (3, 3, 3))
    key(ring, "scale", t_tap + 13, (0, 0, 0))
    key(led_g, "scale", 1, (0, 0, 0))
    key(led_g, "scale", t_tap + 4, (0, 0, 0))
    key(led_g, "scale", t_tap + 6, (1.3, 1.3, 1.3))
    key(door, "rotation_euler", 1, (0, 0, 0))
    key(door, "rotation_euler", t_tap + 10, (0, 0, 0))
    key(door, "rotation_euler", t_tap + 34, (0, 0, math.radians(80)))
    bpy.ops.object.light_add(type="AREA", location=(0, 2.4, 1.3), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.energy = 150
    bpy.context.object.data.size = 1.2
    for x in (-2.5, 2.8):
        cyl(0.35, 0.6, (x, -0.2, 0.3), CONCRETE, verts=24)
        ball(0.45, (x, -0.2, 0.9), mat("bush", "#4F8A45"), seg=10)
    camera((0.9, -3.4, 1.7), (0.4, 1.1, 1.35), lens=30,
           moves=[(m2 / N, (0.6, -2.8, 1.6), None), (1.0, (0.3, -5.2, 2.2), (0, 1.2, 1.6))])


