# M14 — Group Discussion Arena

> **Master plan reference:** §40 · **Phase:** 3 · **Owner:** E2 · **Depends on:** M11 (voice), M12, M13 · **Feeds:** M4, M19 · **Research:** Paper 5
> **Three modes on one engine: you vs an AI panel, you vs your friends, and hybrid rooms.**

---

## 1. In one paragraph

GD is not about the topic. It is a test of social courage under time pressure: can you enter a crowded conversation, hold the floor without bulldozing, build on someone else's point, and land a summary before the moderator calls time? Indian campus drives use it as a hard filter, students dread it more than any technical round, and no tool practises it. We build an arena with three configurations — solo against 3–5 AI panelists with genuinely divergent stances, a room with your actual friends and an AI moderator, or a hybrid where AI agents fill the empty seats — and we score the thing that matters: **contribution versus domination**, measured as novelty × uptake × floor dynamics, not speaking time.

---

## 2. Reverse-thinking: the user

### 2.1 The two students, and both need different things

| | **The quiet one** | **The loud one** |
|---|---|---|
| Reality | Speaks twice in 15 minutes, both times after being invited | Speaks 40% of the time, repeats himself, cuts people off |
| Believes | "I had nothing to add" | "I led the discussion" |
| Actually needs | Entry technique and permission | To find out that talking ≠ leading |
| Our feedback must | Show the 3 moments they *could* have entered | Show that nobody picked up their points |

**The loud student is the harder design problem.** Telling someone they dominated is unwelcome. The way it lands is through the *uptake* metric: *"You spoke for 6 of 15 minutes. Two of your five points were built on by others. Priya spoke for 90 seconds and both of her points were picked up by three people."* That's data, not a lecture, and it changes behaviour.

### 2.2 The emotional arc

```
BEFORE   "I go blank in GDs. I just can't get a word in."       (dread + avoidance)
   ↓
DURING   "There — that pause. That was my moment."               (pattern recognition)
   ↓
AFTER    "I entered 4 times, 2 landed. Last time it was 1."      (measurable courage)
   ↓
NEXT     Books a friends-room to try it with real people.        (transfer)
```

### 2.3 The screens

#### Lobby

```
┌──────────────────────────────────────────────────────────────┐
│  Group Discussion                                            │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │ 🤖 Practise  │ │ 👥 With      │ │ 🎭 Mixed     │          │
│  │   solo       │ │   friends    │ │   room       │          │
│  │              │ │              │ │              │          │
│  │ 4 AI         │ │ Invite up to │ │ Humans +     │          │
│  │ participants │ │ 7 people     │ │ AI fillers   │          │
│  │ Start now    │ │ Share a link │ │ Start now    │          │
│  └──────────────┘ └──────────────┘ └──────────────┘          │
│                                                              │
│  Format    ● Topic GD   ○ Case-based   ○ For/against         │
│  Length    ● 15 min     ○ 10 min       ○ 20 min              │
│  Topic     ● Surprise me   ○ Pick one                        │
│                                                              │
│  ⓘ First time? Solo is easier — the AI participants are      │
│    patient and won't judge you. [ How GDs are scored ]        │
└──────────────────────────────────────────────────────────────┘
```

The nudge toward solo for first-timers is important: a student's first GD experience being a real room with friends where they say nothing is a strong reason never to come back.

#### In the room

```
┌───────────────────────────────────────────────────────────────────┐
│  "Should AI-generated content be labelled by law?"    ⏱ 11:24     │
│  Phase: Free discussion                                           │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ●Meera        ○Rahul        ●YOU         ○Kavya      ○Dev       │
│   speaking      1:20          2:05         0:45        3:10       │
│   ▁▃▅▇▅         ────          ────         ────        ────       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Meera: "...but enforcement is the real problem. Who audits  │  │
│  │ a model's output at scale?"                                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
│               ┌──────────────────────────────┐                    │
│               │   ✋  RAISE HAND TO SPEAK      │                   │
│               │   (or just start talking)     │                   │
│               └──────────────────────────────┘                    │
│                                                                   │
│  Recent: Meera → enforcement · Dev → EU AI Act · Kavya → chilling │
│          effects on art                                           │
└───────────────────────────────────────────────────────────────────┘
```

**Design decisions:**
- **Speaking-time counters are visible for everyone, live.** This is the single most behaviour-changing element in the room: a student at 3:10 sees it and self-regulates; a student at 0:45 sees it and pushes themselves. It's also what real GD observers track.
- **"Raise hand" is optional, and it says so.** Real GDs don't have a hand-raise, but a terrified first-timer needs a low-stakes on-ramp; the moderator will invite them in. Using it is recorded as a distinct (non-penalised) entry style.
- **The "Recent" strip** shows the last three ideas on the table. Students go blank because they lose the thread; this fixes that at zero cost and mirrors what a good participant holds in their head.
- **No live scoring.** Nothing during the discussion may show quality feedback — it would break the social dynamic entirely.

#### The debrief (the product)

```
  Your 15 minutes

  FLOOR
  You          ██████░░░░░░░░░░░░  2:05  (equal share would be 3:00)
  Meera (AI)   ███████████░░░░░░░  3:40
  Dev (AI)     █████████░░░░░░░░░  3:10
  Kavya (AI)   ████████░░░░░░░░░░  2:50
  Rahul (AI)   ███████░░░░░░░░░░░  2:25

  YOUR ENTRIES
  ✓ 4:12  entered cleanly after Dev's pause              → landed
  ✓ 9:30  built on Kavya's point about artists           → landed, Meera picked it up
  ✗ 6:45  started speaking, Meera continued, you stopped → you yielded
  ✗ 12:10 tried twice, both overlapped                   → mistimed

  MOMENTS YOU MISSED
  ▶ 2:40  Dev finished a point and nobody spoke for 2.1s
  ▶ 7:55  Meera asked an open question — nobody answered
  ▶ 13:20 The group repeated itself for 40s — a summary
           would have owned the room here

  WHAT YOU ADDED
  · "chilling effects on independent artists"   ← new to the discussion,
                                                  Meera and Kavya both
                                                  referenced it after
  · "enforcement costs"                          ← already said by Dev

  THE ONE THING
  You yielded twice when someone talked over you. Both times you
  had the floor first. Next time: keep going for two more seconds —
  the other person almost always stops.

  [ Drill: entering under pressure (6 min) ]
```

**"Moments you missed" with a play button is the highest-value element.** The student hears the 2.1-second silence they didn't take. Nothing else teaches GD timing that fast.

---

## 3. Reverse-thinking: the developer

### 3.1 The seven traps

**Trap 1 — Letting agents talk freely and hoping it works.** Free-running LLM agents in a shared room produce either total silence (all deferring) or chaos (all speaking). *Counter: floor control is an explicit scheduler with a bid model; agents never decide when to speak (§6.4).*

**Trap 2 — Latency making AI turns unnatural.** A 2-second gap before every AI contribution kills the illusion instantly. *Counter: speculative pre-generation during the current speaker's turn — the top-2 next bidders have their contribution ready before they're granted the floor (§6.5).*

**Trap 3 — Agents that converge.** Given the same topic and prompt, five LLM personas produce five variations of the same centrist take, all agreeing politely. *Counter: sampled divergent stance vectors + **private knowledge seeds** (each agent holds 3–5 facts nobody else has) + a repetition-similarity block (§6.3). The private facts are what force genuine exchange.*

**Trap 4 — Scoring speaking time as contribution.** The most obvious metric, and it rewards exactly the wrong behaviour. *Counter: novelty × uptake × floor-dynamics, with a domination index that explicitly separates leading from bulldozing (§6.7).*

**Trap 5 — Multi-human sync problems.** 6 humans on campus wifi with WebRTC mesh = disaster at 5+ participants. *Counter: SFU (mediasoup or LiveKit) from the start, not mesh. Do not prototype with mesh "for now".*

**Trap 6 — Publicly ranking students.** A leaderboard that shows the quiet student at the bottom in front of their friends is actively harmful. *Counter: individual debriefs are private by default; the shared room view shows only floor time (a neutral fact), never quality.*

**Trap 7 — Building voice GD first.** All the hard scoring logic can be developed and validated in text, where timing is forgiving. *Counter: text GD first as the correctness harness, then flip on the scheduler for voice.*

### 3.2 The non-obvious hard parts

1. **Turn-taking in real human conversation is 200 ms-scale.** Humans start speaking ~200 ms after the previous speaker ends, often before. Our scheduler must aim for that, which is why pre-generation is mandatory rather than an optimisation.
2. **The discourse graph is what makes scoring possible.** Without typed edges (`builds_on`, `rebuts`, `responds_to`), "uptake" is unmeasurable. Building it is an LLM pass plus coreference, and it must be accurate enough to score on.
3. **Overlap is normal and not always bad.** Cooperative overlap (finishing someone's sentence, backchannelling) is a *positive* social signal; competitive overlap (floor-grabbing) is not. Distinguishing them requires knowing whether the original speaker yielded.
4. **Human rooms need presence, reconnection, and a host.** Someone drops, someone joins late, the host leaves. All standard multiplayer problems, all needed.
5. **Moderator timing is a design problem.** Intervene too much and it's a classroom; too little and the discussion dies. The moderator's intervention budget needs tuning with real students.

---

## 4. Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-14.1 | Three modes: solo-vs-AI, humans-only, hybrid | P0 |
| FR-14.2 | Formats: topic, case-based, for/against (assigned stance), fishbowl | P1 |
| FR-14.3 | AI moderator running a phase machine with time control | P0 |
| FR-14.4 | 3–5 AI panelists with sampled divergent stances and private knowledge | P0 |
| FR-14.5 | Anti-convergence: repetition-similarity block on contributions | P0 |
| FR-14.6 | Floor-control scheduler with a bid model | P0 |
| FR-14.7 | Human speech always wins the floor; AI yields ≤ 350 ms | P0 |
| FR-14.8 | Speculative pre-generation of the next 2 bidders' contributions | P0 |
| FR-14.9 | Multi-human rooms over an SFU, up to 8 participants | P0 |
| FR-14.10 | Invite links, lobby, host controls, late join, reconnect | P0 |
| FR-14.11 | Live speaking-time counters for all participants | P0 |
| FR-14.12 | Optional raise-hand with moderator invitation | P1 |
| FR-14.13 | "Recent ideas" strip | P1 |
| FR-14.14 | Discourse graph construction with typed edges | P0 |
| FR-14.15 | Contribution scoring: novelty, uptake, floor dynamics, entry skill, listening, closure | P0 |
| FR-14.16 | Domination index separating leading from bulldozing | P0 |
| FR-14.17 | Missed-entry-moment detection with audio playback | P1 |
| FR-14.18 | Private individual debriefs; no public quality ranking | P0 |
| FR-14.19 | Text GD mode with the same scheduler and scoring | P0 |
| FR-14.20 | Overlap < 4% of wall clock in a 5-participant session | P0 |
| FR-14.21 | AI contribution latency after floor grant p95 < 800 ms | P0 |

---

## 5. Data contracts

```python
class StanceVector(BaseModel):
    """Sampled to MAXIMISE pairwise distance across the panel."""
    axes: dict[str, float]        # topic-specific axes, each -1..+1
                                  # e.g. {"regulation": +0.8, "innovation_cost": -0.6}

class PanelistPersona(BaseModel):
    id: str
    display_name: str
    stance: StanceVector
    strategy: Literal["data_driven","anecdotal","devils_advocate","consensus_builder",
                      "structurer","challenger","summariser"]
    assertiveness: float          # 0–1 → bid urgency, interruption propensity
    verbosity: float              # target words per contribution (25–70)
    politeness: float
    domain_bias: list[str]
    voice_id: str
    knowledge_seed: list[str]     # 3–5 facts ONLY this agent holds

class GDSession(BaseModel):
    id: UUID
    mode: Literal["solo_ai","humans","hybrid","fishbowl"]
    format: Literal["topic","case","for_against"]
    topic: GDTopic
    duration_s: int
    participants: list[GDParticipant]
    phase_timeline: list[tuple[str,int]]
    host_id: UUID | None

class GDParticipant(BaseModel):
    id: UUID
    kind: Literal["human","ai","moderator"]
    display_name: str
    persona: PanelistPersona | None
    assigned_stance: str | None   # for/against format
    joined_at_ms: int
    left_at_ms: int | None

class Contribution(BaseModel):
    id: UUID
    session_id: UUID
    speaker_id: UUID
    start_ms: int; end_ms: int
    text: str
    audio_uri: str | None
    entry_type: Literal["clean","after_pause","overlap_won","overlap_lost",
                        "invited","raised_hand","interrupted_someone"]
    was_interrupted: bool
    yielded: bool
    novelty: float                # embedding distance from prior discourse
    concepts: list[str]

class DiscourseEdge(BaseModel):
    from_id: UUID
    to_id: UUID
    relation: Literal["builds_on","rebuts","responds_to","repeats","summarises",
                      "asks","answers"]
    confidence: float

class FloorEvent(BaseModel):
    t_ms: int
    kind: Literal["grant","request","overlap_start","overlap_resolved","yield",
                  "silence_start","silence_end","moderator_invite"]
    participant_id: UUID | None
    silence_duration_ms: int | None

class GDScore(BaseModel):
    participant_id: UUID
    speaking_time_s: float
    floor_share: float
    turn_count: int
    mean_turn_s: float
    novel_ideas: int
    uptake_count: int             # times others built on you
    uptake_ratio: float
    entry_attempts: int
    entry_success_rate: float
    mean_entry_latency_ms: float  # after a transition-relevance point
    interruptions_made: int
    interruptions_received: int
    cooperative_overlaps: int
    competitive_overlaps: int
    responsiveness: float         # does your point respond to the prior one?
    structure_moves: int          # signposting, summarising, consensus-building
    closure_quality: float | None
    domination_index: float
    dimension_scores: dict[str, float]     # via M13 rubric

class MissedMoment(BaseModel):
    t_ms: int
    kind: Literal["silence_after_point","open_question_unanswered",
                  "group_repeating","direct_invitation_declined"]
    duration_ms: int
    context_text: str
    audio_clip_uri: str
```

---

## 6. The pipeline in minute detail

### 6.1 Topics
120 topics by end of Phase 3, tagged by category (tech/ethics/business/social/abstract/current-affairs), difficulty, and whether they suit case or for/against format. Each carries:
- 3–5 **stance axes** (the dimensions along which reasonable people disagree),
- 6–10 **seed facts** distributed among the agents,
- 2 **moderator curveballs** (a new constraint, a counterexample),
- expected discussion arcs (for missed-moment detection).

Current-affairs topics need a freshness date and a review cycle — a stale topic in a GD is immediately obvious.

### 6.2 Persona instantiation (anti-convergence)

```python
def build_panel(topic, n=4) -> list[PanelistPersona]:
    # 1. Sample stances to MAXIMISE pairwise distance (farthest-point sampling
    #    over the topic's stance axes) — the panel must genuinely disagree
    stances = farthest_point_sample(topic.stance_axes, n)

    # 2. Assign distinct strategies — no two agents share one
    strategies = sample_without_replacement(STRATEGIES, n)

    # 3. Distribute seed facts — each agent gets 3-5 that NO other agent has
    seeds = partition(topic.seed_facts, n, min_per_agent=3)

    # 4. Vary assertiveness across the range so the room has a loud one and a
    #    quiet one — realistic, and it gives the student both to practise against
    assertiveness = [0.25, 0.5, 0.7, 0.9][:n]  # shuffled

    return [PanelistPersona(...) for ...]
```

**Runtime repetition block:** before a contribution is spoken, embed it and compare against every prior contribution. Cosine > 0.85 → regenerate with an explicit "someone already made this point; add something new or disagree" instruction. Two failures → the agent yields the floor instead. This single check is what prevents the "everyone says the same thing" failure.

**Difficulty tuning to the student's weakness (solo mode):** a student who never enters gets a panel with a high-assertiveness floor-hogger *and* one deliberately generous consensus-builder who invites others in — so there's both a challenge and a foothold.

### 6.3 The phase machine

```
opening (2 min)      each participant states a position, moderator-ordered
                     — guarantees the quiet student speaks at least once
free (60% of time)   scheduler-driven, moderator mostly silent
curveball            moderator injects a new constraint at ~55%
free (cont.)
warning (2 min left) "we have two minutes — let's start converging"
closing (90 s)       moderator asks for a summary; whoever takes it gets
                     credit for closure
```

The opening round is a deliberate humane design: nobody leaves a GD having said nothing.

### 6.4 Floor control (the core engineering)

```python
def compute_bid(agent, state) -> float:
    return (
        0.30 * relevance(agent.stance, state.last_contribution)   # do they disagree?
      + 0.20 * min(1.0, state.since_last_spoke_s[agent.id] / 90)
      + 0.20 * agent.assertiveness
      + 0.15 * has_unused_seed_fact(agent)                        # they hold info
      + 0.15 * moderator_nudge(agent)
      - 0.35 * recent_floor_share(agent)                          # balance
    )

def allocate_floor(state) -> ParticipantId | None:
    if human_speaking(state):        return None          # humans always win
    if state.silence_ms < 350:       return None          # let the pause breathe
    bids = {a: compute_bid(a, state) for a in ai_agents}
    top = argmax(bids)
    if bids[top] < 0.35:             return None          # nobody has anything
                                                          # → real silence, which
                                                          #   is the student's cue
    return top
```

**The `< 0.35` threshold produces genuine silences of 1–3 seconds.** This is intentional and it is the single most valuable teaching mechanic in the module: the student learns to recognise and take an entry moment.

**Human priority:** VAD onset from any human → all AI TTS ducks and stops within 350 ms (M11 §6.5 mechanism); the interrupted agent either yields permanently or re-bids with a compressed version of its point.

**Collision resolution:** if two AI agents somehow start together, the lower bidder aborts within one TTS chunk (~120 ms of audio). It sounds like a natural false start, which is more realistic than perfect politeness.

### 6.5 Speculative pre-generation
```
While the current speaker talks:
  → compute bids continuously
  → for the top-2 bidders, generate their next contribution against the
    partial transcript
  → regenerate if the tail changes materially
  → on floor grant: TTS starts from cached text → first audio in ~250 ms
```
Target: floor grant → first audio p95 < 800 ms. Without pre-generation this is ~2.2 s and the room feels broken.

Cost: ~2.5 generated contributions per actually-spoken one. At mid tier and 40 contributions per session that's real but affordable (§11).

### 6.6 Discourse graph
```
per contribution, an LLM pass (mid tier, batched every 3 contributions):
  → for each prior contribution in the last 90 s, does this one:
      build_on / rebut / respond_to / repeat / summarise / answer?
  → coreference resolution over pronouns and "that point", "what you said"
  → typed edges with confidence
novelty = 1 - max cosine(this, all prior contributions)
```
The graph is what makes uptake measurable, and uptake is what makes the score meaningful.

### 6.7 Scoring

```python
novel_ideas   = count(c for c in mine if c.novelty > 0.55)
uptake_count  = count(edges where from ∈ others and to ∈ mine
                      and relation in {builds_on, rebuts, answers})
uptake_ratio  = uptake_count / max(1, len(mine))

floor_share   = my_time / total_speaking_time
gini          = gini_coefficient([p.time for p in participants])   # room-level

entry_success = clean + after_pause + overlap_won + invited
                / total entry attempts
entry_latency = mean(ms between a transition-relevance point and my onset)

cooperative_overlap = overlap where the original speaker did NOT stop
competitive_overlap = overlap where the original speaker DID stop

responsiveness = mean over my contributions of
                 semantic_link_strength(mine, immediately_prior)
                 # low = pre-loaded monologue

structure_moves = count of signposting / summarising / consensus phrases

domination_index = max(0, floor_share - equal_share) / equal_share
                 * (1 + competitive_overlap_rate)
                 * (1 - uptake_ratio)
```

**The `(1 - uptake_ratio)` factor is the whole insight.** High floor share with high uptake = leadership. High floor share with low uptake = domination. The metric can distinguish them, and no speaking-time-based metric can.

**Rubric dimensions scored via M13:** content contribution · influence/uptake · floor management · listening & responsiveness · structure & closure · clarity under pressure. Evidence spans point at contribution IDs and audio timestamps.

### 6.8 Missed-moment detection
```
silence_after_point       : ≥1.8 s of silence following a completed contribution
                            where the student did not speak
open_question_unanswered  : a contribution ending in a question, no answer for ≥2 s
group_repeating           : ≥3 consecutive contributions with novelty < 0.3
direct_invitation         : moderator or participant addressed the student by name
                            and they didn't take it
```
Each generates a 6–8 second audio clip for the debrief. **These clips are the teaching.**

### 6.9 Human rooms
```
SFU: LiveKit (or mediasoup) — NOT mesh
lobby → host starts → moderator (AI) runs the phase machine
late join: allowed until 30% elapsed, with a 15-second catch-up summary
           spoken by the moderator ("we're discussing X; Meera argued Y")
drop: seat held 60 s, then the moderator notes the absence and continues
host leaves: host transfers to the longest-present participant
hybrid: AI agents fill to a minimum of 4 participants; they are visibly
        labelled as AI — never deceive students about who is real
```

---

## 7. API surface

```
POST /v1/gd/sessions                {mode, format, duration, topic?} → session + join token
POST /v1/gd/sessions/{id}/invite    → shareable link
POST /v1/gd/sessions/{id}/join
WS   /v1/gd/sessions/{id}/room      control + floor events + captions
     (media via SFU)
POST /v1/gd/sessions/{id}/raise-hand
POST /v1/gd/sessions/{id}/start     host only
POST /v1/gd/sessions/{id}/leave
GET  /v1/gd/sessions/{id}/transcript
GET  /v1/gd/sessions/{id}/scores/{participant_id}   private to that participant
GET  /v1/gd/sessions/{id}/moments/{participant_id}  missed moments + clips
GET  /v1/gd/topics?category=&format=
```

---

## 8. UI specification

**Components:** `GDLobby` · `ParticipantStrip` (avatars + live speaking time + speaking indicator) · `TranscriptFeed` (live captions, speaker-attributed) · `RecentIdeasStrip` · `RaiseHandButton` · `PhaseIndicator` · `TimeRemaining` · `FloorTimeBar` · `GDDebrief` · `MomentPlayer` · `UptakeGraph`

**States:**

| State | Visual |
|---|---|
| Nobody speaking (real silence) | All indicators idle. **No prompt, no nudge.** This is the entry moment |
| Someone speaking | Their avatar ring animates |
| You speaking | Your ring animates + a subtle "you're on" indicator |
| Overlap | Both rings animate; brief amber |
| Hand raised | Small icon on your avatar; the moderator will call you |
| Late joiner catching up | Their avatar dimmed with "catching up" |
| Participant dropped | Avatar greyed, "reconnecting…" |

**The debrief is private by default.** A shared post-GD view exists for friends-rooms but shows only: topic, duration, floor distribution (a neutral fact), and total ideas contributed by the group. **Never individual quality scores.** A student can choose to share their own debrief.

**Accessibility:** live captions with speaker attribution are essential (and make the text mode viable for deaf/HoH students, who can participate fully by typing in a text GD); floor time available as text; all clips have transcripts; reduced-motion respected.

**Mobile:** fully supported for voice GD — a phone is a perfectly good GD device. Participant strip becomes a horizontal scroll; transcript takes the screen.

---

## 9. Edge cases

| ID | Case | Behaviour |
|---|---|---|
| EC-14.1 | Student says nothing the entire session | Opening round guarantees ≥1 utterance; debrief focuses entirely on entry moments; **tone must be encouraging, not disappointed** |
| EC-14.2 | Student dominates completely (70% floor) | Moderator intervenes twice with a redirect ("Kavya, what do you think?"); debrief shows uptake data |
| EC-14.3 | Two humans always talk over each other | Moderator intervenes; overlap stats surfaced to both |
| EC-14.4 | All AI agents converge despite mitigations | Repetition block forces yields; if 3 consecutive yields, the moderator injects a curveball |
| EC-14.5 | Human drops mid-session | Seat held 60 s; moderator notes and continues; their partial score is computed |
| EC-14.6 | Only 1 human joins a friends-room | Auto-converts to hybrid with AI fillers, with consent ("nobody else joined — want me to fill the seats?") |
| EC-14.7 | Topic is unfamiliar to everyone | Moderator provides a 20-second framing; unfamiliarity is not penalised |
| EC-14.8 | Student speaks in Hindi/mixed | Fully accepted; transcribed; scored on content, never on language |
| EC-14.9 | Inappropriate content from a human | Moderator intervenes; repeated → removed from the room; logged |
| EC-14.10 | Student uses raise-hand exclusively | Recorded as a distinct entry style; debrief gently notes that real GDs have no hand-raise and offers the entry drill |
| EC-14.11 | 8 participants (max) | AI agents drop to 0; scheduler handles humans-only; overlap will be higher and that's realistic |
| EC-14.12 | Network drops for one participant | SFU handles; on return, a 10-second catch-up summary |
| EC-14.13 | Discourse graph pass fails | Fall back to novelty-only scoring; uptake marked unavailable |
| EC-14.14 | Student asks the AI directly "are you a bot?" | Agents answer honestly: "I'm an AI participant." **Never deceive.** |
| EC-14.15 | Fishbowl observers | Can leave rubric-anchored comments; observers' comments shown only after the session |

**EC-14.1 deserves care.** The debrief for a silent student must open with something true and warm — *"GDs are the round most people find hardest, and you showed up for one. Here's what to work on."* — and then get concrete. Getting this copy wrong loses exactly the students who need it most.

---

## 10. Failure modes & fallbacks

| Failure | Fallback | User sees |
|---|---|---|
| SFU unavailable | Text GD mode with the same scheduler | "Voice is down — running this as a text discussion" |
| TTS fails for one agent | That agent contributes in text (captions only) | A visibly text-only participant |
| Pre-generation lags | Agent yields rather than pausing awkwardly | Slightly fewer AI turns |
| Discourse graph pass fails | Novelty-only scoring | Uptake shown as "couldn't measure" |
| Moderator agent fails | Scripted phase transitions on a timer | Slightly robotic moderation |
| All AI agents fail | Moderator-only Socratic session with the student | Degraded but functional |

---

## 11. Performance & cost budget

| Metric | Target |
|---|---|
| Floor grant → first AI audio (p95) | ≤ 800 ms |
| Overlap as % of wall clock (5 participants) | < 4% |
| Human barge-in → AI stop | ≤ 350 ms |
| Debrief ready after session | ≤ 90 s |

**Cost per 15-minute solo-vs-4-AI session:**
| Item | Cost |
|---|---|
| AI contributions (~40 spoken, ~100 generated incl. speculation, mid tier) | ₹38 |
| Moderator (~12 turns) | ₹6 |
| TTS (~4,500 chars across 5 voices) | ₹8 |
| Discourse graph (batched) | ₹9 |
| Scoring (M13) | ₹6 |
| **Total** | **≈ ₹67** |

Speculation waste is ~60% of contribution cost. Worth it — it's the difference between a real conversation and a stilted one. Tunable by reducing pre-generation to top-1 if budget pressure appears.

---

## 12. Test plan

**Unit** — bid computation monotonicity · farthest-point stance sampling produces divergent panels (assert min pairwise distance) · repetition block · overlap classification (cooperative vs competitive) · domination index behaviour on synthetic transcripts (high-floor-high-uptake must score LOW on domination).

**Simulation** — 100 simulated sessions with scripted human behaviour (silent / balanced / dominant); assert: overlap < 4%, every participant speaks ≥ once, scores correctly characterise each behaviour type.

**Load** — 8 participants over an SFU with 200 ms latency and 3% loss; assert audio quality and floor control hold.

**Validation [Paper 5]** — 60 recorded GD sessions rated by 2 human moderators on contribution/domination; measure Spearman ρ against our metric. **Target ≥ 0.6.** Compare against a speaking-time-only baseline — the delta is the paper.

**Manual QA** (20 min): run a solo GD → deliberately stay silent for 5 minutes and confirm the moderator invites you → then dominate and confirm intervention → check the missed-moment clips play the right audio → run a 3-human room → drop one participant and reconnect.

---

## 13. Metrics & acceptance gates

| ID | Metric | Target |
|---|---|---|
| AC-14.1 **[GATE]** | Overlap in a 5-participant session | < 4% of wall clock |
| AC-14.2 **[GATE]** | Human barge-in stops AI | ≤ 350 ms |
| AC-14.3 **[GATE]** | AI panel stance divergence (min pairwise) | above threshold, 100% of sessions |
| AC-14.4 **[GATE]** | No public individual quality ranking | design + UI test |
| AC-14.5 **[GATE]** | AI participants identify as AI when asked | 100% |
| AC-14.6 | Floor grant → first audio p95 | ≤ 800 ms |
| AC-14.7 | Contribution metric vs human moderators (Spearman) | ≥ 0.6 |
| AC-14.8 | Improvement over speaking-time baseline | reported (the Paper 5 result) |
| AC-14.9 | Every participant speaks at least once | 100% |
| AC-14.10 | Session completion rate | ≥ 70% |
| AC-14.11 | Students who enter more times in session 2 than session 1 | ≥ 50% (the real KPI) |

---

## 14. Build order

| Day | Task |
|---|---|
| 1 | Session/participant/contribution schema; text GD room |
| 2 | Phase machine + moderator agent + opening round |
| 3 | Persona generation: stance sampling, strategies, seed facts |
| 4 | Bid model + floor scheduler (text mode) |
| 5 | Repetition block + anti-convergence tests |
| 6 | Contribution novelty + discourse graph pass |
| 7 | Scoring: uptake, floor dynamics, entry classification |
| 8 | Domination index + rubric integration (M13) |
| 9 | SFU integration (LiveKit), multi-human lobby, invites |
| 10 | Voice: TTS per persona, human priority, barge-in |
| 11 | Speculative pre-generation + latency tuning |
| 12 | Missed-moment detection + clip generation |
| 13 | Debrief UI + uptake graph + moment player |
| 14 | Hybrid mode, fishbowl, load test, validation set collection |

---

## 15. Open decisions

1. **Do AI participants get faces/avatars?** Recommendation: **abstract avatars with names, no faces.** Generated faces are uncanny and raise likeness questions. Names + colours are enough for attribution.
2. **Should the student see live floor-time counters?** Currently yes. Risk: gaming (talking to hit a number). Proposal: keep them — real GD observers track exactly this, and the gaming risk is small compared to the self-regulation benefit. Revisit with data.
3. **Moderator intervention budget.** Currently 2 redirects + 1 curveball + time calls. Needs tuning with 10 real students; too much moderation makes it a classroom.
4. **Do we let friends see each other's scores?** Default no. But friends will screenshot and compare anyway. Proposal: an explicit "share my debrief with this room" button, so sharing is a choice rather than a leak.
5. **Topic freshness** — current-affairs topics go stale in weeks. Who reviews the topic bank, and how often? Proposal: E3, monthly, 30 minutes, with staleness flagged automatically by topic age.
