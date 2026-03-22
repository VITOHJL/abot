#!/usr/bin/env python
"""Pre-download the embedding model. Run with HF_ENDPOINT=https://hf-mirror.com if needed."""

import sys

model_name = "paraphrase-multilingual-MiniLM-L12-v2"
if len(sys.argv) > 1:
    model_name = sys.argv[1]

print(f"Downloading embedding model: {model_name}")
print("(Set HF_ENDPOINT=https://hf-mirror.com if in China)")

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_name)
# Quick test
vec = model.encode(["hello"])
print(f"Done. Vector dim: {len(vec[0])}")
