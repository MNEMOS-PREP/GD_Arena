"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { notifications } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { isEmbedded } from "@/lib/embedded";
import { Icon, type IconName } from "./icons";

// Polling, not a socket: the control-plane socket is scoped to one session, and
// a notification can arrive when the user is not in one (FR-32).
const POLL_MS = 30_000;

const MAIN_NAV: { href: string; label: string; icon: IconName; match: (p: string) => boolean }[] = [
  {
    href: "/",
    label: "Group Discussion",
    icon: "users",
    match: (p) => p === "/" || p.startsWith("/sessions") || p.startsWith("/lobby/") || p.startsWith("/room"),
  },
  { href: "/lobbies", label: "Lobbies", icon: "grid", match: (p) => p === "/lobbies" },
  { href: "/practice/new", label: "AI practice", icon: "bot", match: (p) => p.startsWith("/practice") },
  {
    href: "/history",
    label: "Past sessions",
    icon: "history",
    match: (p) => p === "/history" || p.startsWith("/report"),
  },
];

export function Sidebar() {
  const { user, loading, signOut } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [unread, setUnread] = useState(0);
  // Read after mount: the server cannot know, and both renders must agree.
  const [embedded, setEmbedded] = useState(false);
  useEffect(() => setEmbedded(isEmbedded()), [pathname]);

  useEffect(() => {
    if (!user) {
      setUnread(0);
      return;
    }
    let cancelled = false;
    const poll = async () => {
      try {
        const list = await notifications.list(true);
        if (!cancelled) setUnread(list.unread);
      } catch {
        // A failed poll is not worth surfacing in the chrome.
      }
    };
    void poll();
    const timer = setInterval(poll, POLL_MS);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [user]);

  async function handleSignOut() {
    await signOut();
    router.push("/login");
  }

  const brand = (
    <Link href="/" className="brand wordmark" aria-label="Home">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src="/logo.png" alt="" height={36} style={{ height: 36, width: "auto", display: "block" }} />
    </Link>
  );

  // Inside the platform: its tabs only. The shell owns the brand, the account
  // and signing out, and the student came in signed in.
  if (embedded) {
    return (
      <header className="guestbar guestbar--embedded">
        <nav className="guestbar-nav" aria-label="Group discussion">
          {user &&
            MAIN_NAV.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                className={`nav-link ${n.match(pathname) ? "nav-link--active" : ""}`}
                aria-current={n.match(pathname) ? "page" : undefined}
              >
                {n.label}
              </Link>
            ))}
        </nav>
      </header>
    );
  }

  if (loading) return <header className="guestbar">{brand}</header>;

  if (!user) {
    return (
      <header className="guestbar">
        {brand}
        <nav className="guestbar-nav">
          <Link href="/login" className={`nav-link ${pathname === "/login" ? "nav-link--active" : ""}`}>
            Sign in
          </Link>
          <Link href="/register">
            <button type="button">Get started</button>
          </Link>
        </nav>
      </header>
    );
  }

  const initial = (user.full_name || user.email)[0].toUpperCase();

  return (
    <header className="guestbar topnav">
      {brand}
      <nav className="topnav-links" aria-label="Main">
        {MAIN_NAV.map((n) => (
          <Link
            key={n.href}
            href={n.href}
            className={`topnav-link ${n.match(pathname) ? "topnav-link--active" : ""}`}
            aria-current={n.match(pathname) ? "page" : undefined}
          >
            {n.label}
          </Link>
        ))}
      </nav>
      <div className="topnav-end">
        <Link
          href="/notifications"
          className={`topnav-bell ${pathname === "/notifications" ? "topnav-bell--active" : ""}`}
          aria-label={unread ? `Notifications, ${unread} unread` : "Notifications"}
        >
          <Icon name="bell" className="nav-icon" />
          {unread ? <span className="count">{unread}</span> : null}
        </Link>
        <details className="topnav-user">
          <summary className="avatar" aria-label="Account">
            {initial}
          </summary>
          <div className="topnav-menu">
            <strong>{user.full_name}</strong>
            <span className="meta">{user.role}</span>
            <Link href="/profile">Profile</Link>
            <button type="button" className="secondary" onClick={handleSignOut}>
              Sign out
            </button>
          </div>
        </details>
      </div>
    </header>
  );
}
