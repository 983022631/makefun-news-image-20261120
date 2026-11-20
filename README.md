# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/983022631/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/983022631/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-image front page summing up Friday 20 November 2026: Cyclone Akvan
bears down on India's east coast (300,000 evacuated), European leaders say
they are ready for Ukraine peace talks while Kushner says Russia is
"comfortable" with Article 5-style security guarantees, NASA confirms
Voyager 1 is the first craft a full light-day from Earth, Sensor Tower
estimates GTA VI sold 19 million copies worth $1.84 billion by launch day,
Trump posthumously pardons baseball's hits leader Pete Rose, and Cincinnati
Zoo's beloved hippo Fiona dies at 9. The image is drawn programmatically
with Python (PIL) in `draw.py` — masthead, headlines and six small drawn
illustrations, no AI-generated pictures — and `main.ts` copies it to the
entry point.

## Run it

```sh
python3 draw.py          # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources (all stories verified against reputable outlets)

- Cyclone Akvan: The Hindu ("Cyclone 'Akvan' updates: Three lakh
  evacuated, 423 rescue teams deployed", 20 Nov 2026); NDTV (39 trains
  cancelled, 28 rescheduled in Odisha); Mathrubhumi (landfall expected
  between Puri and Gopalpur on Friday afternoon).
- Ukraine peace talks: Al Jazeera ("Kushner says Russia 'comfortable' with
  NATO-like guarantees for Ukraine", 19 Nov 2026); AP via The Manila Times
  and Arab News (Berlin Coalition of the Willing summit, 19–20 Nov 2026);
  Sky News (Burnham: Europe "ready to enter negotiations", 19 Nov 2026).
- Voyager 1: Reuters ("NASA confirms Voyager 1 probe's 'light-day' distance
  milestone", 19 Nov 2026) — the probe passed 16 billion miles (26 billion
  km) on Wednesday 5:16 a.m. EST; NASA confirmed it on Thursday.
- GTA VI sales: Sensor Tower estimates as reported by Reuters / 80.lv /
  GameSpot (19 Nov 2026): 19.05 million copies, about $1.84 billion by
  launch day, net of returns; Take-Two has published no official figure.
- Pete Rose pardon: Reuters ("Trump pardons late baseball legend Pete Rose
  for tax crimes", 19 Nov 2026); ESPN (published 19 Nov 2026, 21:34 UTC);
  CNN — posthumous pardon over the 1990 tax conviction; 4,256 career hits;
  Hall of Fame vote not before December 2027.
- Fiona the hippo: AP / Reuters / CNN (19–20 Nov 2026) — the nine-year-old
  Nile hippo died at Cincinnati Zoo after swallowing a visitor's knit hat;
  vets' round-the-clock efforts failed.

---

<sub>Entered on [make.fun](https://make.fun/?ref=76bwm2a6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
