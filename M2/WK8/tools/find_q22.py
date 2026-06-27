import json
from pathlib import Path
path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell.get('source', []))
    if 'Diebold-Mariano' in src or 'best_name' in src:
        print('CELL', i)
        for j, line in enumerate(src.splitlines(), 1):
            print(f'{j:03d}: {line}')
        print('---')
