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


