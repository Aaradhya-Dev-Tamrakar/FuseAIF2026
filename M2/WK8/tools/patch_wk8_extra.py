import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))

# patch Q2 annual frequency alias
source = nb['cells'][11]['source']
for i, line in enumerate(source):
    if "annual     = series.resample('Y').last()" in line:
        source[i] = "annual     = series.resample('YE').last()                              # year-end close prices\n"
nb['cells'][11]['source'] = source

# patch Q14 broken multi-line print f-string
source = nb['cells'][54]['source']
for i, line in enumerate(source):
    if line.strip() == 'print(f"':
        source[i] = 'print(f"XGBoost final  MASE={m[\'MASE\']:.4f}  RMSE={m[\'RMSE\']:.1f}\")\n'
        if i + 1 < len(source) and "XGBoost final" in source[i+1]:
            source.pop(i+1)
        break
nb['cells'][54]['source'] = source

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('patched Q2 and Q14')
