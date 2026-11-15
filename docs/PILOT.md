# Rebuild the Lake Nyos pilot

The included example is a 5:29 English science documentary about the 1986 Lake Nyos disaster. Its script, storyboard, sources and scene code are included. Full movies and audio are generated locally rather than committed to Git.

## 1. Set up

Complete [installation](SETUP.md), then run the following from the repository root:

The examples below use PowerShell. In zsh run `source tools/env.zsh` instead of `. ./tools/env.ps1`; in bash use `source tools/env.sh`. The remaining Python commands are shared.

```powershell
. ./tools/env.ps1
python tools/build_nyos_story.py
python tools/build_nyos_full_audio.py
```

The narration uses Kokoro `af_heart` at speed 0.90, with one continuous call per chapter. On a clean clone the first take is synthesized as well; an existing approved first take is reused when present. Faster Whisper creates approximate word timings, which drive emphasis and camera timing. Listen to names and important terms yourself; automated transcription is a coverage check.

## 2. Prepare credited imagery

```powershell
python tools/prepare_nyos_full_assets.py
python .agents/skills/cinematic-film/scripts/fetch_commons.py get --project projects/lake-nyos/film
python .agents/skills/cinematic-film/scripts/prep_assets.py --project projects/lake-nyos/film
python .agents/skills/cinematic-film/scripts/fetch_commons.py credits --project projects/lake-nyos/film
python .agents/skills/cinematic-film/scripts/make_beats.py --project projects/lake-nyos/film
```

This retrieves NASA imagery, Natural Earth boundaries and the two Commons photographs. The source records distinguish historical photographs from schematic reconstructions. Remote hosts may change or throttle downloads.

## 3. Review frames and build sound

```powershell
python tools/review_nyos_film.py
python .agents/skills/cinematic-film/scripts/render.py --project projects/lake-nyos/film --cues
python .agents/skills/cinematic-film/scripts/build_sfx.py --project projects/lake-nyos/film
python .agents/skills/cinematic-film/scripts/mix_soundtrack.py --project projects/lake-nyos/film --sfx-db -12
```

Review sheets appear in `projects/lake-nyos/film/out/review/`. Inspect legibility, timing, scientific meaning and transitions before the full export. The effects are synthesized; no downloaded music track is required.

## 4. Render and prepare release files

```powershell
python tools/render_nyos_checkpointed.py --workers 2
python tools/package_nyos_release.py
python tools/verify_nyos_delivery.py
```

The checkpoint runner saves four-second sections and assembles `projects/lake-nyos/film/out/lake-nyos-full-v1-1080p.mp4` when all sections finish. Re-running resumes sections with matching frame counts. **Use checkpoints only for unchanged input files.** If you edit the scene, assets or timings, move the previous checkpoint folder aside first. This version does not automatically fingerprint inputs.

The verification helper checks the original pilot's expected 9,856 frames and duration-related properties, extracts final-film stills, measures audio and records a checksum. If you intentionally change the film's duration, update that pilot-specific expected frame count. This is a worked example, not a generic one-command documentary generator.

## New documentaries

Start with the [primary cinematic-film skill](../.agents/skills/cinematic-film/SKILL.md) and its scaffold:

```powershell
python .agents/skills/cinematic-film/scripts/new_project.py projects/my-film
```

Write and fact-check the new story, record continuous narration takes, prepare timed beats, and author a scene for that story. The Nyos-specific helpers have explicit episode paths and should be adapted rather than pointed at an unrelated episode.

Carry forward the [saved production lessons](../projects/lake-nyos/feedback.md): engaging scripting and delivery, narration-timed highlights/circles/reveals, and purposeful sound for important visual events. These lessons guide future work; the shared pilot remains the original reviewed film.
