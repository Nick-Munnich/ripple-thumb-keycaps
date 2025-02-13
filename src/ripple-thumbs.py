from build123d import *

__solder_tol = 1.4*MM

__all_parts = Pos(6.11, -12.28, 0.25) * Rot(90, 90, 0) * \
     import_step('src/assets/thumb_cluster.step')
# Originally created in another CAD program
# Full migration to build123d tbd

__p1 = split(__all_parts, Plane.YZ,keep=Keep.BOTTOM)
__p1 = Rot(0,0,-90) *Pos(65.65,-14.77,-0.25) * split(__p1, Plane.XZ,keep=Keep.BOTTOM)
reach1, mid1, tuck1 = split(Pos(-9,0,0) * __p1, Plane.YZ, keep=Keep.BOTH)
tuck = Pos(9,0,0) * tuck1
mid = Rot(0,0,10) * Pos(-10,4,0) * mid1
reach = Rot(0,0,16) * Pos(-28.5,8,0) * reach1
keycaps = [tuck, mid, reach]

# choc stem
cross = Box(8.9, 0.5, 0.4, align=(Align.CENTER, Align.CENTER, Align.MAX)) \
    + [Pos(0,0), Pos(-8.9/2 + .25,0), Pos(8.9/2-.25)] * Box(0.5, 3.5, 0.4,align=(Align.CENTER, Align.CENTER, Align.MAX))
stem = Box(1.2, 3, 3.1,align=(Align.CENTER, Align.CENTER, Align.MAX)) - [Pos(3.9,0), Pos(-3.9, 0)] * Cylinder(3.5, 3.1, align=(Align.CENTER, Align.CENTER, Align.MAX))
stem = fillet(stem.edges().group_by(Axis.Z)[:-1], 0.15)
choc_stem = cross + [Pos(2.85, 0), Pos(-2.85, 0)] * stem
choc_caps = [x + choc_stem for x in keycaps]

# mx stem
mx_stem = Cylinder(5.6/2, 4.4,align=(Align.CENTER, Align.CENTER, Align.MAX)) \
    - [Rot(0,0,90), Rot(0,0)] * Box(4.1, 1.35, 4.4,align=(Align.CENTER, Align.CENTER, Align.MAX))
mx_stem = fillet(mx_stem.edges().sort_by_distance((0,0,-2))[:4], 0.3)


__BRIM_STEM_DIST = -1.1
mx_caps = []
for cap in keycaps:
    bottom_face = cap.faces().sort_by(Axis.Z)[0]
    extrusion_dist = bottom_face.center().Z
    mx_cap = cap + extrude(bottom_face, -(-4.4-extrusion_dist - __BRIM_STEM_DIST))
    mx_caps.append(mx_cap + mx_stem)

def make_sprues(caps):
    sprue_caps = [
        Pos(8.75, -9) *  caps[0], 
        Pos(19+18+8.75,-4-9) *  Rot(0,0,-10) *caps[1],
        Pos(19+8.18-.5,-8-9+1.89) *Rot(0,0,0) *caps[2],
        ]
    sprues = [Pos(42, -3, -0.4),Pos(52, -3, -0.4),Pos(30, -3, -0.4),Pos(23, -3, -0.4), Pos(5.75, -3, -0.4), Pos(11.75, -3, -0.4)] * Cylinder(0.75, 6, align=(Align.CENTER, Align.CENTER, Align.MAX))
    sprue = Pos(5,-3,-6.4) * Rot(0,90) * Cylinder(.75,48, align=(Align.CENTER, Align.CENTER, Align.MIN))
    midsprues = [Pos(42,0,-6.4),Pos(52,0,-6.4),Pos(30,0,-6.4),Pos(23,0,-6.4),Pos(11.75,0,-6.4),Pos(5.75,0,-6.4)] * (Rot(90,0) * Cylinder(0.75, 3, align=(Align.CENTER, Align.CENTER, Align.MIN)))

    sprued = sprue + sprue_caps + sprues + midsprues
    sprued += mirror(sprued)
    return sprued

names = ['tuck', 'mid', 'reach']

for cap,name in zip(choc_caps,names):
    print(f"Export success stl/choc-{name}-left.stl: {export_stl(cap, f"stl/choc-{name}-left.stl")}")
    print(f"Export success stl/choc-{name}-right.stl: {export_stl(mirror(cap, Plane.YZ), f"stl/choc-{name}-right.stl")}")

for cap,name in zip(mx_caps,names):
    print(f"Export success stl/mx-{name}-left.stl: {export_stl(cap, f"stl/mx-{name}-left.stl")}")
    print(f"Export success stl/mx-{name}-right.stl: {export_stl(mirror(cap, Plane.YZ), f"stl/mx-{name}-right.stl")}")

print(f"Export success stl/mx-sprued.stl: {export_stl(make_sprues(mx_caps), f"stl/mx-sprued.stl")}")
print(f"Export success stl/choc-sprued.stl: {export_stl(make_sprues(choc_caps), f"stl/choc-sprued.stl")}")


if __name__ == '__main__':
    from ocp_vscode import *
    show_all()
