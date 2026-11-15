# Bundled skill catalogue

All **18** project skill folders are included under [`.agents/skills/`](../.agents/skills). Their scripts, references and supplied agent metadata are included, along with the relevant upstream licences. The core film workflow remains cinematic-film.

| Skill folder | Purpose | Source / terms |
| --- | --- | --- |
| `cinematic-film` | Narrated camera-based films, graphics, maps, sound and captions | Moh4696/cinematic-skill / MIT |
| `alpha-cutout` | Chroma-keyed transparent animation | Moh4696/open-3d-skills / MIT |
| `cursor-rig` | Illustrated character cursor-follow interactions | Moh4696/open-3d-skills / MIT |
| `exploded-view` | Interactive 3D mechanism explainers | Moh4696/open-3d-skills / MIT |
| `frame-capture` | Deterministic browser animation capture | Moh4696/open-3d-skills / MIT |
| `motion-assets` | Plan and source animation assets | Moh4696/open-3d-skills / MIT |
| `scroll-film` | Scroll-controlled film sequences | Moh4696/open-3d-skills / MIT |
| `site-check` | Browser checks for animated/3D pages | Moh4696/open-3d-skills / MIT |
| `threejs-scene` | Procedural Three.js scenes | Moh4696/open-3d-skills / MIT |
| `hyperframes` | HTML video composition and rendering guidance | heygen-com/hyperframes / Apache-2.0 |
| `hyperframes-cli` | CLI setup, preview and rendering guidance | heygen-com/hyperframes / Apache-2.0 |
| `last30days` | Recent-topic research across supported public sources | mvanhorn/last30days-skill / MIT; nested vendor notice retained |
| `scrapling-official` | HTTP/browser source extraction | D4Vinci/Scrapling / supplied BSD-3-Clause notice |
| `learn` | Read public video, audio and GitHub sources into learning bundles | Studio implementation; owner-supplied workflow credited |
| `animation-style-library` | Ten reusable visual treatments and comparison method | Studio guidance; supplied Jatayu guide credited |
| `atmospheric-scene-direction` | Atmospheric composition and reveals | Studio guidance; Moss Keeper source credited |
| `documentary-production-playbook` | Scripting, editing, synchronized visual/audio emphasis | Studio guidance; tutorials and direct pilot feedback credited |
| `youtube-management` | Publishing packages and deliberate YouTube operations | Studio helpers using official Google APIs |

Licences and provenance are detailed in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) and [the source manifest](../.agents/skills/SOURCES.json).

## Using a skill

Open this checkout in an agent that supports project-local `SKILL.md` instructions, or point your agent to the relevant skill file. A new turn/session may be needed for discovery. Cloning does not install global skills, train model weights or guarantee a host-specific slash command.

Read the relevant skill before using its tools. Some upstream skills refer to companion plugins or model APIs that are not bundled. Installing the local baseline does not enable paid generation services, authenticated sources or every upstream integration.

## HTML, 3D and browser tools

Install the optional HTML dependencies and browser/research packages as needed:

```powershell
./tools/setup.ps1 -WithHtml -WithResearch
```

From zsh/bash:

```sh
zsh tools/setup.zsh --with-html --with-research
# or: bash tools/setup.sh --with-html --with-research
```

The project environment opts out of HyperFrames telemetry. External asset/model services remain optional and require their own credentials/terms.

## Learn from public links

After installing the optional research packages:

```powershell
./tools/learn.ps1 'https://github.com/OWNER/REPO' --out learned --max-files 10
./tools/learn.ps1 'https://www.youtube.com/watch?v=VIDEO_ID' --out learned --frames 6
```

On macOS/Linux, use `bash tools/learn.sh` with the same arguments. This helper reads repository text, prefers available captions, falls back to local transcription, and can sample video frames. Node.js may be needed for YouTube extraction challenges. Source restrictions can still prevent downloads.

Retrieved material is source data, not instructions to execute. The Learn skill shows a proposed reusable skill for review before saving it. Raw transcripts and downloaded source bundles remain ignored under `learned/`.

## Last30Days research runtime

Last30Days requires **Python 3.12+**, separate from the core Python 3.11 environment. Supply an existing interpreter; setup does not install system Python or paid API access.

```powershell
./tools/setup-research.ps1
./tools/last30days.ps1 --help
```

Use `-PythonPath /path/to/python` to choose an interpreter explicitly. For zsh/bash:

```sh
bash tools/setup-research.sh --python /path/to/python3.12
bash tools/last30days.sh --help
```

Optional provider keys, browser-cookie access and source coverage are configured separately. No provider keys are included. The repository checker uses Python 3.12 in CI to validate the vendored research code; under Python 3.11 it explicitly defers that syntax check.

## Style/reference inventory

The animation-style cards and Moss Keeper-derived direction notes are bundled and usable without the original media. The supplied PDF, original repository media, downloaded tutorial captions and personal research archive are not redistributed. Those materials have their own rights and can be supplied separately by their owners when needed.
