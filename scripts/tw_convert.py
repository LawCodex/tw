#!/usr/bin/env python3
"""Convert the law.moj.gov.tw open-data JSON dumps (see tw_fetch.py) to Markdown.

Usage: tw_convert.py [RAW_DIR] [REPO_DIR]

Only texts in force are written (records carrying a 廢止註記 / abandon note are skipped).
Output layout (per language zh/ and en/):
  constitution/<PCode>-<slug>.md
  laws/<category>/<PCode>-<slug>.md          (法規位階 = 法律)
  regulations/<category>/<PCode>-<slug>.md   (法規位階 = 命令)
<category> is derived from the 法規類別 (branch > authority) and mapped to an English slug.
"""
import datetime
import json
import os
import re
import shutil
import sys
import zipfile

RETRIEVED = datetime.date.today().isoformat()

# 法規類別 first two levels -> directory slug
CATEGORY = {
    "憲法": "constitution",
    "總統＞總統府": "office-of-the-president",
    "總統＞國家安全會議": "national-security-council",
    "國民大會（憲法國民大會章條文已停止適用）": "national-assembly",
    "立法": "legislative-yuan",
    "司法＞院本部": "judicial-yuan",
    "司法＞懲戒法院": "disciplinary-court",
    "考試＞院本部": "examination-yuan",
    "考試＞考選部": "ministry-of-examination",
    "考試＞銓敘部": "ministry-of-civil-service",
    "考試＞公務人員保障暨培訓委員會": "civil-service-protection-and-training-commission",
    "監察＞院本部": "control-yuan",
    "監察＞審計部": "national-audit-office",
    "行政＞院本部": "executive-yuan",
    "行政＞不當黨產處理委員會": "ill-gotten-party-assets-settlement-committee",
    "行政＞中央選舉委員會": "central-election-commission",
    "行政＞中央銀行": "central-bank",
    "行政＞交通部": "ministry-of-transportation-and-communications",
    "行政＞個人資料保護委員會籌備處": "personal-data-protection-commission-preparatory-office",
    "行政＞僑務委員會": "overseas-community-affairs-council",
    "行政＞內政部": "ministry-of-the-interior",
    "行政＞公平交易委員會": "fair-trade-commission",
    "行政＞勞動部": "ministry-of-labor",
    "行政＞原住民族委員會": "council-of-indigenous-peoples",
    "行政＞國家發展委員會": "national-development-council",
    "行政＞國家科學及技術委員會": "national-science-and-technology-council",
    "行政＞國家通訊傳播委員會": "national-communications-commission",
    "行政＞國家運輸安全調查委員會": "taiwan-transportation-safety-board",
    "行政＞國立故宮博物院": "national-palace-museum",
    "行政＞國軍退除役官兵輔導委員會": "veterans-affairs-council",
    "行政＞國防部": "ministry-of-national-defense",
    "行政＞外交部": "ministry-of-foreign-affairs",
    "行政＞大陸委員會": "mainland-affairs-council",
    "行政＞客家委員會": "hakka-affairs-council",
    "行政＞教育部": "ministry-of-education",
    "行政＞數位發展部": "ministry-of-digital-affairs",
    "行政＞文化部": "ministry-of-culture",
    "行政＞核能安全委員會": "nuclear-safety-commission",
    "行政＞法務部": "ministry-of-justice",
    "行政＞海洋委員會": "ocean-affairs-council",
    "行政＞環境部": "ministry-of-environment",
    "行政＞經濟部": "ministry-of-economic-affairs",
    "行政＞行政院主計總處": "directorate-general-of-budget-accounting-and-statistics",
    "行政＞行政院人事行政總處": "directorate-general-of-personnel-administration",
    "行政＞行政院公共工程委員會": "public-construction-commission",
    "行政＞衛生福利部": "ministry-of-health-and-welfare",
    "行政＞財政部": "ministry-of-finance",
    "行政＞農業部": "ministry-of-agriculture",
    "行政＞運動部": "ministry-of-sports",
    "行政＞金融監督管理委員會": "financial-supervisory-commission",
}

CN_DIGITS = {"零": 0, "〇": 0, "○": 0, "Ｏ": 0, "一": 1, "二": 2, "三": 3, "四": 4,
             "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2int(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    if not s or any(ch not in CN_DIGITS and ch not in "十百" for ch in s):
        return None
    if "十" not in s and "百" not in s:  # positional, e.g. 一○二
        return int("".join(str(CN_DIGITS[c]) for c in s))
    total, cur = 0, 0
    for ch in s:
        if ch in CN_DIGITS:
            cur = CN_DIGITS[ch]
        elif ch == "百":
            total += (cur or 1) * 100
            cur = 0
        elif ch == "十":
            total += (cur or 1) * 10
            cur = 0
    return total + cur


def roc_date(text):
    m = re.search(r"中華民國\s*([〇○Ｏ零一二三四五六七八九十百\d]+)\s*年\s*([〇○零一二三四五六七八九十\d]+)\s*月"
                  r"\s*([〇○零一二三四五六七八九十\d]+)\s*日", text or "")
    if not m:
        return None
    y, mo, d = (cn2int(g) for g in m.groups())
    try:
        return datetime.date(y + 1911, mo, d).isoformat()
    except (TypeError, ValueError):
        return None


def ymd(s):
    s = (s or "").strip()
    if re.fullmatch(r"\d{8}", s) and not s.startswith("9999"):
        try:
            return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:])).isoformat()
        except ValueError:
            return None
    return None


def slugify(s, maxlen=80):
    s = (s or "").lower()
    s = re.sub(r"[’'`]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0]
    return s


def yq(v):
    return json.dumps(v, ensure_ascii=False)


def pcode_of(url):
    m = re.search(r"pcode=([A-Za-z0-9]+)", url)
    return m.group(1)


BOX = re.compile(r"[─━│┃┌┐└┘├┤┬┴┼┏┓┗┛┣┫┳┻╋═║╔╗╚╝╠╣╦╩╬]")


def esc_line(line):
    line = re.sub(r"<(?=[A-Za-z/!?])", "&lt;", line)
    if re.match(r"[#>+*\-=]|\d+[.)]\s", line):
        line = "\\" + line
    return line


def body(text):
    """Article / foreword text -> Markdown paragraphs; box-drawn tables fenced."""
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n").rstrip()
    if not text.strip():
        return ""
    lines = text.split("\n")
    out, block = [], []

    def flush():
        if block:
            out.append("```text\n" + "\n".join(block) + "\n```")
            block.clear()

    for ln in lines:
        if BOX.search(ln):
            block.append(ln.rstrip())
            continue
        flush()
        s = ln.strip(" \t")
        if s:
            out.append(esc_line(s))
    flush()
    return "\n\n".join(out)


def rewrap_zh(text):
    """Chinese forewords are hard-wrapped at a fixed width: rejoin wrapped lines."""
    lines = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    for ln in lines:
        s = ln.strip(" \t\u3000")
        if out and out[-1] and not re.search(r"[。：；！？」』）:]$", out[-1]) and s and not BOX.search(ln):
            out[-1] += s
        else:
            out.append(s)
    return "\n".join(out)


def one_line(text):
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\s*\n\s*(?=\d+\.)", " ", text)
    text = re.sub(r"\s*\n\s*", "", text)
    return re.sub(r"[ \t]{2,}", " ", text)


def heading_text(s):
    return re.sub(r"\s+", " ", (s or "").replace("　", " ")).strip()


def render_articles(arts, p):
    """arts: list of article dicts; p: key prefix ('' or 'Eng')."""
    divs = sorted({len(a[p + "ArticleContent"]) - len(a[p + "ArticleContent"].lstrip(" "))
                   for a in arts if a[p + "ArticleType"] == "C"})
    rank = {lead: i for i, lead in enumerate(divs)}
    art_level = 2 + len(divs)
    out = []
    for a in arts:
        t = a[p + "ArticleType"]
        c = a[p + "ArticleContent"]
        if t == "C":
            lead = len(c) - len(c.lstrip(" "))
            lvl = min(6, 2 + rank[lead])
            out.append("#" * lvl + " " + heading_text(c))
        else:
            no = heading_text(a[p + "ArticleNo"])
            if no:
                out.append(("#" * art_level + " " + no) if art_level <= 6 else "**" + no + "**")
            b = body(c)
            if b:
                out.append(b)
    return "\n\n".join(out)


def attachments(items, label):
    if not items:
        return ""
    lines = ["## " + label, ""]
    for it in items:
        name = (it.get("FileName") or "").replace("[", "\\[").replace("]", "\\]")
        lines.append("- [%s](%s)" % (name, it.get("FileURL")))
    return "\n".join(lines)


PLAIN = ("type", "jurisdiction", "language", "status")


def front(meta):
    out = ["---"]
    for k, v in meta.items():
        if v is None or v == "":
            continue
        if isinstance(v, bool):
            v = "true" if v else "false"
        elif not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) or k in PLAIN):
            v = yq(v)
        out.append("%s: %s" % (k, v))
    out.append("---")
    return "\n".join(out)


def load(zpath, member):
    with zipfile.ZipFile(zpath) as z:
        return json.loads(z.read(member).decode("utf-8-sig"))["Laws"]


def placement(rec_level, category, pcode, eng_name):
    parts = category.split("＞")
    key2 = "＞".join(parts[:2])
    if rec_level == "憲法":
        kind, cat = "constitution", None
    else:
        kind = "laws" if rec_level == "法律" else "regulations"
        cat = CATEGORY.get(key2) or CATEGORY.get(parts[0])
        if cat is None:
            print("WARN unmapped category", category, pcode, file=sys.stderr)
            cat = "other"
    slug = slugify(eng_name)
    fname = pcode + ("-" + slug if slug else "") + ".md"
    return "/".join(x for x in (kind, cat, fname) if x)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    raw = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..", "_raw", "tw")
    repo = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "..")
    zh = load(os.path.join(raw, "Ch_Law.zip"), "ChLaw.json") + \
        load(os.path.join(raw, "Ch_Order.zip"), "ChOrder.json")
    en = load(os.path.join(raw, "En_Law.zip"), "EnLaw.json") + \
        load(os.path.join(raw, "En_Order.zip"), "EnOrder.json")

    for lang in ("zh", "en"):
        shutil.rmtree(os.path.join(repo, lang), ignore_errors=True)

    zh_by = {}
    counts = {}
    for r in zh:
        if r["LawAbandonNote"].strip():
            continue
        pc = pcode_of(r["LawURL"])
        assert pc not in zh_by, pc
        rel = placement(r["LawLevel"], r["LawCategory"], pc, r["EngLawName"])
        zh_by[pc] = (r, rel)
        typ = {"憲法": "constitution", "法律": "act", "命令": "regulation"}[r["LawLevel"]]
        meta = {
            "title": r["LawName"].strip(),
            "title_en": r["EngLawName"].strip(),
            "identifier": pc,
            "type": typ,
            "law_level": r["LawLevel"],
            "category": r["LawCategory"],
            "jurisdiction": "tw",
            "language": "zh-Hant",
            "date": roc_date(r["LawHistories"]),
            "last_amended": ymd(r["LawModifiedDate"]),
            "effective_date": ymd(r["LawEffectiveDate"]),
            "effective_note": one_line(r["LawEffectiveNote"]),
            "status": "in_force",
            "source": r["LawURL"],
            "retrieved": RETRIEVED,
        }
        parts = [front(meta), "", "# " + r["LawName"].strip()]
        fw = body(rewrap_zh(r["LawForeword"]))
        if fw:
            parts += ["", "## 前言", "", fw]
        arts = render_articles(r["LawArticles"], "")
        if arts:
            parts += ["", arts]
        att = attachments(r["LawAttachements"], "附件")
        if att:
            parts += ["", att]
        hist = body(r["LawHistories"])
        if hist:
            parts += ["", "## 沿革", "", hist]
        write(repo, "zh", rel, "\n".join(parts))
        counts[("zh", rel.split("/")[0])] = counts.get(("zh", rel.split("/")[0]), 0) + 1

    en_skipped = 0
    for r in en:
        pc = pcode_of(r["EngLawURL"])
        if r["EngLawAbandonNote"].strip() or pc not in zh_by:
            en_skipped += 1
            continue
        zr, rel = zh_by[pc]
        typ = {"憲法": "constitution", "法律": "act", "命令": "regulation"}[zr["LawLevel"]]
        meta = {
            "title": r["EngLawName"].strip(),
            "title_zh": r["LawName"].strip(),
            "identifier": pc,
            "type": typ,
            "law_level": zr["LawLevel"],
            "category": zr["LawCategory"],
            "jurisdiction": "tw",
            "language": "en",
            "translation": True,
            "translation_note": "English translation published by the Ministry of Justice for reference; "
                                "the Chinese text is the authoritative version.",
            "date": roc_date(zr["LawHistories"]),
            "last_amended": ymd(r["EngLawModifiedDate"]),
            "status": "in_force",
            "source": r["EngLawURL"],
            "retrieved": RETRIEVED,
        }
        parts = [front(meta), "", "# " + r["EngLawName"].strip(), "",
                 "> Translation. The Chinese text ([zh/%s](%szh/%s)) is authoritative." % (
                     rel, "../" * (rel.count("/") + 1), rel)]
        fw = body(r["EngLawForeword"])
        if fw:
            parts += ["", "## Preamble", "", fw]
        arts = render_articles(r["EngLawArticles"], "Eng")
        if arts:
            parts += ["", arts]
        att = attachments(r["EngLawAttachements"], "Attachments")
        if att:
            parts += ["", att]
        hist = body(r["EngLawHistories"])
        if hist:
            parts += ["", "## History", "", hist]
        write(repo, "en", rel, "\n".join(parts))
        counts[("en", rel.split("/")[0])] = counts.get(("en", rel.split("/")[0]), 0) + 1

    for k in sorted(counts):
        print(k, counts[k])
    print("en skipped (repealed or no in-force Chinese record):", en_skipped)


def write(repo, lang, rel, text):
    path = os.path.join(repo, lang, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text.rstrip() + "\n")


if __name__ == "__main__":
    main()
