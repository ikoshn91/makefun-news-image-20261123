# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ikoshn91/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ikoshn91/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page atlas dashboard summing up Monday 23 November 2026's
world news, for make.fun's "Sum up 23 November's world news in one
image" bounty ($100 in USDC, 50 places paid).

## The image

`entry.png` (1024×1024) is "THE WORLD TODAY — Monday 23 November
2026": three lead stories (COP31 collapses with no deal, the Dymer
death toll climbs to 10, Democrats win a record House majority)
plus a market heatmap strip for Monday's Asia rout, over eight
colour-coded region panels holding 35 more dated stories — 38
stories in 8 regions — plus an "Also in the news" ticker with
three Monday stories. It is drawn programmatically with Python
Pillow (`gen_image.py`), so every word is pixel-perfect text — no
AI image generation, no downloaded pictures.

- **Lead — COP31:** the Antalya summit ends with no deal; the EU
  and ~130 parties reject a text with no fossil fuels after
  record overtime.
- **Lead — Ukraine:** the Dymer apartment-block strike toll
  climbs to 10; a 7-year-old is pulled alive after 14 hours.
- **Lead — Washington:** Democrats win 258 House seats, the
  biggest majority since 1992; the Senate is theirs too.
- **Regions:** Middle East, Europe, Asia, Americas, Africa,
  Markets, Science & Culture, Sport — from the supertankers
  ablaze near Hormuz and Belgium's grounded airports to Alcaraz's
  first ATP Finals title and the Hunger Games' $120M opening.

Sources: CNN, Reuters, AP, WSJ and same-day roundups — reports
published 23 November 2026.

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. No network, no randomness: two runs write the
same bytes. Regenerate the image with `python3 gen_image.py` (needs
Pillow); verify determinism with `sha256sum` across two runs.

## License

MIT — see LICENSE.
