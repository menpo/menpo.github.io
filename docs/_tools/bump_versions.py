"""Move docs/versions.txt to the latest release of each Menpo package on PyPI.

versions.txt pins the exact releases the site is built and tested against (``menpo==0.13.0``).
The ``releases`` workflow runs this daily; when a pin moves it opens a pull request whose build
executes every code sample against the new release. A failing build means the release broke a
sample, and the failing page is what to fix.

    python docs/_tools/bump_versions.py            # rewrite versions.txt, print what changed
    python docs/_tools/bump_versions.py --check    # only print, exit 1 if something is behind
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

from packaging.version import InvalidVersion, Version

VERSIONS = Path(__file__).resolve().parents[1] / "versions.txt"
PIN = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>\S+)\s*$")


def latest_release(name):
    """The newest final (not pre-release, not yanked) version on PyPI."""
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=30) as response:
        releases = json.load(response)["releases"]
    final = []
    for text, files in releases.items():
        try:
            version = Version(text)
        except InvalidVersion:
            continue
        if not version.is_prerelease and not version.is_devrelease and files and not all(f.get("yanked") for f in files):
            final.append(version)
    return max(final)


def main(argv):
    if not VERSIONS.exists():
        print("docs/versions.txt does not exist: the site is still built from development branches.")
        return 0
    lines, changes = [], []
    for line in VERSIONS.read_text().splitlines():
        match = PIN.match(line)
        if match:
            newest = latest_release(match["name"])
            if newest > Version(match["version"]):
                changes.append(f"{match['name']} {match['version']} -> {newest}")
                line = f"{match['name']}=={newest}"
        lines.append(line)
    print("\n".join(changes) if changes else "all pins are up to date")
    if changes and "--check" not in argv:
        VERSIONS.write_text("\n".join(lines) + "\n")
    return 1 if changes and "--check" in argv else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
