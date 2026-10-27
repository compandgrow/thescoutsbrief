# The Scout Brief — reel factory

Automated match-day Reels for Instagram @thescoutbrief: an animated gorilla presenter ("Scout", in a suit with a headset) analyses the data of a big-club match, with emotions from smug to furious. Openly backs Man United, Real Madrid, PSG and Bayern, and banters rivals when they lose.

- Pipeline: `/match-day` skill (`.claude/skills/match-day/SKILL.md`), agents in `.claude/agents/`.
- Data: PitchAPI (`engine/pitch.py`, needs `PITCHAPI_API_KEY`). Watchlist + posting config: `config/teams.json`.
- Render: `engine/voice.py` (Kokoro offline TTS + lip-sync) → `engine/music.py` (composed score, ducking) → `engine/render.js` (Playwright frames of `templates/match-reel.html` → ffmpeg).
- Presenter: `presenter/presenter.js` — emotions in `EMOTIONS`, all motion a pure function of time.
- Demo/format reference: `reels/demo-presenter/reel.json` (demo data, not a real match).
- Facts first: every number on screen comes from data with a source path. Never post to @compandgrow.
