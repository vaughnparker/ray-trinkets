# ray-trinkets

Put some dots on a ball so that:

1. **Every dot sees the same view.** For any two dots, you can rotate the ball so the
   first lands where the second was, and every other dot lands on a dot.
2. **Every dot is a pivot.** For each dot, you can spin the ball around that dot (by
   less than a full turn) and every dot still lands on a dot.
3. **The dots aren't all on one circle.**

There are exactly **7** ways to do it (counting rotated copies as the same). This
project is about turning those 7 into physical objects: 3D prints, wood, or metal.

## The 7

| label | dots | vertex solid (convex hull) | face solid (shaved dual) |
|---|---|---|---|
| T · 4  |  4 | tetrahedron       | tetrahedron |
| O · 6  |  6 | octahedron        | cube |
| O · 8  |  8 | cube              | octahedron |
| O · 12 | 12 | cuboctahedron     | rhombic dodecahedron |
| I · 12 | 12 | icosahedron       | dodecahedron |
| I · 20 | 20 | dodecahedron      | icosahedron |
| I · 30 | 30 | icosidodecahedron | rhombic triacontahedron |

T, O and I are the rotation groups of the tetrahedron, octahedron and icosahedron.
Why the answer is exactly 7, and which wordings of the riddle break it, is in
[`riddle.md`](riddle.md).

## Three physical forms

1. **Spike-ball.** Each dot becomes a thin rod poking out of a sphere. The most
   literal version, but fragile at small sizes, especially with 30 spikes.
2. **Vertex solid.** The dots become the corners of a solid (their convex hull). This
   gives the 5 Platonic solids plus the 2 quasiregular ones.
3. **Face solid.** Shave a flat face into the ball at each dot, until neighboring
   faces meet. This gives the 5 Platonic solids plus the 2 rhombic ones.

Between them, the two solid forms cover all 9 convex polyhedra whose edges are all
alike.

## What's here

- [`riddle.md`](riddle.md): the math. How the riddle was narrowed to exactly 7,
  equivalent wordings, wordings that fail, and a face version of the riddle.
- `script.py`: builds T, O and I from scratch, finds the 9 candidate arrangements,
  confirms they reduce to 7, and writes `renders/data.js`.
- `renders/index.html`: interactive 3D viewer for the 7, in all three forms.
- `renders/generic.html`: sliders for the arrangements the pivot rule excludes, with
  jumps to the Archimedean solids.

## Running it

Open `renders/index.html` in a browser; no build step. To regenerate the data
(needs `numpy` and `scipy`), run from the repo root:

```
python3 script.py
```

## Next

Pick a form and material, and design an actual printable model.
