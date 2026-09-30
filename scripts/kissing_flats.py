"""Kissing-flats balls: printable models and a render of all 7.

Start from a ball and grind one round flat at each dot, all at the same depth,
stopping the moment neighbouring flats touch. The flats are the dots, the
touching points are the edges, and the leftover curved patches are the faces of
the vertex solid. Keep grinding and each ball turns into its face solid.

This script:
  1. builds the 7 dot arrangements,
  2. writes one STL per ball to models/kissing-flats-<D>mm/, resting on a flat,
  3. ray-casts the 7 into images/kissing-flats.png.

Run: python3 scripts/kissing_flats.py              (20 mm balls)
     python3 scripts/kissing_flats.py --diameter 25
Needs numpy, matplotlib, trimesh and manifold3d.
"""
import argparse
import itertools
import os
import numpy as np

PHI = (1 + 5 ** 0.5) / 2

BALLS = [  # name, family
    ("tetrahedron", "tetrahedral"),
    ("octahedron", "octahedral"),
    ("cube", "octahedral"),
    ("cuboctahedron", "octahedral"),
    ("icosahedron", "icosahedral"),
    ("dodecahedron", "icosahedral"),
    ("icosidodecahedron", "icosahedral"),
]


# ---------- dot arrangements ----------

def cyc(v):
    x, y, z = v
    return [(x, y, z), (z, x, y), (y, z, x)]


def signs(v):
    return list({tuple(a * b for a, b in zip(s, v)) for s in itertools.product([1, -1], repeat=3)})


def raw(name):
    if name == "tetrahedron":
        return [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    if name == "octahedron":
        return [p for v in cyc((1, 0, 0)) for p in signs(v)]
    if name == "cube":
        return signs((1, 1, 1))
    if name == "cuboctahedron":
        return [p for v in cyc((1, 1, 0)) for p in signs(v)]
    if name == "icosahedron":
        return [p for v in cyc((0, 1, PHI)) for p in signs(v)]
    if name == "dodecahedron":
        return signs((1, 1, 1)) + [p for v in cyc((0, 1 / PHI, PHI)) for p in signs(v)]
    if name == "icosidodecahedron":
        return ([p for v in cyc((0, 0, PHI)) for p in signs(v)] +
                [p for v in cyc((0.5, PHI / 2, PHI ** 2 / 2)) for p in signs(v)])
    raise ValueError(name)


def rot_to(a, b):
    """Rotation matrix taking unit vector a to unit vector b."""
    v = np.cross(a, b)
    c = float(np.dot(a, b))
    if np.linalg.norm(v) < 1e-12:
        if c > 0:
            return np.eye(3)
        p = np.array([1, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1, 0])
        p = p - a * np.dot(p, a)
        p /= np.linalg.norm(p)
        return 2 * np.outer(p, p) - np.eye(3)
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K * (1 / (1 + c))


def axis_angle(axis, ang):
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def directions(name):
    """Unit dot directions, dot 0 straight down, its nearest neighbour in the x-z plane."""
    P = []
    for p in raw(name):
        p = np.array(p, float)
        if not any(np.allclose(p, q) for q in P):
            P.append(p)
    P = np.array(P)
    P /= np.linalg.norm(P, axis=1)[:, None]
    ref = P[np.lexsort((P[:, 0], P[:, 1], -P[:, 2]))[0]]
    P = P @ rot_to(ref, np.array([0, 0, -1.0])).T
    d = P @ np.array([0, 0, -1.0])
    nb = P[np.argsort(-np.where(d > 1 - 1e-9, -9, d))[0]]
    P = P @ axis_angle(np.array([0, 0, 1.0]), -np.arctan2(nb[1], nb[0])).T
    P[np.abs(P) < 1e-12] = 0.0
    order = np.lexsort((np.round(np.degrees(np.arctan2(P[:, 1], P[:, 0])) % 360, 6), np.round(P[:, 2], 9)))
    return P[order]


def kiss(P):
    """Angle to the nearest neighbour, and how many neighbours sit at that angle."""
    G = P @ P.T
    np.fill_diagonal(G, -2)
    theta = np.arccos(G.max())
    return theta, int((np.abs(G[0] - G.max()) < 1e-9).sum())


# ---------- STL models ----------

def write_models(diameter, out_dir):
    import manifold3d as mf
    import trimesh

    R = diameter / 2
    os.makedirs(out_dir, exist_ok=True)
    print(f"{'ball':18s} flats  flat width  depth   brass")
    for i, (name, _) in enumerate(BALLS, 1):
        P = directions(name)
        P = P @ rot_to(P[0], np.array([0, 0, -1.0])).T      # rest on flat 1
        theta, _ = kiss(P)
        # A 0.5 micron overlap makes touching flats share a tiny real edge instead of
        # meeting at a single point, which mesh checkers reject as non-manifold.
        h = R * np.cos(theta / 2) - 0.0005
        m = mf.Manifold.sphere(R, 480)
        for n in P:
            m = m.trim_by_plane((-n).tolist(), -h)           # keep n.x <= h
        mesh = m.to_mesh()
        t = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts))
        assert t.is_watertight and t.euler_number == 2, name
        t.export(os.path.join(out_dir, f"{i}_{name}_{len(P)}_flats.stl"))
        print(f"{name:18s} {len(P):5d}  {2 * R * np.sin(theta / 2):7.2f} mm  {R - h:4.2f} mm  "
              f"{t.volume / 1000 * 8.5:3.0f} g")


# ---------- render ----------

TILE, SS = 560, 2


def orient(P):
    v0 = np.array([0.28, 0.42, 0.86])
    v0 /= np.linalg.norm(v0)
    Q = P @ rot_to(P[0], v0).T
    return Q @ axis_angle(v0, 0.35).T


def raycast(P, h, R=1.0):
    """Orthographic ray-cast of a unit ball cut by the planes n.x <= h, shaded as brass."""
    n = TILE * SS
    c = (np.arange(n) + 0.5) / n * 2.3 - 1.15
    x, y = np.meshgrid(c, -c)
    rho2 = x * x + y * y
    inside = rho2 < R * R
    s = np.sqrt(np.clip(R * R - rho2, 0, None))
    zin, zout = s.copy(), -s.copy()
    src = np.full(x.shape, -1)
    for i, nv in enumerate(P):
        rhs = h - nv[0] * x - nv[1] * y
        if nv[2] > 1e-9:
            b = rhs / nv[2]
            m = b < zin
            zin[m] = b[m]
            src[m] = i
        elif nv[2] < -1e-9:
            zout = np.maximum(zout, rhs / nv[2])
        else:
            inside &= rhs >= 0
    hit = inside & (zin >= zout)
    N = np.stack([x, y, zin], -1) / R
    for i in range(len(P)):
        N[src == i] = P[i]
    N /= np.linalg.norm(N, axis=-1, keepdims=True)
    V = np.array([0, 0, 1.0])
    Rf = 2 * (N @ V)[..., None] * N - V
    key = np.array([-0.45, 0.62, 0.64]); key /= np.linalg.norm(key)
    fill = np.array([0.75, 0.15, 0.64]); fill /= np.linalg.norm(fill)
    sky = np.clip((Rf[..., 1] + 0.6) / 1.5, 0, 1)
    env = 0.25 + 0.6 * sky + 0.9 * np.exp(-np.sum((Rf - key) ** 2, -1) / 0.10)
    dk = np.clip(N @ key, 0, None)
    df = np.clip(N @ fill, 0, None)
    bounce = np.clip(-N[..., 1], 0, None)
    brass = np.array([0.86, 0.66, 0.36])
    col = brass * (0.30 + 0.50 * dk + 0.28 * df + 0.14 * bounce + 0.32 * env)[..., None]
    col += 0.45 * (np.clip(Rf @ key, 0, None) ** 60)[..., None]
    col = col / (1 + 0.25 * col)
    bg = np.array([0.935, 0.93, 0.92])
    shadow = np.exp(-((x / 0.62) ** 2 + ((y + 1.03) / 0.07) ** 2))
    img = np.where(hit[..., None], col, bg * (1 - 0.22 * shadow)[..., None])
    return np.clip(img.reshape(TILE, SS, TILE, SS, 3).mean((1, 3)), 0, 1)


def write_render(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    tiles = []
    for name, _ in BALLS:
        P = orient(directions(name))
        theta, nbrs = kiss(P)
        tiles.append((name, len(P), nbrs, raycast(P, np.cos(theta / 2))))

    bg = (0.935, 0.93, 0.92)
    fig = plt.figure(figsize=(15, 16.2), dpi=100, facecolor=bg)
    rows = [[0], [1, 2, 3], [4, 5, 6]]
    for r, (row, fam) in enumerate(zip(rows, ["Tetrahedral", "Octahedral", "Icosahedral"])):
        base = 0.675 - r * 0.31
        for c, idx in enumerate(row):
            name, n, nb, img = tiles[idx]
            cx = 0.5 if len(row) == 1 else (c + 0.5) / 3
            ax = fig.add_axes([cx - 0.145, base + 0.02, 0.29, 0.24])
            ax.imshow(img)
            ax.axis("off")
            fig.text(cx, base + 0.012, name.capitalize(), ha="center", va="top",
                     fontsize=17, fontweight="bold", color="#1d242b")
            fig.text(cx, base - 0.012, f"{n} flats, each touching {nb}", ha="center", va="top",
                     fontsize=13, color="#56606a")
        fig.text(0.04, base + 0.25, fam.upper(), fontsize=11, color="#8a6424", fontweight="bold")
    fig.text(0.5, 0.985, "The seven kissing-flats balls", ha="center", va="top",
             fontsize=24, fontweight="bold", color="#1d242b")
    fig.text(0.5, 0.958, "One round flat at each of the riddle's dots, cut until neighbouring flats just touch",
             ha="center", va="top", fontsize=14, color="#56606a")
    fig.savefig(path, facecolor=bg)
    print(f"wrote {os.path.relpath(path)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--diameter", type=float, default=20.0, help="ball diameter in mm (default 20)")
    args = ap.parse_args()
    d = f"{args.diameter:g}"
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    write_models(args.diameter, os.path.join(root, "models", f"kissing-flats-{d}mm"))
    write_render(os.path.join(root, "images", "kissing-flats.png"))
