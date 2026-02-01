"""Debug script to see what's happening with chunking"""

import sys
from pathlib import Path
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load the commands file
commands_file = Path(__file__).parent.parent / "resources" / "commands.md"
commands = commands_file.read_text(encoding='utf-8')

print("=== Original document preview ===")
print(commands[:500])
print("\n" + "="*50 + "\n")

# Remove markdown code fences if present
doc = commands.strip()
if doc.startswith('```'):
    lines = doc.split('\n')
    if lines[0].startswith('```'):
        print(f"Removing opening fence: {lines[0]}")
        lines = lines[1:]
    if lines and lines[-1].startswith('```'):
        print(f"Removing closing fence: {lines[-1]}")
        lines = lines[:-1]
    doc = '\n'.join(lines)

print("\n=== After fence removal ===")
print(doc[:500])
print("\n" + "="*50 + "\n")

# Split by horizontal rules
sections = re.split(r'\n---+\n', doc)

print(f"=== Found {len(sections)} sections ===\n")

for i, section in enumerate(sections):
    section = section.strip()
    if not section:
        print(f"Section {i}: EMPTY")
        continue
    
    # Check if it starts with ##
    starts_with_h2 = section.startswith('##')
    
    # Try to find ### header
    title_match = re.search(r'^###\s+(.+)$', section, re.MULTILINE)
    
    preview = section[:200].replace('\n', ' ')
    print(f"Section {i}:")
    print(f"  Starts with ##: {starts_with_h2}")
    print(f"  Has ### title: {bool(title_match)}")
    if title_match:
        print(f"  Title: {title_match.group(1)}")
    print(f"  Preview: {preview}...")
    print()
