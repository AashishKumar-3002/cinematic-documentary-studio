# Ten animation treatments

Paraphrased from the user-supplied **10 Claude Animation Styles: Jatayu x Pushpak Viman**, 13 PDF pages. The original is archived at `reference/animation-styles/jatayu-10-animation-styles.pdf`. Page numbers below are PDF page numbers. This reference preserves the useful visual criteria without making the guide's example scene mandatory.

## Shared-shot method (pages 3, 5, 12-13)

Build reusable drawing functions for the subject, props and environment. Make motion and layout independent of painting style. A style variant repaints the same geometry and poses instead of replacing the scene. Fix proportions and silhouettes on the shared version before making variants.

The benchmark is five seconds at 30 fps (150 frames). An approach runs to 1.7 seconds; the subject anticipates contact at 1.7; contact occurs at exactly 2.0; reaction and departure occupy the remainder. Its original characters are Jatayu and the Pushpak Viman. Replace these with the actual subject for new work. The original landscape version briefly tilts/drops the vehicle after impact and recovers around 3.0 seconds.

Review the opening action at 0.6 seconds, the contact at 2.0, and the aftermath at 4.0. Exact matching event times make comparisons and rhythmic editing easier. A five-second clip at 30 fps displays frames 0 through 149; the 2.0-second event begins at frame 60.

## Style cards

### 01 Madhubani (page 6)

- Context named by the guide: Mithila painting from Bihar.
- Treatment: handmade-paper ground; paired ink contours separated by a narrow paper gap; flat vermilion, turmeric yellow, leaf green and indigo. Fill forms with dots, hatching and fish-scale patterns. Use almond-shaped eyes and an ornamental border of yellow triangles on red when appropriate.
- Impact language: red/yellow radiating star.
- Verify: recognizable double outlines, patterned interiors and deliberate border. Do not reduce this to generic bright flat colours.

### 02 Ink Wash (page 6)

- Context named by the guide: sumi-e and East Asian brush painting.
- Treatment: rice-paper ground, grey washes that deepen at overlaps, dry-brush marks and soft bleeding edges. Recede distant shapes into mist and leave substantial unpainted space. Restrict vermilion to a few purposeful accents.
- Impact language: an ink splash with a swift brush arc.
- Verify: tonal layering, brush character and negative space. The example's vertical Devanagari title is subject-specific, not a requirement for every ink-wash scene.

### 03 Shadow Puppet (page 7)

- Context named by the guide: Tholu Bommalata leather puppetry from Andhra Pradesh.
- Treatment: backlit cotton-screen stage; translucent dyed-leather shapes with carved edges and light passing through perforations. Visible control rods and soft projected shadows help establish the physical medium.
- Impact language: a brief lamp flare.
- Verify: transmitted light through leather and holes, consistent rods and screen. Derive lamp flicker from time rather than unseeded random calls.

### 04 Paper Cut-out (page 7)

- Treatment: layered coloured card with fine white cut edges, soft contact/drop shadows, paper texture and stacked strips for clouds and sky.
- Motion: poses step at 12 fps while the delivered clip remains 30 fps; use small reproducible offsets for each held pose.
- Impact language: a cut-paper star.
- Verify: readable physical layering and cut edges. Quantize pose time with `floor(t * 12) / 12`; avoid changing texture every output frame.

### 05 Stained Glass (page 7)

- Treatment: jewel-coloured tessellated forms divided by dark lead channels, a pointed window frame, structural bars and light transmitted from behind.
- Impact language: a white/gold glass star with flare.
- Verify: partitioned glass pieces, leading and backlight rather than ordinary coloured shapes with an outer glow.

### 06 Anime (page 8)

- Treatment: bold ink silhouettes, saturated skies, large cloud masses and hard-edged two-tone cel shading. Confine speed lines to the fast approach.
- Impact language: a three-frame monochrome impact burst, then one red frame, with lens flare.
- Verify: at 30 fps with impact at 2.0 seconds, the monochrome treatment spans frames 60-62, followed by the red treatment on frame 63. This frame mapping is a studio interpretation of the guide's timing. Adapt the effect for story tone and viewing comfort; it is not compulsory in every anime treatment.

### 07 Warli (page 8)

- Context named by the guide: a wall-art tradition from Maharashtra.
- Treatment: rice-paste white figures against red-brown earth. Build forms from circles, triangles and lines; examples use paired-triangle bodies, fan-like wings, scalloped clouds and repeating triangular borders.
- Motion: line variation updates at 8 fps, deterministically.
- Impact language: expanding dotted rings.
- Verify: disciplined geometric vocabulary and white/earth contrast. Use `floor(t * 8)` as the held variation index; keep texture stable.

### 08 Blueprint (page 8)

- Treatment: cyanotype-blue field, white technical line work, grid, dimension leaders, callouts, dashed motion paths and a title block. A targeting reticle can become an event/time label.
- Impact language: the tracking label changes to an impact label at the contact time.
- Verify: precise diagram hierarchy, legible labels, exact label-change timing and clear paths.
- Evidence boundary: the source's example values, including 21.6 m and a 7.4 m wingspan, are drawing annotations for its fictional scene. They are not verified historical or engineering measurements. Replace with sourced values or clearly mark a diagram as schematic/not to scale. Technical styling must not manufacture authority.

### 09 Ukiyo-e (page 9)

- Context named by the guide: Edo-period Japanese woodblock printing.
- Treatment: black key-block contours, subdued flat inks, a Prussian-blue sky gradation, red sun, horizontal mist, printed woodgrain and wave-like cloud forms. A cartouche/seal can hold a relevant title if appropriate.
- Impact language: left open by the source. Choose a woodcut-compatible motif deliberately rather than assuming a specified effect.
- Verify: print texture, contour discipline and flat ink relationships. The example's Devanagari lettering is specific to its subject.

### 10 Miniature Painting (page 9)

- Context named by the guide: Pahari court miniature painting from the Himalayan foothills.
- Treatment: a lapis sky band, gold scroll-like clouds, pale lower washes, green rolling hills, rounded dotted trees and a river. Combine jewel-flat colour, very fine contours, burnished gold details, pearl-like dots and a red/gold vine border where appropriate.
- Impact language: gold rays.
- Verify: delicate line weight, fine ornament and the contrast of gold detail with flat jewel colours.

## Formats and framing (pages 5 and 13)

| Preset | Canvas | Text rectangle | Key-action rectangle |
| --- | --- | --- | --- |
| Vertical example | 1080 x 1920 | x 60-960, y 250-1500 | Compose around the actual platform overlay |
| Landscape example | 1920 x 1080 | x 192-1728, y 108-972 | x 96-1824, y 54-1026 |

These are the guide's presets, not current platform specifications. Landscape uses wider travel and edge-to-edge environmental layers; portrait stacks the composition. Reuse shapes and poses, change camera/layout values. Load an appropriate font when a requested title needs Devanagari or another script; inspect actual glyph rendering.

## Optional style-comparison reel (page 11)

Only use this recipe when a style showcase is requested. Ten two-second excerpts make 20 seconds of comparisons; opening and closing bring the example to about 26 seconds. Start each source excerpt at 1.05 seconds: its 2.0-second contact then lands 0.95 seconds into the excerpt. Align the spoken style name and label reveal with the card transition.

The source uses a cream field, gold-framed cards, a numbered list and a promotional comment CTA. Those are showcase choices, not channel defaults or required wording. Its -14 LUFS mix is a useful example target; choose and verify loudness for the actual delivery. Use the installed free Kokoro path unless the user authorizes another service.

## Studio adaptations and limits

- These are textual art-direction recipes with colour swatches; the guide does not provide ten finished animated clips, production code or licensed asset packs.
- No extra software or paid tool is needed merely to add this reference inventory.
- Inspect current HyperFrames help and installed skill contracts when rendering. The PDF's version-specific `render -c ... -w 1` example is not a verified command for the installed release.
- Render one worker at a time as a practical starting point on this studio's approximately 8 GB machine. This is a local production choice, not a guarantee of render time.
- Use the guide's structure as inspiration and keep source facts separate from illustrative conventions.
