"use client";

/** Building blocks of the Arena: orbs, the round table, the ring clock, notices. */

import { useCallback, useEffect, useRef, useState, type CSSProperties, type ReactNode, type RefObject } from "react";

import { Icon, type IconName } from "@/app/icons";

import type { TurnNotice } from "@/lib/use-session-socket";

/** A stable hue per label, spread around the wheel and kept clear of amber. */
export function hueFor(label: string): number {
  let hash = 0;
  for (const ch of label) hash = (hash * 31 + ch.charCodeAt(0)) % 360;
  const hue = (hash * 47 + 200) % 360;
  return hue > 20 && hue < 60 ? hue + 70 : hue;
}

export interface SeatInfo {
  label: string;
  name: string;
  /** What to show under the name when not speaking. */
  sub?: string;
  speaking: boolean;
  /** 0..1 voice level; omit to let the CSS rings carry the animation. */
  level?: number;
  you?: boolean;
  badge?: string;
  /** Interruptions made, shown as a coral counter on the orb. */
  strikes?: number;
  away?: boolean;
  hue?: number;
  /** Their microphone is off. */
  muted?: boolean;
}

export function Orb({ seat, children }: { seat: SeatInfo; children?: ReactNode }) {
  const style = {
    "--h": seat.hue ?? hueFor(seat.label),
    "--lvl": seat.speaking ? Math.max(seat.level ?? 0.35, 0.12) : (seat.level ?? 0) * 0.5,
  } as CSSProperties;
  return (
    <div className={`orb ${seat.you ? "orb--you" : ""}`} style={style}>
      {children ?? seat.name.slice(0, 1).toUpperCase()}
      {seat.badge && <span className="orb-badge">{seat.badge}</span>}
      {(seat.strikes ?? 0) > 0 && (
        <span className="orb-strike" title="Interruptions made">
          {seat.strikes}
        </span>
      )}
    </div>
  );
}

/** Your own camera, for a room with no media server: it never leaves this device. */
export function useSelfCamera() {
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string | null>(null);
  const toggle = useCallback(async () => {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      setStream(null);
      return;
    }
    try {
      const next = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
      setStream(next);
      setError(null);
    } catch {
      setError("The camera is blocked. Allow it in the browser's address bar, then try again.");
    }
  }, [stream]);
  useEffect(() => () => stream?.getTracks().forEach((t) => t.stop()), [stream]);
  return { stream, on: Boolean(stream), toggle, error };
}

export interface SelfVideo {
  on: boolean;
  /** A stream to show (a local camera). */
  stream?: MediaStream | null;
  /** Or an element the media server attaches your published camera to. */
  videoRef?: RefObject<HTMLVideoElement | null>;
}

function SelfVideoEl({ video }: { video: SelfVideo }) {
  const own = useRef<HTMLVideoElement | null>(null);
  const ref = video.videoRef ?? own;
  useEffect(() => {
    const el = ref.current;
    if (!el || video.videoRef) return;
    el.srcObject = video.stream ?? null;
    if (video.stream) void el.play().catch(() => {});
  }, [video.stream, video.videoRef, ref]);
  // The avatar gives way only once a picture is really playing.
  const [live, setLive] = useState(false);
  useEffect(() => {
    if (!video.on) setLive(false);
  }, [video.on]);
  return (
    <video
      ref={ref}
      className={`mt-video ${video.on ? "" : "mt-video--off"} ${live && video.on ? "mt-video--live" : ""}`}
      onLoadedData={() => setLive(true)}
      onEmptied={() => setLive(false)}
      autoPlay
      muted
      playsInline
    />
  );
}

/**
 * The meeting: a tile for everyone at the table. A tile shows a camera when
 * there is one and a large avatar when there is not; the one holding the floor
 * is outlined and its name chip animates. What was said last runs along the
 * bottom as a live caption.
 */
export function RoundTable({
  seats,
  centre,
  selfVideo,
}: {
  seats: SeatInfo[];
  centre?: ReactNode;
  selfVideo?: SelfVideo;
}) {
  const ordered = [...seats].sort((a, b) => Number(!!b.you) - Number(!!a.you));

  // Other people's cameras arrive from the media server in one hidden holder,
  // tagged with who they belong to; move each into its owner's tile.
  const identities = ordered.filter((s) => !s.you).map((s) => s.label).join("|");
  useEffect(() => {
    const place = () => {
      const holder = document.getElementById("remote-media");
      if (!holder) return;
      for (const label of identities.split("|").filter(Boolean)) {
        const slot = document.querySelector<HTMLElement>(`[data-slot="${label}"]`);
        if (!slot) continue;
        holder.querySelectorAll<HTMLVideoElement>(`video[data-identity="${label}"]`).forEach((v) => slot.appendChild(v));
      }
    };
    place();
    const timer = window.setInterval(place, 1500);
    return () => window.clearInterval(timer);
  }, [identities]);

  return (
    <section className="mt" aria-label="The meeting">
      <ul className="mt-grid" data-count={Math.min(ordered.length, 6)}>
        {ordered.map((seat, i) => (
          <li
            key={seat.label}
            className={`mt-tile ${seat.you ? "mt-tile--you" : ""} ${seat.speaking ? "mt-tile--speaking" : ""} ${seat.away ? "mt-tile--away" : ""}`}
            style={{ "--i": i } as CSSProperties}
          >
            <div className="mt-media">
              <span className="mt-avatar" aria-hidden>
                {seat.name.slice(0, 1).toUpperCase()}
              </span>
              {seat.you && selfVideo ? <SelfVideoEl video={selfVideo} /> : <div className="mt-slot" data-slot={seat.label} />}
            </div>
            {seat.badge && <span className="mt-ai">{seat.badge}</span>}
            {(seat.strikes ?? 0) > 0 && (
              <span className="mt-strike" title="Interruptions made">
                {seat.strikes}
              </span>
            )}
            <div className="mt-chip">
              {seat.speaking ? (
                <span className="eq" aria-label="speaking">
                  <i />
                  <i />
                  <i />
                </span>
              ) : (
                <Icon name={seat.muted ? "mic-off" : "mic"} size={14} className={seat.muted ? "mt-muted" : ""} />
              )}
              <span className="mt-name">
                {seat.name}
                {seat.you ? " (you)" : ""}
              </span>
              {!seat.speaking && seat.sub && <small>{seat.sub}</small>}
            </div>
          </li>
        ))}
      </ul>
      <div className="mt-caption" aria-live="polite">
        {centre}
      </div>
    </section>
  );
}

/** A control in the meeting bar: an icon in a round button, its name under it. */
export function MeetButton({
  icon,
  label,
  on,
  danger,
  primary,
  warn,
  disabled,
  title,
  onClick,
}: {
  icon: IconName;
  label: string;
  /** A toggle that is currently on (muted, camera off, hand up). */
  on?: boolean;
  danger?: boolean;
  primary?: boolean;
  /** When on, show it as a problem (muted, camera off) rather than as selected. */
  warn?: boolean;
  disabled?: boolean;
  title?: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      className={`meet-btn ${danger ? "meet-btn--danger" : ""} ${primary ? "meet-btn--primary" : ""} ${warn ? "meet-btn--warn" : ""}`}
      aria-pressed={on}
      disabled={disabled}
      title={title ?? label}
      onClick={onClick}
    >
      <span className="meet-ico">
        <Icon name={icon} size={20} />
      </span>
      <span className="meet-label">{label}</span>
    </button>
  );
}

export function RingClock({
  seconds,
  duration,
  warn,
}: {
  seconds: number;
  duration: number;
  warn?: boolean;
}) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const fraction = duration > 0 ? Math.max(0, Math.min(1, seconds / duration)) : 0;
  const clock = `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
  return (
    <div className={`ring-clock ${warn ? "ring-clock--warn" : ""}`} role="timer" aria-label={clock}>
      <svg viewBox="0 0 100 100" aria-hidden>
        <circle className="track" cx="50" cy="50" r={radius} />
        <circle
          className="fill"
          cx="50"
          cy="50"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - fraction)}
        />
      </svg>
      <span>{clock}</span>
    </div>
  );
}

export function Notices({
  notices,
  nameOf,
  youLabel,
}: {
  notices: TurnNotice[];
  nameOf: (label: string) => string;
  /** The viewer's own label. When given, only the viewer's interruptions carry the penalty line. */
  youLabel?: string;
}) {
  // Newest few only; each fades out of the list as newer ones push it down.
  return (
    <div className="notices" aria-live="polite">
      {notices.slice(0, 3).map((n) => (
        <div key={n.id} className={`notice notice--${n.kind}`}>
          {n.kind === "interruption" ? (
            <>
              <b>{nameOf(n.by)}</b> cut in on <b>{nameOf(n.target)}</b>
              {(youLabel === undefined || n.by === youLabel) && (
                <small>Interrupting costs points. Running penalty: −{n.penalty}</small>
              )}
            </>
          ) : (
            <>
              <b>{nameOf(n.by)}</b> replied to <b>{nameOf(n.target)}</b>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export function ArenaHeader({
  topic,
  phaseLabel,
  live,
  seconds,
  duration,
  warn,
  right,
}: {
  topic: string;
  phaseLabel: string;
  live: boolean;
  seconds: number;
  duration: number;
  warn?: boolean;
  right?: ReactNode;
}) {
  const clock = `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
  const total = `${String(Math.floor(duration / 60)).padStart(2, "0")}:${String(Math.floor(duration % 60)).padStart(2, "0")}`;
  return (
    <header className="arena-head">
      <div className="arena-topic">
        <div className="arena-title">
          <h1>Group Discussion</h1>
          <span className={`arena-phase ${live ? "arena-phase--live" : ""}`}>
            <i />
            {phaseLabel}
          </span>
        </div>
        <p className="arena-sub">{topic}</p>
      </div>
      <div className="arena-tools">
        {right}
        <span
          className={`timer-pill ${warn ? "timer-pill--warn" : ""}`}
          role="timer"
          aria-label={`${clock} remaining of ${Math.round(duration / 60)} minutes`}
        >
          {live && <i className="rec" aria-hidden />}
          {clock}
          {duration > 0 && <small> / {total}</small>}
        </span>
      </div>
    </header>
  );
}

function clockOf(seconds: number): string {
  const whole = Math.max(0, Math.round(seconds));
  return `${Math.floor(whole / 60)}:${String(whole % 60).padStart(2, "0")}`;
}

/** Live speaking time for everyone at the table (M14 FR-14.11): one stacked bar, then who is who. */
export function FloorBars({
  floor,
  order,
  nameOf,
}: {
  floor: Record<string, number>;
  order: string[];
  nameOf: (label: string) => string;
}) {
  const total = order.reduce((sum, label) => sum + (floor[label] ?? 0), 0);
  return (
    <div className="floor" aria-label="Speaking time so far">
      <div className="floor-seg" role="presentation">
        {order.map((label, i) => {
          const share = total > 0 ? (floor[label] ?? 0) / total : 0;
          return share > 0 ? <i key={label} style={{ flexGrow: share, "--i": i } as CSSProperties} /> : null;
        })}
        {total === 0 && <i style={{ flexGrow: 1, background: "transparent" }} />}
      </div>
      <ul className="floor-key">
        {order.map((label, i) => (
          <li key={label} style={{ "--i": i } as CSSProperties}>
            <span className="floor-dot" aria-hidden />
            <span className="floor-name">{nameOf(label)}</span>
            <span className="floor-num">{clockOf(floor[label] ?? 0)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

/** The latest ideas on the table, from the Observer's notes (M14 FR-14.13). */
export function IdeasStrip({
  ideas,
}: {
  ideas: { ideas: string[]; open_questions: string[] } | null;
}) {
  if (!ideas || (ideas.ideas.length === 0 && ideas.open_questions.length === 0)) return null;
  return (
    <div className="ideas" aria-label="Recent ideas" aria-live="polite">
      <span className="ideas-label">On the table</span>
      {ideas.ideas.map((idea, index) => (
        <span key={`idea-${index}`} className="idea">
          {idea}
        </span>
      ))}
      {ideas.open_questions.map((question, index) => (
        <span key={`open-${index}`} className="idea idea--open" title="Still open">
          {question}
        </span>
      ))}
    </div>
  );
}
