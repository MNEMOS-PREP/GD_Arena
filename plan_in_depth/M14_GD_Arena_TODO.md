# M14 — TODO · Group Discussion Arena

> **Completion: 33%** — 2 of 21 functional requirements met, 10 partially. A GD platform exists — built by GS Adithya Krishna and abhinav from 2026-10-04, **on branches** (`groq-edge-tts` holds all of it; `main` has only the initial commit) and to its own design document (`claude/docs/design.md`) rather than this spec. So it meets several requirements by a different route and misses the spec's distinctive ones: the discourse graph, anti-convergence, speculative pre-generation, missed entry moments. It is not yet on Platform_Core or in the shell.
>
> _Method: `(met + ½ × partial) ÷ total`, counted from the spec, 2026-08-28; audited against the `groq-edge-tts` branch's code on 2026-10-17 (0% → 33%). One measure applied the same way to all nineteen modules so they compare; it counts requirements, not screens or gates._

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
| Status | **Built on branches, to its own design.** `groq-edge-tts` (7 commits, 2026-10-04 → 10-10): backend, frontend and tests; `main` holds the initial commit only. Not on Platform_Core, not in the shell. |
| Spec | Written, and the source of every row below. |
| Scope | 21 functional requirements (17 of them P0), 11 acceptance metrics (5 release-blocking), 15 edge cases. |
| Tests | **301** by its README (offline: in-memory SQLite, stubbed STT and LLM); not run in the 2026-10-17 audit |

The requirement table below was audited against the `groq-edge-tts` branch's
code on 2026-10-17. The acceptance gates, edge cases and data model below it
have not been walked against that code yet.

---

## 2. Functional requirements

Spec §4, verbatim; status from the 2026-10-17 audit of `groq-edge-tts`.

| FR | | Priority |
|---|---|---|
| FR-14.1 | 🟡 Three modes: solo-vs-AI, humans-only, hybrid — solo practice against AI personas and humans-only group rooms exist; no hybrid room (one practice room per student) | P0 |
| FR-14.2 | 🟡 Formats: topic, case-based, for/against (assigned stance), fishbowl — open-topic GDs only, typed technical / leadership / HR-social / general | P1 |
| FR-14.3 | 🟡 AI moderator running a phase machine with time control — the phase machine and clock are code (preparation → live → ending → ended; practice timing phases); no AI moderator, though one persona plays a diplomat | P0 |
| FR-14.4 | 🟡 3–5 AI panelists with sampled divergent stances and private knowledge — personas with distinct briefs and eagerness (the analyst, the devil's advocate, the diplomat …); stances are not sampled and there is no private knowledge | P0 |
| FR-14.5 | ⬜ Anti-convergence: repetition-similarity block on contributions | P0 |
| FR-14.6 | 🟡 Floor-control scheduler with a bid model — a weighted pick by eagerness, with chained follow-ons; no bid model | P0 |
| FR-14.7 | 🟡 Human speech always wins the floor; AI yields ≤ 350 ms — the browser's VAD cuts a persona's playback when the student speaks, recorded as an interruption; the 350 ms bound is not measured | P0 |
| FR-14.8 | ⬜ Speculative pre-generation of the next 2 bidders' contributions | P0 |
| FR-14.9 | ✅ Multi-human rooms over an SFU, up to 8 participants — LiveKit; `max_participants` defaults to 8 | P0 |
| FR-14.10 | 🟡 Invite links, lobby, host controls, late join, reconnect — six-character join code, email invites that reserve a seat, a lobby with ready marks, host start and end, reconnect after a drop; late join not found | P0 |
| FR-14.11 | ⬜ Live speaking-time counters for all participants — a live speaking indicator only; speaking time appears in the report | P0 |
| FR-14.12 | ⬜ Optional raise-hand with moderator invitation | P1 |
| FR-14.13 | ⬜ "Recent ideas" strip | P1 |
| FR-14.14 | ⬜ Discourse graph construction with typed edges — the metrics engine builds a who-addressed-whom graph between speakers, not typed edges between contributions | P0 |
| FR-14.15 | 🟡 Contribution scoring: novelty, uptake, floor dynamics, entry skill, listening, closure — specialist evaluator agents and code-measured turns, interruptions and latency, on its own dimensions rather than these six | P0 |
| FR-14.16 | 🟡 Domination index separating leading from bulldozing — a floor-share flag (`dominant()`, ≥ 30%) and a rubric that marks dominating-not-directing down; no index | P0 |
| FR-14.17 | ⬜ Missed-entry-moment detection with audio playback | P1 |
| FR-14.18 | ✅ Private individual debriefs; no public quality ranking — each candidate sees only their own report; the host sees the group report; nothing ranks | P0 |
| FR-14.19 | ⬜ Text GD mode with the same scheduler and scoring | P0 |
| FR-14.20 | 🟡 Overlap < 4% of wall clock in a 5-participant session — overlap is measured; the target is not demonstrated | P0 |
| FR-14.21 | ⬜ AI contribution latency after floor grant p95 < 800 ms — not measured | P0 |

---

## 3. Acceptance gates

Spec §13. A **[GATE]** is release-blocking; the rest are tracked.

| AC | | Target |
|---|---|---|
| AC-14.1 **[GATE]** | ⬜ Overlap in a 5-participant session | < 4% of wall clock |
| AC-14.2 **[GATE]** | ⬜ Human barge-in stops AI | ≤ 350 ms |
| AC-14.3 **[GATE]** | ⬜ AI panel stance divergence (min pairwise) | above threshold, 100% of sessions |
| AC-14.4 **[GATE]** | ⬜ No public individual quality ranking | design + UI test |
| AC-14.5 **[GATE]** | ⬜ AI participants identify as AI when asked | 100% |
| AC-14.6 | ⬜ Floor grant → first audio p95 | ≤ 800 ms |
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
| EC-14.1 | ⬜ Student says nothing the entire session | Opening round guarantees ≥1 utterance; debrief focuses entirely on entry moments; **tone must be encouraging, not disappointed** |
| EC-14.2 | ⬜ Student dominates completely (70% floor) | Moderator intervenes twice with a redirect ("Kavya, what do you think?"); debrief shows uptake data |
| EC-14.3 | ⬜ Two humans always talk over each other | Moderator intervenes; overlap stats surfaced to both |
| EC-14.4 | ⬜ All AI agents converge despite mitigations | Repetition block forces yields; if 3 consecutive yields, the moderator injects a curveball |
| EC-14.5 | ⬜ Human drops mid-session | Seat held 60 s; moderator notes and continues; their partial score is computed |
| EC-14.6 | ⬜ Only 1 human joins a friends-room | Auto-converts to hybrid with AI fillers, with consent ("nobody else joined — want me to fill the seats?") |
| EC-14.7 | ⬜ Topic is unfamiliar to everyone | Moderator provides a 20-second framing; unfamiliarity is not penalised |
| EC-14.8 | ⬜ Student speaks in Hindi/mixed | Fully accepted; transcribed; scored on content, never on language |
| EC-14.9 | ⬜ Inappropriate content from a human | Moderator intervenes; repeated → removed from the room; logged |
| EC-14.10 | ⬜ Student uses raise-hand exclusively | Recorded as a distinct entry style; debrief gently notes that real GDs have no hand-raise and offers the entry drill |
| EC-14.11 | ⬜ 8 participants (max) | AI agents drop to 0; scheduler handles humans-only; overlap will be higher and that's realistic |
| EC-14.12 | ⬜ Network drops for one participant | SFU handles; on return, a 10-second catch-up summary |
| EC-14.13 | ⬜ Discourse graph pass fails | Fall back to novelty-only scoring; uptake marked unavailable |
| EC-14.14 | ⬜ Student asks the AI directly "are you a bot?" | Agents answer honestly: "I'm an AI participant." **Never deceive.** |
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

