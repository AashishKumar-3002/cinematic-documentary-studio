---
name: youtube-management
description: Manage this documentary channel's publishing packages, video metadata, thumbnails, captions, playlists, schedules, comment review, and performance analysis through project-local YouTube API tools or YouTube Studio.
---

# YouTube management

Operate within the user's free-tools, project-local setup. Use the official Google APIs through `tools/youtube.ps1` and the existing `tools/upload_youtube.py`; dependencies are already installed. No third-party transcript subscription or MCP broker is required. This skill supplies workflow and tools, not a connected account or guaranteed channel growth.

Read [connection and commands](references/operations.md) before first account access or an unfamiliar operation. Read [publishing and analysis](references/publishing.md) for release preparation or a performance review. Treat title formulas, upload cadence and experiment ideas as adaptable guidance.

## Ground the channel and intent

Run `tools/youtube.ps1 status` to inspect local setup. This does not sign in or contact Google. Authenticate only when the user asks to connect, using the minimum relevant profile. Verify the returned channel ID/title before recording it in the project's channel profile; never guess the ID from a name. If multiple or wrong channels appear, stop dependent writes and resolve the intended channel.

Every management request requires the expected `--channel` ID; the helper verifies ownership. Keep credentials under ignored `credentials/`. Never paste tokens into messages or save them in release packages. OAuth profile scopes are documented in the setup reference; the management profile includes broad Google permissions even though this helper exposes no delete operation.

## Publishing and updates

Prepare a concrete package: final video, accurate title/thumbnail, description with sources and credits, chapters where useful, time-coded captions, intended audience/disclosure settings, playlist and explicit visibility/timezone. Use the production and style inventory as optional assistance.

The user's request to prepare or optimize is not an instruction to publish. Within already authorized scope, complete preparation and read-only checks without repeatedly seeking permission. For metadata, scheduling, thumbnails, captions and playlists, first run without `--apply`; review the saved plan and existing values. Execute with `--apply` only for a change the user actually authorized. The flag is a technical switch, not user consent. The uploader performs a real upload when invoked and defaults to private.

Preserve unrelated fields. The helper copies mutable snippet/status values before partial edits because YouTube update calls can reset omitted fields within an updated part. Scheduling requires a future timestamp with timezone and private visibility; confirm the video meets YouTube scheduling conditions. Inspect readback and processing state; distinguish API acceptance from complete publication.

The helper reads comment threads for review and drafting only. Do not send replies, post comments, moderate or delete anything without the user's explicit instruction. There is no unattended publishing schedule installed. No automatic public promotion, outreach or account changes follow from loading this skill.

## Analyse and improve

Retrieve the requested date range and report type; label data latency, missing rows, pagination and low sample sizes. Keep Shorts and long-form comparisons distinct. Use traffic context, watch time and retention to form hypotheses rather than diagnosing causes from one number. Use Studio/CSV exports for metrics or features absent from the helper; never invent CTR or revenue.

Report what was prepared, changed and verified, with actual returned IDs/URLs and limitations. Live authentication and mutation checks remain unverified until a channel is connected.
