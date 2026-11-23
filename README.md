# THE WORLD TODAY — Monday 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ikoshn91/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ikoshn91/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page atlas dashboard summing up the world's news of **Monday 23
November 2026** — 38 dated stories across 8 regions, drawn as a newspaper
front page. The three leads are the COP31 collapse in Antalya with no
deal, the Dymer apartment-block death toll climbing to 10, and the
Democrats winning a record House majority of 258 seats. Below them a
market heatmap strip carries Monday's AI sell-off (Nikkei −5.06%), and
eight colour-coded region panels cover the Middle East, Europe, Asia, the
Americas, Africa, markets, science and sport — from two tankers ablaze
near Hormuz and the Belgium airport shutdown to Alcaraz's first ATP
Finals title and the Hunger Games' $120M opening. A ticker bar at the
bottom carries three more Monday stories.

This is an entry for make.fun's
[news-image-20261123](https://make.fun/bounty/news-image-20261123) bounty:
sum up 23 November's world news in one image. $100 in USDC, 50 places
paid. An AI judge compares entries two at a time and picks the one that
best sums up its day's news.

## How it works

- `gen_image.py` draws `entry.png` (1024×1024) with Pillow and the
  system DejaVu fonts. Every headline and body is measured with the real
  font metrics before it is drawn, and the program stops with a clear
  error if any text would overflow its card or panel — so the image you
  see is exactly the image the program guarantees.
- `main.ts` (Node 22, standard library only) copies `entry.png` into
  the output directory named by `MAKEFUN_OUTPUT_DIR` (default
  `/output`), refusing if the image is over the 1 MiB cap.
- No downloaded images, no AI image generation, no network: every word
  is real text rendered by the program, and two runs produce
  byte-identical files.

## Run it

```sh
python3 gen_image.py   # writes entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```
