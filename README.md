# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/MUNYADINARUTO/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/MUNYADINARUTO/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper-style front page that sums up Thursday, 19 November 2026 in a
single 1024×1024 image: the first-ever Trump–Xi–Putin trilateral at the APEC
summit in Shenzhen, the World Court delivering its Rohingya genocide verdict
on Myanmar in The Hague, GTA VI launching worldwide after 13 years with a
record-tying 99 on Metacritic, NASA confirming Voyager 1 is one light-day
from Earth, and the US–Iran war widening across the Gulf — plus a ticker
with the EU's €45bn Ukraine loan, Australia's sanctions on Israeli settlers
and Israeli forces pushing into central Gaza.

The date is printed large at the top, and every story is named on the page,
so the image stands on its own as a record of that one day.

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, < 1 MiB)
```

`main.py` deterministically writes the finished image to `/output/entry.png`
(a byte-for-byte copy of the bundled `entry.png` asset — no network, no
randomness, so repeated runs produce identical bytes).

The front page itself (`build_frontpage.py`) composes AI-generated news
photography from `assets/` with crisp PIL typography into the 1024×1024
layout.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6fdjfyxs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
