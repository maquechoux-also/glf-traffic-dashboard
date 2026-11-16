// Published benchmarks, each checked against its source on 2026-11-16.
// No published study measures ordinary-week traffic for local church websites,
// so most rows use the nearest group and say which group it is.
window.GLF_BENCHMARKS = {
  "checked": "2026-11-16",
  "sources": {
    "wired": {"name": "Wired Impact, Nonprofit Website Benchmarks", "group": "Small nonprofits", "detail": "median of 130+ nonprofit websites built by one web agency, 2025 data; \"small\" is our reading of their traffic, about 600 visitors a month", "url": "https://wiredimpact.com/nonprofit-website-benchmarks/"},
    "siege": {"name": "Siege Media, GA4 Engagement Rate Benchmarks", "group": "All industries", "detail": "median of 546 websites, 2024 to 2026 data; mostly large commercial sites", "url": "https://www.siegemedia.com/research/ga4-engagement-rate-benchmarks"},
    "agency": {"name": "AgencyAnalytics, Sessions per User", "group": "Small businesses", "detail": "agency client websites, as of Dec 2024; time window not stated", "url": "https://agencyanalytics.com/kpi-definitions/sessions-per-user"},
    "mr": {"name": "M+R Benchmarks 2026", "group": "Larger nonprofits", "detail": "study of 180 mostly national nonprofits, 2025 data; how many supplied website data is not stated", "url": "https://mrbenchmarks.com/website-performance/"},
    "churchco22": {"name": "The Church Co, Easter 2022", "group": "Churches, Easter weekend 2022", "detail": "1,000+ church websites on one website builder; share of visitors, not visits, on Easter weekend 2022; the post calls the social figure a referral rate without defining it", "url": "https://web.archive.org/web/20240721004437/https://thechurchco.com/blog/2022/04/26/easter-2022/"},
    "churchco23": {"name": "The Church Co, Easter 2023 Recap", "group": "Churches, Easter weekend 2023", "detail": "2,300+ church websites, Easter weekend 2023; percentage is our arithmetic from 332,000 new of 382,000 visitors", "url": "https://web.archive.org/web/20250122115635/https://thechurchco.com/blog/2023/05/02/easter-2023-recap/"},
    "ahrefs": {"name": "Ahrefs, What is a Good Organic CTR?", "group": "All industries", "detail": "Search Console data from 422,421 websites, 2026", "url": "https://ahrefs.com/blog/what-is-a-good-ctr/"},
    "lifeway": {"name": "Lifeway Research, Church Switcher Study 2023", "group": "US Protestant churchgoers who changed churches", "detail": "survey of 1,001 people, 2023", "url": "https://research.lifeway.com/wp-content/uploads/2023/11/Church-Switcher-2023-Factors-in-Choosing-Current-Church-Report.pdf"}
  },
  // kind: "rate" rows can be compared at any period length; "monthly" rows only when the period is a full month.
  // better: "higher" | "lower" | null (null = a mix, not a score).
  "rows": [
    {"key": "engagement_rate", "label": "Engaged visits", "unit": "%", "kind": "rate", "better": "higher",
     "baselines": [{"value": 43.2, "source": "wired"}, {"value": 51, "source": "siege"}]},
    {"key": "pages_per_session", "label": "Pages per visit", "unit": "", "kind": "rate", "better": "higher",
     "baselines": [{"value": 1.74, "source": "wired"}]},
    {"key": "sessions_per_user", "label": "Visits per visitor", "unit": "", "kind": "rate", "better": null,
     "baselines": [{"value": 1.26, "source": "agency"}], "note": "Rises with a longer period, so a short window reads low."},
    {"key": "users", "label": "Visitors", "unit": "count", "kind": "monthly", "better": "higher",
     "baselines": [{"value": 601, "source": "wired"}]},
    {"key": "sessions", "label": "Visits", "unit": "count", "kind": "monthly", "better": "higher",
     "baselines": [{"value": 782, "source": "wired"}]},
    {"key": "page_views", "label": "Page views", "unit": "count", "kind": "monthly", "better": "higher",
     "baselines": [{"value": 1800, "source": "wired"}]},
    {"key": "share_organic", "label": "Visits from Google and other search", "unit": "%", "kind": "rate", "better": null,
     "baselines": [{"value": 37.5, "source": "wired"}, {"value": 39, "source": "mr"}, {"value": 45, "source": "churchco22"}], "note": "The church figure counts visitors, not visits, and comes from one holiday weekend."},
    {"key": "share_direct", "label": "Visits that came direct", "unit": "%", "kind": "rate", "better": null,
     "baselines": [{"value": 37, "source": "wired"}, {"value": 36, "source": "churchco22"}], "note": "The church figure counts visitors, not visits, and comes from one holiday weekend."},
    {"key": "share_social", "label": "Visits from social media", "unit": "%", "kind": "rate", "better": null,
     "baselines": [{"value": 11, "source": "churchco22"}], "note": "The church figure counts visitors, not visits, and comes from one holiday weekend."},
    {"key": "search_ctr", "label": "Search click-through rate", "unit": "%", "kind": "rate", "better": null,
     "baselines": [{"value": null, "text": "1% to 2% is typical", "source": "ahrefs"}],
     "note": "Churches are searched by name, and name searches get clicked far more often, so a church is expected to sit above this. It is not a score."},
    {"key": "search_position", "label": "Average search position", "unit": "", "kind": "rate", "better": "lower",
     "baselines": [], "none": "No comparable benchmark. Average position depends on which searches a site shows up for, so it is only useful against GLF's own earlier months."},
    {"key": "new_user_share", "label": "First-time visitors", "unit": "%", "kind": "rate", "better": null,
     "baselines": [{"value": 87, "text": "about 87%", "source": "churchco23"}],
     "note": "Everyone looks new in the first weeks of tracking, so compare after two or three months. The church figure is from Easter weekend, the yearly peak for first-time visitors, so an ordinary month should sit below it."}
  ],
  "actions_note": "No published benchmark exists for church website actions such as event registrations, Watch Live clicks, form clicks or Give page visits. They will be compared with Grace Life's own earlier months as those build up.",
  "context": {
    "source": "lifeway",
    "facts": [
      {"value": "37%", "text": "of people who changed churches used church websites while looking (of those who actively searched)."},
      {"value": "15%", "text": "were first introduced to their current church by finding its website."}
    ],
    "helpful_title": "What they found most helpful on the website",
    "helpful_note": "Asked of the 153 people who found their church through its website. This is what people said helped, not a share of page views.",
    "helpful": [
      {"label": "Beliefs and mission", "pct": 67}, {"label": "Location", "pct": 66}, {"label": "Worship times", "pct": 64},
      {"label": "Ministries or events", "pct": 50}, {"label": "Sermons", "pct": 42}, {"label": "Contact information", "pct": 39},
      {"label": "Staff profiles", "pct": 33}, {"label": "Social media links", "pct": 26}
    ]
  }
};
