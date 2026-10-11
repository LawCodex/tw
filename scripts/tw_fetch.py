#!/usr/bin/env python3
"""Download the official open-data bulk files of the Laws & Regulations Database
of the Republic of China (Taiwan), https://law.moj.gov.tw (Open Government Data License).

Four ZIP archives (JSON) are fetched:
  Ch/Law    - Chinese laws (法律) incl. the Constitution
  Ch/Order  - Chinese regulations (命令)
  En/Law    - English translations of laws
  En/Order  - English translations of regulations

Usage: tw_fetch.py [RAW_DIR]   (default: ../../_raw/tw relative to this script)
"""
import os
import sys
import time
import zipfile

import requests

UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
BASE = "https://law.moj.gov.tw/api/{}/JSON"
DATASETS = ["Ch/Law", "Ch/Order", "En/Law", "En/Order"]


def fetch(url, dest, tries=5):
    for i in range(tries):
        try:
            with requests.get(url, headers={"User-Agent": UA}, stream=True, timeout=300) as r:
                r.raise_for_status()
                tmp = dest + ".part"
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(1 << 20):
                        fh.write(chunk)
            with zipfile.ZipFile(tmp) as z:  # integrity check
                bad = z.testzip()
                if bad:
                    raise IOError("corrupt member %s" % bad)
            os.replace(tmp, dest)
            return
        except Exception as e:  # noqa: BLE001
            print("  attempt %d failed: %s" % (i + 1, e), file=sys.stderr)
            time.sleep(10 * (i + 1))
    raise SystemExit("giving up on " + url)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    raw = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..", "_raw", "tw")
    os.makedirs(raw, exist_ok=True)
    for ds in DATASETS:
        dest = os.path.join(raw, ds.replace("/", "_") + ".zip")
        if os.path.exists(dest):
            print("cached", dest)
            continue
        print("fetching", ds)
        fetch(BASE.format(ds), dest)
        time.sleep(5)


if __name__ == "__main__":
    main()
