#!/usr/bin/env python3
"""
community_wiki_init.py — 初始化 Community AI-OS 社区目录结构

Usage:
    python community_wiki_init.py --name "我的社区" --values "共在,涌现,逍遥" --output ./my-community
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


def init_community(name: str, values: list[str], output_dir: str, founders: list[str] | None = None):
    """Initialize a new community directory with all required structure."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "events"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "people"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "state"), exist_ok=True)

    community = {
        "id": name.lower().replace(" ", "-").replace("_", "-"),
        "name": name,
        "values": values,
        "manifesto": "",
        "tags": [],
        "founders": founders or [],
        "admins": founders or [],
        "treasury": {"currency": "", "balance": 0.0, "policy": ""},
        "links": {},
        "created_at": int(datetime.now(timezone.utc).timestamp()),
    }

    community_path = os.path.join(output_dir, "community.json")
    with open(community_path, "w", encoding="utf-8") as f:
        json.dump(community, f, ensure_ascii=False, indent=2)

    log_path = os.path.join(output_dir, "log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("# Community Log\n\n")
        f.write("> Chronological record of all community actions. Append-only.\n\n"
        )
        f.write(f"## [{datetime.now(timezone.utc).strftime('%Y-%m-%d')}] create | Community initialized\n")
        f.write(f"- Name: {name}\n")
        f.write(f"- Values: {', '.join(values)}\n")
        f.write(f"- Founders: {', '.join(founders or [])}\n")

    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write("Community AI-OS data directory.\n\n")
        f.write("## Structure\n\n")
        f.write("- `community.json` — Community metadata\n")
        f.write("- `events/` — Event raw data (唯一事实源)\n")
        f.write("- `people/` — Person profiles with event_refs\n")
        f.write("- `state/` — Computed graph & community state\n")
        f.write("- `log.md` — Operation log\n")

    print(f"Community initialized at: {output_dir}")
    print(f"  - community.json")
    print(f"  - events/")
    print(f"  - people/")
    print(f"  - state/")
    print(f"  - log.md")
    return community_path


def main():
    parser = argparse.ArgumentParser(description="Initialize a Community AI-OS community")
    parser.add_argument("--name", required=True, help="Community name")
    parser.add_argument("--values", default="共在,涌现,逍遥", help="Comma-separated community values")
    parser.add_argument("--founders", default="", help="Comma-separated founder names")
    parser.add_argument("--output", default="./my-community", help="Output directory")
    args = parser.parse_args()

    values = [v.strip() for v in args.values.split(",") if v.strip()]
    founders = [f.strip() for f in args.founders.split(",") if f.strip()] if args.founders else []

    init_community(args.name, values, args.output, founders)


if __name__ == "__main__":
    main()
