import json
from pathlib import Path
path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
for i in [4, 11, 28, 46]:
    cell = nb['cells'][i]
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell.get('source', []))
    print(f'CELL {i} (lines={len(src.splitlines())})')
    for j, line in enumerate(src.splitlines(), 1):
        print(f'{j:03d}: {line!r}')
    print('---')
