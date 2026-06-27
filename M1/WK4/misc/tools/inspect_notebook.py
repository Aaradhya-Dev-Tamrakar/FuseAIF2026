import json
from pathlib import Path

notebook_path = Path('W4_Linear_Models_Assignment.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

output_lines = []
for idx, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    source_str = "".join(cell['source'])
    output_lines.append(f"========================================================================\nCELL {idx:02d} | TYPE: {ctype}\n========================================================================")
    output_lines.append(source_str)
    output_lines.append("\n\n")

Path('notebook_cells.txt').write_text('\n'.join(output_lines), encoding='utf-8')
print("Wrote full structure to notebook_cells.txt successfully!")
