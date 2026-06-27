import json
from pathlib import Path

notebook_path = Path('W4_Linear_Models_Assignment.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx in [16, 17, 18, 19, 20]:
    cell = nb['cells'][idx]
    print(f"--- Cell {idx} (Type: {cell['cell_type']}) ---")
    source_str = "".join(cell['source'])
    print(source_str.encode('ascii', errors='replace').decode('ascii'))
