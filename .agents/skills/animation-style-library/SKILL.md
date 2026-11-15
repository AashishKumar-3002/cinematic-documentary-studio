---
name: animation-style-library
description: Choose and apply reusable animation styles from the user's Jatayu guide when planning documentary visuals, comparing art directions, or requesting Madhubani, ink wash, shadow puppet, paper cut-out, stained glass, anime, Warli, blueprint, ukiyo-e, or miniature painting treatments.
---

# Animation style library

Use the user's guide as an optional creative inventory for this documentary studio. It supplements creative judgment; it does not fix the channel's identity or require every video to use one of these styles. Do not generate a Jatayu reel merely because this skill was loaded.

Read [references/styles.md](references/styles.md) when selecting or applying a treatment. It contains all ten styles, visual checks, the shared-shot technique and source page references. The original workstation keeps the supplied PDF and extracted text under `reference/animation-styles/`; that personal reference archive is not distributed. The bundled style cards work independently. Obtain the original from its owner if exact wording or source pages are needed.

## Choose for the story

Recommend a treatment based on the subject, emotional tone, clarity and available assets. For example, blueprint can support a mechanism explanation; paper cut-out can support layered geography; ink wash can support a reflective sequence. These are studio suggestions, not claims made by the guide. Use culturally specific traditions thoughtfully, without implying a stylized reconstruction is historical evidence.

Keep a coherent visual system within an episode. Use a different treatment when it has a narrative purpose. A request for a comparison should reuse the same scene, framing and event times across variants so differences in art direction can be judged fairly.

## Build with shared structure

Separate subject geometry and poses, camera/layout, time-based motion, and the style's rendering treatment. Reuse the first three across style variants; change palette, contours, material, pattern, lighting treatment and impact language. For landscape versus portrait versions, recompose rather than crop the key action.

Render deterministically: a frame must be reproducible from time and a fixed seed, with no accumulated simulation state. Keep random texture stable across frames. For stepped animation, derive poses from a quantized clock and jitter from the step index. Do not seed every texture with the changing frame number, which causes flicker.

Use the installed HyperFrames skills for HTML composition and the current CLI contract. Use the existing local `tools/hf.ps1` wrapper; do not copy the PDF's older render flags without checking installed help. The guide requires no additional software in this studio. Preserve the user's free-tools constraint; optional commercial voice products mentioned in the source are not enabled.

## Verify the actual style

Write the chosen palette, typography and motion choices into the video's DESIGN.md before authoring. Check a pre-action frame, the exact event frame, and an aftermath frame. For the guide's five-second benchmark, those times are 0.6, 2.0 and 4.0 seconds. Use story-appropriate times for other scenes. Check the treatment's distinguishing features in the reference library, mobile legibility, clear silhouettes, pronunciation and narration sync.

The PDF's safe rectangles are useful composition presets, not verified permanent platform UI guarantees. Check the actual delivery format. Its blueprint dimensions are illustrative and must not enter a factual documentary without a source. Its Jatayu scene is a mythological example, not a factual event reconstruction.

Keep creative freedom: use, adapt, combine selectively, or set aside these treatments when another approach better serves the story. Describe adaptations honestly; do not claim cultural authenticity from a prompt alone.
