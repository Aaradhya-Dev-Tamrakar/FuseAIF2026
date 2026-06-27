import json
from pathlib import Path

notebook_path = Path('W4_Linear_Models_Assignment.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    source_str = "".join(cell['source'])
    if any(word in source_str.lower() for word in ['block 2', 'split', 'scale', 'preprocess']):
        safe_snippet = source_str.strip().replace('\n', ' ')[:100].encode('ascii', errors='replace').decode('ascii')
        print(f"Cell {idx:02d} | Type: {ctype:<8} | Snippet: {safe_snippet}")
