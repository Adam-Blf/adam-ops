#!/usr/bin/env python3
"""Audit typographique quotidien des repos Adam-Blf.

Echoue (exit 1) si un README ou une description de repo public contient
un tiret cadratin, demi-cadratin, mediopoint ou puce.
Stdlib uniquement, tourne en GitHub Actions avec GITHUB_TOKEN.
"""
import base64
import json
import os
import re
import sys
import urllib.request

OWNER = "Adam-Blf"
BANNED = re.compile("[—–·•]")


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", OWNER)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    offenders = []
    page = 1
    while True:
        repos = api(f"/users/{OWNER}/repos?per_page=100&page={page}")
        if not repos:
            break
        for repo in repos:
            if repo.get("fork"):
                continue
            name = repo["name"]
            desc = repo.get("description") or ""
            if BANNED.search(desc):
                offenders.append(f"{name}: description")
            try:
                readme = api(f"/repos/{OWNER}/{name}/readme")
                content = base64.b64decode(readme["content"]).decode("utf-8")
                for i, line in enumerate(content.splitlines(), 1):
                    if BANNED.search(line):
                        offenders.append(f"{name}: README.md ligne {i}")
                        break
            except Exception:
                pass
        if len(repos) < 100:
            break
        page += 1

    if offenders:
        print("Caracteres typographiques interdits detectes :")
        for o in offenders:
            print(" -", o)
        return 1
    print("Audit typo OK, aucun caractere interdit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
