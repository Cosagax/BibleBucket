# Following His Star — 2.0

The original game remains independently archived in `../jesus-birth/`.

## Painted travelers

- `wise-man-painted.png`: Jake-approved teal-robed hero prototype, generated as transparent artwork.
- `wise-men-companions-painted.png`: two equal-width transparent atlas cells: plum-robed elder and green-robed companion.
- Runtime alpha trimming creates small cached sprites. A lightweight cloth mesh adds opposing foot shuffle, step lift, body bob, sash flutter, airborne foot tuck, and a damped landing settle. The held gift and face stay comparatively steady. Reduced-motion preference suppresses decorative sway and walking shuffle.
- The legacy code-drawn characters remain the asset-failure fallback. Physics, hitbox, jump velocity, obstacles, scoring, and journey timing are unchanged. Finale destinations leave room for both companions alongside the hero to keep the painted trio readable on phones.
- `captain-orbs.png` is the canonical Orbs Captain artwork. His visual-only cameo appears once from 7 to 9.8 active seconds, travels left-to-right, and naturally resets with elapsed time on replay.

## Verification

Check desktop, portrait phone, and short landscape: walking, jump ascent/descent, landing, Captain's single pass, the two companions joining at 50 seconds, and replay reset. Use browser-only script instrumentation for controlled visual checks; never publish testing hooks. Verify exact Pages build commit and live changed file bytes after publication.
