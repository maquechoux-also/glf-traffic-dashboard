# GLF website report

Public one-page traffic report for Grace Life Fellowship elders and staff. Echo Tango maintains it. Plain HTML and JS, no build step.

## Deploy
- GitHub Pages, published by the `Deploy site` workflow on every push to `main`: https://maquechoux-also.github.io/glf-traffic-dashboard/
- Only `index.html`, `data.js`, `benchmarks.js` and `assets/` are published to the site. Everything in the repo is still public on github.com.
- **A merge or push to main is a live deploy. Ask before every merge.** The one exception is the scheduled `Monthly update` job, which commits `data.js` and publishes by itself.
- The repo is public on purpose (free Pages). Everything in it, branches included, is public.

## Rules
- Totals only. No names, emails, phone numbers, form entries or anything else about a person, in any file or commit.
- No secrets in the repo: the Google key and the GA4 property ID live in GitHub Actions secrets. Never print or commit them.
- Never guess a number. GLF figures come from `scripts/pull_data.py` or a dated manual read; every baseline in `benchmarks.js` names its source, year, sample and the group it describes.
- The page is `noindex`. Keep it that way. That hides only the page from search engines; the repo and its data files are public.
- Search terms are published only when every word is in `SAFE_WORDS` in `scripts/pull_data.py`, so a search that names a person never reaches the page. Add words to that list with care.
- Plain words: elders and staff read this, not analysts.

## Git
- Every change goes on a branch and lands by pull request, like `email-editor`. Pushing a branch and opening a PR needs no ask; merging does.
- Tracking setup, the measurement plan and the written monthly report are kept privately, not here.

## Checks
- `node -e "global.window={};require('./data.js');require('./benchmarks.js')"`
- `python3 -m py_compile scripts/pull_data.py`
- Open `index.html` in a browser at desktop and phone width.
