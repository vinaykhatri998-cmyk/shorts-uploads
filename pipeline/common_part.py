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


