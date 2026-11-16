#!/usr/bin/env python3
"""Pull one month of GA4 and Search Console numbers and write data.js for the report page.

Read-only against Google. Totals only: no personal data is requested or written.

    python scripts/pull_data.py            # last full month
    python scripts/pull_data.py 2026-11    # a named month
    python scripts/pull_data.py --check    # test access only, writes nothing

Environment:
    GA4_PROPERTY_ID               digits only (not the G- measurement ID)
    GOOGLE_SERVICE_ACCOUNT_JSON   the service-account key file's contents
    SEARCH_CONSOLE_SITE           optional, default https://www.gracelifefellowship.org/
"""
import calendar
import datetime as dt
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data.js"
TRACKING_START = "2026-11-05"  # GA4 has no data before this day
SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/webmasters.readonly",
]
# Searches containing any of these count as searches for the church by name.
BRAND_TERMS = ["grace life", "gracelife", "glf"]
# A search is listed on the public page only if every word in it is in this list, so a search
# that names a person is never published. Everything else is counted under "other_clicks".
SAFE_WORDS = set("""
grace life gracelife glf fellowship church churches baton rouge la louisiana preschool pre school daycare
kids children childrens youth student students ministry ministries counseling counselling christian
non nondenominational denominational denomination bible study studies devotional devotionals devotion
sermon sermons service services times time sunday worship live stream livestream online watch give giving
events event calendar near me in the a an of and for to at on is what how why does do god jesus christ
prayer pray new covenant gospel faith community small group groups lifegroups women womens men mens
staff about contact address directions location hours welcome visit visitor
""".split())


def publishable(query):
    words = "".join(ch if ch.isalnum() else " " for ch in query.lower()).split()
    return bool(words) and all(w in SAFE_WORDS or w.isdigit() for w in words)
# Tracked actions shown on the page, in order. An event GA4 does not return had zero.
ACTIONS = [
    ("view_give_page", "Give page visits"),
    ("event_registration_click", "Event registration clicks"),
    ("watch_live_click", "Watch Live clicks"),
    ("form_click", "Prayer, membership, preschool and counseling form clicks"),
    ("contact_click", "Phone and email clicks"),
    ("generate_lead", "Sign-ups (newsletter or book)"),
    ("get_directions", "Directions clicks"),
    ("book_action", "Book button clicks"),
    ("visitor_card_click", "Visitor card clicks"),
]


def fail(msg):
    print(f"STOP: {msg}", file=sys.stderr)
    sys.exit(2)


def session():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account

    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        fail("GOOGLE_SERVICE_ACCOUNT_JSON is not set. See README.md, 'Monthly update'.")
    try:
        info = json.loads(raw)
    except ValueError:
        fail("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON.")
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return AuthorizedSession(creds)


def post(s, url, body):
    r = s.post(url, json=body, timeout=60)
    if r.status_code != 200:
        # The log of a public repo is public: print Google's short status only, never the reply body.
        try:
            status = r.json().get("error", {}).get("status", "")
        except ValueError:
            status = ""
        api = "Search Console" if "webmasters" in url else "Google Analytics"
        fail(f"{api} returned {r.status_code} {status}".strip())
    return r.json()


def ga4(s, prop, start, end, metrics, dimensions=(), limit=50, order=None):
    body = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "metrics": [{"name": m} for m in metrics],
        "dimensions": [{"name": d} for d in dimensions],
        "limit": limit,
    }
    if order:
        body["orderBys"] = [{"metric": {"metricName": order}, "desc": True}]
    data = post(s, f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport", body)
    rows = []
    for row in data.get("rows", []):
        item = {d: v["value"] for d, v in zip(dimensions, row.get("dimensionValues", []))}
        item.update({m: float(v["value"]) for m, v in zip(metrics, row["metricValues"])})
        rows.append(item)
    return rows


def gsc(s, site, start, end, dimensions=(), limit=1000):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{quote(site, safe='')}/searchAnalytics/query"
    body = {"startDate": start, "endDate": end, "dimensions": list(dimensions), "rowLimit": limit}
    return post(s, url, body).get("rows", [])


def month_range(ym):
    y, m = (int(x) for x in ym.split("-"))
    start = f"{y:04d}-{m:02d}-01"
    end = f"{y:04d}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"
    return max(start, TRACKING_START), end


def prev_month(ym):
    y, m = (int(x) for x in ym.split("-"))
    return f"{y - 1:04d}-12" if m == 1 else f"{y:04d}-{m - 1:02d}"


def pull(s, prop, site, start, end, detail=True):
    tot = ga4(s, prop, start, end, ["totalUsers", "newUsers", "sessions", "engagedSessions", "screenPageViews"])
    tot = tot[0] if tot else {}
    g = gsc(s, site, start, end)
    g = g[0] if g else {}
    out = {
        "totals": {
            "users": int(tot.get("totalUsers", 0)), "new_users": int(tot.get("newUsers", 0)),
            "sessions": int(tot.get("sessions", 0)), "engaged_sessions": int(tot.get("engagedSessions", 0)),
            "page_views": int(tot.get("screenPageViews", 0)),
        },
        "search": {
            "clicks": int(g.get("clicks", 0)), "impressions": int(g.get("impressions", 0)),
            "impressions_rounded": False,
            "ctr_pct": round(g.get("ctr", 0) * 100, 1), "position": round(g.get("position", 0), 1),
        },
    }
    if not detail:
        return out
    out["channels"] = [
        {"channel": r["sessionDefaultChannelGroup"], "sessions": int(r["sessions"]), "engaged_sessions": int(r["engagedSessions"])}
        for r in ga4(s, prop, start, end, ["sessions", "engagedSessions"], ["sessionDefaultChannelGroup"], order="sessions")
    ]
    out["pages"] = [
        {"page": r["pagePath"], "views": int(r["screenPageViews"]), "users": int(r["totalUsers"])}
        for r in ga4(s, prop, start, end, ["screenPageViews", "totalUsers"], ["pagePath"], limit=10, order="screenPageViews")
    ]
    events = {r["eventName"]: int(r["eventCount"]) for r in ga4(s, prop, start, end, ["eventCount"], ["eventName"], limit=200)}
    out["actions"] = [{"event": e, "label": label, "count": events.get(e, 0)} for e, label in ACTIONS]
    queries = gsc(s, site, start, end, ["query"])
    shown = [q for q in queries if publishable(q["keys"][0])]
    out["search"]["queries_total"] = len(queries)
    out["search"]["other_clicks"] = int(sum(q["clicks"] for q in queries if not publishable(q["keys"][0])))
    out["queries"] = [
        {"query": q["keys"][0], "clicks": int(q["clicks"]), "impressions": int(q["impressions"]),
         "position": round(q["position"], 1), "by_name": any(t in q["keys"][0].lower() for t in BRAND_TERMS)}
        for q in shown[:10]
    ]
    return out


def label(start, end):
    a, b = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    full = a.day == 1 and b.day == calendar.monthrange(b.year, b.month)[1]
    if full:
        return a.strftime("%B %Y")
    return f"{a.strftime('%b')} {a.day} to {b.strftime('%b')} {b.day}, {b.year}"


def main():
    args = sys.argv[1:]
    prop = os.environ.get("GA4_PROPERTY_ID", "").strip()
    site = os.environ.get("SEARCH_CONSOLE_SITE", "").strip() or "https://www.gracelifefellowship.org/"
    if not prop.isdigit():
        fail("GA4_PROPERTY_ID is missing or is not digits only. See README.md, 'Monthly update'.")
    try:
        s = session()
    except Exception as e:  # key problems: say what kind, never the content
        fail(f"Could not use the Google key ({type(e).__name__}).")
    today = dt.date.today()

    if "--check" in args:
        week_ago = (today - dt.timedelta(days=7)).isoformat()
        g = ga4(s, prop, week_ago, today.isoformat(), ["totalUsers"])
        c = gsc(s, site, week_ago, today.isoformat())
        print(f"GA4 ok: {int(g[0]['totalUsers']) if g else 0} users in the last 7 days")
        print(f"Search Console ok: {int(c[0]['clicks']) if c else 0} clicks in the last 7 days")
        return

    ym = args[0] if args else prev_month(today.strftime("%Y-%m"))
    start, end = month_range(ym)
    if end < TRACKING_START:
        fail(f"{ym} is before tracking began ({TRACKING_START}).")
    if dt.date.fromisoformat(end) > today - dt.timedelta(days=3):
        fail(f"{ym} is not finished, or Search Console has not caught up with it yet (it runs about 3 days behind).")
    data = {
        "period": {"start": start, "end": end, "label": label(start, end),
                   "days": (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days + 1},
        "pulled": today.isoformat(),
        "how": "Updated automatically on the 4th of each month.",
        "tracking_start": TRACKING_START,
    }
    data.update(pull(s, prop, site, start, end))
    pstart, pend = month_range(prev_month(ym))
    data["previous"] = None
    if pend >= TRACKING_START:
        prev = pull(s, prop, site, pstart, pend, detail=False)
        prev["period"] = {"start": pstart, "end": pend, "label": label(pstart, pend)}
        data["previous"] = prev
    if data["totals"]["users"] == 0:
        fail(f"Google Analytics returned zero users for {start} to {end}; data.js was left unchanged.")
    if data["search"]["impressions"] == 0 or not data["queries"]:
        fail(f"Search Console returned no rows for {start} to {end}; data.js was left unchanged.")

    OUT.write_text(
        "// Written by scripts/pull_data.py. The page reads only this file for GLF's numbers.\n"
        "window.GLF_DATA = " + json.dumps(data, indent=2) + ";\n"
    )
    print(f"Wrote {OUT.name}: {data['period']['label']}, {data['totals']['users']} users, {data['search']['clicks']} search clicks")


if __name__ == "__main__":
    main()
