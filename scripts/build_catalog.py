#!/usr/bin/env python3
"""
Awesome Linux Commands — Metadata Catalog Builder & Validator
Parses markdown command modules in `commands/`, validates metadata tags,
and compiles `metadata.json` for the companion web application.
"""

import sys
import glob
import re
import json
from pathlib import Path

METADATA_REGEX = re.compile(r'<!--\s*@([a-zA-Z0-9_\-]+):\s*(.*?)\s*-->')

def parse_markdown_module(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by level-3 headings (###)
    sections = re.split(r'\n(?=###\s+)', content)
    entries = []

    for section in sections:
        if not section.strip().startswith('###'):
            continue

        lines = section.strip().split('\n')
        title_line = lines[0].replace('###', '').strip()

        # Clean title (e.g. "1. `eza` — Modern, Colorful...")
        clean_title = re.sub(r'^\d+\.\s*', '', title_line)

        # Extract metadata comments
        metadata = {}
        for match in METADATA_REGEX.finditer(section):
            key = match.group(1).lower()
            val = match.group(2).strip()
            metadata[key] = val

        if not metadata.get('id'):
            continue

        # Extract command block
        code_match = re.search(r'```(?:bash|sh)\n([\s\S]*?)```', section)
        command_code = code_match.group(1).strip() if code_match else ""

        # Extract description (text before code block, excluding title and metadata)
        desc_lines = []
        for line in lines[1:]:
            if line.strip().startswith('```'):
                break
            if not line.strip().startswith('<!--') and line.strip():
                desc_lines.append(line.strip())
        description = " ".join(desc_lines)

        # Extract tags
        tags = [t.strip() for t in metadata.get('tags', '').split(',') if t.strip()]

        entries.append({
            "id": metadata.get('id'),
            "name": metadata.get('name', clean_title.split('—')[0].strip(' `')),
            "title": clean_title,
            "category": metadata.get('category', 'General'),
            "risk": metadata.get('risk', 'Safe'),
            "privilege": metadata.get('privilege', 'Normal'),
            "replaces": metadata.get('replaces', None),
            "command": command_code,
            "description": description,
            "tags": tags,
            "source_file": Path(filepath).as_posix()
        })

    return entries

def main():
    repo_root = Path(__file__).resolve().parent.parent
    command_dir = repo_root / "commands"
    output_json = repo_root / "metadata.json"

    files = sorted(glob.glob(f"{command_dir}/*.md"))
    if not files:
        print(f"Error: No markdown command files found in '{command_dir}'", file=sys.stderr)
        sys.exit(1)

    all_entries = []
    for f in files:
        entries = parse_markdown_module(f)
        all_entries.extend(entries)

    # Save metadata.json
    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(all_entries, out, indent=2, ensure_ascii=False)

    print(f"✅ Successfully compiled {len(all_entries)} commands across {len(files)} modules into {output_json.name}")
    
    # Print breakdown
    categories = {}
    for e in all_entries:
        cat = e['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"  • {cat}: {count} commands")

if __name__ == "__main__":
    main()
