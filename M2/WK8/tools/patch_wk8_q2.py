import json
from pathlib import Path
path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
nb['cells'][11]['source'] = [
    "# Q2 ──────────────────────────────────────────────────────────────────────────\n",
    "quarterly  = series.resample('QE').last()                             # quarter-end close prices\n",
    "annual     = series.resample('Y').last()                              # year-end close prices\n",
    "q_ret      = np.log(quarterly).diff().dropna()                        # log-returns of quarterly prices\n",
    "decade_ret = q_ret.groupby(q_ret.index.year // 10 * 10).mean()        # mean quarterly log-return grouped by decade\n",
    "\n",
    "print(\"Mean quarterly log-return by decade:\", decade_ret.round(4))\n",
    "\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 4))\n",
    "quarterly.plot(ax=axes[0], title='Quarterly S&P 500 Close', color='teal')\n",
    "q_ret.plot(ax=axes[1], title='Quarterly Log-Returns', color='steelblue')\n",
    "plt.tight_layout(); plt.show()\n"
]
path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('patched cell 11')
