#!/usr/bin/env python3
"""
GenCon Demo Checklist Generator
-------------------------------
Generates a mobile-friendly, Google Docs-compatible Markdown checklist from a
BoardGameGeek (BGG) GenCon preview CSV export.

Usage:
    python generate_checklist.py [--input input.csv] [--output GenCon_Demo_Checklist.md]
"""

import argparse
import csv
import os
import re
import urllib.parse


VERIFIED_CATALOG_EVENTS = {
    "Food Truck Fury": {"type": "Free Demo Event Available", "free": True},
    "Drillers": {"type": "Free Demo Event", "free": True},
    "War of the Dragon: The Wheel of Time": {"type": "Free Demo Event", "free": True},
    "Kingdom Come: Deliverance – The Board Game": {"type": "Free Demo Event", "free": True},
    "Primacy": {"type": "Free Demo Event", "free": True},
    "One in a Million": {"type": "Free Demo Event", "free": True},
    "Gnomeville": {"type": "Free Demo Event", "free": True},
    "Crits & Tricks": {"type": "Free Demo Event", "free": True},
    "Brave & Bold: Bag Building Combat Game": {"type": "Free Demo Event", "free": True},
    "Cozy Stickerville": {"type": "Free Demo Event", "free": True},
    "Gunsen: The Battle for Toshi Ranbo": {"type": "Free Demo Event", "free": True},
    "The Lord of the Rings: The King's Gambit": {"type": "Free Demo Event", "free": True},
    "Ringyō": {"type": "Free Demo Event", "free": True},
    "Potemkin Villages": {"type": "Free Demo Event", "free": True},
    "Raas: A Dance of Love": {"type": "Free Demo Event", "free": True},
    "Estate: Raise the Realm": {"type": "Free Demo Event", "free": True},
    "Àiyé": {"type": "Free Demo Event", "free": True},
    "Las Vegas": {"type": "Free Demo Event", "free": True},
    "The Glorious Guilds of Buttonville": {"type": "Free Demo Event", "free": True}
}


def parse_location(location_raw):
    """
    Parses location text into a tuple for sorting:
    1. Exhibit Hall Booths (sorted numerically by booth number)
    2. Event Rooms / Dedicated Rooms
    3. Halls & Stadium Areas
    4. Unspecified Locations
    """
    loc_clean = location_raw.strip()
    if not loc_clean or loc_clean == ', ':
        return (4, 99999, 'Unspecified')
    
    loc_lower = loc_clean.lower()
    
    # Event / Dedicated Rooms
    if 'room' in loc_lower:
        match = re.search(r'\d+', loc_clean)
        num = int(match.group(0)) if match else 999
        return (2, num, loc_clean)
    
    # Halls / Stadium
    if 'hall' in loc_lower or 'stadium' in loc_lower:
        return (3, 0, loc_clean)
        
    # Numerical Exhibit Hall Booths
    match = re.search(r'\b(\d{3,4})\b', loc_clean)
    if match:
        return (1, int(match.group(1)), loc_clean)
        
    return (4, 9999, loc_clean)


def generate_checklist(input_csv, output_md):
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input CSV file not found: {input_csv}")
        
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for r in rows:
        r['sort_key'] = parse_location(r.get('Location', ''))

    # Sort by location category, booth number, location string, then Title
    rows.sort(key=lambda x: (x['sort_key'][0], x['sort_key'][1], x['sort_key'][2], x.get('Title', '')))

    category_names = {
        1: "🏛️ EXHIBIT HALL BOOTHS",
        2: "🚪 EVENT ROOMS & DEDICATED ROOMS",
        3: "🏟️ HALLS & STADIUM AREAS",
        4: "📍 OTHER / UNSPECIFIED LOCATIONS"
    }

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("# GenCon Demo Checklist\n\n")
        f.write("> **Legend:** 🔥 = MUST HAVE | ⭐ = INTERESTED\n")
        f.write("> **Demo Status:** `[🎟️ Event Catalog]` = 1+ Scheduled Events Listed in Catalog | `[Free Show Floor Demo]` = Walk-up Booth Demo | `[For Sale]` = Retail Booth\n\n")
        
        current_category = None

        for r in rows:
            cat_type = r['sort_key'][0]
            if cat_type != current_category:
                current_category = cat_type
                f.write(f"\n### {category_names[cat_type]}\n\n")

            title = r.get('Title', '').strip()
            pub = r.get('Publisher', '').strip()
            loc = r.get('Location', '').strip()
            if not loc or loc == ', ':
                loc = 'Unspecified'
                
            notes = r.get('Notes', '').strip()
            avail = r.get('Availability', '').strip()
            priority = r.get('Priority', '').strip()
            bgg_id = r.get('BGGId', '').strip()
            
            p_badge = "🔥 **MUST HAVE**" if priority == '1' else "⭐ **INTERESTED**"
            
            cat_event_info = CATALOG_EVENTS.get(title)
            
            if cat_event_info:
                demo_str = f"🎟️ Event Catalog ({cat_event_info['type']})"
            elif 'room' in loc.lower():
                demo_str = "🎟️ Event Catalog (Free Demo Session)"
            elif avail == 'Demo':
                demo_str = "Free Show Floor Demo"
            else:
                demo_str = "For Sale"
                
            bgg_url = f"https://boardgamegeek.com/boardgame/{bgg_id}" if bgg_id else None
            title_encoded = urllib.parse.quote_plus(title)
            gencon_url = f"https://www.gencon.com/event-catalog?search={title_encoded}"
            
            links = []
            if bgg_url:
                links.append(f"[BGG Page]({bgg_url})")
                
            # Only include GenCon Catalog link if 1+ events exist in the catalog
            if cat_event_info or 'room' in loc.lower():
                links.append(f"[GenCon Catalog]({gencon_url})")
                
            links_str = " • ".join(links)
            
            # Format: No leading bullet on main line, plain text Thoughts/Notes
            f.write(f"**Booth {loc}** — {p_badge} — **{title}** ({pub}) `[{demo_str}]`  \n")
            f.write(f"  * 🔗 {links_str}  \n")
            if notes:
                f.write(f"  * 💡 Note: {notes}  \n")
            f.write(f"  * 💬 Thoughts: \n\n")

    print(f"✅ Successfully generated checklist at: {output_md}")


def main():
    parser = argparse.ArgumentParser(description="GenCon Demo Checklist Generator")
    parser.add_argument("-i", "--input", default="games.csv", help="Path to input BGG preview CSV file (default: games.csv)")
    parser.add_argument("-o", "--output", default="GenCon_Demo_Checklist.md", help="Path to output Markdown file (default: GenCon_Demo_Checklist.md)")
    
    args = parser.parse_args()
    generate_checklist(args.input, args.output)


if __name__ == "__main__":
    main()
