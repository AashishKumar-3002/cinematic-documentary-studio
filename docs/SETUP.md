# Installation and environment

## Supported baseline

The pilot was produced on Windows with Python 3.11 and approximately 16 GB RAM. This is the tested setup. Rendering is CPU-based; a dedicated GPU is not required. Start with two render workers on another machine and increase only when memory allows. Full-film export can take many minutes.

Install Git and Python 3.11 beforehand. Node.js 22.20+ is optional for the HTML/HyperFrames workflow. An AI coding assistant helps author scripts and scenes, but is separate from the free local runtime and may have its own subscription cost.

## Windows / PowerShell

From the cloned repository root in PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup.ps1
. ./tools/env.ps1
./tools/setup.ps1 -CheckOnly
```

`-ExecutionPolicy Bypass` applies to that process; it does not change the machine's stored policy. The setup creates `.venv`, installs the direct dependencies from `requirements.txt`, downloads two Kokoro model/voice files (about 354 MB total), and prepares FFmpeg/FFprobe under `tools/bin`. Existing FFmpeg executables on PATH are reused when available; otherwise a Gyan Windows essentials build is downloaded and checked against the vendor's SHA-256.

The model downloads use a named release and SHA-256 values matching the pilot. `tools/download_runtime.py --check` verifies the models without downloading. Faster Whisper downloads its speech model under `models/whisper` on first use. Downloads require an internet connection; narration and alignment run locally after the files are present.

For optional integrations:

```powershell
./tools/setup.ps1 -WithHtml
./tools/setup.ps1 -WithResearch
```

The first installs npm dependencies using `package-lock.json`. The second installs the optional research packages and a project-local Chromium browser. Source websites may require authentication, impose limits or block extraction; installing a tool does not grant access.

## What is included in Git

Source code, project scripts/storyboards, image-source manifests, licence notices, all 18 project skills, the licensed cinematic engine, and a small documentation preview are included. Virtual environments, model weights, executables, caches, downloaded transcripts, reference PDFs, original downloaded photographs, narration and rendered films are excluded.

The [skill catalogue](SKILLS.md) lists all bundled skills and their optional dependencies. This repository's core example uses cinematic-film; other skills are available for supporting workflows. Last30Days uses its own Python 3.12+ research environment so the core studio can remain on Python 3.11.

## macOS and Linux / zsh or bash

The Unix entry points use the same pinned Python dependencies and model hashes as Windows. They use executables named `ffmpeg` and `ffprobe` from `tools/bin` or PATH, and do not download Windows binaries. Existing system media tools remain in their original location so their dynamic-library paths stay intact.

Prerequisites:

- Python 3.11+ with `venv` support; Python 3.11 is recommended. Use `--python /path/to/python3.11` to select it explicitly.
- FFmpeg and FFprobe, either already installed or supplied as executable, platform-compatible files under `tools/bin`.
- A working system font/graphics runtime for the Skia wheel. Minimal Linux installations may need distribution libraries before `import skia` succeeds.
- Node.js 22.20+ only when using `--with-html`.

Install system prerequisites separately using your preferred method. The scripts never run a package manager with elevated privileges or modify shell startup files. On a workstation that already uses Homebrew, `brew install python@3.11 ffmpeg` is one possible manual route; on Linux use your distribution's packages. These manual system installations are outside the project-local bootstrap.

For zsh:

```zsh
zsh tools/setup.zsh --python /path/to/python3.11
source tools/env.zsh
zsh tools/setup.zsh --check-only
```

For bash:

```bash
bash tools/setup.sh --python /path/to/python3.11
source tools/env.sh
bash tools/setup.sh --check-only
```

Omit `--python` when the intended interpreter is discoverable as `python3.11` or `python3`. `--with-html` and `--with-research` enable the same optional components as their PowerShell equivalents. Optional browser downloads do not install operating-system browser libraries automatically.

The zsh launcher delegates installation to the Bash 3.2-compatible script. `env.zsh` configures zsh directly; `env.sh` supports bash. Both keep the virtual environment and caches inside this checkout. Python helpers resolve native tools by platform, and thumbnail generation has project/macOS/Linux font fallbacks.

The setup scripts' syntax/help and environment sourcing were checked under Ubuntu's bash/zsh. Windows remains the only platform with a verified complete pilot production; a full Unix installation, model inference and movie export are not claimed as tested.

## Manual Windows setup

For a manual Windows setup:

```powershell
py -3.11 -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe tools/download_runtime.py --models --ffmpeg
. ./tools/env.ps1
```

On macOS/Linux, use the shell environment above before running the shared Python commands. The Windows-only render-progress PowerShell helper can be replaced by reading the episode's `out/render-progress.json`.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `ffmpeg` or `ffprobe` missing | Load `tools/env.ps1`; rerun the runtime downloader if necessary. |
| Model SHA-256 mismatch | Keep the rejected `.part` file out of Git; confirm the upstream release and retry. |
| Missing `timing.json` | Generate the full narration before reviewing or rendering the scene. |
| Missing photograph/prepared asset | Run the asset preparation commands in [the pilot guide](PILOT.md). |
| High memory use | Reduce `--workers`; begin with two. |
| New scene edits but old output reused | Checkpoints currently validate frame count, not source changes. Move the old `out/checkpoints1080` folder aside before rendering changed scene/timing inputs. |
| YouTube connection unavailable | Local production still works. Publishing setup is separate; see [publishing](PUBLISHING.md). |

`requirements-lock.txt` and `requirements-research-lock.txt` record the original larger workstation environments for reference. The bootstrap uses the smaller direct-dependency files; a fresh machine has not yet been used for a complete independent film reproduction.
