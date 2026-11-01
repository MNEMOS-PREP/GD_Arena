"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { ApiError, practice } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { PersonaPreset } from "@/lib/types";

const MAX_PERSONAS = 5;
/** Where the Mock Interview lives, beside this module. */
const MOCK_URL = process.env.NEXT_PUBLIC_MOCK_URL ?? "/mock";

type Format = "open" | "for_against" | "case";

const FORMATS: { id: Format; icon: string; title: string; sub: string }[] = [
  { id: "open", icon: "messages-square", title: "Open topic", sub: "Anyone may take any view. Build on each other." },
  { id: "for_against", icon: "users-round", title: "For / against", sub: "You hold a side and defend it." },
  { id: "case", icon: "notebook-pen", title: "Case study", sub: "Read a short case, then solve it together." },
];

const LEVELS: { id: string; icon: string; title: string; sub: string; tag: string }[] = [
  { id: "beginner", icon: "sprout", title: "Beginner", sub: "Gentle peers. Room to think between turns.", tag: "A good place to start" },
  { id: "intermediate", icon: "timer", title: "Intermediate", sub: "Peers push back and take the floor.", tag: "Feel the real round" },
  { id: "advanced", icon: "flame", title: "Advanced", sub: "Assertive, fast, and quick to interrupt.", tag: "Bring your best listening" },
];

const MINUTES = [3, 5, 8, 10, 15];
const PREP_SECONDS = 20;
const PART_COLOURS = ["#c9f4c8", "#8dcba4", "#6eaa8a"];
const AVATAR_COLOURS = ["#c9f4c8", "#f0ecdd", "#eae5f6", "#dce6b5", "#d6e7f2"];

function Fig({ name, size }: { name: string; size: number }) {
  // eslint-disable-next-line @next/next/no-img-element
  return <img src={`/figma/${name}.svg`} width={size} height={size} alt="" className="gdset-icon" />;
}

function initials(name: string): string {
  return name
    .replace(/^Dr\.?\s+/i, "")
    .split(/\s+/)
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function StepHead({ n, title, note }: { n: string; title: string; note?: string }) {
  return (
    <div className="gdset-head">
      <span className="gdset-num">{n}</span>
      <h2>{title}</h2>
      {note && <span className="gdset-note">{note}</span>}
    </div>
  );
}

export default function NewPracticePage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [presets, setPresets] = useState<PersonaPreset[]>([]);
  const [voice, setVoice] = useState<"elevenlabs" | "browser">("browser");
  const [chosen, setChosen] = useState<string[]>(["arjun", "bhavana", "chitra"]);
  const [topic, setTopic] = useState("");
  const [format, setFormat] = useState<Format>("open");
  const [side, setSide] = useState<"for" | "against">("for");
  const [caseBrief, setCaseBrief] = useState("");
  const [minutes, setMinutes] = useState(5);
  const [difficulty, setDifficulty] = useState("intermediate");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!user) return;
    practice
      .personas()
      .then((res) => {
        setPresets(res.personas);
        setVoice(res.voice);
      })
      .catch(() => setError("Could not load the personas. Is the backend running?"));
  }, [user]);

  if (loading) return <p className="empty">Loading…</p>;
  if (!user) return <p className="empty">Sign in to practice.</p>;

  function toggle(key: string) {
    setChosen((prev) =>
      prev.includes(key)
        ? prev.filter((k) => k !== key)
        : prev.length < MAX_PERSONAS
          ? [...prev, key]
          : prev,
    );
  }

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const created = await practice.create({
        topic,
        difficulty,
        duration_seconds: minutes * 60,
        preparation_seconds: PREP_SECONDS,
        personas: chosen.map((preset) => ({ preset })),
        format,
        ...(format === "for_against" ? { student_side: side } : {}),
        ...(format === "case" ? { case_brief: caseBrief } : {}),
      });
      router.push(`/practice/${created.id}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not start the practice session.");
      setBusy(false);
    }
  }

  let step = 0;
  const num = () => String(++step).padStart(2, "0");
  const table = chosen
    .map((key) => presets.find((p) => p.key === key))
    .filter((p): p is PersonaPreset => Boolean(p));
  const formatTitle = FORMATS.find((f) => f.id === format)?.title ?? "";
  const levelTitle = LEVELS.find((l) => l.id === difficulty)?.title ?? difficulty;
  const ready = !busy && chosen.length > 0 && topic.trim().length >= 5 && (format !== "case" || caseBrief.trim().length >= 20);

  return (
    <form className="gdset" onSubmit={submit}>
      <h1 className="gdset-sr">Practice with AI personas</h1>

      <div className="gdset-main">
        <div className="gdset-card">
          {error && <div className="alert alert--error">{error}</div>}

          {/* 01 — the room */}
          <section aria-label="Format of the room" className="gdset-sec">
            <StepHead n={num()} title="What are we practising?" />
            <div className="gdset-row">
              <a href={MOCK_URL} className="gdset-opt gdset-opt--link">
                <span className="gdset-opt-top"><Fig name="mic" size={21} /><Fig name="circle" size={17} /></span>
                <strong>Interview</strong>
                <span>A live AI panel that follows your answers.</span>
              </a>
              <div className="gdset-opt" aria-pressed="true" role="group" aria-label="Group discussion, chosen">
                <span className="gdset-opt-top"><Fig name="messages-square" size={21} /><Fig name="circle-check" size={17} /></span>
                <strong>Group discussion</strong>
                <span>3–5 AI peers. Speak, listen, and build on others.</span>
              </div>
            </div>
          </section>

          {/* 02 — topic */}
          <section aria-label="Topic" className="gdset-sec gdset-sec--rule">
            <StepHead n={num()} title="Choose your topic" />
            <textarea
              id="topic"
              className="gdset-text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Should companies make remote work the default?"
              minLength={5}
              required
              rows={3}
            />
            <div className="gdset-opts gdset-opts--3" role="group" aria-label="Format">
              {FORMATS.map((f) => (
                <button
                  key={f.id}
                  type="button"
                  className="gdset-opt"
                  aria-pressed={format === f.id}
                  onClick={() => setFormat(f.id)}
                >
                  <span className="gdset-opt-top"><Fig name={f.icon} size={18} /><Fig name={format === f.id ? "circle-check-sm" : "circle-sm"} size={16} /></span>
                  <strong>{f.title}</strong>
                  <span>{f.sub}</span>
                </button>
              ))}
            </div>
            {format === "for_against" && (
              <div className="gdset-seg" role="group" aria-label="Your side">
                {(["for", "against"] as const).map((s) => (
                  <button key={s} type="button" aria-pressed={side === s} onClick={() => setSide(s)}>
                    {s === "for" ? "For the motion" : "Against the motion"}
                  </button>
                ))}
              </div>
            )}
            {format === "case" && (
              <textarea
                id="case"
                className="gdset-text"
                value={caseBrief}
                onChange={(e) => setCaseBrief(e.target.value)}
                placeholder="A 40-person firm loses its biggest client after a missed deadline…"
                minLength={20}
                required
                rows={4}
                aria-label="The case"
              />
            )}
          </section>

          {/* 03 — time */}
          <section aria-label="Length" className="gdset-sec">
            <StepHead n={num()} title="How much time do you have?" />
            <div className="gdset-seg" role="group" aria-label="Length">
              {MINUTES.map((m) => (
                <button key={m} type="button" aria-pressed={minutes === m} onClick={() => setMinutes(m)}>
                  {m} min
                  {minutes === m && <Fig name="check" size={13} />}
                </button>
              ))}
            </div>
          </section>

          {/* 04 — intensity */}
          <section aria-label="Difficulty" className="gdset-sec gdset-sec--rule">
            <StepHead n={num()} title="Set the intensity" />
            <div className="gdset-opts gdset-opts--3">
              {LEVELS.map((l) => (
                <button
                  key={l.id}
                  type="button"
                  className="gdset-opt"
                  aria-pressed={difficulty === l.id}
                  onClick={() => setDifficulty(l.id)}
                >
                  <span className="gdset-opt-top"><Fig name={l.icon} size={18} /><Fig name={difficulty === l.id ? "circle-check-sm" : "circle-sm"} size={16} /></span>
                  <strong>{l.title}</strong>
                  <span>{l.sub}</span>
                  <em>{l.tag}</em>
                </button>
              ))}
            </div>
          </section>

          {/* 05 — table */}
          <section aria-label="Who is at the table" className="gdset-sec gdset-sec--rule">
            <StepHead n={num()} title="Who is at the table?" note={`Pick 1 to ${MAX_PERSONAS}`} />
            <div className="gdset-opts gdset-opts--2">
              {presets.map((p, i) => {
                const on = chosen.includes(p.key);
                return (
                  <button key={p.key} type="button" className="gdset-person" aria-pressed={on} onClick={() => toggle(p.key)}>
                    <span className="gdset-avatar" style={{ background: AVATAR_COLOURS[i % AVATAR_COLOURS.length] }}>{initials(p.name)}</span>
                    <span className="gdset-person-text">
                      <strong>{p.name}</strong>
                      <span>{p.tagline}. {p.brief}</span>
                    </span>
                    <Fig name={on ? "circle-check-sm" : "circle-sm"} size={16} />
                  </button>
                );
              })}
            </div>
            <p className="gdset-fine">
              <Fig name="lock" size={12} />
              {voice === "elevenlabs"
                ? "Each persona speaks in their own voice."
                : "No voice service is configured, so your browser reads the personas aloud."}{" "}
              Use headphones so their voices do not trigger your microphone.
            </p>
          </section>
        </div>

        <section className="gdset-mint" aria-label="How a GD is assessed">
          <p className="gdset-kicker">A different kind of room</p>
          <p className="gdset-mint-title">Your voice matters; so does how you listen.</p>
          <div className="gdset-mint-rule">
            <strong>Feedback on every contribution</strong>
            <span>Initiating · Structuring · Listening · Building on others · Concluding</span>
          </div>
          <a href={MOCK_URL} className="gdset-link">Set up an interview instead <Fig name="arrow-right" size={16} /></a>
        </section>
      </div>

      <aside className="gdset-side">
        <section className="gdset-deep" aria-label="Your discussion, planned">
          <div className="gdset-deep-head">
            <p>Your discussion, planned</p>
            <Fig name="sparkles" size={18} />
          </div>
          <div className="gdset-deep-title">
            <p>{topic.trim() || "Pick a topic to begin"}</p>
            <div className="gdset-tags">
              <span>{minutes} min</span>
              <span>{formatTitle}</span>
              <span>{levelTitle}</span>
            </div>
          </div>
          <ol className="gdset-parts">
            <li>
              <i style={{ background: PART_COLOURS[0] }} />
              <span><b>Collect your thoughts</b><small>Quiet preparation before anyone speaks</small></span>
              <em><strong>{PREP_SECONDS}</strong><small>SEC</small></em>
            </li>
            <li>
              <i style={{ background: PART_COLOURS[1] }} />
              <span><b>The discussion</b><small>{table.length} {table.length === 1 ? "peer" : "peers"} at the table, plus you</small></span>
              <em><strong>{String(minutes).padStart(2, "0")}</strong><small>MIN</small></em>
            </li>
            <li>
              <i style={{ background: PART_COLOURS[2] }} />
              <span><b>Feedback</b><small>On every contribution you made</small></span>
              <em><strong>&infin;</strong><small>KEPT</small></em>
            </li>
          </ol>
          <p className="gdset-deep-note">
            <Fig name="route" size={15} />
            <span>
              Cutting a peer off counts as an interruption and costs points, as in a real group discussion.
            </span>
          </p>
          <div className="gdset-deep-go">
            <button type="submit" className="gdset-start" disabled={!ready}>
              {busy ? "Setting up…" : "Enter the room"}
              <Fig name="arrow-right-lg" size={17} />
            </button>
            <p>Mic check comes next. Your peers can wait.</p>
          </div>
        </section>

        <section className="gdset-panel" aria-label="Your table">
          <div className="gdset-panel-head">
            <h2>{table.length === 0 ? "An empty table" : `${table.length} ${table.length === 1 ? "voice" : "voices"}. One table.`}</h2>
            <Fig name="users-round" size={17} />
          </div>
          <ul>
            {table.map((p, i) => (
              <li key={p.key}>
                <span className="gdset-avatar gdset-avatar--sm" style={{ background: AVATAR_COLOURS[i % AVATAR_COLOURS.length] }}>{initials(p.name)}</span>
                <span>
                  <b>{p.name}</b>
                  <small>{p.tagline}</small>
                </span>
              </li>
            ))}
          </ul>
        </section>

        <p className="gdset-after">
          <Fig name="notebook-pen" size={16} />
          <span>After your round: feedback on every contribution, plus focused practice for the gaps.</span>
        </p>
      </aside>
    </form>
  );
}
