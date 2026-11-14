# Noah’s Ark 2.0 — Two by Two

Independent storybook rebuild, November 2026. The original game remains permanently in `../noah/` and remains linked from the games shelf. Copied legacy PNG artwork is retained here but is no longer used by this version.

## Play

Tap a destination, drag, or use arrow/WASD keys to guide Noah. Touch any waiting animal to lead it, find its highlighted matching partner, and walk both to the glowing Ark ramp. Eight pairs wins. Storm watch lasts 90 seconds; Peaceful gathering has no timer. Both modes use the same rescue mechanics.

Pause with the Pause button, P, or Escape. Changing tabs or losing focus automatically pauses the active journey. Replay and new-journey paths clear overlays, input, collections, and animation state. Optional Web Audio chimes start only after the player enables sound. Reduced-motion preference disables walking bob, rain streaks, and animated wave motion and shortens the ending.

## Files and artwork

- `index.html`: semantic screens, journey choices, game HUD and controls.
- `story.css`: responsive cream/evergreen storybook UI.
- `story.js`: canvas landscape and Ark, pointer/keyboard input, matching, escort/boarding, storm and ending state machine.
- `art/*.svg`: nine original code-native illustrated assets: Noah and eight animal species. No emoji, external fonts, CDNs, libraries, generated raster assets, or network APIs are required.

The meadow scene is cached; the canvas caps DPR at 1.5. Actors use CSS-pixel coordinates; resize remaps their positions proportionally. Boarding enters a fixed door at the top of the actual ramp. Animals are kept clear of the bottom instruction panel.

## Story framing

Eight pairs and the timed rescue are gameplay simplifications, not an exhaustive depiction of Genesis. Winning is not a measure of faith. The ending quotes Genesis 7:16 (KJV), “and the LORD shut him in.” The rainbow is a storybook epilogue recalling the later covenant in Genesis 9:13, not a claim that it appeared while boarding. The unsuccessful-round quotation is an excerpt from Genesis 6:18 (KJV).

## Verification

Serve the repository root with a static HTTP server. Check desktop, narrow portrait, and short landscape; exercise pointer/touch and keyboard movement, all eight actual pair rescues and boarding, both journey clocks, pause/resume including hidden-tab pause, win/loss cinematic, skip/Escape, and repeated replay/new journey. Verify artwork loading and navigation back to the shelf. Tests may instrument private state in a browser-only intercepted script; do not add test hooks or forced outcomes to production code.

Publishing follows the repository’s GitHub Pages main-branch flow. Verify the exact commit is built, live HTML/JS/CSS/art match committed bytes, and replay the main interactions on biblebucket.net.
