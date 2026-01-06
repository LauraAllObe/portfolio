import nodemailer from "nodemailer";

// ---- Config ----
const MIN_FORM_FILL_MS = 2500; // 2.5s
const MAX_MESSAGE_LEN = 4000;
const MAX_PER_IP_PER_WINDOW = 8;
const WINDOW_MS = 10 * 60 * 1000; // 10 minutes

// Simple in-memory rate limiting (works per serverless instance)
const ipHits = new Map(); // ip -> { count, resetAt }

// ---- Mail transporter ----
const transporter = nodemailer.createTransport({
  host: "smtp.mailgun.org",
  port: 587,
  secure: false,
  auth: {
    user: process.env.MAILGUN_USER,
    pass: process.env.MAILGUN_PASS
  }
});

// ---- Helpers ----
function getClientIp(req) {
  // Vercel adds x-forwarded-for
  const xff = req.headers["x-forwarded-for"];
  if (typeof xff === "string" && xff.length > 0) return xff.split(",")[0].trim();
  return req.socket?.remoteAddress || "unknown";
}

function rateLimit(ip) {
  const now = Date.now();
  const entry = ipHits.get(ip);

  if (!entry || entry.resetAt <= now) {
    ipHits.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return { ok: true };
  }

  if (entry.count >= MAX_PER_IP_PER_WINDOW) {
    return { ok: false, retryAfterMs: entry.resetAt - now };
  }

  entry.count += 1;
  return { ok: true };
}

function isValidEmail(email) {
  return typeof email === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ---- Handler ----
export default async function handler(req, res) {
  // If you’re calling same-origin (/api/sendEmail), you can remove CORS entirely.
  res.setHeader("Access-Control-Allow-Origin", process.env.CORS_ORIGIN || "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const ip = getClientIp(req);
  const rl = rateLimit(ip);
  if (!rl.ok) {
    res.setHeader("Retry-After", Math.ceil(rl.retryAfterMs / 1000));
    return res.status(429).json({ error: "Too many requests" });
  }

  try {
    const { name, email, subject, message, time, website, form_ts } = req.body || {};

    // 🕳️ Honeypot: if filled, silently pretend success (don’t help bots)
    if (typeof website === "string" && website.trim().length > 0) {
      return res.status(200).json({ success: true });
    }

    // ⏱️ Minimum time-to-submit
    const ts = Number(form_ts);
    if (!Number.isFinite(ts) || ts <= 0) {
      // missing timestamp => suspicious; you can either reject or silently accept
      return res.status(400).json({ error: "Invalid submission" });
    }
    const elapsed = Date.now() - ts;
    if (elapsed < MIN_FORM_FILL_MS) {
      return res.status(400).json({ error: "Too fast" });
    }

    // Basic validation & limits
    if (typeof name !== "string" || name.trim().length < 1) {
      return res.status(400).json({ error: "Invalid name" });
    }
    if (!isValidEmail(email)) {
      return res.status(400).json({ error: "Invalid email" });
    }
    if (typeof subject !== "string" || subject.trim().length < 1) {
      return res.status(400).json({ error: "Invalid subject" });
    }
    if (typeof message !== "string" || message.trim().length < 1) {
      return res.status(400).json({ error: "Invalid message" });
    }
    if (message.length > MAX_MESSAGE_LEN) {
      return res.status(400).json({ error: "Message too long" });
    }

    await transporter.sendMail({
      from: `"${name}" <contact@lauralovelace.info>`,
      to: process.env.MAIL_TO || "laura.builds.tech@gmail.com",
      replyTo: email,
      subject,
      html: `
        <div style="font-family: system-ui, sans-serif, Arial; font-size: 12px">
          <div>A message by ${escapeHtml(name)} has been received.</div>
          <div style="margin-top: 20px; padding: 15px 0; border-top: dashed 1px lightgrey;">
            <p><strong>From:</strong> ${escapeHtml(email)}</p>
            <p><strong>Time:</strong> ${escapeHtml(time || "")}</p>
            <p><strong>Message:</strong><br/>${escapeHtml(message).replace(/\n/g, "<br/>")}</p>
          </div>
        </div>
      `
    });

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error("Email send failed:", err);
    return res.status(500).json({ error: "Email failed to send." });
  }
}

// Minimal HTML escaping to prevent injection in your email template
function escapeHtml(str) {
  if (typeof str !== "string") return "";
  return str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
