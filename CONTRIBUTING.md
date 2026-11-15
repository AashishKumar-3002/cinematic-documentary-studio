# Contributing

Contributions that improve documentary storytelling, local production, rendering reliability or setup portability are welcome.

1. Open an issue describing the concrete problem or proposed improvement.
2. Keep changes focused and preserve the primary cinematic-film workflow.
3. Include reproduction steps, validation and a small visual example when animation changes.
4. Keep credentials, models, downloaded transcripts and rendered films out of commits.
5. Credit upstream code and media, retain licence notices, and distinguish illustrations from factual evidence.

Before submitting:

```powershell
. ./tools/env.ps1
python tools/check_repository.py
python -m unittest discover -s tools/tests -v
```

For scene changes, also inspect representative frames and transitions. Automated imports and syntax checks cannot judge narration, scientific correctness, visual timing or emotional delivery. Avoid presenting predicted growth as measured audience performance.

Downloaded tutorial transcripts and personal reference files are intentionally excluded. Contribute independently worded notes with source attribution rather than redistributing source material without permission.

Project contributions are offered under the root MIT licence. Third-party code retains its own licence. Do not add paid-service requirements to the free local baseline without explaining why they are needed and keeping them optional.
