#!/usr/bin/env python3
"""Turn a CSV of locations into the location list the portfolio kit expects.

Usage: python3 _portfolio/locations_from_csv.py locations.csv <account>/data/<account>-locations.json

CSV columns (header row required): name, brand, address, city, state, zip, phone, website, lat, lng
(slug is optional; it is made from the name when missing). lat/lng can be blank: the scan then
searches by name and city, and the map-pin check is skipped.
"""
import csv, json, re, sys

def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")

rows = []
with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        rows.append({
            "slug": r.get("slug") or slug(r["name"]), "name": r["name"], "brand": r.get("brand") or r["name"],
            "address": r.get("address", ""), "city": r.get("city", ""), "state": r.get("state", ""), "zip": r.get("zip", ""),
            "phone": r.get("phone", ""), "website": r.get("website", ""),
            "lat": float(r["lat"]) if r.get("lat") else None, "lng": float(r["lng"]) if r.get("lng") else None,
        })
json.dump(rows, open(sys.argv[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"{len(rows)} locations -> {sys.argv[2]}")
