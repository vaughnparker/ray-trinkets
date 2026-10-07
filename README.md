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

   Stopping earlier, the moment neighboring flats just touch, gives the
   **kissing-flats balls**. The round flats are the dots, the touching points are the
   edges, and the leftover curved patches are the faces of the vertex solid.

Between them, the two solid forms cover all 9 convex polyhedra whose edges are all
alike.

## What's here

Live site: <https://vaughnparker.github.io/ray-trinkets/>. The home page links to every
other page. The riddle page poses the riddle without giving the answer away; everything
under `viewer/` shows it.

- [`index.html`](index.html): the home page, a short list of links to everything else.
- [`riddle.html`](riddle.html): the riddle, a test bench that checks any candidate
  against the rules and says why it fails, hints one at a time, and a button that
  reveals the answer.
- [`riddle.md`](riddle.md): the math. How the riddle was narrowed to exactly 7,
  equivalent wordings, wordings that fail, and a face version of the riddle.
- `viewer/`: the answer, in the browser.
  - [`index.html`](viewer/index.html): interactive 3D viewer for the 7, in all three forms.
  - [`spike-balls.html`](viewer/spike-balls.html): the 7 as spike balls on a stand,
    with buttons that act out the riddle, facts for each ball, and drilling angles.
  - [`kissing-flats.html`](viewer/kissing-flats.html): spin the 7 kissing-flats balls in
    3D, with a grind-depth slider from the plain ball through the kissing point to the
    face solid.
  - [`explore.html`](viewer/explore.html): sliders for the arrangements the pivot rule
    excludes, with jumps to the Archimedean solids.
  - `lib/`: three.js, its orbit controls, and `data.js` (the 7, written by `script.py`).
- `scripts/`
  - `script.py`: builds T, O and I from scratch, finds the 9 candidate arrangements,
    confirms they reduce to 7, and writes `viewer/lib/data.js`.
  - `kissing_flats.py`: writes the kissing-flats models and `images/kissing-flats.png`.
- `models/kissing-flats-20mm/`: one STL per kissing-flats ball, in millimetres, resting
  on a flat.
- `images/kissing-flats.png`: a render of the 7 kissing-flats balls.

## Running it

Open any of the pages in a browser; no build step. To regenerate the data (needs
`numpy` and `scipy`):

```
python3 scripts/script.py
```

To rebuild the kissing-flats models and render (needs `numpy`, `matplotlib`,
`trimesh` and `manifold3d`), optionally at another size:

```
python3 scripts/kissing_flats.py
python3 scripts/kissing_flats.py --diameter 25
```

## Next

Get the 20 mm kissing-flats models cast in metal (Shapeways: Lost Wax Casting,
polished finish).
