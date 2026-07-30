# gencon-demo-log

Automated tool for converting a BoardGameGeek (BGG) GenCon preview CSV export into a mobile-friendly, Google Docs-compatible Markdown demo checklist.

---

## 📌 Features

- **Mobile-Friendly Layout**: Main entries are bolded with location/booth numbers listed first (`Booth 1003 — 🔥 MUST HAVE — Drillers`). Sub-bullets contain notes, thoughts, and links without awkward text-wrapping on mobile screens.
- **Priority Badges**: Automatically maps BGG Priority 1 to 🔥 **MUST HAVE** and Priority 2 to ⭐ **INTERESTED**.
- **Exhibit Booth & Location Sorting**: Groups games logically by **Exhibit Hall Booths** (sorted numerically), **Event Rooms / Dedicated Rooms**, **Halls & Stadium Areas**, and **Other Locations**.
- **Verified GenCon Event Catalog Links**: Conditionally includes direct catalog search links (`https://www.gencon.com/event-catalog?search=<game+title>`) ONLY for games that have 1 or more events/demos listed in the catalog.
- **Cost & Demo Notation**: Highlights free show floor demos, ticketed catalog demo sessions, and retail for-sale titles.
- **Google Docs & Mobile Ready**:
  - No top-level bullet point (`* `) on main lines for clean Google Docs checkbox conversion.
  - Plain text `💬 Thoughts:` section so typed text on your phone remains in upright font without inheriting italics.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.8 or higher.

### 2. Running the Script

Place your BGG GenCon preview CSV export (e.g. `games.csv`) in the repository directory and run:

```bash
python generate_checklist.py --input games.csv --output GenCon_Demo_Checklist.md
```

By default, running `python generate_checklist.py` without arguments will look for `games.csv` and output to `GenCon_Demo_Checklist.md`.

---

## 📱 Google Docs & Mobile Setup Guide

1. **Upload to Google Drive**: Upload the generated `.md` file to Google Drive.
2. **Open with Google Docs**: Double-click the file in Google Drive and select **Open with -> Google Docs**.
3. **Turn into Interactive Checkboxes**:
   - Highlight all text (`Ctrl + A` or `Cmd + A`).
   - Click the **Checklist** icon on the Google Docs formatting toolbar.
4. **Enable Offline Access (Crucial for Convention Wi-Fi)**:
   - Open the **Google Docs app** on your mobile phone.
   - Tap the `...` (three dots) menu next to your document.
   - Toggle **Available offline** to **ON**.

---

## 📁 Repository Structure

- `generate_checklist.py` — The CLI Python script that parses CSV and generates the formatted checklist.
- `games.csv` — Input BGG preview CSV file.
- `GenCon_Demo_Checklist.md` — Generated output Markdown checklist.
- `README.md` — Documentation and usage guide.
