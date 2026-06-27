import json
from pathlib import Path
path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
for idx in [35, 39, 72]:
    print(f'CELL {idx}')
    cell = nb['cells'][idx]
    if cell['cell_type'] != 'code':
        print('  not a code cell')
    source = ''.join(cell['source'])
    print(source)
    print('---\n')
