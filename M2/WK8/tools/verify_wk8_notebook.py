import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))

issues = []
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') != 'code':
        continue
    src = ''.join(cell.get('source', []))
    if 'None' in src or 'TODO' in src:
        issues.append((i, src[:200].replace('\n', '\\n')))

print('placeholder issues:', issues)

try:
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    print('executing notebook... this may take a few minutes')
    notebook = nbformat.read(path, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': str(path.parent)}})
    print('notebook executed successfully')
except Exception as exc:
    print('notebook execution failed:', type(exc).__name__, exc)
    import traceback
    traceback.print_exc()
