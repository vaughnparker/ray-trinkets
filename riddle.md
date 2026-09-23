# The riddle, and the restrictions that make its answer 7

Companion to [`notes.md`](notes.md). This file records how the riddle was tightened
step by step until exactly the 7 elementary ray-sets remain, the equivalent ways to
phrase it, and the phrasings that sound right but don't work. Section 7 turns it into
a face riddle whose answer is the dual 7 (the Platonic solids plus the two rhombic
solids).

---

## 1. The original riddle (answer: infinitely many)

> A ball has dots on its surface. For any dot, you can rotate the ball so that dot
> lands on any other dot, and every other dot also lands on a dot. How many
> arrangements are there?

This asks for a single **orbit** of a finite rotation group. Every finite subgroup of
SO(3) is one of:

| group | order | notes |
|---|---|---|
| C_n (cyclic) | n | one axis, every n |
| D_n (dihedral) | 2n | one main axis plus n half-turn flips, every n |
| T (tetrahedral) | 12 | |
| O (octahedral) | 24 | |
| I (icosahedral) | 60 | |

The orbit of any point under any of these groups is a valid answer, so there are
infinitely many. There are three separate sources of infinity:

1. **n is unbounded** for C_n and D_n.
2. **Latitude is free** for C_n and D_n. For a fixed n, a ring can sit at any height.
3. **Generic orbits.** Even under T, O, or I, any point that isn't on a symmetry axis
   has a full-size orbit (12, 24, or 60 dots), and that point can slide continuously.
   `renders/generic.html` explores this family.

A tighter riddle has to shut off all three.

---

## 2. Restriction A: more than one axis of order ≥ 3

> The arrangement has at least two different axes that each allow a turn of a third
> of a revolution or less.

C_n and D_n have at most one such axis (the main axis), so this removes sources 1
and 2 and leaves only T, O, I.

**On its own this isn't enough.** It leaves the generic orbits of T, O, I (source 3),
so the answer is still infinite.

---

## 3. Restriction B: every dot is a pivot

> For each dot, some rotation other than "do nothing" keeps that dot fixed and still
> maps every dot onto a dot.

In other words, every dot lies on a rotation axis of the arrangement, so its
stabilizer is nontrivial.

This removes source 3. A generic point is fixed only by the identity, so it fails. The
survivors are the **pole orbits** of T, O, I: the face centers, edge midpoints, and
corners of each group.

**Restrictions A + B together give exactly 7:**

- T, O, I each have 3 pole families, so there are 9 naive candidates.
- T's three families collapse to one distinct shape:
  - T's corner and face-center families are two tetrahedra that are rotated copies
    of each other.
  - T's edge-midpoint family is an octahedron, identical to O's corner family.
- O's and I's families are all distinct.

1 (T) + 3 (O) + 3 (I) = **7**. `script.py` verifies this collapse with an explicit
orthogonal map.

| label | dots | vertex solid (convex hull) | face solid (shaved dual) |
|---|---|---|---|
| T · 4  |  4 | tetrahedron       | tetrahedron |
| O · 6  |  6 | octahedron        | cube |
| O · 8  |  8 | cube              | octahedron |
| O · 12 | 12 | cuboctahedron     | rhombic dodecahedron |
| I · 12 | 12 | icosahedron       | dodecahedron |
| I · 20 | 20 | dodecahedron      | icosahedron |
| I · 30 | 30 | icosidodecahedron | rhombic triacontahedron |

---

## 4. The simplified riddle (answer: 7)

Restriction A can be replaced with something easier to picture.

> **Put some dots on a ball so that:**
> 1. **Every dot sees the same view.** For any two dots, you can rotate the ball so
>    the first lands where the second was, and every other dot lands on a dot.
> 2. **Every dot is a pivot.** For each dot, you can spin the ball around that dot
>    (by less than a full turn) and every dot still lands on a dot.
> 3. **The dots aren't all on one circle.**
>
> **How many arrangements are there?** (Count two as the same if one is a rotated
> copy of the other.)

**Why condition 3 can replace restriction A.** Once condition 2 holds, the only
arrangements with C_n or D_n symmetry are:

- a single dot (C_n pole),
- two opposite dots (D_n main-axis poles),
- a regular polygon around the equator (D_n half-turn poles).

All of these lie on one circle. A finite set with infinite symmetry is at most two
opposite dots, which are also on a circle.

**Riddle-style version:**

> Stand on any dot and look around. The view is the same from every dot, and it
> repeats if you turn in place by less than a full turn. The dots don't all lie on
> one circle. How many ways can you do this?

**Wording details that matter:**

- **"Less than a full turn" can't become "a third of a turn."** The cuboctahedron and
  icosidodecahedron dots only have half-turn pivots, so that version gives 5.
- **"Rotated copies count as the same" is required.** Otherwise every arrangement can
  be tilted in infinitely many ways.
- **Ball size and mirror images don't need to be mentioned.** None of the 7 has a
  separate left-handed version.

---

## 5. Equivalent swaps, one condition at a time

### Instead of "every dot is a pivot"

> There are more ways to turn the ball onto itself than there are dots.
> (Doing nothing counts as one way.)

For a transitive arrangement, (number of symmetries) = (number of dots) × (number of
spins fixing one dot). So "more symmetries than dots" is the same as "some spin fixes
each dot."

- Tetrahedron: 12 symmetries, 4 dots. Passes.
- Cuboctahedron: 24 symmetries, 12 dots. Passes.
- Generic O orbit: 24 symmetries, 24 dots. Fails.

### Instead of "not all on one circle"

> Any flat cut through the center of the ball leaves dots strictly on both sides.

or

> Joining the dots makes a solid, not a flat shape.

Every excluded case (one dot, two opposite dots, an equatorial polygon) either fits in
half the ball or is flat. Every pole orbit of T, O, I surrounds the center.

---

## 6. Versions that describe the solid instead

### Corners and edges (convex hull)

> Join the dots into a solid. Any corner can be rotated onto any other corner, and
> any edge onto any other edge.

The convex solids that are both vertex-transitive and edge-transitive are the
5 Platonic solids plus the 2 quasiregular solids (cuboctahedron, icosidodecahedron).
That's the same 7. No pivot condition is needed here. Prisms and antiprisms fail
because their edges come in two kinds, except for the cube and octahedron, which are
already on the list.

### Faces and edges (the shaving version)

> Shave one flat face into the ball at each dot. Any face can be rotated onto any
> other face, and any edge onto any other edge.

This is the dual of the version above. It gives the 5 Platonic solids plus the rhombic
dodecahedron and rhombic triacontahedron. Still 7, and the closest to how the physical
trinket would be made.

---

## 7. The face riddle (answer: the dual 7)

Suppose the answer is meant to be this set of solids instead:

- tetrahedron, cube, octahedron, dodecahedron, icosahedron
- rhombic dodecahedron, rhombic triacontahedron

These are the duals of the 7 dot arrangements. Each dot becomes a flat face instead
of a corner, so the riddle is the dot riddle with "dot" replaced by "face":

> **Shave flat faces into a ball until you have a solid, so that:**
> 1. **Every face looks the same.** You can turn the solid so any face lands where
>    any other face was, and the solid lands on itself.
> 2. **Every face is a pivot.** For each face, you can spin the solid around that
>    face's center (less than a full turn) and it lands on itself.
>
> **How many solids are there?** (Count rotated or resized copies as the same.)
>
> **Answer: 7**

**Why this matches the dot riddle.** A face's center plays the role of a dot:

- Every face alike ⇔ every dot alike.
- A spin around a face's center ⇔ a spin around a dot, so the pivot condition carries
  over unchanged.

**"Not all on one circle" is no longer needed.** "Until you have a solid" already does
its job:

- **Cuts all around one circle** of the ball never meet at the top and bottom, so they
  make an endless prism, not a solid.
- **One or two cuts** don't make a solid either.

Every case the circle condition removed from the dot riddle is removed automatically
here, so the face riddle needs only two conditions.

**Why the pivot condition is still needed.** Without it, "every face looks the same"
lets in every convex solid with all faces alike (these are the fair dice). That's an
infinite list:

- **Duals of the other Archimedean solids**, whose faces have no spin symmetry. Examples:
  the triakis tetrahedron (isosceles triangles) and the pentagonal icositetrahedron
  (lopsided pentagons).
- **Double pyramids** of every size (isosceles triangle faces). Only the octahedron
  passes the pivot condition.
- **Trapezohedra** of every size (kite faces). Only the cube passes.
- **Disphenoids**, tetrahedra whose four faces are congruent but not equilateral. None
  pass.

### Other phrasings of the face riddle

**Faces and edges (no pivot needed):**

> A solid shaved from a ball where any face can be turned onto any other face, and any
> edge onto any other edge.

The convex solids where both faces and edges are all alike are exactly these 7.

- **The cuboctahedron and icosidodecahedron fail.** Their edges are all alike, but they
  have two kinds of faces.
- **"Shaved from a ball" is required.** It keeps the solid convex. Without it, the four
  regular star polyhedra (Kepler–Poinsot: spiky, self-intersecting shapes) also have
  all faces and all edges alike, which would make the answer 11.

**As dice:**

> Which dice are fair, and look the same after you twist the die in place around
> whichever face is on top?

- **"Fair"** means every face is equivalent to every other, which is condition 1. It's
  why fair gaming dice have the shapes they do.
- **The twist** is the pivot condition. It rules out fair but lopsided dice, such as the
  kite-faced d10 and pentagon-faced shapes.
- **What's left:** the d4, d6, d8, d12 and d20, plus the rhombic d12 and the d30, both
  of which are sold as real dice.

### Face-riddle phrasings that don't work

| candidate | why it fails |
|---|---|
| "Every face looks the same" alone | Infinite: all fair dice, including every double pyramid, trapezohedron and disphenoid, plus the duals of the other Archimedean solids. |
| Faces and edges alike, without "shaved from a ball" | Adds the 4 Kepler–Poinsot star polyhedra. Gives 11. |
| "Every face is a regular polygon" | Drops the two rhombic solids (their faces are rhombi, not squares). Gives 5. |

---

## 8. Phrasings that don't work

| candidate restriction | why it fails |
|---|---|
| Restriction A alone ("more than one ≥ 3-fold axis") | Leaves all generic T, O, I orbits. Still infinite. |
| "Every dot's nearest neighbors are equally far away" / "all edges have equal length" | The **snub cube** (a generic O · 24 orbit) and **snub dodecahedron** (generic I · 60) are vertex-transitive with all edges equal, but their edges aren't all alike. Edges need to be rotatable onto each other, not just equal in length. |
| Pivots must be "a third of a turn or less" | Drops the cuboctahedron and icosidodecahedron. Gives 5. |
| "The dots are the corners of a Platonic solid" | Gives 5, not 7. |
| "The dots are as spread out as possible" (best packing for their count) | Not the same list. Optimal packings are a separate problem, and most of them aren't symmetric like this at all. |
| "The dots are isotropic" (second-moment matrix ∝ identity) | **Every** orbit of T, O, or I is isotropic, generic ones included, because those groups act irreducibly on 3D space. Some D_n double rings at a "magic latitude" also pass. It removes neither the generics nor all of D_n. |
| Drop "rotated copies count as the same" | Every answer then comes in infinitely many orientations. |

---

## 9. What the rotation-only rule excludes among Archimedean solids

The Archimedean solids are vertex-transitive under their full symmetry group, which
includes reflections. Under **rotations only**:

- **Reachable as a single orbit** (`generic.html` jumps to these). Only the two
  quasiregular ones are pivot orbits; the rest are generic orbits.

| solid | group · dots | pivot? |
|---|---|---|
| truncated tetrahedron | T · 12 | no |
| cuboctahedron | O · 12 | yes |
| truncated cube | O · 24 | no |
| truncated octahedron | O · 24 | no |
| rhombicuboctahedron | O · 24 | no |
| snub cube | O · 24 | no |
| icosidodecahedron | I · 30 | yes |
| truncated dodecahedron | I · 60 | no |
| truncated icosahedron | I · 60 | no |
| rhombicosidodecahedron | I · 60 | no |
| snub dodecahedron | I · 60 | no |

- **Not reachable.** The **truncated cuboctahedron** (48 dots) and **truncated
  icosidodecahedron** (120 dots) have more dots than O (24) or I (60) has rotations.
  Each one splits into two mirror-image orbits, so a rotation can never move a dot
  from one half to the other. These two already fail condition 1 of the riddle,
  before the pivot rule applies.
