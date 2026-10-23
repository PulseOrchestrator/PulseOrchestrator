"""Writes redirect pages for the addresses of the former versioned docs.

The docs used to live under /latest/, /dev/ and one folder per release
(/1.0.0/, /1.0.0-beta.1/, ...). Those pages are now under /pulse-1/. For
every page there, this writes the same path under each old folder as a
small page that redirects to the new address, so existing links keep
working. Run after `zensical build`: python scripts/redirects.py site
"""

import sys
from pathlib import Path

OLD_FOLDERS = ["latest", "dev", "1.0.0"] + [f"1.0.0-beta.{n}" for n in range(1, 7)]
TARGET = "pulse-1"
BASE = "/PulseOrchestrator/"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirecting</title>
<link rel="canonical" href="{url}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}">
</head>
<body><a href="{url}">This page has moved to {url}</a></body>
</html>
"""


def main(site: Path) -> int:
    target = site / TARGET
    pages = sorted(path.parent.relative_to(target) for path in target.rglob("index.html"))
    if not pages:
        print(f"no pages under {target}; build the site first", file=sys.stderr)
        return 1
    written = 0
    for folder in OLD_FOLDERS:
        for page in pages:
            relative = "" if page == Path(".") else f"{page.as_posix()}/"
            out = site / folder / page / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(PAGE.format(url=f"{BASE}{TARGET}/{relative}"), encoding="utf-8")
            written += 1
    print(f"wrote {written} redirects for {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "site")))
