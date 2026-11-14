# Noah’s Ark 2.0 — Two by Two

Independent storybook rebuild, November 2026. The original game remains permanently in `../noah/` and remains linked from the games shelf. Copied legacy PNG artwork is retained here but is no longer used by this version.

## Play

Tap a destination, drag, or use arrow/WASD keys to guide Noah. Collect any waiting animal and find its highlighted partner. On a match, both animals run to the Ark automatically, leaving Noah free to collect another pair immediately. There are ten pairs and one 60-second round, matching BibleBucket’s quick-play arcade theme. No escort trips or mode selector remain.

A match made before the buzzer is honored: any pairs already running finish boarding before the result is shown. The playable clock stops at 60 seconds; the short boarding/result animation does not permit extra matches. Completing all ten matches early closes the gates after the runners board. The clock uses active elapsed wall time independently of capped movement steps; pausing or changing tabs stops the clock.

Pause with the Pause button, P, or Escape. Replay and new-journey paths clear overlays, input, collections, cameo discovery, and animation state. Optional Web Audio chimes, procedural thunder, last-ten-second urgency tones, and Captain’s bark are enabled with Sound on. Reduced-motion preference disables walking bob, rain streaks, cloud drift, distant lightning, and animated wave motion and shortens the ending.

The storm builds over four 15-second phases: clouds, rain, heavy wind-driven rain, and encroaching puddles with an urgent clock. Landscape shading occurs before actors are drawn, preserving animal/Noah readability. There are no full-screen lightning flashes.

## Files and artwork

- `index.html`: semantic screens, 60-second round briefing, game HUD and controls.
- `story.css`: responsive cream/evergreen storybook UI.
- `story.js`: canvas landscape and Ark, pointer/keyboard input, matching, automatic boarding, storm and ending state machine.
- `art/*.svg`: eleven original code-native illustrated assets: Noah and ten animal types. No emoji, external fonts, CDNs, libraries, generated raster assets, or network APIs are required.

The meadow scene is cached; the canvas caps DPR at 1.5. Actors use CSS-pixel coordinates; resize remaps their positions proportionally. Boarding enters a fixed door at the top of the actual ramp. Animals are kept clear of the bottom instruction panel.

## Story framing

Ten pairs and the timed rescue are gameplay simplifications, not an exhaustive depiction of Genesis. Winning is not a measure of faith. The ending quotes Genesis 7:16 (KJV), “and the LORD shut him in.” The rainbow is a storybook epilogue recalling the later covenant in Genesis 9:13, not a claim that it appeared while boarding. The unsuccessful-round quotation is an excerpt from Genesis 6:18 (KJV).

## Verification

Serve the repository root with a static HTTP server. Check desktop, narrow portrait, and short landscape; exercise pointer/touch and keyboard movement, ten-pair matching and automatic boarding, exact 60-second clock and pre-buzzer match credit, pause/resume including hidden-tab pause, win/loss cinematic, skip/Escape, and repeated replay/new journey. Verify artwork loading and navigation back to the shelf. Tests may instrument private state in a browser-only intercepted script; do not add test hooks or forced outcomes to production code.

Publishing follows the repository’s GitHub Pages main-branch flow. Verify the exact commit is built, live HTML/JS/CSS/art match committed bytes, and replay the main interactions on biblebucket.net.

## The two surprise pairs

- **Red pandas:** August’s surprise animal choice, with rust-colored fur, cream facial markings and a striped bushy tail.
- **Captain:** Jake’s American Pitbull, illustrated from his supplied photograph: brindle brown coat, broad happy face, folded ears, white chest and white toes, and a dark collar. Use **Captain** only in the game. His first pickup reveals the cameo with an optional bark; boarding announces “Captain’s aboard. All paws accounted for.” His matching buddy uses the same recognizable illustration. The cameo idea may extend to other BibleBucket games later; this change is confined to Noah 2.0.

Do not modify Noah’s current illustration when adjusting Captain or the round mechanics; Jake specifically approved Noah’s look.
