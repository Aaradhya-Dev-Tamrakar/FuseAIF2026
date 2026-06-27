import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))

updates = {
    11: [
        "# Q2 ──────────────────────────────────────────────────────────────────────────\n",
        "quarterly  = series.resample('QE').last()                             # quarter-end close prices\n",
        "annual     = series.resample('A').last()                              # year-end close prices\n",
        "q_ret      = np.log(quarterly).diff().dropna()                        # log-returns of quarterly prices\n",
        "decade_ret = q_ret.groupby(q_ret.index.year // 10 * 10).mean()        # mean quarterly log-return grouped by decade\n",
        "\n",
        "print(\"Mean quarterly log-return by decade:\", decade_ret.round(4))\n",
        "\n",
        "fig, axes = plt.subplots(1, 2, figsize=(14, 4))\n",
        "quarterly.plot(ax=axes[0], title='Quarterly S&P 500 Close', color='teal')\n",
        "q_ret.plot(ax=axes[1], title='Quarterly Log-Returns', color='steelblue')\n",
        "plt.tight_layout(); plt.show()\n",
    ],
    28: [
        "# Q7 ──────────────────────────────────────────────────────────────────────────\n",
        "hw = ExponentialSmoothing(\n",
        "    log_train,\n",
        "    trend=None,              # type of trend component ('add' or 'mul')\n",
        "    seasonal=None,           # type of seasonal component ('add' or 'mul')\n",
        "    seasonal_periods=None,   # number of months in one full seasonal cycle\n",
        "    initialization_method='estimated',\n",
        ").fit(optimized=True)\n",
        "\n",
        "print(f\"α (level)    = {hw.params['smoothing_level']:.4f}\")\n",
        "print(f\"β (trend)    = {hw.params['smoothing_trend']:.4f}\")\n",
        "print(f\"γ (seasonal) = {hw.params['smoothing_seasonal']:.4f}\")\n",
        "print(f\"AIC = {hw.aic:.2f}   BIC = {hw.bic:.2f}\")\n",
        "\n",
        "hw_log_fc = hw.forecast(H)                      # H-step ahead forecast in log space\n",
        "results['Holt-Winters'] = np.exp(hw_log_fc)      # inverse log-transform to price space\n",
        "\n",
        "m = compute_metrics(test, results['Holt-Winters'], train)\n",
        "print(f\"Holt-Winters  MASE={m['MASE']:.4f}  RMSE={m['RMSE']:.1f}\")\n",
    ],
    46: [
        "# Q12 ─────────────────────────────────────────────────────────────────────────\n",
        "from prophet.diagnostics import cross_validation, performance_metrics\n",
        "\n",
        "initial_window = '3650 days'   # minimum training period as a string (10 years ≈ '3650 days')\n",
        "\n",
        "df_cv = cross_validation(\n",
        "    m_prop,\n",
        "    initial=initial_window,\n",
        "    period='180 days',\n",
        "    horizon='365 days',\n",
        "    parallel=None,\n",
        ")\n",
        "df_pm = performance_metrics(df_cv)\n",
        "print(\"Prophet CV — performance by horizon:\")\n",
        "print(df_pm[['horizon', 'rmse', 'mape']].head())\n",
        "print(f\"Mean RMSE across horizons: {df_pm['rmse'].mean():.4f}  (log space)\")\n",
    ],
}

for idx, src in updates.items():
    nb['cells'][idx]['source'] = src

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('updated cells', list(updates.keys()))
