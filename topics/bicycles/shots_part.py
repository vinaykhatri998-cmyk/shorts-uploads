
# ---------------------------------------------------------------- bicycle shots
RUBBER = mat("rubber", "#1C1D21", rough=0.7)
CARBON = mat("carbon", "#22252B", rough=0.25, metal=0.3)
FRAME_R = mat("frame_r", "#B8322B", rough=0.35, metal=0.4)
ROAD_M = mat("roadm", "#5C5A56")
LEAF = mat("leaf", "#6E9B4A", noise=("#58823A", 4))


def scene_park(road=ROAD_M):
    ground(m=GRASS)
    box((400, 2.4, 0.04), (0, 0.6, 0.02), road)
    rnd = random.Random(4)
    for i in range(16):
        x = -30 + i * 4 + rnd.uniform(-1, 1)
        y = rnd.uniform(4, 9)
        cyl(0.15, 1.6, (x, y, 0.8), LOG, verts=8)
        ball(rnd.uniform(0.8, 1.2), (x, y, 2.0), LEAF, seg=8)


def wheel(r, loc, rim=None, tire=0.05, spokes=12, spoke_m=None, solid=False):
    """Wheel in the x-z plane; returns its hub empty (spin it around y)."""
    bpy.ops.object.empty_add(location=loc)
    hub = bpy.context.object
    t = torus(r, tire, (0, 0, 0), rim or RUBBER, rot=(math.radians(90), 0, 0))
    t.parent = hub
    t.location = (0, 0, 0)
    parts = []
    if solid:
        d = cyl(r * 0.95, 0.06, (0, 0, 0), spoke_m or WOOD, rot=(math.radians(90), 0, 0), verts=24)
        parts.append(d)
    for k in range(spokes):
        a = math.tau * k / spokes
        s = beam((0, 0, 0), (r * math.cos(a), 0, r * math.sin(a)), 0.015 if not solid else 0.05, spoke_m or STEEL)
        parts.append(s)
    c = cyl(0.05, 0.12, (0, 0, 0), IRON, rot=(math.radians(90), 0, 0), verts=12)
    parts.append(c)
    for p in parts:
        p.parent = hub
    return hub


def ride(rootobj, wheels, x0, x1, f0=1, f1=None, y=0.6):
    f1 = f1 or N
    key(rootobj, "location", f0, (x0, y, 0))
    key(rootobj, "location", f1, (x1, y, 0))
    for fc in rootobj.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    for w, r in wheels:
        turns = (x1 - x0) / (math.tau * r)
        spin(w, 1, turns, f0, f1)


def rider(x, z, s=1.0, shirt=None, legs=True):
    body = person(x, 0, z, s, shirt)
    hat = None
    return body


def group(loc, objs):
    bpy.ops.object.empty_add(location=loc)
    g = bpy.context.object
    for o in objs:
        o.parent = g
        o.location = o.location - g.location
    return g


def shot_draisine():
    m2 = MARKS[2]
    scene_park(mat("dirt", "#A88B62", noise=("#8E7450", 4)))
    R = 0.45
    wf = wheel(R, (0.75, 0, R), rim=mat("woodrim", "#6B4426"), tire=0.05, spokes=10, spoke_m=WOOD)
    wb = wheel(R, (-0.75, 0, R), rim=mat("woodrim", "#6B4426"), tire=0.05, spokes=10, spoke_m=WOOD)
    parts = [beam((-0.75, 0, R + 0.35), (0.85, 0, R + 0.35), 0.08, DARK_WOOD),
             beam((0.75, 0, R), (0.85, 0, R + 0.5), 0.05, DARK_WOOD),
             beam((-0.75, 0, R), (-0.6, 0, R + 0.35), 0.05, DARK_WOOD),
             box((0.4, 0.25, 0.06), (-0.15, 0, R + 0.45), mat("saddle", "#5A2E1E")),
             beam((0.85, -0.3, R + 0.6), (0.85, 0.3, R + 0.6), 0.04, DARK_WOOD)]
    p = person(-0.15, 0, R + 0.45, 1.0, mat("coat", "#2F4F7A"))
    legs = []
    for side in (-1, 1):
        lg = beam((-0.1, side * 0.1, R + 0.5), (0.0, side * 0.1, 0.05), 0.08, mat("trousers", "#3A3A44"))
        legs.append(lg)
    hat = cyl(0.12, 0.25, (-0.15, 0, R + 0.45 + 0.88), BLACK, verts=12)
    g = group((0, 0, 0), [wf, wb, p, hat] + parts + legs)
    for i, lg in enumerate(legs):
        for f in range(1, N, 14):
            k = ((f // 14) + i) % 2
            key(lg, "rotation_euler", f, (0, math.radians(-25 if k else 25), 0))
    ride(g, [(wf, R), (wb, R)], -4, 4, f0=m2)
    key(g, "location", 1, (-4, 0.6, 0))
    yr = text3d("1817", (0, 0, 2.8), size=0.6, m=mat("yr_b", "#F2C14E", emit=1.2))
    yr.parent = g
    yr.location = (0, -0.6, 2.6)
    pop_in(yr, m2 + 6, 8)
    camera((0.5, -6.5, 1.6), (-3.6, 0.6, 0.9), lens=38,
           moves=[(m2 / N, (0.0, -5.5, 1.5), (-3.2, 0.6, 1.0)), (1.0, (1.5, -6.0, 1.7), (2.5, 0.6, 1.0))])


def shot_boneshaker():
    scene_park(mat("cobble", "#8C8880", noise=("#6E6A62", 12)))
    Rf, Rb = 0.5, 0.42
    wf = wheel(Rf, (0.7, 0, Rf), rim=IRON, tire=0.04, spokes=12, spoke_m=WOOD)
    wb = wheel(Rb, (-0.7, 0, Rb), rim=IRON, tire=0.04, spokes=12, spoke_m=WOOD)
    parts = [beam((-0.7, 0, Rb), (0.55, 0, Rf + 0.45), 0.07, IRON),
             beam((0.7, 0, Rf), (0.6, 0, Rf + 0.7), 0.05, IRON),
             beam((0.6, -0.3, Rf + 0.75), (0.6, 0.3, Rf + 0.75), 0.04, IRON),
             box((0.35, 0.22, 0.06), (0.0, 0, Rf + 0.52), mat("saddle2", "#5A2E1E"))]
    crank = []
    for side in (-1, 1):
        c = beam((0.7, side * 0.12, Rf), (0.7, side * 0.12, Rf - 0.18), 0.04, IRON)
        crank.append(c)
    p = person(0.0, 0, Rf + 0.52, 1.0, mat("coat2", "#6B3A3A"))
    g = group((0, 0, 0), [wf, wb, p] + parts + crank)
    ride(g, [(wf, Rf), (wb, Rb)], -4, 4)
    # shaking: small rapid bumps
    for f in range(1, N, 3):
        key(p, "location", f, (0.0, 0, Rf + 0.52 + (0.03 if (f // 3) % 2 else -0.01)))
    camera((0.5, -6.0, 1.4), (-2.5, 0.6, 0.9), lens=38, moves=[(1.0, (1.5, -5.5, 1.5), (2.8, 0.6, 1.0))])


def shot_penny():
    scene_park()
    Rf, Rb = 1.0, 0.25
    wf = wheel(Rf, (0.4, 0, Rf), rim=RUBBER, tire=0.04, spokes=24)
    wb = wheel(Rb, (-1.0, 0, Rb), rim=RUBBER, tire=0.03, spokes=10)
    parts = [curve_tube([(-1.0, 0, Rb), (-0.6, 0, 1.3), (0.1, 0, 2.05), (0.4, 0, 2.0)], 0.04, IRON),
             beam((0.4, -0.35, 2.15), (0.4, 0.35, 2.15), 0.03, IRON),
             box((0.3, 0.2, 0.06), (0.15, 0, 2.08), mat("saddle3", "#5A2E1E"))]
    p = person(0.15, 0, 2.08, 1.0, mat("coat3", "#2E5E3E"))
    g = group((0, 0, 0), [wf, wb, p] + parts)
    fall = int(N * 0.72)
    ride(g, [(wf, Rf), (wb, Rb)], -4, 3.5, 1, fall)
    # hits a stone and pitches forward over the big wheel
    ball(0.18, (3.85, 0.6, 0.08), STONE, seg=8, squash=0.6)
    key(g, "rotation_euler", fall, (0, 0, 0))
    key(g, "rotation_euler", fall + 12, (0, math.radians(35), 0))
    key(p, "location", fall + 4, p.location.copy())
    key(p, "location", fall + 16, (1.9, 0, 0.6))
    key(p, "rotation_euler", fall + 4, (0, 0, 0))
    key(p, "rotation_euler", fall + 16, (0, math.radians(110), 0))
    camera((0.0, -7.0, 1.8), (-2.5, 0.6, 1.3), lens=38, moves=[(0.7, (2.5, -6.5, 1.8), (3.0, 0.6, 1.2)), (1.0, (3.5, -6.0, 1.6), (4.2, 0.6, 0.7))])


def chain_bike(R, frame_m, wheel_rim, motor=False, carbon=False):
    wf = wheel(R, (0.55, 0, R), rim=wheel_rim, tire=0.06 if not carbon else 0.045, spokes=16 if not carbon else 5,
               spoke_m=CARBON if carbon else STEEL)
    wb = wheel(R, (-0.55, 0, R), rim=wheel_rim, tire=0.06 if not carbon else 0.045, spokes=16 if not carbon else 5,
               spoke_m=CARBON if carbon else STEEL)
    t = 0.05 if not carbon else 0.07
    bb = (0.0, 0, R - 0.02)
    seat = (-0.15, 0, R + 0.55)
    head = (0.38, 0, R + 0.5)
    parts = [beam(bb, seat, t, frame_m), beam(seat, head, t, frame_m), beam(bb, head, t, frame_m),
             beam((-0.55, 0, R), bb, t * 0.8, frame_m), beam((-0.55, 0, R), seat, t * 0.8, frame_m),
             beam(head, (0.55, 0, R), t, frame_m), beam((0.38, 0, R + 0.5), (0.34, 0, R + 0.7), 0.04, frame_m),
             beam((0.34, -0.25, R + 0.7), (0.34, 0.25, R + 0.7), 0.035, BLACK),
             box((0.28, 0.14, 0.06), (-0.17, 0, R + 0.62), BLACK)]
    ch = curve_tube([(-0.55, -0.08, R + 0.06), (0.0, -0.08, R + 0.1), (0.0, -0.08, R - 0.14), (-0.55, -0.08, R - 0.06)], 0.012, IRON, closed=True)
    parts.append(ch)
    parts.append(cyl(0.1, 0.03, (0.0, -0.08, R - 0.02), STEEL, rot=(math.radians(90), 0, 0), verts=16))
    if motor:
        parts.append(box((0.42, 0.12, 0.14), (0.15, 0, R + 0.15), mat("battery", "#3A3F47"), bevel=0.02))
        parts.append(box((0.3, 0.02, 0.03), (0.15, -0.065, R + 0.18), mat("batt_led", "#3BE37A", emit=3.0)))
        parts.append(cyl(0.11, 0.1, (-0.55, 0, R), mat("hubmotor", "#3A3F47"), rot=(math.radians(90), 0, 0), verts=16))
    return wf, wb, parts


def shot_safety():
    m1 = MARKS[1]
    scene_park()
    R = 0.42
    wf, wb, parts = chain_bike(R, mat("enamel", "#1C1D21", rough=0.3), mat("tyre_solid", "#4A4A4A"))
    p = person(-0.17, 0, R + 0.62, 1.0, mat("coat4", "#7A5A3A"))
    hat = cyl(0.16, 0.06, (-0.17, 0, R + 0.62 + 0.88), mat("boater", "#E2CC8F"), verts=16)
    g = group((0, 0, 0), [wf, wb, p, hat] + parts)
    ride(g, [(wf, R), (wb, R)], -5, 5)
    # air tyres puff up after the second line
    for w in (wf, wb):
        t = [c for c in w.children if c.type == "MESH" and c.data.materials[0].name.startswith("tyre")][0]
        key(t, "scale", m1, (1, 1, 1))
        key(t, "scale", m1 + 8, (1.02, 1.02, 1.9))
    yr = text3d("1885", (0, 0, 2.6), size=0.6, m=mat("yr_sf", "#F2C14E", emit=1.2))
    yr.parent = g
    yr.location = (0, -0.6, 2.4)
    pop_in(yr, 6, 8)
    camera((-1.0, -5.0, 1.3), (-4.0, 0.6, 0.8), lens=38, moves=[(1.0, (2.0, -4.6, 1.3), (4.4, 0.6, 0.8))])


def shot_ebike():
    m1 = MARKS[1]
    ground(m=CONCRETE)
    box((400, 2.4, 0.04), (0, 0.6, 0.02), mat("asphalt", "#3B3D42"))
    box((400, 0.12, 0.05), (0, 1.5, 0.03), mat("bikelane", "#3BB273"))
    rnd = random.Random(9)
    for i in range(14):
        x = -30 + i * 5
        h = rnd.uniform(4, 12)
        box((3.5, 3, h), (x, 8, h / 2), mat(f"bld{i%3}", ["#9AA8B5", "#B7C0C8", "#C9CFD4"][i % 3]))
    R = 0.4
    wf, wb, parts = chain_bike(R, CARBON, RUBBER, motor=True, carbon=True)
    p = person(-0.17, 0, R + 0.62, 1.0, mat("jersey", "#2E86C1"))
    helmet = ball(0.16, (-0.17, 0, R + 0.62 + 0.8), mat("helmet", "#F2F2F2", rough=0.3), seg=12, squash=0.75)
    g = group((0, 0, 0), [wf, wb, p, helmet] + parts)
    ride(g, [(wf, R), (wb, R)], -6, 8)
    for i in range(12):
        s = ball(0.04, (0, 0, 0), mat("zap", "#3BE37A", emit=4.0), seg=6)
        s.parent = g
        t0 = 8 + i * 14
        if t0 + 10 >= N:
            break
        pop_in(s, t0, 2)
        key(s, "location", t0, (0.15, -0.1, R + 0.15))
        key(s, "location", t0 + 10, (-0.55, -0.1, R))
        pop_out(s, t0 + 8, 2)
    camera((-2.0, -4.6, 1.2), (-4.5, 0.6, 0.8), lens=36, moves=[(m1 / N, (2.5, -4.2, 1.0), (4.0, 0.6, 0.8)), (1.0, (4.0, -7.0, 2.0), (7.5, 0.6, 0.8))])
