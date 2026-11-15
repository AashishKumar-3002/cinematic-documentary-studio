# Third-party software and media

The root MIT licence covers this project's original contributions. It does not replace the licences of dependencies, downloaded models or archival media.

## Included cinematic engine

`.agents/skills/cinematic-film/` comes from [Moh4696/cinematic-skill](https://github.com/Moh4696/cinematic-skill), copyright (c) 2026 exploraX, MIT licensed. Its [original licence](.agents/skills/cinematic-film/LICENSE) is included unchanged. The supplied Wright Flyer and coffee examples belong to that upstream distribution.

Local changes include bounded FFmpeg encoder threads, an opt-in broad-spotlight optimization and a link to the studio's saved production feedback. The Lake Nyos scene, cached backdrop, continuous local narration workflow, checkpoint runner and publishing helpers are studio additions. This project builds on that engine; it does not claim to have authored the upstream engine.

## Dependencies downloaded separately

| Component | Upstream | Role |
| --- | --- | --- |
| Skia Python | https://github.com/kyamagu/skia-python | CPU graphics rendering |
| Kokoro ONNX | https://github.com/thewh1teagle/kokoro-onnx | Local narration runtime and model download links |
| Kokoro model | https://huggingface.co/hexgrad/Kokoro-82M | Model and voice information; consult upstream terms |
| Faster Whisper | https://github.com/SYSTRAN/faster-whisper | Local speech alignment |
| FFmpeg | https://ffmpeg.org/ | Video and audio processing; downloaded builds retain their own licence |
| Gyan Windows builds | https://www.gyan.dev/ffmpeg/builds/ | Optional Windows FFmpeg/FFprobe download |
| HyperFrames | https://github.com/heygen-com/hyperframes | Optional HTML video workflow |
| GSAP | https://gsap.com/ | Optional HTML animation; consult its own licence |
| Three.js | https://threejs.org/ | Optional 3D animation |
| Scrapling | https://github.com/D4Vinci/Scrapling | Optional source extraction |
| Google API Python client | https://github.com/googleapis/google-api-python-client | Optional YouTube management |

Python and npm dependencies retain their package licences. Models, executable binaries, dependency installations and browser downloads are excluded from Git.

## Example media

The pilot downloads images from Wikimedia Commons and NASA using the records in [photos.json](projects/lake-nyos/film/photos.json). Individual asset credits remain authoritative:

- Lake Nyos, 1986: Jack Lockwood / USGS, public domain, via Wikimedia Commons.
- Degassing installation, 2001: Bill Evans / USGS, public domain, via Wikimedia Commons.
- Landsat-7 image, 5 February 2001: NASA/Goddard Space Flight Center Scientific Visualization Studio; [source record](https://svs.gsfc.nasa.gov/2348/) and [usage guidance](https://www.nasa.gov/nasa-brand-center/images-and-media/).
- Geographic boundaries: Natural Earth, [public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/).

`docs/assets/pilot-preview.jpg` combines studio-rendered graphics with the credited archival lake photograph. The original downloaded media, generated audio and films are not distributed in the Git repository. Rebuilding an episode downloads its source media and regenerates its credits ledger.

## Additional bundled skills

- The eight Open 3D skill folders originate from [Moh4696/open-3d-skills](https://github.com/Moh4696/open-3d-skills), copyright (c) 2026 exploraX, MIT licensed. Each folder retains a copy of the upstream licence.
- `hyperframes` and `hyperframes-cli` originate from [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), distributed under Apache-2.0. Each folder includes the upstream licence. The installed CLI version used to obtain the skills was 0.9.52.
- `last30days` is the installed 3.39.0 skill snapshot from [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill), copyright (c) 2026 Matt Van Horn, MIT licensed. Its licence and the nested bird-search vendor licence are retained.
- `scrapling-official` retains its supplied [BSD-3-Clause notice](.agents/skills/scrapling-official/LICENSE.txt), copyright (c) 2024 Karim shoair.
- `learn`, `animation-style-library`, `atmospheric-scene-direction`, `documentary-production-playbook` and `youtube-management` contain studio-authored implementation/guidance. The Learn workflow credits setup material supplied by the project owner; its bundled helper is the studio implementation, not the original Claude-only installer. Style and editing notes credit their source guides/videos; the Moss Keeper reference credits the inspected repository. The root MIT licence covers original studio contributions, not the referenced third-party source materials.

See [the full skill catalogue](docs/SKILLS.md) and [source manifest](.agents/skills/SOURCES.json). Bundling a skill does not convey rights to external footage, illustrations, downloaded models or paid provider services.

## References outside the distribution

Downloaded tutorial transcripts, the supplied animation-guide PDF and inspected third-party repository copies are excluded. They are not relicensed or republished here. The production playbook contains attributed, independently worded guidance and direct project feedback; it does not bundle the tutorials themselves.
