import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
source = nb['cells'][81]['source']
for i, line in enumerate(source):
    if line.strip() == 'print(f"':
        source[i] = 'print(f"Diebold-Mariano  stat={dm_stat:.4f}  p={dm_p:.4f}\")\n'
        if i + 1 < len(source) and 'Diebold-Mariano' in source[i+1]:
            source.pop(i+1)
        break
nb['cells'][81]['source'] = source
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('patched Q22 f-string')
