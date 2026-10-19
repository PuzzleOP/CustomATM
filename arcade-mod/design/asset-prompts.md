# Runtime artwork

Generated with the built-in ImageGen tool. Reference: `concept-1.png`, the selected Redstone Arcade concept.

## skin.png

Edit the provided Minecraft casino concept into a production UI texture, exactly 1536x1024. Preserve the exact original layout, positions, dimensions, dark stone textures, copper frame, eight sidebar item icons, emerald decorations, central pedestal, button frames, green primary button and green selected Coin Flip sidebar row. Remove every text character, word, numeral, currency sign, arrow glyph, plus/minus sign from every region so all UI labels can be rendered dynamically by game code. Remove the large central floating emerald coin only; retain its pedestal below and replace the coin space with the same dark stone background. Remove the tiny coins inside the Heads/Tails buttons too, leaving blank control interiors. Remove background Minecraft world outside the outer frame to transparent alpha. Preserve the entire frame at its original position. Keep every panel border and control geometry unchanged. Do not add or move objects.

The generated skin retains faint color outside the frame despite the prompt; the renderer never samples that region. The slots icon's decorative 777 is intentionally harmless artwork, not a dynamic UI value.

## heads.png

Create one isolated game sprite matching the large emerald gold coin in the reference concept as closely as possible. Front-facing circular thick gold coin with crisp pixel-art stepped outline, bevel highlights top-left, dark gold bottom-right and a faceted bright green emerald emblem centered. Slight thickness visible on the right edge, almost front on, same warm pixel art style. No pedestal, background, letters, numbers, other objects or glow outside the silhouette. True transparent alpha background. Target a square canvas with equal margins. This is the heads face for a Minecraft coin sprite.

## tails.png

Create one isolated game sprite matching the reference coin but showing its tails face. Front-facing circular thick silver/iron coin, crisp pixel-art stepped outline, bevel highlights top-left, dark silver bottom-right, a faceted subtle gray iron-ingot embossed emblem centered. Same pixel scale, circular silhouette, lighting and art direction as the reference gold emerald coin. No pedestal, background, letters, numbers, other objects or outside glow. True transparent alpha, square canvas, equal margins.

Actual returned coin dimensions are 1254 × 1254. The renderer and package check use these actual dimensions, not the initially requested size. PNGs are copied unchanged into the addon resources.

## All-game shell and pieces (0.2.0)

Generated with ImageGen using the existing skin as the visual reference and requesting transparency. Each result was copied unchanged; the renderer crops the functional artwork from the returned canvas.

- `shell.png` (1536×1024): preserve the original outer stone/copper frame, header, footer and eight sidebar icons/rows. Neutralize all selected rows. Clear the central area to dark stone; remove the coin pedestal, controls and information panel. No labels or numbers.
- `slot_frame.png` (1875×839 returned): front-facing horizontal pixel-art cabinet with exactly three blank ivory reel windows, stone/copper/emerald trim, transparent surroundings, no lettering or symbols inside the reels.
- `card_face.png` (1024×1536): one blank ivory/parchment playing card with a stepped copper border, matching the reference's pixel scale and lighting. No ranks, suits, text or numbers.
- `card_back.png` (1024×1536): matching card silhouette with an emerald woven/pixel pattern and central emerald emblem, copper corner trim, no text.

Original outputs are retained in the Codex generated-images directory under this thread ID. Slot symbols, mine gems, Plinko pins/ball and scratch symbols reference vanilla Minecraft textures at runtime. Those vanilla images and the preview font are extracted only into ignored `.work/` for offline rendering; they are not distributed in the addon.
