import pickle
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from scipy.stats import beta as beta_dist
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pymc as pm

# Load Telco data
url = (
    'https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d'
    '/master/data/Telco-Customer-Churn.csv'
)
df_raw = pd.read_csv(url)
df = df_raw.copy()
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
df = df.drop(columns=['customerID'])
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Feature preparation for Bayesian logistic regression
features_mcmc = ['tenure', 'MonthlyCharges', 'Contract', 'InternetService', 'SeniorCitizen']
df_mcmc = df[features_mcmc + ['Churn']].copy()
df_mcmc = pd.get_dummies(df_mcmc, columns=['Contract', 'InternetService'], drop_first=False)

contract_cols = [c for c in df_mcmc.columns if 'Contract_Month' in c]
internet_cols = [c for c in df_mcmc.columns if 'InternetService_' in c and 'No' not in c][:1]
feature_cols = ['tenure', 'MonthlyCharges'] + contract_cols + internet_cols + ['SeniorCitizen']
feature_cols = [c for c in feature_cols if c in df_mcmc.columns]

X_mc = df_mcmc[feature_cols].values.astype(float)
y_mc = df_mcmc['Churn'].values.astype(float)

X_tr_mc, X_te_mc, y_tr_mc, y_te_mc = train_test_split(
    X_mc, y_mc, test_size=0.2, random_state=42, stratify=y_mc
)

scaler_mc = StandardScaler()
X_tr_scaled = X_tr_mc.copy(); X_te_scaled = X_te_mc.copy()
X_tr_scaled[:, :2] = scaler_mc.fit_transform(X_tr_mc[:, :2])
X_te_scaled[:, :2] = scaler_mc.transform(X_te_mc[:, :2])

n_features = X_tr_scaled.shape[1]

def main():
    with pm.Model() as bayes_lr:
        intercept = pm.Normal('intercept', mu=0, sigma=5)
        beta = pm.Normal('beta', mu=0, sigma=2, shape=n_features)
        mu = pm.Deterministic('mu', pm.math.sigmoid(
            intercept + pm.math.dot(X_tr_scaled, beta)
        ))
        y_obs = pm.Bernoulli('y_obs', p=mu, observed=y_tr_mc)

        idata = pm.sample(draws=2000, tune=1000, chains=4,
                          target_accept=0.90, random_seed=42,
                          progressbar=True)

    save_path = 'telco_bayes_lr_v1.pkl'
    with open(save_path, 'wb') as f:
        pickle.dump(idata, f)
    print(f'Saved MCMC trace to {save_path}')


if __name__ == '__main__':
    main()
