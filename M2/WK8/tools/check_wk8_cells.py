import json
from pathlib import Path
path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell.get('source', []))
    if ('Train:' in src and 'index_dtype' in src) or ('Mean quarterly log-return by decade' in src) or ('Q1' in src) or ('Q2' in src):
        print('CELL', i)
        print(src)
        print('----')
