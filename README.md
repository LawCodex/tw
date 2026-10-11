# Taiwan (Republic of China) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

This repository contains the **Constitution of the Republic of China**, its **Additional Articles**
(增修條文) and **all laws (法律) and regulations (命令) currently in force** at central-government level,
as published in the **Laws & Regulations Database of the Republic of China (全國法規資料庫)**
operated by the Ministry of Justice, <https://law.moj.gov.tw>, together with the
**official English translations** published in the same database.

Retrieved: 2026-10-12 (database update stamp: 2026-10-02).

## Coverage

| | Traditional Chinese (`zh/`, authoritative) | English (`en/`, translation) |
|---|---:|---:|
| Constitution & constitutional instruments (`constitution/`) | 7 | 2 |
| Laws — 法律 (`laws/`) | 1,022 | 904 |
| Regulations — 命令 (`regulations/`) | 7,250 | 1,982 |
| **Total** | **8,279** | **2,888** |

`zh/constitution/` holds every in-force text whose 法規位階 (legal rank) is 憲法: A0000001 中華民國憲法,
A0000002 中華民國憲法增修條文, A0000003 憲法實施之準備程序, A0000004 訓政結束程序法,
A0000015 全國戒嚴令, A0000016 臺灣地區解嚴令, A0000017 宣告動員戡亂時期終止.

### By authority

The 法規類別 (category) of each text is "branch ＞ authority ＞ subject"; the first two levels
are used as the directory (mapped to an English slug), the full category is kept in the front matter.

| Authority (directory) | zh laws | zh regulations | en laws | en regulations |
|---|---:|---:|---:|---:|
| `central-bank` | 2 | 33 | 2 | 25 |
| `central-election-commission` | 2 | 55 | 2 | 1 |
| `civil-service-protection-and-training-commission` | 4 | 23 | 4 | 1 |
| `control-yuan` | 4 | 23 | 4 | 3 |
| `council-of-indigenous-peoples` | 12 | 49 | 12 | 2 |
| `directorate-general-of-budget-accounting-and-statistics` | 6 | 22 | 6 | 2 |
| `directorate-general-of-personnel-administration` | 11 | 25 | 11 | 7 |
| `disciplinary-court` | 0 | 3 | 0 | 0 |
| `examination-yuan` | 1 | 13 | 0 | 0 |
| `executive-yuan` | 16 | 24 | 13 | 2 |
| `fair-trade-commission` | 3 | 18 | 3 | 8 |
| `financial-supervisory-commission` | 33 | 358 | 32 | 260 |
| `hakka-affairs-council` | 4 | 24 | 4 | 1 |
| `ill-gotten-party-assets-settlement-committee` | 1 | 7 | 1 | 0 |
| `judicial-yuan` | 42 | 217 | 32 | 22 |
| `legislative-yuan` | 5 | 29 | 0 | 0 |
| `mainland-affairs-council` | 4 | 26 | 4 | 5 |
| `ministry-of-agriculture` | 60 | 552 | 57 | 110 |
| `ministry-of-civil-service` | 19 | 81 | 1 | 0 |
| `ministry-of-culture` | 32 | 214 | 32 | 22 |
| `ministry-of-digital-affairs` | 6 | 55 | 6 | 33 |
| `ministry-of-economic-affairs` | 80 | 604 | 64 | 147 |
| `ministry-of-education` | 59 | 448 | 59 | 43 |
| `ministry-of-environment` | 25 | 320 | 25 | 82 |
| `ministry-of-examination` | 6 | 111 | 3 | 2 |
| `ministry-of-finance` | 64 | 328 | 64 | 113 |
| `ministry-of-foreign-affairs` | 12 | 48 | 12 | 17 |
| `ministry-of-health-and-welfare` | 86 | 646 | 81 | 290 |
| `ministry-of-justice` | 64 | 275 | 64 | 75 |
| `ministry-of-labor` | 26 | 258 | 25 | 127 |
| `ministry-of-national-defense` | 49 | 193 | 44 | 31 |
| `ministry-of-sports` | 8 | 83 | 8 | 1 |
| `ministry-of-the-interior` | 111 | 779 | 109 | 144 |
| `ministry-of-transportation-and-communications` | 80 | 545 | 53 | 134 |
| `national-assembly` | 3 | 34 | 0 | 0 |
| `national-audit-office` | 4 | 38 | 4 | 1 |
| `national-communications-commission` | 7 | 145 | 7 | 107 |
| `national-development-council` | 10 | 37 | 9 | 19 |
| `national-palace-museum` | 1 | 8 | 1 | 1 |
| `national-science-and-technology-council` | 12 | 61 | 12 | 24 |
| `national-security-council` | 4 | 38 | 0 | 0 |
| `nuclear-safety-commission` | 13 | 84 | 9 | 33 |
| `ocean-affairs-council` | 11 | 83 | 11 | 25 |
| `office-of-the-president` | 6 | 35 | 1 | 2 |
| `overseas-community-affairs-council` | 2 | 14 | 2 | 4 |
| `personal-data-protection-commission-preparatory-office` | 1 | 4 | 1 | 1 |
| `public-construction-commission` | 6 | 66 | 5 | 41 |
| `taiwan-transportation-safety-board` | 2 | 8 | 2 | 6 |
| `veterans-affairs-council` | 3 | 106 | 3 | 8 |

### Not covered

- **Repealed texts** (records marked 廢止 in the database: 322 laws, 3,202 regulations, and 284 English
  translations of repealed texts) — only texts in force are published. 9 further English translations whose
  Chinese record is not in the in-force set were also skipped.
- **Attachments** (附件: forms, annexed tables and schedules distributed as PDF/ODT/DOC files) are not
  copied; each file links to them at the official URL under a 附件 / Attachments heading. Tables that the
  database embeds in the article text as box-drawing characters are kept, in fenced `text` blocks.
- Local government (municipal / county) self-governance ordinances, which are not part of this database.
- Administrative rules (行政規則), judicial interpretations / Constitutional Court judgments and court
  decisions.
- Article-by-article amendment history and legislative reasons; only the consolidated current text and the
  history summary (沿革) are included.

## Structure

```
zh/                                   Traditional Chinese (authoritative)
  constitution/<PCode>[-<slug>].md
  laws/<authority>/<PCode>[-<slug>].md
  regulations/<authority>/<PCode>[-<slug>].md
en/                                   English translations (same paths)
scripts/                              fetch + conversion code
```

- Filenames start with the database's **PCode** (e.g. `B0000001`), the stable official identifier of each
  text, followed by a slug of the official English title when one exists (e.g.
  `zh/laws/ministry-of-justice/B0000001-civil-code.md`, `en/laws/ministry-of-justice/B0000001-civil-code.md`).
  The same PCode/path is used in both languages.
- Divisions (編 / 章 / 節 / 款 / 目, Part / Chapter / Section ...) become Markdown headings; articles
  (第 N 條 / Article N) are headings at the next level, or **bold** labels when the hierarchy is deeper
  than six levels (e.g. the Civil Code).
- Front matter: `title`, `title_en` / `title_zh`, `identifier` (PCode), `type` (`constitution`, `act`,
  `regulation`), `law_level` (法規位階), `category` (法規類別), `date` (first promulgation, parsed from the
  history), `last_amended` (法規異動日期), `effective_date` / `effective_note` (生效日期 / 生效內容 when
  given), `status`, `source`, `retrieved`. English files carry `translation: true`.
- Each file ends with the history (沿革 / History) as given by the database.

## Source and licence

- Source: 全國法規資料庫 Laws & Regulations Database of the ROC (Taiwan), Ministry of Justice —
  open-data bulk downloads (JSON) at `https://law.moj.gov.tw/api/Ch/Law/JSON`, `.../api/Ch/Order/JSON`,
  `.../api/En/Law/JSON`, `.../api/En/Order/JSON` (listed on the database's 資料開放 page and on
  data.gov.tw).
- Statutes, regulations and official documents are not protected by copyright in Taiwan
  (Copyright Act art. 9, 著作權法第9條); the open data is released under the
  [Open Government Data License, version 1.0](https://data.gov.tw/license) (政府資料開放授權條款第1版).
- English texts are translations published for reference; in case of discrepancy the Chinese text prevails.
- This repository is an unofficial conversion. Check the official database for authoritative text.

## Regenerating

```sh
pip install -r scripts/requirements.txt
python3 scripts/tw_fetch.py   ../_raw/tw          # 4 ZIP files, ~48 MB, cached
python3 scripts/tw_convert.py ../_raw/tw .        # rewrites zh/ and en/
```

`tw_fetch.py` downloads only the four documented open-data archives (4 requests, 5 s apart, with a
ZIP integrity check). Note: law.moj.gov.tw's robots.txt disallows crawling the site apart from law pages;
the site was therefore **not crawled** — only the officially published open-data bulk endpoints were used.
