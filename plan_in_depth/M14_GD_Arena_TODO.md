# M14 — TODO · Group Discussion Arena

> **Completion: 86%** — 17 of 21 functional requirements met, 2 partially (19 Oct: abhinav's `m14-to-90` merged and reviewed; 33% on 17 Oct, 43% after Day 2, 62% after Day 3, 64% after Day 4, 67% after Day 5's walk). Four of the five release gates met, the fifth partly. A GD platform exists — built by GS Adithya Krishna and abhinav from 2026-10-04, **on branches** (`groq-edge-tts` holds all of it; `main` has only the initial commit) and to its own design document (`claude/docs/design.md`) rather than this spec. So it meets several requirements by a different route and misses the spec's distinctive ones: the discourse graph, anti-convergence, speculative pre-generation, missed entry moments. Since Day 4 (19 Oct) it is part of the platform: it signs in with Platform_Core's identity, opens from the shell's menu at `/gd`, and sends its results to the skill graph (M04).
>
> _Method: `(met + ½ × partial) ÷ total`, counted from the spec, 2026-08-28; audited against the `groq-edge-tts` branch's code on 2026-10-17 (0% → 33%); re-counted on `wrap-up` after Day 2, 2026-10-18 (33% → 43%), after Day 3 the same day (43% → 62%), after Day 4 on 19 Oct (62% → 64%: FR-14.7's 350 ms bound shown), and after Day 5's walk the same day (64% → 67%: FR-14.20's overlap shown in a five-participant session), and after abhinav's `m14-to-90` with its review the same evening (67% → 86%: FR-14.4, 14.10, 14.14, 14.15, 14.16, 14.17 met). One measure applied the same way to all nineteen modules so they compare; it counts requirements, not screens or gates._

Task list for taking **M14 — Group Discussion Arena** to 100% of [M14_GD_Arena.md](M14_GD_Arena.md).

> **This is the branch that holds the plan.** The `todo` branch carries the
> spec and this list and nothing else, so the module's own history stays
> about its code. Sync it here when something lands.

> **Read this first when starting a session on M14.** It is the running state of
> the module: what is done, what is next, and what is deliberately deferred.
> Update it as things land — a stale list is worse than no list, because the
> next session trusts it.

- **Repo:** `GD_Arena`

Legend: ✅ done · 🟡 partly done · ⬜ not started

---

### 2026-10-17 — the plan: wrap GD by Wed 21 Oct

All wrap-up work lands on branch **`wrap-up`** (cut from `groq-edge-tts`, which
holds everything the team built); `main` gets it on Day 5. Owners are
suggested from who built each part — adjust them.

| Day | Goal | Work | Owner (suggested) | Done when |
|---|---|---|---|---|
| **1 · Sat 17 Oct** ✅ | It runs on today's keys | Commit the two model fixes with tests (blockers 1–2 below); fix the database lock — LLM work outside write transactions, the job visible the moment it exists, SQLite in WAL mode (3); pace calls from Groq's remaining-tokens header and fall back to the other model instead of sleeping, one organization's key only (4); `edge-tts` in requirements, `.env.example` for Groq and Edge (5) | Ansh | ✅ **Done 17 Oct** (`8edaf70`, `f29b607`, `f5c2f4c` on `wrap-up`): six persona lines, replies 1.1–1.4 s; the report in 75 s (was 6+ min or never), the job visible as RUNNING meanwhile; 17 of 17 sign-ups during it succeeded (were 500s); 13 rate limits each moved to the other model, no lockstep sleeps; 366 tests |
| **2 · Sun 18 Oct** ✅ | A panel that behaves like one | A moderator persona: an opening round that invites the student (EC-14.1), a redirect when one voice dominates (EC-14.2), a closing call (FR-14.3); stances sampled per persona (FR-14.4); an anti-convergence block, and a curveball after three yields (FR-14.5, EC-14.4); a bid scheduler — eagerness × relevance × time since last turn (FR-14.6); personas admit they are AI when asked (AC-14.5, EC-14.14); no invented statistics (6) | Adithya | ✅ **Done 18 Oct** (`fe22deb`, `ab246fa`, `2dea9f6`, `aa4625d` on `wrap-up`): live, the moderator opened with "Asha, what's your take first?", all three personas spoke, no line repeated another, nothing invented; "are you a bot?" answered honestly 6 of 6 by the model with the turn instruction, guaranteed by a guard; replies 0.9–1.45 s (a barge-in reply had waited 14.6 s — fixed); 0 persona and 0 evaluator failures; 405 tests |
| **3 · Mon 19 Oct** ✅ | What the student sees | Text GD mode — typed turns, same scheduler and scoring (FR-14.19); live speaking-time bars (FR-14.11); a recent-ideas strip (FR-14.13); raise-hand (FR-14.12); a silent student's report that encourages and does not contradict itself (EC-14.1, blocker 8) | abhinav | 🟡 **Built 18 Oct, a day early** (`6fcd1d1`, `091891d` on `wrap-up`). In a real browser (headless Edge): "Type instead" starts the session live, typed turns are answered, "are you a bot?" typed → "I'm an AI participant…", raise hand → "Asha Rao, please go ahead", the bars move, the ideas strip shows two ideas and an open question, no console errors. Found and fixed on the way: with no preparation the page never learned the discussion had started (composer disabled, microphone deaf). ✅ **Both morning checks done 19 Oct** (`1258678`): a silent student's report is kind all the way through — the narrative is now written without a model (told to be kind, it still opened "you contributed nothing"), and it quotes the real invitation; typed turns re-walked, credited by their spoken length (0:05 for one point, was 0:01). Also: a pending raised hand is cancelled when the student comes in on their own. 421 tests |
| **4 · Tue 20 Oct** ✅ | Part of the platform | Sign in with the platform session (Platform_Core identity), not a second account; ports 8114 / 5214 and the platform's start script; a "Group discussion" entry in the shell; GD results reach the skill graph as M04 observations; measure barge-in (AC-14.2, ≤ 350 ms) and floor grant → first audio (AC-14.6, ≤ 800 ms) | Ansh | ✅ **Done 19 Oct, a day early** (`677f8b4`, `6b9cba0` on `wrap-up`; the shell's side on Platform_Shell branch `feat/gd-entry`, `b18024f`, not merged). Live, in headless Edge: a student signed in on `:5173` opened **Group discussion** from the menu, practised (typed) inside the frame — GD's own brand and sign-out gone — finished, and their skill graph gained a **Communication** group: Listening to the Question, Structuring an Answer, Handling Interruptions, "just started · tested 1×" (15 → 18 topics with evidence). M04 records GD's evidence but by its own rule (EC-4.17) does not move the ability estimate; BKT p(known) did move (0.44, then 0.78 after a second session). Content and leadership have no honest M04 concept and are not sent; critical thinking is sent when the GD type scores it. `start_gd.bat` opened both tabs and the platform's `stop` closed them; the model key appears on no command line. **Found and fixed on the way:** the report page never noticed a report it was opened before ("updates by itself" while it never asked again); a nameless platform student was "Student" and the moderator invited himself; `.local` addresses failed email validation, so every response with one would 500; a package named `platform` shadowed Python's own; and with no speech-to-text engine the stub would have turned a spoken turn into canned sentences, scored them and quoted them to M04 — now nothing is sent with the stub, and the platform runs Groq's Whisper on the same key (heard word for word). **Measured** (12 lines, 6 barge-ins): barge-in — the server stops a line **8–13 ms** after the student starts; with the browser's voice detector (3 × 2048-sample frames, ~128–171 ms) about **150–230 ms**, inside AC-14.2's 350 ms, not yet measured with a real microphone. Floor grant → first audio — **p95 4.5 s, median 3.2 s: fails AC-14.6 (800 ms)**. The model takes 0.73 s; Edge speech 1.25 s to its first chunk and 2.2 s to a playable line, and the browser plays only once the whole line has arrived. A student hears a reply ~3.8 s after they stop (the 1.1–1.4 s on Days 1–2 was to the text). On this connection Whisper adds 1.5–13 s to a spoken turn (variable; typed turns skip it). 454 tests |
| **5 · Wed 21 Oct** 🟡 | Proven and merged | Walk the 5 gates and 15 edge cases and write the results here; a two-browser human room on Docker/LiveKit; merge `wrap-up` → `main`; README and this TODO brought to the new state | all | 🟡 **Walked 19 Oct** (`b2e81b0`, `d0f6347`, `998784f`, `0b0a348` on `wrap-up`): the gates and edge cases are written up below. **Gates:** AC-14.1 ✅, AC-14.2 ✅, AC-14.4 ✅ (fixed), AC-14.5 ✅, AC-14.3 🟡. **Edge cases:** 5 ✅, 2 🟡, 8 ⬜ — the ⬜ ones are human rooms, features not built, or (EC-14.10) not yet shown. **Ports:** GD now takes only PORTS.txt's: API 8114 and web 5214 standalone too (it took 8000, the gateway's, and 3000, on the do-not-use list), Grafana 8314 by the 83xx ops-app rule (it took 3001, Langfuse's), Prometheus no host port (9090 is a native service here); its containers' ports recorded in a new PORTS.txt section, and all ten PORTS.txt copies made identical. **Not done, by the user's call ("don't use docker unnecessarily, deployment is not needed"):** the two-browser human room over LiveKit, so EC-14.3, 14.5, 14.11 and 14.12 were not walked. **Still to do:** merge `wrap-up` → `main` (a team call), and the README pass. 465 tests |

**AC-14.6 after Day 4 — the call to make.** 800 ms from floor grant to sound cannot be met by tuning: the line is written after the floor is granted (0.73 s) and Edge speech needs 1.25 s to its first chunk. Two changes together could: (1) play each line from its first chunk instead of when it has fully arrived (about −1 s); (2) FR-14.8, writing the next bidders' lines while the student is still speaking, so the model's time leaves the path. FR-14.8 is in the deferred list below; moving it forward is the user's decision.

**Deliberately after the five days** — each is research-sized and would be
rushed: the discourse graph with typed edges, and the uptake and novelty
scoring built on it (FR-14.14, the rest of FR-14.15); missed-entry moments
with audio playback (FR-14.17); speculative pre-generation (FR-14.8); hybrid
human + AI rooms (the rest of FR-14.1); case, for/against and fishbowl formats
(FR-14.2); the Spearman study against human moderators (AC-14.7).

**Target:** about 69% of the 21 requirements by Wed 21 Oct (33% today) if every
day lands — 11 met, 7 partly, the 3 above deferred — with all five release
gates checked. **Reached 67% on 19 Oct**, four gates met and AC-14.3 partly.

### 2026-10-19 — abhinav's `m14-to-90`, merged and reviewed

abhinav's `634f502` (PR #1 into `wrap-up`) built six requirements: panels of up to
five with private knowledge, for/against and case formats, late join, the six
contribution measures, a domination index, a typed discourse graph, and missed
openings with replay. 484 tests, ruff and tsc clean. Reviewed by running it;
kept as built, with these fixed (`53f5976`):

1. ✅ **Hindi scored 0 on novelty.** Words were counted with `[a-z]`, so the same point
   scored 10 in English and 0 in Hindi, against EC-14.8. Now any script; closure
   is also read from what a late contribution does, not only English phrases.
2. ✅ **"Openings you let pass" listed openings that were taken.** A reply after 12 s
   was "missed" (every typed answer), and "building on Asha's point" counted as an
   invitation. Now only invitations count, and the next voice decides.
3. ✅ **For/against told the panel "You argue FOR"** beside a persona's own "You
   OPPOSE". Now third person.
4. ✅ **Entry skill gave 10/10 with no invitation.** Now "not measured".
5. ✅ **Three features were stored but never shown.** Now "How you took part" (the six
   measures) and "Floor and flow" (domination, how contributions connected, with
   names). Seen live in headless Edge, no console errors.
6. ✅ **Line endings rewritten on the report page** (2,105 lines of diff for 67); back to
   CRLF. The same slip I had made in `service.py` on Day 3, also fixed.

**Found while walking it, older than either, not fixed:** the behaviour evaluator
wrote "28% in a 6-person discussion, over the 17% even share" for four people
(its rubric's example misleads it); a raw parser error reaches the host's group
summary when an evaluator's JSON is malformed; the group narrative says "A" and
"P1" rather than names. **Cost:** three panelists by default (was two), up to
five, so each session spends more of the daily allowance.

### 2026-10-19 — Day 5's walk: what it found

Walked on the platform build (no Docker): a voice session in headless Edge with a
synthetic microphone, and three socket sessions. Scripts in the session scratchpad
(`gd_day5_room.mjs`, `gd_day5_edges.mjs`).

1. ✅ **Gates measured, not assumed.** Barge-in end to end in the browser: 184–205 ms
   from the voice reaching the microphone to the persona's audio pausing (voice
   detector 168–191 ms, server 13–17 ms, page <1 ms; n=6). A five-participant
   session: 9 turns, 5 speakers, 165 s, 0.0% recorded overlap. "Hang on, are you a
   bot?" said aloud → "I'm an AI participant…".
2. ✅ **A leaderboard, removed.** The host's results were sorted best-first with a
   trophy on the top scorer, and anyone can host a room of friends (Trap 6). Now
   seat order, no trophy; a candidate still reads only their own report.
3. ✅ **Hindi and mixed speech scored on content.** Transcribed exactly by Whisper,
   answered on its point, and a rule in every evaluator now says language, accent
   and switching never lower a score.
4. 🟡 **An insult went unanswered and was praised.** "You lot are idiots, shut up"
   → the panel carried on, and the report called the student's etiquette
   respectful. The scoring is fixed (insults are disruptive conduct); a moderator
   who intervenes, and removal on repeat, are not built (EC-14.9).
5. ✅ **The model's daily allowance — the real ceiling.** Groq's free tier caps each
   model at **200K tokens a day**; a day of testing spent both models (199,088 and
   198,467). A session with its report costs roughly 40–50K tokens, so one free
   organization supports **about four to eight practice sessions a day**, shared
   with every other module on the same key. GD then slept 65 s ten times per call:
   a silent panel with no word why, and reports that failed after ten minutes and
   were never written. Fixed (`0b0a348`): a daily cap fails at once with how long it
   will be; the room tells the student ("back in about N min"); a report waits with
   a plain sentence and is written by itself when the allowance is back. **Capacity
   for more students is a decision: a paid tier, or a second provider.**
6. ✅ **A report a restart cut off stayed "analysing" for good.** The job stayed
   RUNNING; the worker now writes such reports again when it starts.
7. ⬜ **Back-to-back sessions starve the panel.** A report being written falls back
   to the personas' model when its own is busy, so a student who starts a second
   practice straight after the first can meet a slow or silent panel (seen: a 30 s
   opening, raised hands not invited). Not fixed: the cure is to keep reports off
   the personas' model while a room is live.
8. ⬜ **One unidentified flaky test**: one failure in five full runs, not reproduced
   in eighteen runs of the timing-sensitive files.

### 2026-10-17 — the first real run: what it took, and what broke

Run on this machine in GD's no-Docker mode, with the platform's Groq key and
Edge voices (recipe below).

- ✅ The suite: **353 passed** (the README says 301); ruff and tsc clean; `next
  build` succeeds. Python 3.12 works (ruff targets 3.13).
- ✅ With fixes 1–2 below, a real two-minute practice against three personas:
  five persona lines with Edge audio, replies **1.2–1.4 s** after the student
  stops (0.6 s of it a deliberate "hear them out" hold), and a barge-in drops
  the line it cuts into.

**Blockers found by running it:**

1. ✅ **The personas are silent on today's models.** The platform's keys serve
   only `openai/gpt-oss-120b`, `gpt-oss-20b` and `qwen/qwen3.8-27b` — the llama
   models are gone (see `ai_core.models.RETIRED`). gpt-oss spends the persona
   line's 150-token cap on hidden reasoning, and Groq answers
   `json_validate_failed`, every turn. Fix: `reasoning_effort=low` for gpt-oss
   (`LLM_REASONING_EFFORT`) — a line in **0.5–0.7 s**. Fixed 17 Oct (`8edaf70`).
2. ✅ **Every evaluator fails.** On the final round gpt-oss delivers its answer
   as a call to a tool named `json`, and Groq rejects it (`tool_use_failed`).
   Fix: retry that round with `tool_choice="none"` — 4/4 in isolation. Fixed
   17 Oct (`8edaf70`).
3. ✅ **The database locks while a report is made.** An evaluation runs inside
   one SQLite write transaction for its whole length — minutes on the free
   tier — so the job row stays invisible (`GET …/evaluation` answers 404) and
   every other write fails: registration 500s. The Observer also calls the LLM
   inside a write transaction. Fixed 17 Oct (`f29b607`): progress committed before
   each model step, each window committed as it is observed, SQLite in WAL with a
   30 s busy timeout.
4. ✅ **Free-tier rate limits.** Five evaluators fire at once, all get 429, all
   sleep ~20 s together. Measured per key, per model: **8,000 tokens/min and
   1,000 requests/day**. Fixed 17 Oct (`f5c2f4c`): a 429 cools that model for the
   window Groq names and calls move to `LLM_FALLBACK_MODELS`; they wait only when
   every model is cooling.
5. ✅ `edge-tts` is in no requirements file, and `.env.example` does not say how
   to use Groq or Edge voices. Fixed 17 Oct (`8edaf70`).
6. ✅ The analyst persona invents statistics ("a 2021 NASSCOM study shows
   companies hire 70% of interns") — its brief demands a number for every
   point. Fixed 18 Oct (`fe22deb`): the brief no longer asks for numbers, and every AI
   participant is told never to invent figures or sources.
7. ✅ No persona is told to admit it is an AI (AC-14.5 [GATE], EC-14.14). Fixed 18 Oct:
   the rule alone got an admission 2 times in 5 on Groq; the turn after the question says
   so (6 in 6), and a guard prefixes one if a reply still omits it.
8. ✅ A silent student's report contradicts itself — "you spoke for 0% of the
   discussion. Your points landed, but there were fewer of them…" — where
   EC-14.1 asks for encouragement. Fixed 18 Oct in code (`6fcd1d1`): a silent candidate's
   debrief is the moments someone turned to them by name, kindly worded; checked live on
   19 Oct (`1258678`), narrative included.

**Keys: one Groq organization per running app.** The two `GROQ_API_KEYS` have
separate quotas (measured from the rate-limit headers), and Groq applies limits
per organization, so they are almost certainly two organizations. Groq's
[Acceptable Use Policy](https://console.groq.com/docs/legal/ai-policy)
(effective 2025-10-15) forbids use "beyond published parameters, rate limits,
or use limitations, including by registering multiple accounts or orchestrating
usage between multiple organizations." So GD gets its headroom the compliant
way: spread calls across models (each has its own bucket), pace them from the
remaining-tokens header, and spend fewer tokens. Switching keys because one is
revoked or down is fine; switching because one ran out is the forbidden part.
M06 and M13 already rotate the two keys — recorded as a decision in their TODOs.

**Capacity on the free tier (measured 19 Oct).** One persona line costs ~1.1K tokens on
Groq; a key allows 8K tokens a minute per model, so ~7 lines a minute on the persona
model. One live session fits (replies ~1.3 s); a second session, or a report being
made at the same time, puts both models into cooldown and replies wait 15–25 s. Run
one live session at a time on the free tier; a paid tier lifts this.

**How to run it without Docker** (environment only; no `.env` needed):
`APP_ENV=local`, `DATABASE_URL=sqlite+aiosqlite:///./gd_local.db`,
`REDIS_URL=disabled`, `STT_PROVIDER=stub`, `TTS_PROVIDER=edge` (and
`pip install edge-tts`), `LLM_PROVIDER=openai`,
`OPENAI_BASE_URL=https://api.groq.com/openai/v1`,
`LLM_MODEL=openai/gpt-oss-120b`, `PERSONA_LLM_MODEL=openai/gpt-oss-20b`,
`LLM_API_KEY=<one key>`; then `alembic upgrade head`, uvicorn on `:8000`, and
`npm run build && npm start` in `frontend/`. A client drives practice over
`/ws/practice/{id}?token=`: `START`, then per turn `UTTERANCE_START`,
`UTTERANCE_END` and *then* the WAV bytes — in that order.

### 2026-10-17 — what the team built, audited against this spec

Built by GS Adithya Krishna (2026-10-04 to 10-07) and abhinav (2026-10-10):

| Branch | Commits | What it adds |
|---|---|---|
| `main` | 1 | Initial commit only (2026-10-04) |
| `demo` | 2 | One-step start script, a no-Docker mode |
| `arena-modes` | 4 | Student lobbies, AI practice mode, agentic evaluation, an immersive UI; practice speaks one voice at a time and listens before replying |
| `groq-edge-tts` | 7 | All of the above, plus Edge TTS voices, a Gemini/Groq OpenAI-compatible provider, agent-written personal reports, a UI redesign, and tests |

**What it is.** A FastAPI backend (`services/`: auth, session, lobby,
realtime, speech, metrics, observer, evaluation, practice, notifications) and
a Next.js frontend, on Postgres, Redis, LiveKit and MinIO in Docker (SQLite
and no Redis in its no-Docker mode). Live discussion is decoupled from
evaluation: speech in 45-second windows → Whisper → transcript segments; a
metrics engine in code (speaking time, turns, interruptions, overlap, who
addressed whom); an Observer agent's rolling state; at the end a LangGraph
supervisor fans out to specialist evaluator agents, a deterministic
aggregator computes the score, and a synthesis agent writes the report
through tools that cannot change it. Its README counts **301 tests**
(offline, stubbed STT and LLM); not run in this audit.

**Where it stands against the platform — the integration work, not yet started:**

- ⬜ **Not on Platform_Core.** Its own accounts and JWT (`services/auth`), not
  `ai_core.identity` and the shell's session; no `module.json`, no
  `candidate_guard`, no service secret.
- ⬜ **Not in the shell.** A separate Next.js app on `:3000` with its API on
  `:8000`; the platform's port plan has no M14 entry yet.
- ⬜ **Nothing reaches the skill graph or M13.** Its evaluation is its own;
  the spec's M13/M19 seams are untouched.
- ⬜ **Nothing is on `main`.** Merging `groq-edge-tts` is the team's call.

### 2026-10-05 — from the voice research (M11, Revision 2)

- **FR-14.7 (an AI participant yields within 350 ms when a human speaks)** maps
  onto Revision 2's browser VAD: the stop happens in the browser, before any
  network round trip.
- **Distinct voices for several AI participants.** Edge has only two neural
  Indian-English voices (Neerja, Prabhat), so a five-person GD needs more: other
  English neural voices (en-GB, en-US) chosen by each participant's `voice_id`,
  or Kokoro's American and British voices as M11's tier 1. Indian-language
  neural voices exist too (Hindi, Bengali, Gujarati, Kannada and more), should
  a vernacular round ever be wanted.
- **Trap 5's SFU:** LiveKit (Apache-2.0) is the open choice Revision 2 names
  for multi-party audio.
- **Avatars:** the spec's open question says abstract avatars with names, no
  faces. M06's drawn faces — which talk since 2026-10-05 — and the face options
  in M11's §15.6 are there if that changes.
- When M14 starts, M06's voice client (`voice-core.ts`, `voice.ts`) graduates
  to Platform_Core rather than being copied (M11 TODO §6).

---

## 0. Ideas and scouting

Things worth building that did not come from the spec — usually from reading
somebody else's implementation. **New ideas go at the top of this section.**

The rule we keep arriving at: borrow a **technique**, not a **component**. The
platform's contracts — character offsets, per-fact provenance, permanent
evidence — are more demanding than general-purpose tools assume, so integration
usually costs more than reimplementing the one idea we actually wanted.

_Nothing scouted for this module yet._

---

## 1. Where the module stands

| | |
|---|---|
| Status | **Built on branches, to its own design.** `groq-edge-tts` (7 commits, 2026-10-04 → 10-10): backend, frontend and tests; `main` holds the initial commit only. Not on Platform_Core, not in the shell. On today's Groq models it runs only with two fixes, landing on branch `wrap-up` (Day 1). |
| Spec | Written, and the source of every row below. |
| Scope | 21 functional requirements (17 of them P0), 11 acceptance metrics (5 release-blocking), 15 edge cases. |
| Tests | **353 passed** on 2026-10-17 (offline: in-memory SQLite, stubbed STT and LLM; the README still says 301) |

The requirement table below was audited against the `groq-edge-tts` branch's
code on 2026-10-17. The acceptance gates, edge cases and data model below it
have not been walked against that code yet.

---

## 2. Functional requirements

Spec §4, verbatim; status from the 2026-10-17 audit of `groq-edge-tts`.

| FR | | Priority |
|---|---|---|
| FR-14.1 | 🟡 Three modes: solo-vs-AI, humans-only, hybrid — solo practice against AI personas and humans-only group rooms exist; no hybrid room (one practice room per student) | P0 |
| FR-14.2 | 🟡 Formats: topic, case-based, for/against (assigned stance), fishbowl — open topic, for/against (the student is given a side and the panel splits around it) and case study (the student pastes a short case) (abhinav, 634f502); fishbowl not built | P1 |
| FR-14.3 | ✅ AI moderator running a phase machine with time control — the coded phase machine and clock, plus a moderator persona (`panel.pick_moderator`) who opens and invites the student, brings a silent student in, redirects a dominant voice and closes (Day 2) | P0 |
| FR-14.4 | ✅ 3–5 AI panelists with sampled divergent stances and private knowledge — panels of up to five (three by default), stances sampled per persona, a private angle each, and private knowledge per angle: reasoning only, never figures (abhinav, 634f502) | P0 |
| FR-14.5 | ✅ Anti-convergence: repetition-similarity block on contributions — a restated point goes back once, then the persona yields; three yields bring a curveball (Day 2) | P0 |
| FR-14.6 | ✅ Floor-control scheduler with a bid model — each persona bids eagerness × freshness × disagreement × relevance × floor balance; the highest speaks (Day 2) | P0 |
| FR-14.7 | ✅ Human speech always wins the floor; AI yields ≤ 350 ms — the browser's VAD cuts a persona's playback when the student speaks, recorded as an interruption; the server stops the line 8–13 ms after the student starts, ~150–230 ms with the browser's detection (Day 4) | P0 |
| FR-14.8 | ⬜ Speculative pre-generation of the next 2 bidders' contributions | P0 |
| FR-14.9 | ✅ Multi-human rooms over an SFU, up to 8 participants — LiveKit; `max_participants` defaults to 8 | P0 |
| FR-14.10 | ✅ Invite links, lobby, host controls, late join, reconnect — six-character join code, email invites that reserve a seat, a lobby with ready marks, host start and end, reconnect after a drop, and late join to a live room for two minutes or half the session (abhinav, 634f502) | P0 |
| FR-14.11 | ✅ Live speaking-time counters for all participants — bars per participant, in each orb's colour, in the practice and group rooms, from recorded turns (Day 3) | P0 |
| FR-14.12 | ✅ Optional raise-hand with moderator invitation — the moderator invites the student by name at the next gap (Day 3) | P1 |
| FR-14.13 | ✅ "Recent ideas" strip — the Observer's latest arguments and open questions, sent to the room when its understanding changes (Day 3) | P1 |
| FR-14.14 | ✅ Discourse graph construction with typed edges — one node per contribution, an edge to the one it answers, typed answer / challenge / support / extend / new from its wording, no model (abhinav, 634f502); summarised for the host in "Floor and flow" | P0 |
| FR-14.15 | ✅ Contribution scoring: novelty, uptake, floor dynamics, entry skill, listening, closure — all six counted in code, each with what it was counted from, shown as "How you took part" (abhinav, 634f502; reviewed 53f5976: any script counts, closure read from what a contribution does, entry skill "not measured" with no invitation). Proxies beside the agents' scores; they do not move the overall | P0 |
| FR-14.16 | ✅ Domination index separating leading from bulldozing — per speaker, from excess floor share, interruptions and how little they build on others; leading vs bulldozing vs balanced in the host's group summary (abhinav, 634f502) | P0 |
| FR-14.17 | ✅ Missed-entry-moment detection with audio playback — "Openings you let pass" in the debrief, each replayable in the persona's voice (abhinav, 634f502; reviewed 53f5976: only invitations count, and an opening is taken when theirs is the next voice, so a typed reply is not "missed") | P1 |
| FR-14.18 | ✅ Private individual debriefs; no public quality ranking — each candidate sees only their own report; the host sees the group report; nothing ranks | P0 |
| FR-14.19 | ✅ Text GD mode with the same scheduler and scoring — typed turns take the spoken path minus speech-to-text, never cut anyone off, and hold the floor for their spoken length (Day 3) | P0 |
| FR-14.20 | ✅ Overlap < 4% of wall clock in a 5-participant session — shown in a practice session, the student and four AI personas: 0.0% recorded, under 1% counting six barge-ins (Day 5); a room of five humans not walked | P0 |
| FR-14.21 | ⬜ AI contribution latency after floor grant p95 < 800 ms — measured Day 4: p95 4.5 s (model 0.73 s, speech to a playable line 2.2 s, played only when whole); needs play-on-first-chunk and FR-14.8 together | P0 |

---

## 3. Acceptance gates

Spec §13. A **[GATE]** is release-blocking; the rest are tracked.

| AC | | Target |
|---|---|---|
| AC-14.1 **[GATE]** | ✅ Overlap in a 5-participant session — 0.0% recorded over 165 s, 9 turns, 5 speakers; under 1% counting barge-ins physically (Day 5, practice; humans-only not walked) | < 4% of wall clock |
| AC-14.2 **[GATE]** | ✅ Human barge-in stops AI — 184–205 ms end to end in the browser, voice at the microphone to the persona's audio paused (n=6, Day 5); only the physical mic and speaker are outside the loop | ≤ 350 ms |
| AC-14.3 **[GATE]** | 🟡 AI panel stance divergence (min pairwise) — in 40,000 sampled panels no two personas ever share both stance and angle (min pairwise 1.0 up to three personas, 0.5 at four); divergent live, but not yet measured on what they say | above threshold, 100% of sessions |
| AC-14.4 **[GATE]** | ✅ No public individual quality ranking — the room shows floor time only; a candidate reads only their own report (API tests); the host's best-first table with a trophy is now seat order, no trophy (Day 5) | design + UI test |
| AC-14.5 **[GATE]** | ✅ AI participants identify as AI when asked — prompt rule + turn instruction (6/6 live) + a guard that guarantees it; also asked aloud in voice mode (Day 5) | 100% |
| AC-14.6 | ⬜ Floor grant → first audio p95 — **fails: 4.5 s** (median 3.2 s, n=12, Day 4) | ≤ 800 ms |
| AC-14.7 | ⬜ Contribution metric vs human moderators (Spearman) | ≥ 0.6 |
| AC-14.8 | ⬜ Improvement over speaking-time baseline | reported (the Paper 5 result) |
| AC-14.9 | ⬜ Every participant speaks at least once | 100% |
| AC-14.10 | ⬜ Session completion rate | ≥ 70% |
| AC-14.11 | ⬜ Students who enter more times in session 2 than session 1 | ≥ 50% (the real KPI) |

---

## 4. Edge cases

Spec §12. Listed in full, because several are one afternoon each and are the
difference between a demo and a product.

| EC | | Expected behaviour |
|---|---|---|
| EC-14.1 | ✅ Student says nothing the entire session — the moderator invites them by name in the opening and after 40 s of silence; the debrief is the moments someone turned to them, kindly worded, narrative included (Days 2–3, checked live) | Opening round guarantees ≥1 utterance; debrief focuses entirely on entry moments; **tone must be encouraging, not disappointed** |
| EC-14.2 | ✅ Student dominates completely (70% floor) — the moderator hands the floor to the quietest persona, twice at most (Day 2); live on Day 5: "Thanks, Asha. Arjun, what's your take…" | Moderator intervenes twice with a redirect ("Kavya, what do you think?"); debrief shows uptake data |
| EC-14.3 | ⬜ Two humans always talk over each other | Moderator intervenes; overlap stats surfaced to both |
| EC-14.4 | ✅ All AI agents converge despite mitigations — repetition block forces yields; three in a row bring the moderator's curveball (Day 2) | Repetition block forces yields; if 3 consecutive yields, the moderator injects a curveball |
| EC-14.5 | ⬜ Human drops mid-session | Seat held 60 s; moderator notes and continues; their partial score is computed |
| EC-14.6 | ⬜ Only 1 human joins a friends-room | Auto-converts to hybrid with AI fillers, with consent ("nobody else joined — want me to fill the seats?") |
| EC-14.7 | 🟡 Topic is unfamiliar to everyone — the opening restates the topic and invites the student, but does not frame it (tried with quadratic voting, Day 5); unfamiliarity is not a scoring rule | Moderator provides a 20-second framing; unfamiliarity is not penalised |
| EC-14.8 | ✅ Student speaks in Hindi/mixed — Whisper transcribed a Hindi–English turn exactly, the panel answered its point, and every evaluator is told never to score language, accent or switching (Day 5) | Fully accepted; transcribed; scored on content, never on language |
| EC-14.9 | 🟡 Inappropriate content from a human — scored as disruptive conduct (Day 5); no moderator intervention, removal or log yet: the panel carried on as if nothing was said | Moderator intervenes; repeated → removed from the room; logged |
| EC-14.10 | ⬜ Student uses raise-hand exclusively — hands are counted, but no debrief note; the live walk was confounded by the spent model allowance (Day 5) | Recorded as a distinct entry style; debrief gently notes that real GDs have no hand-raise and offers the entry drill |
| EC-14.11 | ⬜ 8 participants (max) | AI agents drop to 0; scheduler handles humans-only; overlap will be higher and that's realistic |
| EC-14.12 | ⬜ Network drops for one participant | SFU handles; on return, a 10-second catch-up summary |
| EC-14.13 | ⬜ Discourse graph pass fails | Fall back to novelty-only scoring; uptake marked unavailable |
| EC-14.14 | ✅ Student asks the AI directly "are you a bot?" — answered honestly, guaranteed (Day 2) | Agents answer honestly: "I'm an AI participant." **Never deceive.** |
| EC-14.15 | ⬜ Fishbowl observers | Can leave rubric-anchored comments; observers' comments shown only after the session |

---

## 5. Data model

Spec §5 declares 9 types. None exist under these names; the `groq-edge-tts` branch has its own (`GDSession`, participants, transcript segments, turns, evaluation outputs), not yet mapped onto these.

| Type | | |
|---|---|---|
| `StanceVector` | ⬜ | Not written |
| `PanelistPersona` | ⬜ | Not written |
| `GDSession` | ⬜ | Not written |
| `GDParticipant` | ⬜ | Not written |
| `Contribution` | ⬜ | Not written |
| `DiscourseEdge` | ⬜ | Not written |
| `FloorEvent` | ⬜ | Not written |
| `GDScore` | ⬜ | Not written |
| `MissedMoment` | ⬜ | Not written |

---

## 6. Deferred — inter-module

Not gaps in this module. Each needs a module that is not built or not wired
yet, and each is listed so it is not mistaken for an oversight.

The spec names **M11, M12, M13, M19**. Until those are wired, anything
depending on them is blocked rather than unstarted, and the distinction
matters: one is work waiting to be done and the other is work that cannot
begin.

---

## 7. First moves

Work has begun outside the platform (the 2026-10-17 audit above). Bringing it in, the order that has worked on M01 and M02 still applies, as integration rather than a blank page:

1. **The manifest and the ports.** `module.json` with `depends_on` declaring
   every upstream as OPTIONAL, each with an `on_missing` sentence a student
   can act on. Rule 2: a missing dependency narrows scope, never quality, and
   never silently.
2. **Identity before endpoints.** Router-level `enforce_access` on
   `ai_core.identity`, so no route can be written without it. A per-route
   check is the one somebody omits on the sixteenth endpoint, and the
   sixteenth endpoint is the one that leaks.
3. **The P0 that carries the module's name**, not the easiest one.
4. **Contract gates from the first commit** — every route has a client, every
   hook has a screen, every response field is declared on the frontend. M01
   shipped ten routes nobody could reach before these existed.
5. **A golden corpus before the third extraction fix**, not after. On M02 it
   found four real bugs within an hour of existing.

