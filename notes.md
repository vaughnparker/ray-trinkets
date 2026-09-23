# ray-trinkets

Physical objects (3D print / wood / metal) built from a simple idea: a sphere with
dots on it, placed so that **you can rotate the sphere and map every dot onto every
other dot.** Spin-off of the [`ray-sets`](../ray-sets) project — same underlying
math, aimed at a physical trinket instead of a puzzle.

## The symmetry, precisely

A dot arrangement qualifies if the sphere's rotation group acts **transitively**
on the dots — i.e. the dots form a single orbit under some group of rotations.
Concretely: there must exist rotations taking any one dot to any other, all of
which also map the *whole set* of dots back onto itself (closure).

Two families of rotation groups can do this:

- **Polyhedral (T, O, I)** — the rigid symmetries of the tetrahedron, cube/octahedron,
  and dodecahedron/icosahedron. For a fixed group and a fixed orbit ("family" of
  poles: faces, corners, or edges), the dot positions are **pinned down exactly** —
  no free parameters once you pick the group and the family.
- **Cyclic/dihedral (C_n, D_n)** — one axis, n-fold symmetry. These are **degenerate**
  for this purpose: not only is there one such ring for every n (infinite), but for
  a *fixed* n there's a continuous free choice of latitude for the ring. Two
  independent infinities. Excluded for being underdetermined, not for being large.

So restricting to polyhedral symmetry is what makes this a finite, well-posed
question rather than a knob to fiddle with.

## Why exactly 7

T, O, I each have three orbit types ("pole families"): faces, corners, edges.
3 groups x 3 families = 9 naive candidates, but:

- T's own 3 families collapse to 1 distinct: two are mirror images of each other,
  and the third (T's edge-midpoints) coincides exactly with O's face family
  (a tetrahedron's edge midpoints are an octahedron's vertices).
- O and I's families are each already distinct from one another and from T.

Net: **1 (from T) + 3 (from O) + 3 (from I) = 7 elementary ray-sets.**

`script.py` builds this from scratch: constructs T/O/I by closing two generator
rotations, extracts orbits, and *proves* the T-family collapses (via an explicit
orthogonal map, not just a coincidence-of-counts) rather than asserting it.

## The 7

| label | dots | shape (as spike positions) |
|---|---|---|
| T · 4  |  4 | tetrahedron vertices |
| O · 6  |  6 | octahedron vertices |
| O · 8  |  8 | cube vertices |
| O · 12 | 12 | cuboctahedron vertices |
| I · 12 | 12 | icosahedron vertices |
| I · 20 | 20 | dodecahedron vertices |
| I · 30 | 30 | icosidodecahedron vertices |

## Physical form — three options

1. **Ball-and-spike.** Literal rays as thin cylinders poking out of a sphere.
   Most direct reading of the math; fragile at small scale, especially at 30 dots.
2. **Vertex polyhedron** (convex hull of the dots). Solid, no fragile parts.
   Gives, per row above: tetrahedron, octahedron, cube, cuboctahedron, icosahedron,
   dodecahedron, icosidodecahedron — the 5 Platonic solids plus the 2 **quasiregular**
   solids (the only two solids where two kinds of regular polygon alternate around
   every vertex).
3. **Face polyhedron** (dual). Put a plane perpendicular to each ray and slide it
   inward until neighboring cuts meet — same physical process as "shaving flats
   into a sphere." Gives: tetrahedron, cube, octahedron, rhombic dodecahedron,
   dodecahedron, icosahedron, rhombic triacontahedron — the 5 Platonic solids plus
   the 2 **edge-transitive Catalan solids** (duals of the quasiregular pair above).

Columns 2 and 3 are each independently a complete, classically-named set. Together
they span all **9 convex edge-transitive (isotoxal) polyhedra** that exist — the 5
Platonic solids appear once, shared by both columns.

## Status

- [x] Define the symmetry and why it's finite (this file)
- [x] `script.py` — derive and verify the 7 from scratch
- [x] [`riddle.md`](riddle.md) — the riddle's restrictions, equivalent phrasings, and ones that fail
- [x] `renders/generic.html` — slider-built generic orbits, Archimedean jumps, all 3 forms
- [ ] HTML renders of all 7, in each of the 3 physical forms
- [ ] Pick a form / material and design an actual printable model
