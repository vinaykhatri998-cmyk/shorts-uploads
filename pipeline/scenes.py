# Low-poly 3D shots for "How Toilets Evolved", rendered with Blender EEVEE.
#
#   blender -b -P scenes.py -- <shot> [--still FRAME]
#
# Reads timeline.json for each shot's length and beat marks, writes PNG frames
# to frames/<shot>/0001.png ... Run render.sh to render every shot.

import bpy, json, math, random, sys
from pathlib import Path
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SHOT = ARGS[0]
STILL = int(ARGS[ARGS.index("--still") + 1]) if "--still" in ARGS else None
PREVIEW = "--preview" in ARGS      # half resolution, fewer samples

TL = json.loads((HERE / "timeline.json").read_text())
INFO = next(s for s in TL["shots"] if s["shot"] == SHOT)
N = INFO["frames"]
MARKS = INFO["marks"]
bpy.ops.wm.read_factory_settings(use_empty=True)


# ---------------------------------------------------------------- basics
def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def F(t):
    """Shot-relative time 0..1 -> frame number."""
    return 1 + round(t * (N - 1))


def mat(name, color, rough=0.85, metal=0.0, alpha=1.0, emit=0.0, noise=None, spec=0.3):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    if emit:
        b.inputs["Emission Color"].default_value = lin(color)
        b.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
        m.shadow_method = "NONE"
        m.show_transparent_back = False
    if noise:
        c2, scale = noise
        tex = nt.nodes.new("ShaderNodeTexNoise")
        tex.inputs["Scale"].default_value = scale
        tex.inputs["Detail"].default_value = 6
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = lin(color)
        ramp.color_ramp.elements[1].color = lin(c2)
        ramp.color_ramp.elements[0].position = 0.35
        ramp.color_ramp.elements[1].position = 0.65
        nt.links.new(tex.outputs["Fac"], ramp.inputs["Fac"])
        nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    return m


def flowing(name, color, color2, scale=4.0, alpha=1.0, speed=(3, 0, 0)):
    """Material whose noise pattern slides over the shot: reads as moving water."""
    m = mat(name, color, rough=0.15, alpha=alpha, noise=(color2, scale), spec=0.6)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nt.nodes["Noise Texture"].inputs["Vector"])
    loc = mp.inputs["Location"]
    loc.default_value = (0, 0, 0)
    loc.keyframe_insert("default_value", frame=1)
    loc.default_value = tuple(-s * N / 30 for s in speed)
    loc.keyframe_insert("default_value", frame=N)
    linear(nt)
    return m


def linear(idblock):
    ad = idblock.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for k in fc.keyframe_points:
                k.interpolation = "LINEAR"


def finish(o, m=None, smooth=False, bevel=0.0):
    if m:
        o.data.materials.clear()
        o.data.materials.append(m)
    if smooth:
        bpy.ops.object.shade_smooth()
    if bevel:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        b = o.modifiers.new("bevel", "BEVEL")
        b.width = bevel
        b.segments = 2
    return o


def box(size, loc, m=None, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.scale = size
    return finish(o, m, bevel=bevel)


def cyl(r, depth, loc, m=None, rot=(0, 0, 0), verts=32, r2=None, smooth=True, bevel=0.0):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object
    if smooth:
        bpy.ops.object.shade_smooth()
        o.data.use_auto_smooth = True
        o.data.auto_smooth_angle = math.radians(40)
    return finish(o, m, bevel=bevel)


def ball(r, loc, m=None, seg=16, squash=1.0):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2)
    o = bpy.context.object
    o.scale.z = squash
    return finish(o, m, smooth=True)


def torus(R, r, loc, m=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot,
                                     major_segments=40, minor_segments=14)
    return finish(bpy.context.object, m, smooth=True)


def cut(target, cutter):
    mod = target.modifiers.new("cut", "BOOLEAN")
    mod.object = cutter
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    cutter.hide_render = True
    cutter.hide_viewport = True
    return mod


def curve_tube(points, radius, m, closed=False):
    cu = bpy.data.curves.new("tube", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(points) - 1)
    for bp, p in zip(sp.bezier_points, points):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new("tube", cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def key(o, path, frame, value, ease=True):
    setattr(o, path, value)
    o.keyframe_insert(path, frame=frame)


def pop_in(o, frame, length=8, final=None):
    final = tuple(final or o.scale)
    key(o, "scale", 1, (0, 0, 0))
    key(o, "scale", max(1, frame), (0, 0, 0))
    key(o, "scale", frame + length, final)


def pop_out(o, frame, length=6):
    s = tuple(o.scale)
    key(o, "scale", frame, s)
    key(o, "scale", frame + length, (0, 0, 0))


# ---------------------------------------------------------------- palette
SAND = mat("sand", "#D8C29A", noise=("#C9B07F", 1.2))
SAND_TOP = mat("sand_top", "#E2CFA6", noise=("#CDB585", 3))
SOIL = mat("soil", "#94643E", noise=("#7E5131", 2.5))
WATER_BAND = mat("ground_water", "#8FC9EC", rough=0.4)
ROCK = mat("rock", "#9A9A9A", noise=("#868686", 2))
MUD = mat("mud", "#C9A97A", noise=("#B89466", 4))
STRAW = mat("straw", "#D6B46A", noise=("#B8964E", 8))
STONE = mat("stone", "#C9C2B4", noise=("#ADA597", 5))
WOOD = mat("wood", "#9B6B3D", noise=("#7E5530", 6))
WASTE = mat("waste", "#6E4A2A", rough=0.6)
GERM = mat("germ", "#7BE36A", emit=1.5)
STINK = mat("stink", "#9BE36A", alpha=0.55, emit=0.8)
PORCELAIN = mat("porcelain", "#F4F4F2", rough=0.15, spec=0.6)
CHROME = mat("chrome", "#D0D4D8", rough=0.2, metal=1.0)
PIPE = mat("pipe", "#B8BEC4", rough=0.4, metal=0.4)
GLASS = mat("glass", "#E6F4FC", rough=0.1, alpha=0.22)
CONCRETE = mat("concrete", "#BDBAB3", noise=("#A8A59E", 3))
TILE = mat("tile", "#ECE8E1", rough=0.3)
WALL = mat("wall", "#DCE6EA", rough=0.8)
GRASS = mat("grass", "#9DB36A", noise=("#86A055", 3))


# ---------------------------------------------------------------- world
def world_setup():
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, N
    sc.render.fps = TL["fps"]
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.render.resolution_percentage = 50 if PREVIEW else int(__import__("os").environ.get("RES", "75"))
    sc.eevee.taa_render_samples = 6 if PREVIEW else int(__import__("os").environ.get("SAMPLES", "8"))
    sc.eevee.use_gtao = True
    sc.eevee.gtao_distance = 1.2
    sc.eevee.use_soft_shadows = True
    sc.eevee.shadow_cube_size = "1024"
    sc.eevee.shadow_cascade_size = "2048"
    sc.eevee.use_bloom = True
    sc.eevee.bloom_intensity = 0.03
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Base Contrast"
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = str(HERE / "frames" / SHOT) + "/"
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = lin("#C9D6E0")
    ramp.color_ramp.elements[1].color = lin("#86A9CC")
    ramp.color_ramp.elements[1].position = 0.45
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.9
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(10), math.radians(35)))
    sun = bpy.context.object.data
    sun.energy = 3.2
    sun.angle = math.radians(6)
    sun.color = (1.0, 0.95, 0.88)


def camera(loc, target, lens=35, moves=()):
    """moves: [(t, loc, target)] keyframes in shot time."""
    bpy.ops.object.empty_add(location=target)
    tgt = bpy.context.object
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.data.lens = lens
    cam.data.sensor_fit = "VERTICAL"
    cam.data.sensor_height = 36 * 16 / 9 * 0.62
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    bpy.context.scene.camera = cam
    if moves:
        key(cam, "location", 1, loc)
        key(tgt, "location", 1, target)
        for t, l, g in moves:
            if l is not None:
                key(cam, "location", F(t), l)
            if g is not None:
                key(tgt, "location", F(t), g)
    return cam, tgt


def ground(y0=None, size=400, m=None):
    """Flat ground; with y0 it starts at y = y0 (cuts the world open toward the camera)."""
    if y0 is None:
        box((size, size, 0.02), (0, 0, -0.01), m or SAND)
    else:
        box((size, size, 0.02), (0, y0 + size / 2, -0.01), m or SAND)


def section(front=-1.0, half_w=9, depth=40, layers=None):
    """Cross-section block below ground, open toward the camera at y = front."""
    layers = layers or [(0.0, -0.35, SAND_TOP), (-0.35, -2.8, SOIL), (-2.8, -3.5, WATER_BAND), (-3.5, -9, ROCK)]
    objs = []
    for top, bot, m in layers:
        objs.append(box((2 * half_w, depth, top - bot), (0, front + depth / 2, (top + bot) / 2), m))
    ground(y0=front)
    return objs


def scatter_rocks(n, xr, yr, seed=1):
    rnd = random.Random(seed)
    for _ in range(n):
        r = rnd.uniform(0.05, 0.18)
        ball(r, (rnd.uniform(*xr), rnd.uniform(*yr), r * 0.3), STONE, seg=8, squash=0.6)


def hut(loc, s=1.0):
    x, y = loc
    cyl(0.9 * s, 1.1 * s, (x, y, 0.55 * s), MUD, verts=24)
    cyl(1.15 * s, 0.9 * s, (x, y, 1.1 * s + 0.45 * s), STRAW, r2=0.05, verts=24)
    box((0.45 * s, 0.1, 0.7 * s), (x, y - 0.88 * s, 0.35 * s), mat("door", "#4A3322"))


def prism(w, d, h, loc, m):
    x, y, z = loc
    v = [(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (0, -d / 2, h), (-w / 2, d / 2, 0), (w / 2, d / 2, 0), (0, d / 2, h)]
    f = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (0, 2, 5, 3)]
    me = bpy.data.meshes.new("prism")
    me.from_pydata(v, [], f)
    o = bpy.data.objects.new("prism", me)
    o.location = loc
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


def house(loc, s=1.0, color="#E9DCC6"):
    x, y = loc
    box((1.4 * s, 1.2 * s, 1.0 * s), (x, y, 0.5 * s), mat("hw" + color, color), bevel=0.03)
    prism(1.6 * s, 1.4 * s, 0.7 * s, (x, y, 1.0 * s), mat("roof", "#B5543C"))
    box((0.3 * s, 0.05, 0.55 * s), (x, y - 0.6 * s, 0.28 * s), mat("door", "#4A3322"))


# ---------------------------------------------------------------- shots
def shot_village():
    ground()
    for i, (x, y, s) in enumerate([(-2.2, 4, 1.0), (1.8, 6, 1.1), (-0.3, 10, 0.9), (3.5, 12, 1.0), (-4, 9, 0.8)]):
        hut((x, y), s)
    scatter_rocks(30, (-6, 6), (-2, 14), seed=3)
    camera((0.5, -9, 4.5), (0, 5, 0.8), lens=30, moves=[(1.0, (0.2, -5.5, 3.2), (0, 6, 0.9))])


def shot_river():
    g = box((400, 400, 0.4), (0, 0, -0.2), SAND)
    cut(g, box((60, 3.2, 1), (0, 4, 0)))
    # river channel: water strip slightly below the sand, between two banks
    water = box((40, 3.2, 0.05), (0, 4, -0.15), flowing("river", "#6FAFCF", "#8FCBE6", scale=3, speed=(2.5, 0, 0)))
    box((40, 0.3, 0.12), (0, 2.25, 0.0), MUD)
    box((40, 0.3, 0.12), (0, 5.75, 0.0), MUD)
    rnd = random.Random(5)
    for i in range(7):
        ball(0.18, (rnd.uniform(-3, 3), rnd.uniform(0.5, 1.8), 0.05), WASTE, seg=10, squash=0.5)
    # germs multiply along the water
    for i in range(26):
        g = ball(0.16, (rnd.uniform(-4, 4), rnd.uniform(2.8, 5.2), -0.05), GERM, seg=10)
        start = F(0.25 + 0.5 * i / 26)
        pop_in(g, start, 6)
        key(g, "location", start, g.location.copy())
        key(g, "location", N, g.location + Vector((2.0, 0, 0)))
    scatter_rocks(25, (-6, 6), (-3, 12), seed=8)
    hut((-3.5, 11), 0.9)
    hut((2.5, 13), 1.0)
    camera((0, -4.5, 4.2), (0, 3.2, 0), lens=30, moves=[(1.0, (0.8, -3.2, 3.4), (0.4, 3.5, 0))])


def shot_pit():
    front = -1.0
    layers = section(front)
    cutter = box((1.6, 2.6, 6), (0, front + 1.2, 3.0))     # starts above ground, digs down
    for l in layers[:2]:
        cut(l, cutter)
    dig_end = F(0.22)
    key(cutter, "location", 1, (0, front + 1.2, 3.0))
    key(cutter, "location", dig_end, (0, front + 1.2, -0.3 - 0.5))
    # wooden planks over the pit after digging
    planks = [box((0.6, 2.6, 0.12), (x, front + 1.2, 0.07), WOOD, bevel=0.02) for x in (-0.75, 0.75)]
    for p in planks:
        pop_in(p, dig_end + 4, 8)
    # PROBLEM beat: the pit fills and stinks
    m2 = MARKS[1] if len(MARKS) > 1 else N // 2
    fill = box((1.58, 2.58, 0.01), (0, front + 1.2, -2.8), WASTE)
    t_full = m2 + round((N - m2) * 0.55)
    key(fill, "scale", 1, (1.58, 2.58, 0.01))
    key(fill, "location", 1, (0, front + 1.2, -2.8))
    key(fill, "scale", m2, (1.58, 2.58, 0.01))
    key(fill, "location", m2, (0, front + 1.2, -2.8))
    key(fill, "scale", t_full, (1.58, 2.58, 2.2))
    key(fill, "location", t_full, (0, front + 1.2, -2.8 + 1.1))
    rnd = random.Random(2)
    for i in range(16):
        s = ball(rnd.uniform(0.12, 0.25), (rnd.uniform(-0.7, 0.7), front + 1.2, 0.2), STINK, seg=12)
        t0 = m2 + round((N - m2) * (0.3 + 0.6 * i / 16))
        pop_in(s, t0, 6)
        key(s, "location", t0, s.location.copy())
        key(s, "location", min(N, t0 + 30), s.location + Vector((rnd.uniform(-0.6, 0.6), 0, 2.2)))
        pop_out(s, min(N - 1, t0 + 24), 6)
    scatter_rocks(20, (-5, 5), (1, 12), seed=4)
    hut((-3, 8), 0.9)
    camera((0, front - 9.5, 1.6), (0, front + 1, -1.1), lens=34,
           moves=[(1.0, (0.3, front - 8.2, 1.4), None)])


def shot_roman():
    front = -1.2
    layers = [(0.0, -0.4, STONE), (-0.4, -3.0, SOIL), (-3.0, -9, ROCK)]
    objs = section(front, layers=layers)
    # water channel under the seats
    ch_cut = box((14, 3.0, 1.6), (0, front + 0.3, -0.4 - 0.6))
    for o in objs[:2]:
        cut(o, ch_cut)
    box((14, 1.8, 0.7), (0, front + 0.9, -1.45), flowing("channel", "#5FA6CC", "#8ECCEA", scale=2.5, speed=(3, 0, 0)))
    # stone bench with holes
    bench = box((7, 1.7, 0.35), (0, front + 1.0, 0.85), STONE, bevel=0.04)
    for x in (-2.4, -0.8, 0.8, 2.4):
        cut(bench, cyl(0.28, 2, (x, front + 1.0, 0.85), smooth=False))
    for x in (-3.3, 0, 3.3):
        box((0.35, 1.5, 0.7), (x, front + 1.0, 0.35), STONE, bevel=0.03)
    box((8, 0.4, 2.6), (0, front + 2.2, 1.3), mat("wall_r", "#D9C9A8", noise=("#C7B490", 4)), bevel=0.04)
    for x in (-3.6, -1.2, 1.2, 3.6):
        cyl(0.22, 3.2, (x, front + 2.6, 1.6), mat("col", "#E8DFCC"), verts=16)
    rnd = random.Random(9)
    for i in range(6):
        w = ball(0.14, (-6, front + 0.5, -1.05), WASTE, seg=10, squash=0.6)
        t0 = F(0.15 + 0.12 * i)
        key(w, "location", t0, (-2.4 + 1.6 * (i % 4), front + 0.5, -0.2))
        key(w, "location", t0 + 8, (-2.4 + 1.6 * (i % 4), front + 0.5, -1.05))
        key(w, "location", min(N, t0 + 50), (8, front + 0.5, -1.05))
        pop_in(w, t0, 3)
    camera((-1.2, front - 6.5, 3.4), (0, front + 1, -0.2), lens=30, moves=[(1.0, (1.2, front - 6.0, 3.0), None)])


def toilet_box(x, y, m=WOOD):
    seat = box((1.2, 1.0, 0.9), (x, y, 0.45), m, bevel=0.03)
    cut(seat, cyl(0.3, 2, (x, y, 0.9), smooth=False))
    return seat


def shot_harington():
    ground()
    box((7, 0.3, 4.2), (0, 1.6, 2.1), mat("plaster", "#E6DCC8", noise=("#D8CDB6", 3)))
    box((7, 4, 0.08), (0, -0.4, 0.04), mat("floor", "#A07A52", noise=("#8B6744", 5)))
    toilet_box(0, 0.6)
    tank = box((1.0, 0.6, 0.7), (0, 1.2, 2.7), WOOD, bevel=0.04)
    for x in (-0.45, 0.45):
        box((0.08, 0.08, 2.0), (x, 1.2, 1.3), WOOD)
    pipe = cyl(0.07, 1.4, (0.35, 1.0, 1.65), PIPE, verts=16)
    # a slug of water falls from the tank through the pipe into the seat
    for i in range(3):
        d = ball(0.11, (0.35, 1.0, 2.3), mat(f"drop{i}", "#6FB7E3", rough=0.1), seg=12, squash=1.6)
        t0 = F(0.35 + 0.15 * i)
        pop_in(d, t0, 3)
        key(d, "location", t0, (0.35, 1.0, 2.3))
        key(d, "location", t0 + 14, (0.0, 0.6, 0.6))
        pop_out(d, t0 + 14, 3)
    camera((2.2, -5.5, 2.6), (0, 0.8, 1.3), lens=36, moves=[(1.0, (1.4, -4.6, 2.3), None)])


def bathroom_section(front=-1.0):
    """Floor slab on top, open service space below with a dark back wall."""
    slab = box((16, 3.0, 0.3), (0, front + 1.5, -0.15), mat("slab", "#C8C3BA"))
    box((16, 0.3, 6), (0, front + 3.0, 3.0), WALL)                       # bathroom wall
    box((16, 0.3, 5.5), (0, front + 3.0, -3.05), mat("back", "#6B6158"))   # back wall below floor
    box((16, 3.0, 3), (0, front + 1.5, -7.3), ROCK)
    box((16, 3.0, 0.08), (0, front + 1.5, 0.04), TILE)
    return [slab]


def bowl(x, y):
    b = cyl(0.32, 0.8, (x, y, 0.4), PORCELAIN, r2=0.55, verts=40)
    b.rotation_euler = (0, 0, 0)
    b.scale = (1, 1, 1)
    b.location.z = 0.4
    b.data.vertices  # noqa
    torus(0.48, 0.07, (x, y, 0.82), PORCELAIN)
    return b


def smell_column(x, y, z0, z_stop, start_t, count=14, seed=1, spread=0.5):
    rnd = random.Random(seed)
    for i in range(count):
        s = ball(rnd.uniform(0.09, 0.15), (x, y, z0), STINK, seg=12)
        t0 = F(start_t + (1 - start_t) * 0.85 * i / count)
        pop_in(s, t0, 5)
        key(s, "location", t0, (x + rnd.uniform(-0.1, 0.1), y, z0))
        end = min(N, t0 + 26)
        key(s, "location", end, (x + rnd.uniform(-spread, spread), y, z_stop + rnd.uniform(-0.1, 0.3)))
        pop_out(s, max(t0 + 6, end - 5), 5)


def shot_smell():
    front = -1.0
    objs = bathroom_section(front)
    y = front + 1.2
    bowl(0, y)
    box((0.9, 0.35, 0.8), (0, y + 0.7, 1.15), PORCELAIN, bevel=0.06)
    pipe = cyl(0.25, 4.8, (0, y, -2.7), GLASS, verts=32)
    box((14, 1.6, 1.0), (0, y, -5.3), flowing("sewer_flow", "#6E5236", "#8A6A47", scale=3, speed=(2, 0, 0)))
    smell_column(0, y, -4.8, 2.4, 0.15, count=18, seed=3)
    camera((0, front - 7.2, 0.4), (0, y, -1.8), lens=30, moves=[(1.0, (0.3, front - 6.6, 0.4), None)])


def shot_strap():
    front = -1.0
    bathroom_section(front)
    y = front + 1.2
    bowl(0, y)
    box((0.9, 0.35, 0.8), (0, y + 0.7, 1.15), PORCELAIN, bevel=0.06)
    # S-bend: down, under, up, over, down to the sewer
    pts = [(0, y, 0.1), (0, y, -1.0), (0.45, y, -1.9), (1.0, y, -1.0), (1.4, y, -0.6),
           (1.9, y, -1.3), (1.9, y, -3.0), (1.9, y, -4.8)]
    curve_tube(pts, 0.24, GLASS)
    # trapped water in the lowest bend
    water = curve_tube([(0, y, -1.15), (0.45, y, -1.9), (0.95, y, -1.15)], 0.2,
                       mat("trap_water", "#2F8FE0", rough=0.1, emit=0.6))
    water.data.bevel_factor_end = 1.0
    water.data.bevel_factor_mapping_end = "SPLINE"
    water.data.bevel_factor_end = 0.0
    water.data.keyframe_insert("bevel_factor_end", frame=1)
    water.data.keyframe_insert("bevel_factor_end", frame=F(0.15))
    water.data.bevel_factor_end = 1.0
    water.data.keyframe_insert("bevel_factor_end", frame=F(0.32))
    box((14, 1.6, 1.0), (0, y, -5.3), flowing("sewer_flow", "#6E5236", "#8A6A47", scale=3, speed=(2, 0, 0)))
    # smell rises from the sewer but stops at the water
    smell_column(1.9, y, -4.8, -1.45, 0.4, count=14, seed=5, spread=0.05)
    camera((0.9, front - 7.2, 0.3), (0.9, y, -1.8), lens=30, moves=[(1.0, (1.1, front - 6.6, 0.3), None)])


def shot_sewer():
    front = -1.0
    objs = section(front, layers=[(0.0, -0.3, mat("road", "#8F8A82")), (-0.3, -6.0, SOIL), (-6.0, -12, ROCK)])
    Y = front + 0.6
    tunnel_cut = cyl(1.3, 30, (0, Y, -4.0), rot=(0, math.pi / 2, 0), smooth=False)
    cut(objs[1], tunnel_cut)
    tube = cyl(1.3, 30, (0, Y, -4.0), mat("brick", "#A4664A", noise=("#8D5640", 6)), rot=(0, math.pi / 2, 0))
    tube_in = cyl(1.1, 31, (0, Y, -4.0), rot=(0, math.pi / 2, 0), smooth=False)
    cut(tube, tube_in)
    cut(tube, box((32, 3, 4), (0, Y - 1.5, -4.0)))   # open the front half
    box((30, 1.1, 0.6), (0, Y + 0.45, -4.75), flowing("sewage", "#6E5236", "#8F6F4A", scale=2.5, speed=(3, 0, 0)))
    for i, x in enumerate((-3.0, 0.0, 3.0)):
        house((x, front + 1.2), 1.1, ["#E9DCC6", "#DCC8B0", "#EAD7C0"][i])
        p = cyl(0.14, 3.0, (x + 0.3, Y, -1.5), PIPE, verts=16)
        pc = box((0.6, 2.0, 3.0), (x + 0.3, Y - 0.6, -1.5))
        cut(objs[1], pc)
        for k in range(3):
            w = ball(0.13, (x + 0.3, Y - 0.15, -0.4), WASTE, seg=8)
            t0 = F(0.15 + 0.22 * k + 0.05 * i)
            pop_in(w, t0, 3)
            key(w, "location", t0, (x + 0.3, Y - 0.15, -0.4))
            key(w, "location", t0 + 12, (x + 0.3, Y + 0.2, -4.4))
            key(w, "location", min(N, t0 + 60), (x + 6, Y + 0.2, -4.4))
    camera((0, front - 8.5, 0.6), (0, front + 1, -2.0), lens=30, moves=[(1.0, (0.8, front - 7.8, 0.6), None)])


def modern_toilet(x, y):
    base = cyl(0.42, 0.75, (x, y, 0.375), PORCELAIN, r2=0.3, verts=48)
    bowl_ = cyl(0.62, 0.32, (x, y - 0.1, 0.78), PORCELAIN, r2=0.52, verts=48)
    bowl_.scale.y = 1.25
    torus(0.52, 0.06, (x, y - 0.1, 0.96), PORCELAIN).scale.y = 1.25
    water = cyl(0.42, 0.02, (x, y - 0.1, 0.88), mat("bowl_water", "#9ED3F0", rough=0.05))
    water.scale.y = 1.25
    tank = box((1.0, 0.4, 0.9), (x, y + 0.65, 1.25), PORCELAIN, bevel=0.06)
    btn = cyl(0.09, 0.05, (x, y + 0.65, 1.72), CHROME, verts=24)
    return btn, water


def shot_modern():
    box((12, 12, 0.05), (0, 2, -0.025), TILE)
    for i in range(-6, 7):
        box((0.02, 12, 0.052), (i * 0.6, 2, -0.02), mat("grout", "#C9C4BC"))
        box((12, 0.02, 0.052), (0, 2 + i * 0.6, -0.02), mat("grout", "#C9C4BC"))
    box((12, 0.2, 5), (0, 1.25, 2.5), WALL)
    btn, water = modern_toilet(0, 0.4)
    press = F(0.35)
    key(btn, "location", press - 3, btn.location.copy())
    key(btn, "location", press, btn.location - Vector((0, 0, 0.03)))
    key(btn, "location", press + 5, btn.location.copy() + Vector((0, 0, 0.03)))
    key(water, "rotation_euler", press, (0, 0, 0))
    key(water, "rotation_euler", N, (0, 0, math.radians(720)))
    cam_l = (1.4, -3.2, 2.5)
    camera(cam_l, (0, 0.4, 1.0), lens=32, moves=[(0.3, (0.6, -2.4, 2.3), (0, 0.5, 1.4)),
                                                 (1.0, (0.3, -1.6, 2.4), (0, 0.6, 1.6))])


def shot_plant():
    ground(m=GRASS)
    flow_m = flowing("tank_water", "#5C9FC4", "#7FBEDD", scale=2, speed=(1, 1, 0))
    for x, y, r in [(-3.5, 3, 2.0), (1.2, 3.5, 2.0), (-1.2, 8.5, 2.4), (4.4, 8.5, 1.6)]:
        t = cyl(r, 1.0, (x, y, 0.5), CONCRETE, verts=48)
        cut(t, cyl(r - 0.18, 1.0, (x, y, 1.1), smooth=False, verts=48))
        w = cyl(r - 0.18, 0.05, (x, y, 0.85), flow_m, verts=48)
        arm = box((r * 2 - 0.3, 0.12, 0.12), (x, y, 1.15), PIPE)
        key(arm, "rotation_euler", 1, (0, 0, 0))
        key(arm, "rotation_euler", N, (0, 0, math.radians(120)))
        linear(arm)
    box((3, 2, 1.6), (6.0, 2.0, 0.8), CONCRETE, bevel=0.05)
    box((40, 3.0, 0.06), (0, 14, -0.02), flowing("river2", "#6FB4D8", "#93CFEA", scale=3, speed=(2, 0, 0)))
    for x in (-5.5, 6.5, -6.0):
        cyl(0.12, 1.0, (x, -1.0, 0.5), WOOD, verts=8)
        ball(0.7, (x, -1.0, 1.5), mat("tree", "#6E9A4C"), seg=10)
    camera((-1, -6, 6.5), (0, 5, 0), lens=26, moves=[(1.0, (4, -4.5, 5.5), (0, 6, 0))])


# ---------------------------------------------------------------- main
world_setup()
globals()["shot_" + SHOT]()
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action and o.name.startswith("tube") is False:
        pass

if STILL is not None:
    sc = bpy.context.scene
    sc.frame_set(STILL)
    sc.render.filepath = str(HERE / "stills" / f"{SHOT}_{STILL:04d}.png")
    bpy.ops.render.render(write_still=True)
else:
    if "--range" in ARGS:
        a, b = ARGS[ARGS.index("--range") + 1].split("-")
        bpy.context.scene.frame_start, bpy.context.scene.frame_end = int(a), int(b)
    bpy.ops.render.render(animation=True)
