import json
from pathlib import Path
path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
source = nb['cells'][11]['source']
for i, line in enumerate(source):
    if "annual     = series.resample('Y').last()" in line:
        source[i] = "annual     = series.resample('YE').last()                              # year-end close prices\n"
nb['cells'][11]['source'] = source
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('updated Q2 annual frequency to YE')
