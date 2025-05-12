"""
fix_broken_json.py

This script reads a potentially corrupted or multi-line JSON file where each line is expected 
to be a separate JSON object (e.g., Reddit comments or logs), but may contain malformed entries 
due to unescaped characters or newlines within string fields (such as 'body').

The script attempts to:
- Reconstruct incomplete JSON objects by buffering lines until a complete object is formed.
- Parse and validate each JSON object.
- Save the cleaned output in both JSON Lines (.jsonl) format and, optionally, as a standard JSON array.

"""

import json

def is_complete_json(s):
    """Check if a string is a complete JSON object."""
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False

fixed_rows = []
buffer = ""

with open("D:\CS\Reddit Chatbot\RC_2015-01\RC_2015-01", encoding='utf-8') as f:
    for line in f:
        buffer += line.strip()  # Append line (strip only \n)
        if is_complete_json(buffer):
            try:
                data = json.loads(buffer)
                fixed_rows.append(data)
            except json.JSONDecodeError as e:
                print(f"Failed to decode: {e}")
            buffer = ""  # Reset for next JSON object
        else:
            buffer += " "  # Add space in case a word was split by newline

# Save or process fixed_rows
print(f"Successfully loaded {len(fixed_rows)} JSON objects.")

with open("cleaned_RC_2015-01.jsonl", "w", encoding="utf-8") as out:
    for obj in fixed_rows:
        out.write(json.dumps(obj) + "\n")

# Optionally, save as a single JSON array
with open("cleaned_RC_2015-01.json", "w", encoding="utf-8") as out:
    json.dump(fixed_rows, out, ensure_ascii=False, indent=2)