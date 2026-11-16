# GLF website report

A one-page report on gracelifefellowship.org traffic for Grace Life Fellowship elders and staff, with published baselines beside each number.

Live: https://maquechoux-also.github.io/glf-traffic-dashboard/

## Files
| File | What it is |
|---|---|
| `index.html` | The page. It only draws what the two data files hold. |
| `data.js` | Grace Life's numbers for one period. Written by `scripts/pull_data.py`. |
| `benchmarks.js` | The published baselines, each with its source and the group it describes. Edited by hand. |
| `scripts/pull_data.py` | Read-only pull from Google Analytics (GA4) and Search Console. |
| `.github/workflows/monthly-update.yml` | Runs the pull on the 4th of each month and commits `data.js`. |
| `.github/workflows/deploy.yml` | Publishes the page and its two data files to GitHub Pages on every push to `main`. |

## Monthly update
The scheduled job needs two repository secrets (Settings → Secrets and variables → Actions):
- `GA4_PROPERTY_ID`: the property's ID, digits only.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: the full contents of a Google service-account key that has Viewer access on the GA4 property and Restricted access on the Search Console property.

Creating the service account is a one-time job done by a person signed in to Google; Echo Tango keeps the steps privately. Until the secrets exist the job fails with a message starting `STOP:` and the page keeps its last numbers.

GitHub switches off scheduled jobs in a public repo after 60 days with no activity. If a month is missed, re-enable the workflow under Actions and run it by hand.

Search terms are listed on the page only when every word is on the safe list in `scripts/pull_data.py`, so a search that names a person is never published.

To run it by hand: Actions → Monthly update → Run workflow.

Locally:
```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
GA4_PROPERTY_ID=... GOOGLE_SERVICE_ACCOUNT_JSON="$(cat /path/to/key.json)" .venv/bin/python scripts/pull_data.py --check
```

## Baselines
No published study measures ordinary-week traffic for local church websites. Each row in `benchmarks.js` therefore names the nearest group with real data (small nonprofits, churches on Easter weekend, all industries). Add a figure only with a source you opened, the year, the sample and the group it describes. Unsourced "church statistics" from vendor blogs stay out.

## Checks
```
node -e "global.window={};require('./data.js');require('./benchmarks.js')"
python3 -m py_compile scripts/pull_data.py
```
Then open `index.html` in a browser.
