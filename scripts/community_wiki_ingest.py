#!/usr/bin/env python3
"""
community_wiki_ingest.py — 导入 Event 数据到社区

支持：
  - 单条 JSON 字符串录入
  - JSONL 文件批量导入
  - 自动更新 Person 的 event_refs

Usage:
    # 单条录入
    python community_wiki_ingest.py --community ./my-community --event '{"type":"activity",...}'

    # 批量导入
    python community_wiki_ingest.py --community ./my-community --events-file events.jsonl
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


def load_people(people_dir: str) -> dict:
    """Load all existing people into memory."""
    people = {}
    if not os.path.isdir(people_dir):
        return people
    for fname in os.listdir(people_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(people_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        people[data.get("id", fname[:-5])] = data
    return people


def save_person(people_dir: str, person_id: str, data: dict):
    """Save a person profile to disk."""
    fpath = os.path.join(people_dir, f"{person_id}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ensure_person(people: dict, people_dir: str, person_id: str) -> dict:
    """Ensure a person exists in the people dict."""
    if person_id not in people:
        people[person_id] = {
            "id": person_id,
            "profile": {},
            "skills": [],
            "interests": [],
            "links": {},
            "works_input": [],
            "event_refs": [],
            "external_inputs": [],
        }
        save_person(people_dir, person_id, people[person_id])
    return people[person_id]


def add_event_ref(person: dict, event_id: str, role: str, event_type: str, timestamp: int):
    """Add an event reference to a person's profile."""
    ref = {
        "event_id": event_id,
        "role": role,
        "type": event_type,
        "timestamp": timestamp,
    }
    person["event_refs"].append(ref)


def ingest_event(community_dir: str, event: dict) -> str:
    """Ingest a single event. Returns the event file path."""
    events_dir = os.path.join(community_dir, "events")
    people_dir = os.path.join(community_dir, "people")
    os.makedirs(events_dir, exist_ok=True)
    os.makedirs(people_dir, exist_ok=True)

    # Validate required fields
    if "id" not in event:
        event["id"] = f"evt_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
    if "timestamp" not in event:
        event["timestamp"] = int(datetime.now(timezone.utc).timestamp())

    # Save event
    event_path = os.path.join(events_dir, f"{event['id']}.json")
    with open(event_path, "w", encoding="utf-8") as f:
        json.dump(event, f, ensure_ascii=False, indent=2)

    # Update people
    people = load_people(people_dir)
    event_type = event.get("type", "activity")
    ts = event["timestamp"]

    # Initiator
    initiator_id = event.get("initiator")
    if initiator_id:
        p = ensure_person(people, people_dir, initiator_id)
        add_event_ref(p, event["id"], "initiator", event_type, ts)
        save_person(people_dir, initiator_id, p)

    # Co-creators
    for cid in event.get("co_creators", []):
        p = ensure_person(people, people_dir, cid)
        add_event_ref(p, event["id"], "co_creator", event_type, ts)
        save_person(people_dir, cid, p)

    # Participants
    for pid in event.get("participants", []):
        p = ensure_person(people, people_dir, pid)
        add_event_ref(p, event["id"], "participant", event_type, ts)
        save_person(people_dir, pid, p)

    # Append to log
    log_path = os.path.join(community_dir, "log.md")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n## [{datetime.now(timezone.utc).strftime('%Y-%m-%d')}] ingest | Event {event['id']}\n")
        f.write(f"- Type: {event_type}\n")
        f.write(f"- Initiator: {initiator_id}\n")
        f.write(f"- Co-creators: {', '.join(event.get('co_creators', []))}\n")
        f.write(f"- Participants: {', '.join(event.get('participants', []))}\n")

    return event_path


def main():
    parser = argparse.ArgumentParser(description="Ingest events into a Community AI-OS")
    parser.add_argument("--community", required=True, help="Community directory path")
    parser.add_argument("--event", help="Single event as JSON string")
    parser.add_argument("--events-file", help="Path to JSONL file with multiple events")
    args = parser.parse_args()

    if not args.event and not args.events_file:
        parser.error("Provide either --event or --events-file")

    count = 0
    if args.event:
        event = json.loads(args.event)
        path = ingest_event(args.community, event)
        print(f"Ingested: {path}")
        count += 1

    if args.events_file:
        with open(args.events_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                event = json.loads(line)
                path = ingest_event(args.community, event)
                print(f"Ingested: {path}")
                count += 1

    print(f"\nTotal events ingested: {count}")


if __name__ == "__main__":
    main()
