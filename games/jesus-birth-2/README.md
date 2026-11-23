# Following His Star — 2.0

The original game remains independently archived in `../jesus-birth/`.

## Painted travelers

- `wise-man-painted.png`: Jake-approved teal-robed hero prototype, generated as transparent artwork.
- `wise-men-companions-painted.png`: two equal-width transparent atlas cells: plum-robed elder and green-robed companion.
- Runtime alpha trimming creates small cached sprites. A lightweight cloth mesh adds opposing foot shuffle, step lift, body bob, sash flutter, airborne foot tuck, and a damped landing settle. The held gift and face stay comparatively steady. Reduced-motion preference suppresses decorative sway and walking shuffle.
- The legacy code-drawn characters remain the asset-failure fallback. Physics, hitbox, jump velocity, obstacles, scoring, and journey timing are unchanged. Finale destinations leave room for both companions alongside the hero to keep the painted trio readable on phones.
- `captain-orbs.png` is the canonical Orbs Captain artwork. His visual-only cameo appears once from 7 to 11.2 active seconds, travels left-to-right, and naturally resets with elapsed time on replay. Two visual “Woof!” bubbles accompany the pass; no bark audio is added.

## Verification

Check desktop, portrait phone, and short landscape: walking, jump ascent/descent, landing, Captain's single pass, the two companions joining at 50 seconds, and replay reset. Use browser-only script instrumentation for controlled visual checks; never publish testing hooks. Verify exact Pages build commit and live changed file bytes after publication.

## Holiday release polish (2026-11-22)

- Public title, canonical URL, search description, and Facebook/Open Graph sharing metadata point to this independent game.
- Space / Up Arrow instructions match keyboard controls; native link/button keyboard activation is preserved.
- Replay resets the obstacle spawn clock. Repeated starts cannot create parallel animation loops; unavailable audio cannot block starting.
- Axis-aligned collision comparisons use each rock’s own width and height, fixing false hits when jumping above a rock.
- Preserve the approved art, 60-second journey, Captain’s 4.2-second cameo, and finale.

## Painted angel (2026-11-22)

- `angel-painted.png`: approved transparent, auburn-haired angel artwork. Original generated PNG is preserved byte-for-byte. No reference portrait is published.
- The angel retains her 45-second arrival and existing descent/audio timing. An entrance fade and gentle hover accompany subtle lower-robe movement; the face and wings remain unwarped. Reduced-motion preference removes the decorative sway, bob, and new descent particles.
- Draw the portrait after the star glow to protect facial detail. Size and anchors derive from the current viewport each frame, including rotation during descent. Retain the original code-drawn angel solely as a failed-image fallback.
- Check entrance at 45.8 seconds, settled pose at 49.5, and the trio at 55 seconds on desktop, portrait phone, and short landscape. Also check reduced motion, mid-descent rotation, image failure, win sequence, and replay cleanup. Use browser-only intercepted instrumentation; do not publish testing hooks.
