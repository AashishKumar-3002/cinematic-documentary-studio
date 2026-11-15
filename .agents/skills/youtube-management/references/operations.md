# Connection and operation reference

Verified against official API documentation on 2026-11-15. The Python client libraries already live in `.venv`; scripts do not need an API broker subscription. Google quotas, account feature eligibility and OAuth project restrictions still apply.

## Connect when requested

1. In the user's Google Cloud project, enable YouTube Data API v3. Enable YouTube Analytics API for analytics access.
2. Configure the OAuth consent screen and a Desktop application OAuth client. If the project is in testing, add the intended Google account as a test user. Save the downloaded client JSON as `credentials/client_secret.json` in this project. Never request the client JSON contents in chat.
3. Run `./tools/youtube.ps1 connect --profile read`. This explicitly starts browser sign-in and prints the returned channel resource. Confirm its title and ID with the user's intended channel. Brand-account/delegated access can vary; API access must actually return the intended channel.
4. Connect `upload`, `manage` or `analytics` profiles only when those capabilities are requested. Each profile has its own local token. No write is made merely by connecting.

| Profile | Scopes | Intended use |
| --- | --- | --- |
| read | youtube.readonly | Channel, video, playlist and comment inspection |
| upload | youtube.readonly + youtube.upload | Verify channel, upload video |
| manage | youtube.force-ssl | Metadata, thumbnails, captions, playlists, visibility and scheduling |
| analytics | youtube.readonly + yt-analytics.readonly | Channel verification and non-monetary reports |

Google describes force-ssl as a broad management permission that can include deletion. This helper does not implement deletion, but the granted scope is broader than its command surface. Monetary reports are not requested. Existing legacy `credentials/token.json` is not reused; profiles are saved as `credentials/youtube-<profile>.json`.

## Read commands

Run from the project root. The channel ID in examples is a placeholder.

```powershell
./tools/youtube.ps1 status
./tools/youtube.ps1 channel --channel UC_EXPECTED
./tools/youtube.ps1 videos --channel UC_EXPECTED
./tools/youtube.ps1 video --channel UC_EXPECTED --video VIDEO_ID
./tools/youtube.ps1 playlists --channel UC_EXPECTED
./tools/youtube.ps1 comments --channel UC_EXPECTED --video VIDEO_ID
./tools/youtube.ps1 analytics --channel UC_EXPECTED --start 2026-11-01 --end 2026-11-14 --report daily
./tools/youtube.ps1 analytics --channel UC_EXPECTED --start 2026-11-01 --end 2026-11-14 --report traffic --video VIDEO_ID
./tools/youtube.ps1 analytics --channel UC_EXPECTED --start 2026-11-01 --end 2026-11-14 --report retention --video VIDEO_ID
```

Videos, playlists and comment listing return at most 50 entries per request; use `--page-token` with `nextPageToken`. Thread replies are an included subset, not necessarily every reply. Channel ownership is verified before reading a specific video's comments. Empty analytics rows can mean no available data; they are not proof of zero audience interest. Daily and traffic queries return views/watch time; daily also includes average view duration. Retention requires one video. Dates are report dates, not local scheduling times.

## Write plans

Connect the read profile first for dry-run inspection. Below, commands without `--apply` validate inputs, read existing resources and save a plan under `output/youtube-management/`, but do not modify YouTube. After an authorized review, the same command with `--apply` uses the manage profile. Plans are review records, not automatically approved actions.

```powershell
./tools/youtube.ps1 metadata --channel UC_EXPECTED --video VIDEO_ID --file projects/episode/metadata-patch.json
./tools/youtube.ps1 visibility --channel UC_EXPECTED --video VIDEO_ID --privacy private --publish-at '2026-12-01T18:00:00+05:30'
./tools/youtube.ps1 thumbnail --channel UC_EXPECTED --video VIDEO_ID --file projects/episode/thumbnail.png
./tools/youtube.ps1 captions --channel UC_EXPECTED --video VIDEO_ID --file projects/episode/captions.srt --language en --name English
./tools/youtube.ps1 create-playlist --channel UC_EXPECTED --file projects/episode/playlist.json
./tools/youtube.ps1 add-to-playlist --channel UC_EXPECTED --video VIDEO_ID --playlist PLAYLIST_ID
```

Metadata patches support title, description, tags, categoryId, defaultLanguage and defaultAudioLanguage. The helper preserves other writable snippet values. It refuses unsupported fields. Playlist creation expects title and optional description/privacyStatus; privacy defaults to private. Adding an existing video to the same playlist returns `already_present` rather than duplicating it.

Visibility changes preserve the video's other writable status properties. A command without `--publish-at` removes a prior scheduled publish time deliberately; include that cancellation in the review. YouTube scheduling is for private videos not previously published. Some conditions are enforced by Google, so report a rejection rather than retrying blindly.

Thumbnail upload accepts PNG/JPEG, checks the documented API media-size ceiling and waits for a nonfailed processing state; account custom-thumbnail eligibility still matters. Do not assume web Studio and API size limits match or that all accounts expose all features. Caption insertion accepts SRT/VTT with authored timing; it adds a track, so inspect existing tracks in Studio to avoid repeated insertion. Deprecated automatic caption synchronization is not used.

## Video upload

```powershell
. ./tools/env.ps1
python tools/upload_youtube.py output/final.mp4 --channel UC_EXPECTED --metadata projects/episode/upload.json
```

This command uploads immediately; it is not a dry run. It requires the connected upload profile and verifies the expected channel before sending the media. Metadata must explicitly include title, description, madeForKids and containsSyntheticMedia (the latter two must be JSON booleans); optional tags/categoryId are supported. It defaults to private. Use `--privacy public` only for an explicitly authorized public upload. Prefer private upload, processing/review, then a separately authorized visibility/schedule change. Google can restrict uploads from unaudited projects to private.

## Known feature limits

No delete, comment posting/moderation, ad settings, premieres, community posts, end screens/cards, revenue reports, title/thumbnail native experiments, channel-branding mutation or unattended scheduler is implemented. Use YouTube Studio for these when requested and available. Analytics API metrics do not map one-for-one to every Studio screen; obtain a Studio export when needed rather than claiming unavailable metrics.

## Sources

- OAuth scopes: https://developers.google.com/identity/protocols/oauth2/scopes
- Video updates: https://developers.google.com/youtube/data/reference/rest/v3/videos/update
- Video status and scheduling: https://developers.google.com/youtube/data/reference/rest/v3/videos
- Thumbnail upload: https://developers.google.com/youtube/data/reference/rest/v3/thumbnails/set
- Captions: https://developers.google.com/youtube/data/reference/rest/v3/captions/insert
- Playlist items: https://developers.google.com/youtube/data/reference/rest/v3/playlistItems/insert
- Analytics queries: https://developers.google.com/youtube/analytics/reference/reports/query
- Channel report combinations: https://developers.google.com/youtube/analytics/channel_reports
