# Noah’s Ark 2.0 — Two by Two

Independent storybook rebuild, November 2026. The original game remains permanently in `../noah/` and remains linked from the games shelf. Copied legacy PNG artwork is retained here but is no longer used by this version.

## Play

Tap a destination, drag, or use arrow/WASD keys to guide Noah. Collect any waiting animal and remember its briefly highlighted partner. On a match, both animals run to the Ark automatically, leaving Noah free to collect another pair immediately. There are ten pairs and one 60-second round, matching BibleBucket’s quick-play arcade theme. No escort trips or mode selector remain.

A match made before the buzzer is honored: any pairs already running finish boarding before the result is shown. The playable clock stops at 60 seconds; the short boarding/result animation does not permit extra matches. Completing all ten matches early closes the gates after the runners board. The clock uses active elapsed wall time independently of capped movement steps; pausing or changing tabs stops the clock.

Pause with the Pause button, P, or Escape. Replay and new-journey paths clear overlays, input, collections, cameo discovery, and animation state. Web Audio chimes, procedural thunder, last-ten-second urgency tones, and Captain’s bark are enabled automatically when the player starts the round. There is no in-game sound toggle; use device/browser volume controls. Reduced-motion preference disables walking bob, rain streaks, cloud drift, distant lightning, and animated wave motion and shortens the ending.

The storm is already underway from the opening second: immediate driving rain, an opening thunderclap, a dark cloud bank, and water at the meadow edges. It intensifies throughout the round; runoff forms along the painted path and water advances over the lower meadow. Landscape shading occurs before actors are drawn, preserving animal/Noah readability. There are no full-screen lightning flashes.

## Files and artwork

- `index.html`: semantic screens, 60-second round briefing, game HUD and controls.
- `story.css`: responsive cream/evergreen storybook UI.
- `story.js`: painted-scene camera, fallback scenery, pointer/keyboard input, matching, automatic boarding, storm and ending state machine.
- `art/*.svg`: original code-native illustrations retained for Noah and nine animal species; the original Captain SVG remains recoverable but is no longer the active cameo art. No emoji, external fonts, CDNs, libraries, or network APIs are required.

The meadow scene is cached; the canvas caps DPR at 1.5. Actors use CSS-pixel coordinates; resize remaps their positions proportionally. Boarding uses the same normalized painting transform as the background: the doorway floor is at image coordinate (0.504, 0.389). Animals are kept clear of the bottom instruction panel.

## Story framing

Ten pairs and the timed rescue are gameplay simplifications, not an exhaustive depiction of Genesis. Winning is not a measure of faith. The ending quotes Genesis 7:16 (KJV), “and the LORD shut him in.” The rainbow is a storybook epilogue recalling the later covenant in Genesis 9:13, not a claim that it appeared while boarding. The unsuccessful-round quotation is an excerpt from Genesis 6:18 (KJV).

## Verification

Serve the repository root with a static HTTP server. Check desktop, narrow portrait, and short landscape; exercise pointer/touch and keyboard movement, ten-pair matching and automatic boarding, exact 60-second clock and pre-buzzer match credit, pause/resume including hidden-tab pause, win/loss cinematic, skip/Escape, and repeated replay/new journey. Verify artwork loading and navigation back to the shelf. Tests may instrument private state in a browser-only intercepted script; do not add test hooks or forced outcomes to production code.

Publishing follows the repository’s GitHub Pages main-branch flow. Verify the exact commit is built, live HTML/JS/CSS/art match committed bytes, and replay the main interactions on biblebucket.net.

## The two surprise pairs

- **Red pandas:** August’s surprise animal choice, with rust-colored fur, cream facial markings and a striped bushy tail.
- **Captain:** Jake’s American Pitbull. The active sprite is now the exact Orbs artwork, not a redraw: `art/captain-orbs.png`, copied byte-for-byte from `../orbs-2/captain-character.png`. It has his happy face, brown/brindle coat, white chest/toes, and red collar. Use **Captain** only in the game. His first pickup reveals the cameo with a bark; boarding announces “Captain’s aboard. All paws accounted for.” His matching buddy uses the same recognizable illustration. The same Orbs artwork is the canonical Captain look for cameos in every BibleBucket game. This implementation change is confined to Noah 2.0.

Jake approved Noah’s current look and later authorized broader character changes if needed to suit the painting. This release keeps his illustration and enlarges it slightly for readability.

## Gentle meadow movement

Waiting animals take short, slow strolls (8–13 scaled pixels/second), pause between steps, and turn to face their travel direction. Each stays within 30 scaled pixels of its starting spot, with meadow bounds preserved. Collected/running animals use their existing follow/boarding movement; reduced-motion preference disables decorative wandering. Resize remaps home and current destinations together.

## Approved painted background and art direction

The user-approved base is `art/ark-meadow-painted.png`, generated with the built-in image tool, reviewed in chat, and explicitly approved before integration. It includes the Ark, its open doorway/ramp, the meadow and the winding path; no UI, people, or animals are baked into it. The previous code-drawn scenery and Ark remain in `story.js` as an asset-failure fallback, and all previous assets are retained.

Source: generated `exec-1ea90298-946c-4c02-9a52-04397873ca18.png`; copied without image edits. SHA-256: `49b12465437587af231051a9e504e8d353d1b2aeed57f2d7c2079c2fe2aafb00`.
Captain’s canonical copied PNG SHA-256: `bca255683ef3dc09a3fc0532ec799d7176cc78a8eefc2a185627133319a2e6ef`.

The painting fills the scene vertically with a minimum horizontal image extent of 0.78 times the scene height, centered on the doorway. This avoids crushing the Ark on tall phones; all scenery/door/stream coordinates use the same transform. Short, very wide viewports use a narrower centered canvas and put HUD elements in the side gutters. Runtime Canvas sizing and pointer coordinates use the canvas dimensions, not the outer stage. Resize remaps characters and runners as before.

The painted Ark is not drawn a second time. Endings layer a closing-door overlay and rising water over the same painting; they never swap back to the legacy vector Ark. Readability is preserved by shading/flooding the world before drawing actors, with only a light near-rain pass over them. Rain, clouds, runoff, ripples and the flood remain animated code-art. Main assets finish decoding before the start button enables, so downloads do not eat into the 60-second round.

Captain is intentionally a little larger than the other animals, with his paws aligned to the ground, original aspect ratio preserved, and pickup radius scaled accordingly. The brief partner hint lasts 1.15 active-game seconds. The animal identity in the task panel remains available afterwards, but there is no permanent map locator.

Noah and all animal artwork render 15% larger for readability, including automatic boarding. Artwork, movement, pickup distances, and the round mechanics are unchanged.
