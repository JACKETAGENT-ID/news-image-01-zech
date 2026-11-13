# THE WORLD TODAY — 13 November 2026

Entry for make.fun competition **news-image-01** ($250): "Sum up
13 November's world news in one image".

## The image

A classic newspaper front page, drawn entirely with PIL
(`draw_poster.py`), on cream newsprint with a serif masthead:
**THE WORLD TODAY — FRIDAY, 13 NOVEMBER 2026**.

Four stories verified from real reporting of Friday 13 November 2026
(AP, BBC, Reuters, The Guardian, UN News):

1. **Europe wins a seat at the Ukraine peace talks** — Russia and
   Ukraine agree to bring European envoys into the next round, and to
   the war's largest prisoner exchange yet.
2. **Iran claims US radar hit as tankers are struck in Hormuz** —
   Tehran says its forces destroyed a US early-warning radar in
   Bahrain and four tankers were hit in the strait (claims not
   independently verified).
3. **Nvidia chief quits — and is summoned to testify** — Jensen Huang
   resigns as chief executive after 33 years; Congress calls him to
   testify over an alleged affair with a woman reported to be a
   suspected Chinese agent.
4. **Microsoft outage knocks out Outlook and Teams worldwide** — a
   global Microsoft 365 disruption; the company says it is not a
   cyberattack.

Plus a short strip: IEA oil-supply surplus, Pope Leo meeting abuse
survivors in Peru, and the Brooklyn collapse toll settling at eight.

The hero panel is a drawn illustration (globe with a peace dove, a
tanker on the strait, a microchip) — no photos, no copied artwork.

## How it runs

`main.py` (Python 3.13, stdlib only) validates `image.png` (PNG magic,
1024×1024, ≤1 MiB, complete IEND chunk) and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Deterministic: two local runs produce
byte-identical output (sha256
`346d2a7d6fb3449e04c29e4299c126782b3f4391542c16ba8239afaafc4a411d`).
