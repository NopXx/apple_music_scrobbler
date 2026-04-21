# Apple Music Scrobbler

**English** · [ภาษาไทย](README.th.md)

<img src="assets/icon.png" width="128" alt="icon">

A macOS menu bar app that tracks what's playing in **Apple Music**, sends it to **Last.fm** (now playing + scrobble), and fires **Webhooks** for third-party integrations.

<img src="screenshot/image_1.png" alt="screenshot">

---

## ✨ Features

- 🎵 **Real-time now playing** via AppleScript — no extensions required
- 📡 **Last.fm scrobbling** — instant now-playing updates, scrobble once the threshold is reached
- 🔁 **Smart replay / pause / resume detection** — pause-then-play doesn't re-scrobble (only genuine replay from the start does)
- 🪝 **Webhooks** — POST JSON (compatible with Music-Scrobbler format) with heartbeat support
- 🖼️ **Artwork + animated covers** from iTunes API with hi-res fallback
- 🛎️ **Native notifications** with album artwork
- ✏️ **Edit history** — correct wrong track/artist/album metadata; applied before every scrobble/webhook
- 📊 **Play history** stored in SQLite, exportable/importable as JSON or CSV
- 🍔 **Customizable menu bar** — choose what to show (icon, play state, track, artist, max length)
- 🌍 **Bilingual UI** — English / ไทย

---

## 🚀 Install

### Option 1 — Run as menu bar app (fastest)

```bash
git clone <repo-url> apple-music-scrobbler
cd apple-music-scrobbler
pip3 install -r requirements.txt
python3 app.py
```

The ♪ icon appears in your menu bar. Open Apple Music and hit play.

### Option 2 — Server only (no menu bar)

```bash
python3 server.py
# visit http://localhost:8765
```

### Option 3 — Build .app bundle

```bash
cp .env.example .env
# fill in LASTFM_API_KEY / LASTFM_API_SECRET
# register at: https://www.last.fm/api/account/create

./build.sh
open "dist/Apple Music Scrobbler.app"
```

---

## ⚙️ Configuration

Click the ♪ icon → **Open Settings** (or go to `http://localhost:8765/settings.html`)

| Section | What you can configure |
|---|---|
| **Last.fm** | Connect account, enable/disable scrobbling |
| **Webhook** | URL, heartbeat interval, view payload example, send test |
| **Scrobble** | % of track to listen before scrobble (default 50%), minimum duration |
| **Menu Bar** | Choose what to display (icon, ▶/⏸ state, track name, artist, max length) |
| **Notifications** | Enable/disable, on new play, on successful scrobble |
| **Play History** | Browse / export / import play history (JSON / CSV) |
| **Edit History** | Pre-configure corrections for bad metadata — applied before every scrobble |

---

## 🪝 Webhook Payload

POSTs JSON when events occur (`play`, `replay`, `resume`, `pause`, `scrobble`, `stopped`) using this mapping:

| Internal event | Outgoing `eventName` |
|---|---|
| play / replay / resume | `nowplaying` |
| pause / stopped | `paused` |
| scrobble | `scrobble` |

Example payload:

```json
{
  "eventName": "scrobble",
  "time": 1713600000000,
  "data": {
    "song": {
      "processed": { "artist": "...", "track": "...", "album": "...", "duration": 201 },
      "parsed":    { "artist": "...", "track": "...", "duration": 201, "currentTime": 120, "isPlaying": true },
      "flags":     { "isValid": true },
      "metadata": {
        "label": "Apple Music Scrobbler",
        "trackArtUrl": "https://...",
        "animationUrl": "",
        "primaryMediaUrl": "https://...",
        "primaryMediaType": "image"
      },
      "connector": { "label": "Apple Music" }
    }
  }
}
```

---

## 🧠 Scrobble Logic

- **First play** — new track → send `now playing` immediately
- **Scrobble trigger** — listened ≥ 50% (configurable) **or** ≥ 240 seconds, **and** at least 30 seconds played → send scrobble
- **Pause → Play (same track)** — no re-scrobble
- **Replay** (seek back to start) — allowed to scrobble again
- **Stop → Play (same track)** — counts as a new session, can scrobble again
- **Tracks shorter than 30s** — skipped (per Last.fm rules)

---

## 📂 Project Structure

```
apple-music/
├── app.py              # Menu bar app (rumps + pyobjc)
├── server.py           # HTTP server + tracker + webhook + Last.fm
├── web/                # Static web assets (UI)
│   ├── index.html      # Main UI (now playing + history)
│   ├── settings.html   # Settings UI
│   └── i18n.js         # Thai/English dictionary
├── scripts/            # AppleScripts for music tracking
│   └── tracker.applescript # Legacy — pure AppleScript version
├── setup.py            # py2app build config
├── build.sh            # Build .app bundle
├── start.sh            # Dev start (python3 server.py)
└── requirements.txt
```

Runtime files (stored in `~/Library/Application Support/AppleMusicScrobbler/` when built as .app):

- `settings.json` — config
- `history.db` — play history (SQLite)
- `now_playing.json` — current snapshot
- `edit_history.json` — saved metadata corrections

---

## 🛠️ Development

```bash
# dev build (symlinked — edit code without rebuilding)
python3 setup.py py2app -A

# clean + release build
./build.sh
```

Main dependencies:

- **rumps** — menu bar app framework
- **pyobjc** — NSUserNotification + native macOS APIs
- **py2app** — .app bundle packaging

---

## 📋 Requirements

- macOS 11+
- Python 3.9+
- Apple Music (bundled with macOS)
- Last.fm account (optional) + API key

---

## 🔒 Privacy

- All music data stays local (SQLite + JSON)
- No telemetry / analytics
- Last.fm credentials stored in `settings.json` (local) or bundled at build time
- Webhook URL is user-owned
