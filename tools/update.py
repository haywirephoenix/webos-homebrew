#!/usr/bin/env python3
"""Rebuild apps.json, the Homebrew Channel repository, from each app's latest GitHub release.

Each app's release carries <id>.manifest.json, written by that app's build. Run this after
publishing a release, then commit apps.json. Needs Python 3 and curl.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = "https://haywirephoenix.github.io/webos-homebrew/"
APPS = [
    # (app id, source repository, description page, short description)
    ("com.haywire.localvoice", "haywirephoenix/webos-localvoice", "localvoice.html",
     "Speech recognition that runs on the TV, for the remote's microphone button and apps with their own"),
    ("com.homebrew.tailscalectl", "haywirephoenix/webos-tailscale", "tailscale.html",
     "Install, update and run Tailscale on the TV, with a status page and console. Not affiliated with Tailscale Inc."),
]


def latest(app, repo):
    """The manifest URL of the latest release, with the version in it, and the manifest."""
    release = get("https://api.github.com/repos/%s/releases/latest" % repo)
    url = "https://github.com/%s/releases/download/%s/%s.manifest.json" % (repo, release["tag_name"], app)
    return url, get(url)


def get(url):
    return json.loads(subprocess.run(["curl", "-fsSL", "-A", "webos-homebrew", url], check=True,
                                     stdout=subprocess.PIPE).stdout)


def main():
    packages = []
    for app, repo, page, summary in APPS:
        url, manifest = latest(app, repo)
        assert manifest["id"] == app, url
        packages.append({"id": app, "title": manifest["title"], "iconUri": manifest["iconUri"],
                         "shortDescription": summary, "pool": "main",
                         "fullDescriptionUrl": PAGES + "descriptions/" + page,
                         "manifestUrl": url, "manifest": manifest})
        print("%s %s" % (app, manifest["version"]))
    n = len(packages)
    repo = {"paging": {"page": 1, "count": n, "maxPage": 1, "itemsTotal": n, "itemsPerPage": n}, "packages": packages}
    (ROOT / "apps.json").write_bytes((json.dumps(repo, indent=2) + "\n").encode())


if __name__ == "__main__":
    main()
