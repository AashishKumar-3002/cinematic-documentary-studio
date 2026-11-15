# YouTube publishing

Production works without a YouTube account. Publishing is a separate, optional step; cloning or running setup does not connect an account or upload a film.

Examples below use PowerShell. On macOS/Linux load `source tools/env.zsh` or `source tools/env.sh`, and replace `./tools/youtube.ps1` with `python tools/youtube_manage.py`. The upload helper is the same Python command on each platform.

## Prepare the package

```powershell
. ./tools/env.ps1
python tools/package_nyos_release.py
```

This creates the example's metadata, description, chapters, subtitle track, source notes, credits and thumbnails under `projects/lake-nyos/film/release/`. Review the complete rendered film and the actual audience/disclosure settings before publishing. Package generation resets the example's release record; run final verification afterwards if you need its checksum recorded again.

## Connect your own account

1. Enable the YouTube Data API in your own Google Cloud project.
2. Create a Desktop OAuth client and save its JSON as `credentials/client_secret.json` locally.
3. Configure your OAuth consent/test-user settings as needed.
4. Run the local status command, then explicitly connect the required profile:

```powershell
./tools/youtube.ps1 status
./tools/youtube.ps1 connect --profile read
./tools/youtube.ps1 channel --channel YOUR_CHANNEL_ID
```

Confirm the returned channel is the intended destination. Separate profiles exist for `upload`, `manage` and `analytics`; use only those needed for your action. Each user supplies their own credentials. The repository contains none.

## Upload deliberately

The uploader makes a real upload and defaults to private:

```powershell
./tools/youtube.ps1 connect --profile upload
python tools/upload_youtube.py projects/lake-nyos/film/out/lake-nyos-full-v1-1080p.mp4 --channel YOUR_CHANNEL_ID --metadata projects/lake-nyos/film/release/upload.json
```

Metadata must explicitly include `title`, `description`, `madeForKids` and `containsSyntheticMedia`. Do not copy the example's settings blindly for a different video. Confirm processing and playback after uploading; an accepted API request is not proof that the film is ready to publish.

Management commands such as metadata, thumbnails and scheduling default to a read-only plan. Their `--apply` switch performs the change. Channel verification is required. Comment tools read threads for review; they do not post replies. No unattended public publishing schedule is included.

For command details and scope descriptions, see [the management reference](../.agents/skills/youtube-management/references/operations.md). Actual API access, account eligibility and quotas must be checked on the connected account; local unit tests use mocks.
