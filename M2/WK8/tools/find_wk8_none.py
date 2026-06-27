import json
from pathlib import Path
import re

path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell.get('source', []))
    if re.search(r'\b=\s*None\b', src):
        print('CELL', i)
        for line in src.splitlines():
            if re.search(r'\b=\s*None\b', line):
                print('   ', line)
