import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'W8_Forecasting_Assignment.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))

replacements = {
    35: [
        "# Q9 ──────────────────────────────────────────────────────────────────────────\n",
        "residuals = sarima.resid.dropna()   # fitted residuals from sarima with NaN removed\n",
        "\n",
        "lb = acorr_ljungbox(residuals, lags=[6, 12, 24], return_df=True)\n",
        "print(\"Ljung-Box (p > 0.05 = white noise at that lag):\")\n",
        "print(lb[['lb_stat', 'lb_pvalue']].round(4))\n",
        "\n",
        "from scipy import stats as scipy_stats\n",
        "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n",
        "scipy_stats.probplot(residuals, plot=axes[0])\n",
        "axes[0].set_title('QQ-Plot of SARIMA Residuals')\n",
        "pd.Series(residuals).plot(ax=axes[1], title='Residuals over time')\n",
        "axes[1].axhline(0, color='red', lw=0.8)\n",
        "plt.tight_layout(); plt.show()\n",
        "\n",
        "failed = (lb['lb_pvalue'] < 0.05).sum()\n",
        "print(f\"\\n{'✅ All lags passed' if failed == 0 else f'⚠️  {failed} lag(s) failed — adjust SARIMA order'}\")\n",
    ],
    39: [
        "# Q10 ──────────────────────────────────────────────────────────────────────────\n",
        "fc_obj   = sarima.get_forecast(steps=H)   # H-step forecast object from sarima\n",
        "log_mean = fc_obj.predicted_mean         # point forecast in log space\n",
        "log_ci   = fc_obj.conf_int(alpha=0.05)   # confidence interval in log space (alpha=0.05 → 95%)\n",
        "\n",
        "sarima_fc    = np.exp(log_mean.values)    # point forecast in price space (inverse log-transform log_mean)\n",
        "sarima_fc_lo = np.exp(log_ci.iloc[:, 0].values)\n",
        "sarima_fc_hi = np.exp(log_ci.iloc[:, 1].values)\n",
        "\n",
        "results['SARIMA'] = sarima_fc\n",
        "m = compute_metrics(test, sarima_fc, train)\n",
        "print(f\"SARIMA  MASE={m['MASE']:.4f}  RMSE={m['RMSE']:.1f}\")\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(13, 5))\n",
        "train.iloc[-48:].plot(ax=ax, label='Train (last 4y)', color='steelblue', lw=1.5)\n",
        "test.plot(ax=ax, label='Actual', color='black', lw=1.5)\n",
        "ax.plot(test.index, sarima_fc, label='SARIMA', color='tomato', lw=2)\n",
        "ax.fill_between(test.index, sarima_fc_lo, sarima_fc_hi,\n",
        "                alpha=0.2, color='tomato', label='95% CI')\n",
        "ax.axvline(pd.Timestamp('2020-03-01'), color='orange', lw=1.5, ls='--', label='COVID crash')\n",
        "ax.legend(); ax.set_title('SARIMA Forecast vs Actual S&P 500')\n",
        "plt.tight_layout(); plt.show()\n",
    ],
    72: [
        "# Q19 ─────────────────────────────────────────────────────────────────────────\n",
        "metric_rows = {}\n",
        "for name, fc in results.items():\n",
        "    if len(np.array(fc)) == H:\n",
        "        row = compute_metrics(test, fc, train)   # compute all 7 metrics for this model's forecast\n",
        "        metric_rows[name] = row\n",
        "\n",
        "metrics_df = pd.DataFrame(metric_rows).T.round(4).sort_values('MASE')   # DataFrame from metric_rows, transposed, rounded to 4 places, sorted by MASE\n",
        "\n",
        "print(\"=== Model Comparison (sorted by MASE) ===\")\n",
        "print(metrics_df.to_string())\n",
        "\n",
        "metrics_df['MASE'].plot(\n",
        "    kind='bar', figsize=(10, 4),\n",
        "    color=['tomato' if v > 1.0 else 'steelblue' for v in metrics_df['MASE']],\n",
        "    title='MASE by Model (red = worse than naïve baseline)')\n",
        "plt.axhline(1.0, color='red', ls='--', label='Naïve = 1.0')\n",
        "plt.ylabel('MASE'); plt.xticks(rotation=45, ha='right')\n",
        "plt.legend(); plt.tight_layout(); plt.show()\n",
    ],
}

for idx, src in replacements.items():
    nb['cells'][idx]['source'] = src

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
print('patched', list(replacements.keys()))
