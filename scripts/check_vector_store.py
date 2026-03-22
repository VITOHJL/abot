#!/usr/bin/env python
"""Check if vector store (ChromaDB) exists and has data. Run from abot root."""

import sys
from pathlib import Path

# Resolve workspace (default ~/.abot/workspace)
workspace = Path.home() / ".abot" / "workspace"
if len(sys.argv) > 1:
    workspace = Path(sys.argv[1]).expanduser()

chroma_path = workspace / "memory" / "rag" / "chroma"
index_jsonl = workspace / "memory" / "rag" / "index.jsonl"

print(f"Workspace: {workspace}")
print(f"Chroma path: {chroma_path}")
print(f"Chroma exists: {chroma_path.exists()}")

if chroma_path.exists():
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(chroma_path))
        coll = client.get_or_create_collection("turns")
        count = coll.count()
        print(f"Vector collection 'turns' count: {count}")
        if count > 0:
            sample = coll.peek(limit=1)
            print(f"Sample ids: {sample['ids'][:3]}")
            if sample.get("metadatas"):
                print(f"Sample metadata keys: {list(sample['metadatas'][0].keys()) if sample['metadatas'] else 'none'}")
    except ImportError:
        print("chromadb not installed. Run: pip install abot-ai[embedding]")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Chroma dir not created yet. Vector indexing only runs when:")
    print("  1. embeddingModel is set in ~/.abot/config.json (tools.memory.embeddingModel)")
    print("  2. pip install abot-ai[embedding]")
    print("  3. Compression or /new has been triggered")

print(f"\nKeyword index (index.jsonl): {index_jsonl}")
if index_jsonl.exists():
    lines = sum(1 for _ in open(index_jsonl, encoding="utf-8") if _.strip())
    print(f"  Records: {lines}")
else:
    print("  Not found")
