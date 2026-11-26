# ---------------------------------------------------------------- light shots
FLAME = mat("flame", "#FFB13B", emit=12.0)
FLAME_CORE = mat("flame_core", "#FFF1B0", emit=18.0)
SMOKE = mat("smoke", "#6E6E6E", alpha=0.45)
CLAY = mat("clay", "#B5643A", noise=("#9A5230", 5))
WAX = mat("wax", "#F3EBD6", rough=0.4)
LOG = mat("log", "#5A3A22", noise=("#43291A", 6))
EMBER = mat("ember", "#FF5A1F", emit=6.0)
GLASS_BULB = mat("glass_bulb", "#F4F8FF", rough=0.05, alpha=0.25, spec=0.9)
GLASS_BULB.shadow_method = "NONE"
FILAMENT = mat("filament", "#FFB347", emit=0.0)
LED_GLOW = mat("led_glow", "#F5FAFF", emit=0.0)
HEAT = mat("heat_p", "#FF5A2A", emit=4.0, alpha=0.8)
WINDOW = mat("window_lit", "#FFD98A", emit=4.0)
NIGHT_GROUND = mat("night_ground", "#3A3530", noise=("#2E2A26", 2))
SEA = mat("sea", "#1E3A5A", rough=0.3)


def night(strength=0.12, top="#0E1630", bottom="#23304F", sun=0.15):
    w = bpy.context.scene.world.node_tree
    w.nodes["Background"].inputs["Strength"].default_value = strength
    ramp = [n for n in w.nodes if n.type == "VALTORGB"][0]
    ramp.color_ramp.elements[0].color = lin(bottom)
    ramp.color_ramp.elements[1].color = lin(top)
    for o in bpy.data.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy = sun
            o.data.color = (0.6, 0.7, 1.0)


def point_light(loc, energy, color=(1.0, 0.65, 0.3), radius=0.1, flicker=True, seed=0):
    bpy.ops.object.light_add(type="POINT", location=loc)
    L = bpy.context.object
    L.data.energy = energy
    L.data.color = color
    L.data.shadow_soft_size = radius
    if flicker:
        rnd = random.Random(seed)
        for fr in range(1, N + 1, 4):
            L.data.energy = energy * rnd.uniform(0.8, 1.15)
            L.data.keyframe_insert("energy", frame=fr)
    return L


def flame(loc, s=1.0, seed=0):
    outer = cyl(0.12 * s, 0.4 * s, (loc[0], loc[1], loc[2] + 0.2 * s), FLAME, r2=0.0, verts=16)
    core = cyl(0.06 * s, 0.22 * s, (loc[0], loc[1] - 0.02, loc[2] + 0.11 * s), FLAME_CORE, r2=0.0, verts=12)
    rnd = random.Random(seed)
    for fr in range(1, N + 1, 3):
        k = rnd.uniform(0.85, 1.2)
        outer.scale = (rnd.uniform(0.9, 1.1), rnd.uniform(0.9, 1.1), k)
        outer.keyframe_insert("scale", frame=fr)
    return outer, core


def glow_ramp(m, frame0, frame1, value):
    inp = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    m.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value
    inp.default_value = 0.0
    inp.keyframe_insert("default_value", frame=frame0)
    inp.default_value = value
    inp.keyframe_insert("default_value", frame=frame1)


def shot_fire():
    night()
    ground(m=NIGHT_GROUND)
    m2, m3 = MARKS[1], MARKS[2]
    for a in (0, 60, 120):
        cyl(0.09, 1.1, (0, 2, 0.12), LOG, rot=(math.radians(90), 0, math.radians(a)), verts=10)
    for i in range(6):
        ang = i * math.tau / 6
        ball(0.12, (0.5 * math.cos(ang), 2 + 0.5 * math.sin(ang), 0.05), STONE, seg=8, squash=0.6)
    flames = []
    for i, (dx, dy, s) in enumerate([(0, 0, 2.2), (0.12, 0.05, 1.6), (-0.13, -0.04, 1.5), (0.02, 0.12, 1.3)]):
        o, c = flame((dx, 2 + dy, 0.15), s, seed=i)
        flames += [o, c]
    # fire is lit at the start of the "First came fire" beat; before that, only embers glow
    for o in flames:
        home = o.location.copy()
        key(o, "location", 1, home - Vector((0, 0, 1.2)))
        key(o, "location", m3 - 1, home - Vector((0, 0, 1.2)))
        key(o, "location", m3 + 6, home)
    for i in range(5):
        ball(0.05, (random.Random(i).uniform(-0.25, 0.25), 2 + random.Random(i + 9).uniform(-0.2, 0.2), 0.1), EMBER, seg=8)
    L = point_light((0, 2, 0.8), 0, flicker=False)
    key(L.data, "energy", 1, 2)
    key(L.data, "energy", m3 - 1, 2)
    key(L.data, "energy", m3 + 8, 250)
    rnd = random.Random(5)
    for i in range(14):
        s = ball(rnd.uniform(0.15, 0.3), (rnd.uniform(-0.2, 0.2), 2, 0.9), SMOKE, seg=12)
        t0 = m3 + 8 + i * 5
        if t0 >= N - 4:
            break
        pop_in(s, t0, 6)
        key(s, "location", t0, s.location.copy())
        key(s, "location", min(N, t0 + 40), s.location + Vector((rnd.uniform(-0.6, 0.6), 0.3, 2.5)))
    for x, y in ((-3, 6), (2.8, 7.5), (-0.5, 9)):
        hut((x, y), 1.0)
    camera((0.8, -5.0, 2.6), (0, 2.5, 0.9), lens=30, moves=[(m3 / N, (0.5, -3.8, 2.0), None), (1.0, (0.2, -2.6, 1.6), (0, 2, 0.8))])


def shot_oillamp():
    night(0.08)
    box((10, 8, 0.1), (0, 1, -0.05), mat("stone_tab", "#7D7466", noise=("#6C6457", 4)))
    box((10, 0.3, 6), (0, 1.8, 3), mat("mud_wall", "#5E4A38", noise=("#4E3C2C", 4)))
    body = ball(0.45, (0, 0.6, 0.2), CLAY, seg=24, squash=0.45)
    cut(body, cyl(0.15, 0.4, (-0.1, 0.6, 0.38), smooth=False))
    spout = cyl(0.11, 0.5, (0.45, 0.6, 0.22), CLAY, rot=(0, math.radians(80), 0), verts=16)
    cyl(0.06, 0.3, (-0.48, 0.6, 0.25), CLAY, rot=(0, math.radians(-60), 0), verts=12)
    torus(0.15, 0.03, (-0.1, 0.6, 0.38), CLAY)
    cyl(0.025, 0.12, (0.68, 0.6, 0.3), mat("wick", "#2A2420"), verts=8)
    flame((0.68, 0.6, 0.33), 0.9, seed=3)
    point_light((0.68, 0.45, 0.8), 60, seed=3)
    camera((0.3, -2.2, 1.0), (0.2, 0.6, 0.35), lens=34, moves=[(1.0, (-0.2, -1.7, 0.85), None)])


def shot_candle():
    night(0.06)
    box((10, 8, 0.1), (0, 1, -0.05), DARK_WOOD)
    box((10, 0.3, 6), (0, 1.8, 3), mat("plaster_n", "#4F4639"))
    cyl(0.45, 0.06, (0, 0.6, 0.03), BRASS, verts=32)
    torus(0.45, 0.03, (0, 0.6, 0.06), BRASS)
    c = cyl(0.14, 1.0, (0, 0.6, 0.56), WAX, verts=24)
    fl = flame((0, 0.6, 1.08), 0.8, seed=7)
    wick = cyl(0.015, 0.08, (0, 0.6, 1.08), mat("wick2", "#1E1A16"), verts=6)
    L = point_light((0, 0.45, 1.5), 45, seed=7)
    # candle burns down over the shot
    key(c, "scale", 1, (1, 1, 1))
    key(c, "location", 1, (0, 0.6, 0.56))
    key(c, "scale", N, (1, 1, 0.45))
    key(c, "location", N, (0, 0.6, 0.06 + 0.225))
    drop = 1.0 - 0.45
    for o in list(fl) + [wick, L]:
        key(o, "location", 1, o.location.copy())
        key(o, "location", N, o.location - Vector((0, 0, drop)))
        linear(o)
    linear(c)
    rnd = random.Random(4)
    for i in range(7):
        a = rnd.uniform(0, math.tau)
        d = ball(0.05, (0.14 * math.cos(a), 0.6 + 0.14 * math.sin(a), 0.9), WAX, seg=8, squash=1.6)
        t0 = F(0.1 + 0.11 * i)
        pop_in(d, t0, 3)
        key(d, "location", t0, d.location.copy())
        key(d, "location", min(N, t0 + 20), (d.location.x * 1.05, d.location.y, 0.12))
    camera((0.4, -2.4, 1.2), (0, 0.6, 0.75), lens=34, moves=[(1.0, (0.1, -2.0, 1.0), None)])


def shot_whale():
    night(0.1, top="#1B2A4A", bottom="#3A4F75")
    box((10, 6, 0.1), (0, 0, -0.05), DARK_WOOD)
    wall = box((10, 0.3, 6), (0, 1.6, 3), mat("ship_wall", "#5A3C24", noise=("#4A301C", 6)))
    cut(wall, box((2.6, 1, 1.6), (0.3, 1.6, 2.2)))
    box((40, 40, 0.05), (0, 21, 0.4), SEA)
    tail = prism(1.4, 0.15, 0.8, (1.2, 9, 0.4), mat("whale", "#2C3440"))
    key(tail, "location", 1, (1.2, 9, -0.6))
    key(tail, "location", F(0.35), (1.2, 9, 0.4))
    key(tail, "location", F(0.75), (1.2, 9, 0.9))
    # brass hurricane lamp
    cyl(0.32, 0.12, (-0.5, 0.4, 0.06), BRASS, verts=32)
    cyl(0.22, 0.45, (-0.5, 0.4, 0.35), mat("oil_glass", "#C9A24A", rough=0.1, alpha=0.6), verts=32)
    cyl(0.16, 0.9, (-0.5, 0.4, 1.05), GLASS_BULB, r2=0.12, verts=32)
    flame((-0.5, 0.4, 0.62), 0.9, seed=9)
    point_light((-0.5, 0.25, 1.0), 120, color=(1.0, 0.75, 0.45), seed=9)
    camera((0.2, -3.0, 1.4), (0.1, 1.0, 1.0), lens=30, moves=[(1.0, (-0.3, -2.5, 1.3), None)])


def shot_gaslamp():
    night(0.1)
    front = -1.0
    layers = section(front, layers=[(0.0, -0.25, mat("cobble", "#5E5A55", noise=("#4E4A46", 6))), (-0.25, -3.0, SOIL), (-3.0, -9, ROCK)])
    pipe_cut = cyl(0.35, 30, (0, front + 0.3, -1.3), rot=(0, math.radians(90), 0), smooth=False)
    cut(layers[1], pipe_cut)
    cyl(0.28, 30, (0, front + 0.3, -1.3), IRON, rot=(0, math.radians(90), 0))
    riser = cyl(0.07, 1.1, (0.6, front + 0.3, -0.75), IRON, verts=12)
    cut(layers[0], box((0.3, 0.8, 1), (0.6, front + 0.3, -0.1)))
    cut(layers[1], box((0.3, 0.8, 1.2), (0.6, front + 0.3, -0.6)))
    post = cyl(0.09, 3.2, (0.6, front + 0.3, 1.6), IRON, verts=16)
    cyl(0.18, 0.3, (0.6, front + 0.3, 0.15), IRON, verts=16)
    lantern = box((0.5, 0.5, 0.6), (0.6, front + 0.3, 3.45), GLASS_BULB)
    prism(0.65, 0.65, 0.3, (0.6, front + 0.3, 3.75), IRON)
    fl = flame((0.6, front + 0.3, 3.25), 0.8, seed=11)
    L = point_light((0.6, front + 0.1, 3.45), 0, color=(1.0, 0.85, 0.55), flicker=False)
    t_on = F(0.55)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", t_on, 0)
    key(L.data, "energy", t_on + 6, 260)
    for o in fl:
        key(o, "location", 1, o.location - Vector((0, 0, 3)))
        key(o, "location", t_on, o.location - Vector((0, 0, 3)))
        key(o, "location", t_on + 4, o.location.copy())
    # gas flowing through the main and up the post
    path = [Vector((-4.5, front + 0.0, -1.3)), Vector((0.6, front + 0.0, -1.3)), Vector((0.6, front + 0.0, 3.2))]
    segs = [(path[i + 1] - path[i]).length for i in range(2)]
    tot = sum(segs)

    def at(u):
        d = u * tot
        if d <= segs[0]:
            return path[0] + (path[1] - path[0]) * (d / segs[0])
        d -= segs[0]
        return path[1] + (path[2] - path[1]) * min(1.0, d / segs[1])
    for j in range(14):
        g = ball(0.07, at(0), mat("gas_p", "#9FD8FF", emit=2.0), seg=8)
        t0 = F(0.05 + 0.035 * j)
        pop_in(g, t0, 3)
        for k, fr in enumerate(range(t0, min(N, t0 + 60) + 1, 4)):
            g.location = at(min(1.0, k * 4 / 60))
            g.keyframe_insert("location", frame=fr)
        pop_out(g, min(N - 1, t0 + 58), 3)
    for x in (-3.2, 3.6):
        house((x, front + 5.5), 1.3, "#7D6B5C")
        box((0.35, 0.05, 0.4), (x, front + 4.84, 0.75), WINDOW)
    camera((0.2, front - 8.2, 1.3), (0.3, front + 1, 0.9), lens=30, moves=[(1.0, (0.5, front - 7.2, 1.4), None)])


def bulb(loc, s=1.0, glass=GLASS_BULB):
    x, y, z = loc
    g = ball(0.55 * s, (x, y, z + 0.55 * s), glass, seg=32)
    neck = cyl(0.3 * s, 0.35 * s, (x, y, z + 0.05 * s), glass, r2=0.22 * s, verts=32)
    base = cyl(0.23 * s, 0.45 * s, (x, y, z - 0.3 * s), BRASS, verts=32)
    for k in range(4):
        torus(0.23 * s, 0.025 * s, (x, y, z - 0.45 * s + 0.1 * s * k), BRASS)
    cyl(0.1 * s, 0.08 * s, (x, y, z - 0.56 * s), BLACK, verts=16)
    return g


def shot_edison():
    night(0.08)
    m2 = MARKS[1] if len(MARKS) > 1 else int(N * 0.6)
    box((10, 8, 0.1), (0, 1, -0.05), DARK_WOOD)
    box((10, 0.3, 6), (0, 2.0, 3), mat("lab_wall", "#3E3A36"))
    bulb((0, 0.6, 1.2), 1.2)
    # filament: a loop inside the bulb
    pts = [(-0.12, 0.6, 1.25), (-0.12, 0.6, 1.75), (0.0, 0.6, 1.95), (0.12, 0.6, 1.75), (0.12, 0.6, 1.25)]
    curve_tube(pts, 0.012, FILAMENT)
    for x in (-0.12, 0.12):
        cyl(0.008, 0.35, (x, 0.6, 1.1), STEEL, verts=6)
    t_on = F(0.2)
    glow_ramp(FILAMENT, t_on, t_on + 10, 25.0)
    L = point_light((0, 0.4, 1.8), 0, color=(1.0, 0.72, 0.38), flicker=False)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", t_on, 0)
    key(L.data, "energy", t_on + 10, 220)
    # stand and wires
    cyl(0.5, 0.12, (0, 0.6, 0.06), DARK_WOOD, verts=32)
    curve_tube([(0, 0.6, 0.5), (0.6, 0.8, 0.2), (1.8, 1.0, 0.1)], 0.03, BLACK)
    yr = text3d("1879", (0, 0.2, 3.0), size=0.42, m=mat("gold_e", "#F2C14E", emit=1.5))
    pop_in(yr, F(0.08), 8)
    # heat: particles radiating out of the bulb
    rnd = random.Random(6)
    for i in range(36):
        a = rnd.uniform(0, math.tau)
        h = ball(0.07, (0, 0.5, 1.85), HEAT, seg=8)
        t0 = m2 + 4 + i * 2
        if t0 >= N - 4:
            break
        pop_in(h, t0, 3)
        key(h, "location", t0, h.location.copy())
        key(h, "location", min(N, t0 + 24), (1.8 * math.cos(a), 0.3, 1.85 + 1.8 * math.sin(a)))
        pop_out(h, min(N - 1, t0 + 20), 4)
    heat = text3d("90% HEAT", (0, 0.2, 3.1), size=0.42, m=mat("heat_t", "#FF6A3D", emit=2.0))
    pop_in(heat, m2 + 12, 8)
    key(yr, "scale", m2, (1, 1, 1))
    key(yr, "scale", m2 + 6, (0, 0, 0))
    camera((0.3, -3.4, 1.9), (0, 0.6, 1.7), lens=30, moves=[(m2 / N, (0.1, -3.0, 1.9), None), (1.0, (0, -3.6, 2.0), None)])


def shot_led():
    night(0.1)
    m2 = MARKS[1] if len(MARKS) > 1 else int(N * 0.6)
    ground(m=NIGHT_GROUND)
    # LED bulb up close
    dome = ball(0.55, (0, 0.6, 1.75), mat("frost", "#F8FAFF", rough=0.5), seg=32)
    body = cyl(0.42, 0.55, (0, 0.6, 1.2), mat("plastic_w", "#F2F2F2", rough=0.4), r2=0.55, verts=32)
    cyl(0.23, 0.4, (0, 0.6, 0.78), CHROME, verts=32)
    t_on = F(0.08)
    glow_ramp(dome.active_material, t_on, t_on + 6, 8.0)
    L = point_light((0, -0.5, 1.9), 0, color=(0.92, 0.96, 1.0), flicker=False)
    key(L.data, "energy", 1, 0)
    key(L.data, "energy", t_on, 0)
    key(L.data, "energy", t_on + 6, 180)
    yrs = text3d("20+ YEARS", (0, 0.2, 2.55), size=0.24, m=mat("cool_t", "#7FD8FF", emit=2.0))
    pop_in(yrs, F(0.4), 8)
    # city with lit windows for the pull-back
    rnd = random.Random(12)
    for i in range(14):
        x = -7 + i * 1.1
        h = rnd.uniform(2, 6)
        y = 9 + rnd.uniform(0, 3)
        box((0.9, 0.9, h), (x, y, h / 2), mat(f"bld{i%3}", ["#2A3142", "#323A4D", "#262C3A"][i % 3]))
        for r in range(int(h / 0.6)):
            for c in range(2):
                if rnd.random() < 0.7:
                    box((0.16, 0.02, 0.22), (x - 0.2 + 0.4 * c, y - 0.46, 0.4 + 0.6 * r), mat("win_led", "#E8F1FF", emit=3.0))
    camera((0.3, -2.2, 1.7), (0, 0.6, 1.6), lens=30,
           moves=[(m2 / N, (0.1, -1.8, 1.7), None), (1.0, (0.5, -5.5, 2.6), (0, 4, 2.0))])


