"""Derive the 7 elementary ray-sets from scratch and export their coordinates.

A dot arrangement on a sphere is "elementary" here if it is a *single orbit*
under one of the three polyhedral rotation groups (T, O, I): pick a group and one
of its pole families (faces / corners / edges), and every dot can be rotated onto
every other dot while the whole set maps back onto itself.

This script:
  1. builds T, O, I by closing two generator rotations each,
  2. finds each group's pole families (orbits),
  3. shows the naive 9 candidates (3 groups x 3 families) collapse to 7 by
     proving -- with an explicit rotation, not just matching counts --
     that two of T's three families are redundant,
  4. writes data.js for the HTML renders.

Run: python3 script.py
"""
from collections import namedtuple
from itertools import combinations
import json
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

PHI = (1 + 5 ** 0.5) / 2
TOL = 1e-6

Family = namedtuple("Family", "shape size rays")


def rot(axis, angle):
    x, y, z = np.array(axis, float) / np.linalg.norm(axis)
    c, s, C = np.cos(angle), np.sin(angle), 1 - np.cos(angle)
    return np.array([
        [x*x*C + c,   x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, y*y*C + c,   y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, z*z*C + c],
    ])


def close(gens):
    """All rotations reachable by multiplying the generators together."""
    G = [np.eye(3)]
    seen = lambda M: any(np.allclose(M, H, atol=TOL) for H in G)
    changed = True
    while changed:
        changed = False
        for A in list(G):
            for B in gens:
                M = A @ B
                if not seen(M):
                    G.append(M)
                    changed = True
    return G


def families(G):
    """Orbits of rotation axes (poles) under the group G, smallest first."""
    poles = []
    for M in G:
        if np.allclose(M, np.eye(3), atol=TOL):
            continue
        w, v = np.linalg.eig(M)
        a = np.real(v[:, np.argmin(np.abs(w - 1))])
        a = a / np.linalg.norm(a)
        for p in (a, -a):
            if not any(np.allclose(p, q, atol=TOL) for q in poles):
                poles.append(p)

    fams, placed = [], []
    for p in poles:
        if any(np.allclose(p, q, atol=TOL) for q in placed):
            continue
        orbit = []
        for M in G:
            q = M @ p
            if not any(np.allclose(q, r, atol=TOL) for r in orbit):
                orbit.append(q)
        fams.append(np.array(orbit))
        placed += orbit
    return sorted(fams, key=len)


def fingerprint(R, decimals=6):
    """Sorted pairwise dot products: invariant under rotation and reflection."""
    return tuple(np.round(np.sort((R @ R.T).ravel()), decimals))


def align(A, B):
    """A rotation carrying ray-set A onto ray-set B, or None.

    Reflections are skipped: arrangements only count as the same if one is a
    rotated copy of the other.
    """
    if len(A) != len(B):
        return None
    for idx in combinations(range(len(A)), 3):
        P = A[list(idx)].T
        if abs(np.linalg.det(P)) > 0.1:
            break
    else:
        return None
    a1, a2, a3 = A[list(idx)]
    d12, d13, d23 = a1 @ a2, a1 @ a3, a2 @ a3
    Pinv = np.linalg.inv(P)
    for b1 in B:
        for b2 in B:
            if abs(b1 @ b2 - d12) > TOL:
                continue
            for b3 in B:
                if abs(b1 @ b3 - d13) > TOL or abs(b2 @ b3 - d23) > TOL:
                    continue
                M = np.column_stack([b1, b2, b3]) @ Pinv
                if not np.allclose(M.T @ M, np.eye(3), atol=TOL):
                    continue
                if np.linalg.det(M) < 0:
                    continue
                if all(any(np.allclose(M @ a, b, atol=TOL) for b in B) for a in A):
                    return M
    return None


def _wind(axis, pts):
    """Order points into a ring, wound around `axis` (for drawing as a polygon)."""
    u = np.cross(axis, [1, 0, 0])
    if np.linalg.norm(u) < 0.1:
        u = np.cross(axis, [0, 1, 0])
    u = u / np.linalg.norm(u)
    w = np.cross(axis, u)
    center = np.mean(pts, axis=0)
    pts = sorted(pts, key=lambda p: np.arctan2((p - center) @ w, (p - center) @ u))
    return [p.tolist() for p in pts]


def vertex_polyhedron(rays):
    """Convex hull of the rays: rays become vertices. Returns wound face polygons
    (coplanar hull triangles merged back into their real face, e.g. squares stay
    squares instead of showing as two triangles with a diagonal seam)."""
    hull = ConvexHull(rays)
    eqs = np.round(hull.equations, 6)
    faces = []
    for eq in {tuple(e) for e in eqs}:
        idx = np.where((eqs == eq).all(axis=1))[0]
        verts_idx = sorted(set(hull.simplices[idx].ravel()))
        pts = rays[verts_idx]
        faces.append(_wind(np.array(eq[:3]), pts))
    return faces


def face_polyhedron(rays, offset=1.0):
    """Plane perpendicular to each ray, slid in to `offset`: rays become faces.

    Returns ordered polygon loops (one per ray/face) as lists of 3D points, found
    via half-space intersection then sorting each face's vertices angularly
    around its own normal.
    """
    halfspaces = np.hstack([rays, -offset * np.ones((len(rays), 1))])
    hs = HalfspaceIntersection(halfspaces, np.zeros(3))
    verts = hs.intersections

    faces = []
    for r in rays:
        on_face = [v for v in verts if abs(v @ r - offset) < 1e-6]
        if len(on_face) < 3:
            continue
        faces.append(_wind(r, on_face))
    return faces


NAMES = {
    (4, "T"): "tetrahedron",
    (6, "O"): "octahedron",
    (8, "O"): "cube",
    (12, "O"): "cuboctahedron",
    (12, "I"): "icosahedron",
    (20, "I"): "dodecahedron",
    (30, "I"): "icosidodecahedron",
}


def main():
    groups = {
        "T": close([rot([1, 0, 0], np.pi),      rot([1, 1, 1], 2*np.pi/3)]),
        "O": close([rot([0, 0, 1], np.pi/2),    rot([1, 1, 1], 2*np.pi/3)]),
        "I": close([rot([0, 1, PHI], 2*np.pi/5), rot([0, -1, PHI], 2*np.pi/5)]),
    }

    candidates = []
    for shape, G in groups.items():
        for fam in families(G):
            candidates.append(Family(shape, len(fam), fam))

    print(f"{len(candidates)} naive candidates (3 groups x 3 families each):")
    for f in candidates:
        print(f"  {f.shape} · {f.size:>2}")

    fps = [fingerprint(f.rays) for f in candidates]
    prefer = {"O": 0, "I": 1, "T": 2}          # keep the more familiar group's name
    order = sorted(range(len(candidates)), key=lambda i: prefer[candidates[i].shape])

    kept, merged = [], {}
    for i in order:
        for r in kept:
            if fps[i] == fps[r]:
                M = align(candidates[i].rays, candidates[r].rays)
                if M is not None:
                    merged[i] = (r, M)
                    break
        else:
            kept.append(i)
    kept = sorted(kept)

    print(f"\n{len(candidates)} -> {len(kept)} distinct")
    print("\nmerged away (each confirmed by an explicit rotation):")
    for i, (r, M) in sorted(merged.items()):
        a, b = candidates[i], candidates[r]
        print(f"  {a.shape} · {a.size:<2} = {b.shape} · {b.size}")

    print(f"\nthe {len(kept)} elementary ray-sets:")
    export = []
    for i in kept:
        f = candidates[i]
        name = NAMES[(f.size, f.shape)]
        print(f"  {f.shape} · {f.size:<2} rays  ({name})")
        export.append({
            "shape": f.shape,
            "size": f.size,
            "name": name,
            "rays": f.rays.round(6).tolist(),
            "vertexFaces": vertex_polyhedron(f.rays),
            "dualFaces": face_polyhedron(f.rays),
        })

    export.sort(key=lambda e: e["size"])
    out_path = "renders/data.js"
    with open(out_path, "w") as fh:
        fh.write("const RAYSETS = ")
        json.dump(export, fh, indent=2)
        fh.write(";\n")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
