#!/usr/bin/env python3
"""Send a notification email via the Resend API.

Usage:
    python3 send_email.py "<subject>" <path-to-html-body-file>

Requires the RESEND_API_KEY environment variable. Optionally reads
RESEND_FROM_EMAIL (defaults to Resend's sandbox sender, which can only
send to the email address used to sign up for Resend).
"""
import json
import os
import sys
import urllib.request

RECIPIENT = "hiroshige.ichino@gmail.com"


def send_email(subject: str, html: str, to: str = RECIPIENT) -> str:
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise RuntimeError("RESEND_API_KEY is not set")
    from_addr = os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev")

    payload = json.dumps({
        "from": from_addr,
        "to": [to],
        "subject": subject,
        "html": html,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            # Resend sits behind Cloudflare, which blocks the default
            # Python-urllib User-Agent (HTTP 403 / Cloudflare error 1010).
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: send_email.py <subject> <html_body_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[2], "r", encoding="utf-8") as f:
        body_html = f.read()

    result = send_email(sys.argv[1], body_html)
    print(result)
