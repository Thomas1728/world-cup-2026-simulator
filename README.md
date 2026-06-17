# ⚽ World Cup 2026 Simulator

An installable, single-file web app for simulating the **2026 FIFA World Cup**
(48 teams, 12 groups, Round of 32 → Final). Set each group's final standings, pick
the 8 best third-placed teams, then click your way through the knockout bracket to
crown a champion.

No build step, no dependencies — open `index.html` and play. It also installs as a
**Progressive Web App** (works offline, runs in its own window) once served over HTTPS.

<!-- LIVE_DEMO -->
> 🔗 **Live demo:** https://thomas1728.github.io/world-cup-2026-simulator/

## Features

- **Group stage** — all 12 groups (A–L) with the real teams from the Final Draw
  (5 Dec 2025). Drag rows or use ▲▼ to set the final 1–4 standings in each group.
- **Best third-placed teams** — pick exactly 8 of the 12 third-place finishers to
  advance. They're auto-assigned to their Round-of-32 slots by a constraint solver
  over FIFA's official eligibility table, so **no group-stage rematch** happens
  before the quarter-finals (validated against all 495 possible combinations).
- **Knockout bracket** — the full official mirrored layout (matches M73–M104, plus
  the play-off for third place). Click a team to advance it; winners propagate
  automatically and a slot only becomes selectable once both feeders are known.
- **National flags** for every team (via [flagcdn.com](https://flagcdn.com)).
- **Save / share image** — export the whole bracket as a PNG. On phones this opens the
  native share sheet (e.g. *Save to Photos* on iPhone); on desktop it downloads the file.
- **iOS & Android friendly** — responsive touch layout, larger tap targets, horizontal
  scroll + pinch-zoom for the bracket, and an *Add to Home Screen* hint on iPhone/iPad.
- **Randomize** a whole tournament, **Clear winners**, or **Reset all**.
- **Installable & offline** — add it to your desktop/phone; flags and the app shell
  are cached on first visit so it keeps working without a connection.
- **Auto-save** — your picks persist in the browser via `localStorage`.

## Install as an app

- **Desktop / Android (Chrome, Edge):** open the live demo and click **⬇ Install app**
  in the toolbar (or the install icon in the address bar). It launches in its own window
  and stays available offline.
- **iPhone / iPad (Safari):** open the live demo, tap the **Share** icon, then
  **Add to Home Screen**. (iOS has no install button — the app shows a hint banner.)

## Run locally

```
index.html        →  double-click, or drag into a browser tab
```

Service-worker install/offline features need an HTTP(S) origin, so to test those:

```bash
python -m http.server 8000
# then visit http://localhost:8000
```

## Editing the teams

Team data lives in the `GROUPS` object near the top of the `<script>` in
`index.html`. Each team is `[name, FIFA 3-letter code, flag code]`:

```js
C:[["Brazil","BRA","br"], ["Morocco","MAR","ma"], ["Haiti","HAI","ht"], ["Scotland","SCO","gb-sct"]],
```

The flag code is an ISO 3166-1 alpha-2 code (e.g. `br`), or a flagcdn region code
(`gb-eng`, `gb-sct`) for the home nations.

## Project files

| File | Purpose |
|------|---------|
| `index.html` | The entire app (HTML + CSS + JS) |
| `manifest.webmanifest` | PWA metadata (name, icons, theme) |
| `service-worker.js` | Offline caching of the app shell + flags |
| `icon-*.png`, `apple-touch-icon.png` | App icons |
| `generate_icons.py` | Regenerates the icons (needs Pillow) |

## Notes & accuracy

- Teams, group letters, match codes (M73–M104), dates and bracket layout follow the
  official 2026 schedule.
- The third-place **eligibility** sets (the `3ABCDF`-style labels) are official. The
  exact pairing chosen *within* the legal options can differ from FIFA's Annex C
  lookup in some scenarios, but the result is always a legal, rematch-free allocation.
- Flags are loaded from flagcdn.com (cached for offline use after the first online visit).

## Tech

Plain HTML + CSS + vanilla JavaScript in one file, plus a small service worker and web
app manifest. Bracket connector lines are drawn with an SVG overlay computed from live
element positions, so they stay aligned at any size.
