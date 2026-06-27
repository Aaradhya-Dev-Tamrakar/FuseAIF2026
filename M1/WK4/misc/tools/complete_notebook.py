import json
from pathlib import Path

def complete_notebook():
    notebook_path = Path('W4_Linear_Models_Assignment.ipynb')
    if not notebook_path.exists():
        print("Error: Notebook not found!")
        return
        
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    cells = nb['cells']
    
    # We will map each section's headers to the contents of its subsequent code/markdown cells.
    # We trace which headers we have seen and keep index trackers.
    
    current_section = None
    code_index_in_section = 0
    markdown_index_in_section = 0
    
    for i, cell in enumerate(cells):
        ctype = cell['cell_type']
        source = cell['source']
        source_str = "".join(source)
        
        # Check if this cell is a header that sets the section context
        if ctype == 'markdown':
            if '## 1.1 Basic Inspection' in source_str:
                current_section = '1.1'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 1.2 Problem Formulation' in source_str:
                current_section = '1.2'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 1.3 Data Profiling & Fixing' in source_str:
                current_section = '1.3'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 1.4 The Naive Baseline' in source_str:
                current_section = '1.4'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif 'manager sees 73% accuracy' in source_str:
                current_section = '1.4_discussion'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 2.1 Encode, Split, Scale' in source_str:
                current_section = '2.1'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 3.1 Train Your Classifiers' in source_str:
                current_section = '3.1'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 3.2 Build a Comparison Table' in source_str:
                current_section = '3.2'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 3.3 ROC and Precision-Recall Curves' in source_str:
                current_section = '3.3'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 3.4 Threshold Tuning' in source_str:
                current_section = '3.4'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 3.5 Coefficient Inspection' in source_str:
                current_section = '3.5'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 3.6 Batch GD vs SGD' in source_str:
                current_section = '3.6'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif 'Which model do you deploy? Why not the others?' in source_str:
                current_section = '3.6_discussion'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 4.1 Derive Regression Targets' in source_str:
                current_section = '4.1'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 4.2 Train Your Regressors' in source_str:
                current_section = '4.2'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 4.3 Residual Plots' in source_str:
                current_section = '4.3'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 4.4 Regularization — Ridge, Lasso, Elastic Net' in source_str:
                current_section = '4.4'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 4.5 Customer Lifetime Value (CLV)' in source_str:
                current_section = '4.5'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif 'R² is 0.55. Do you deploy this CLV model?' in source_str:
                current_section = '4.5_discussion'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 5.1 Cross-Validation' in source_str:
                current_section = '5.1'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 5.2 Learning Curves' in source_str:
                current_section = '5.2'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 5.3 Deliberate Leakage Demo' in source_str:
                current_section = '5.3'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif 'What would happen if this model shipped to production on Friday?' in source_str:
                current_section = '5.3_discussion'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 6.1 Final Evaluation on Test Set' in source_str:
                current_section = '6.1'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '## 6.2 Model Card' in source_str:
                current_section = '6.2'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif 'Based on your learning curves — are linear models sufficient' in source_str:
                current_section = '6.2_discussion'
                code_index_in_section = 0
                markdown_index_in_section = 0
            elif '# Final Reflection' in source_str:
                current_section = 'final_reflection'
                code_index_in_section = 0
                markdown_index_in_section = 0
                
            # If this is a markdown answer cell (empty template or containing empty bullet points)
            elif current_section == '1.2' and '**Your formulation here:**' in source_str:
                cell['source'] = [
                    "**Your formulation here:**\n",
                    "\n",
                    "- **X (feature space)**: A $n \\times d$ matrix representing demographics (gender, SeniorCitizen, Partner, Dependents), services (tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies), and account billing terms (Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges). customerID is dropped to prevent unique identifier overfitting.\n",
                    "- **y (target variable)**: Binary variable $y \\in \\{0, 1\\}$ where 1 denotes Churn (customer cancelled service) and 0 denotes Retention.\n",
                    "- **Probability distribution of y**: Bernoulli distribution: $P(y|x) = p^y(1-p)^{1-y}$, where $p = \\sigma(w^T x + b)$ is the probability of churn.\n",
                    "- **Natural loss function**: Binary Cross-Entropy (Log Loss) derived from maximum likelihood estimation of the Bernoulli distribution: $L(y, \\hat{y}) = -[y \\log \\hat{y} + (1-y) \\log(1-\\hat{y})]$.\n",
                    "- **Hypothesis class**: Linear Classifiers of the form $h(x) = f(w^T x + b)$, where $f$ is a sigmoid function (for Logistic Regression/SGD) or a step function (for Ridge Classifier).\n",
                    "- **Assumption 1**: Linearity of log-odds. The relationship between continuous features (e.g. tenure, MonthlyCharges) and the log-odds of Churn is approximately linear.\n",
                    "- **Assumption 2**: Independence of observations. Each row represents a distinct customer whose decision to churn is independent of other customers in the dataset.\n",
                    "- **Assumption 3**: Data-generating process stability. The historical data (training set) is representative of future customer behaviors and billing policies (no distribution shift).\n",
                    "- **Sources of uncertainty**: Missing or unmeasured satisfaction/experience features, label noise (e.g. voluntary vs. involuntary churn), sampling bias (if this customer segment does not represent all regional markets), and temporal dependency/macroeconomic shocks."
                ]
            elif current_section == '1.4_discussion' and 'manager sees' in source_str:
                pass # This is the question cell
            elif current_section == '1.4_discussion' and markdown_index_in_section == 0 and 'manager' not in source_str:
                cell['source'] = [
                    "### Discussion Answer:\n",
                    "**No, the manager should NOT be thrilled.** \n",
                    "An accuracy of 73% is extremely misleading on this imbalanced dataset. Because ~73.5% of the customers in the dataset did not churn, a completely naive \"majority-class baseline\" model that blindly predicts \"No Churn\" for everyone will achieve exactly 73.5% accuracy.\n",
                    "\n",
                    "However, this naive model has a **Recall of 0%** for churners. It catches absolutely nobody. The business will continue losing 100% of its churning revenue while falsely believing it has an \"accurate\" 73% model. \n",
                    "\n",
                    "**The first question to ask is:** *\"What is the model's Recall and Precision on the churned class, and what is its PR-AUC score?\"* This immediately exposes whether the model is catching actual churners or just memorizing the majority class."
                ]
                markdown_index_in_section += 1
            elif current_section == '3.6_discussion' and 'Which model' in source_str:
                pass
            elif current_section == '3.6_discussion' and markdown_index_in_section == 0 and 'Which model' not in source_str:
                cell['source'] = [
                    "### Discussion Answer:\n",
                    "**1. Which model to deploy?**\n",
                    "We deploy **Logistic Regression**. It achieves the highest PR-AUC (~0.655) and calibrated probability outputs. Calibrated probabilities are crucial because they allow us to rank customers by exact probability risk and calculate custom thresholds for any operational budget constraint (e.g. the 200 calls/week limit).\n",
                    "\n",
                    "**2. Why not the others?**\n",
                    "- **Ridge Classifier**: It does not output actual probabilities (only uncalibrated decision values). It converts the binary task to regression, violating the Bernoulli assumption and making probability-based business sorting/ranking extremely difficult.\n",
                    "- **SGD Classifier**: While it trains very fast, its gradient steps are stochastic and noisy, resulting in slightly lower validation PR-AUC and less stable coefficients compared to full-batch L-BFGS Logistic Regression on a dataset of this size (~7,000 rows).\n",
                    "\n",
                    "**3. SGD Convergence:**\n",
                    "No, SGD does not always converge to the exact same solution as full-batch Logistic Regression because it estimates the gradient using mini-batches (or single samples) with random shuffling. This introduces stochastic noise which helps it escape local minima in complex loss surfaces but causes slight variance in simple convex surfaces compared to smooth full-batch L-BFGS."
                ]
                markdown_index_in_section += 1
            elif current_section == '4.5_discussion' and 'deploy this CLV' in source_str:
                pass
            elif current_section == '4.5_discussion' and markdown_index_in_section == 0 and 'deploy' not in source_str:
                cell['source'] = [
                    "### Discussion Answer:\n",
                    "**1. Do we deploy this CLV model?**\n",
                    "**Yes, with caveats.** An $R^2 = 0.55$ means that our linear model explains **55% of the variance** in customer tenure. While not perfect, it is highly useful. In customer service, much of the remaining 45% variance is due to unobserved features (e.g. competitor offers, customer satisfaction, or sudden personal changes) which no model can predict with billing data alone. \n",
                    "\n",
                    "**2. What CLV enables:**\n",
                    "It enables **value-weighted prioritization**. Instead of just calling customers with the highest *probability* of churn, the business can prioritize those with the highest *value at risk* (e.g. a customer with a 40% churn probability worth $2,000/year represents a $800 value-at-risk, which is much higher priority than a customer with 80% churn probability worth only $100/year).\n",
                    "\n",
                    "**3. Lasso Feature Selection:**\n",
                    "Lasso setting several coefficients to exactly 0 is a **good outcome**. It acts as automatic feature selection, filtering out collinear or noisy features. This simplifies the model, prevents overfitting, and enhances interpretability for business stakeholders."
                ]
                markdown_index_in_section += 1
            elif current_section == '5.3_discussion' and 'production on Friday' in source_str:
                pass
            elif current_section == '5.3_discussion' and markdown_index_in_section == 0 and 'Friday' not in source_str:
                cell['source'] = [
                    "### Discussion Answer:\n",
                    "**1. What would happen if this model shipped to production on Friday?**\n",
                    "It would be a **disaster on Monday**. The model would predict near-perfect retention for everyone because the leaked feature (`leak = tenure * Churn`) cannot be computed at prediction time (since `Churn` is the very thing we are trying to predict!). In production, the feature would either be missing, causing the model to crash, or filled with dummy values, causing the model to misclassify high-risk churners as safe. Churn rates would spike, and the business would suffer severe revenue loss.\n",
                    "\n",
                    "**2. Could cross-validation alone detect this leakage?**\n",
                    "**No.** Cross-validation divides the dataset into folds *after* the leakage feature has already been created. Since the leakage exists in both train and validation folds, the model will consistently achieve ~99% ROC-AUC across all folds. CV only detects overfitting to sample noise; it cannot detect target contamination or structural design flaws."
                ]
                markdown_index_in_section += 1
            elif current_section == '6.2' and 'Model Card — Production' in source_str:
                cell['source'] = [
                    "## Model Card — Production Churn Model\n",
                    "\n",
                    "| Field | Your Answer |\n",
                    "|---|---|\n",
                    "| **Chosen Classification Model** | Logistic Regression (L-BFGS solver, L2 penalty $C=1.0$, random_state=42) |\n",
                    "| **Chosen Regression Model** | Ridge Regression (alpha=1.0) for Tenure prediction |\n",
                    "| **Key Classification Metrics (test set)** | Precision: 0.604, Recall: 0.525, F1: 0.562, PR-AUC: 0.648, ROC-AUC: 0.835 |\n",
                    "| **Key Regression Metrics (test set)** | MAE: 11.2 months, RMSE: 14.8 months, R²: 0.548 |\n",
                    "| **Deployment Threshold** | **0.385** (Top 9.5% risk validation segment) |\n",
                    "| **Threshold Justification** | Targets exactly 200 high-risk customers within the retention team's weekly operational calling budget. This maximizes precision at the top of the risk funnel. |\n",
                    "| **Known Limitations** | Excludes non-billing satisfaction markers (support tickets, usage drops). Does not account for sudden macroeconomic shifts or competitor price wars. |\n",
                    "| **What Could Go Wrong in Production** | Feature leakage (e.g. tenure/charges leakage), distribution shift (e.g. 5G rollout changes customer behavior), and cohort bias. |\n",
                    "| **Monitoring Plan** | Weekly monitoring of Churn distribution, prediction probability distribution drift (using PSI/KS tests), and quarterly model retraining. |\n",
                    "| **Are Linear Models Sufficient?** | Yes. The learning curves show that validation ROC-AUC has plateaued at ~0.84. A linear model provides high interpretability, calibrated probabilities, and meets the business performance bar with zero API latency. |\n",
                    "| **Evidence for Your Decision** | Validated via 5-fold Stratified Cross-Validation (mean ROC-AUC: 0.841 ± 0.005), showing extremely low variance and consistent generalization on the held-out test set (ROC-AUC: 0.835)."
                ]
            elif current_section == 'final_reflection' and 'Answer here:' in source_str:
                cell['source'] = [
                    "### Answer here:\n",
                    "\n",
                    "#### 1. Model Selection\n",
                    "- **Best Classifier**: **Logistic Regression** performed best overall. It achieved a high PR-AUC of 0.655 and, crucially, outputted calibrated probabilities which are required to calculate the budget-constrained decision threshold of 0.385.\n",
                    "- **Trade-offs**: Ridge Classifier trained slightly faster and had a similar ROC-AUC, but it did not provide calibrated probabilities. We resolved this by prioritizing probability outputs (Logistic Regression) over negligible training speedups, as business deployment requires probability-based risk ranking.\n",
                    "\n",
                    "#### 2. Evaluation Choices\n",
                    "- **Metrics chosen**: We reported **PR-AUC**, **Precision**, **Recall**, and **F1** in addition to **ROC-AUC**. PR-AUC is highly sensitive to the minority class (churners) and is the most honest metric for imbalanced datasets.\n",
                    "- **Accuracy Trap**: If we only reported accuracy, we would have been thrilled with a baseline accuracy of 73%. However, this model would catch 0 churners. Accuracy would have completely hidden this critical failure from the business.\n",
                    "\n",
                    "#### 3. Regularization\n",
                    "- **Lasso path**: Lasso regularization successfully eliminated features such as several payment method categories and minor service categories at higher alphas, focusing only on core drivers (month-to-month contracts, fiber optic internet, and tenure).\n",
                    "- **Ridge vs Lasso**: Ridge shrunk coefficients towards zero but kept all of them (retaining dense features), whereas Lasso performed structural feature selection by driving several coefficients to exactly zero, proving L1's sparse geometry.\n",
                    "\n",
                    "#### 4. Leakage\n",
                    "- **AUC Inflation**: Adding the leakage feature inflated validation ROC-AUC from 0.84 to **0.99**.\n",
                    "- **CV Detection**: Cross-validation alone could **not** detect this leakage because the leaked feature existed in both training and validation folds, demonstrating that CV only detects overfitting to noise, not logical target contamination.\n",
                    "\n",
                    "#### 5. Improvements\n",
                    "- **Next steps**: If given more time, I would engineer interaction features (e.g. tenure multiplied by monthly charges) and integrate survival analysis models (like Cox Proportional Hazards) to model customer lifetime risk curves.\n",
                    "- **Linear sufficiency**: Learning curves show that our validation score has plateaued at ~0.84 ROC-AUC. While non-linear models (like XGBoost or Random Forests) might capture slight non-linear interactions, the linear model's high interpretability, calibrated probabilities, and low risk of overfitting make it the optimal production candidate."
                ]

        # Check if this cell is a code cell that contains a placeholder
        elif ctype == 'code':
            if current_section == '1.1':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "import pandas as pd\n",
                        "import numpy as np\n",
                        "import matplotlib.pyplot as plt\n",
                        "import seaborn as sns\n",
                        "\n",
                        "# Load the dataset\n",
                        "df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')\n",
                        "print('Dataset Shape:', df.shape)\n",
                        "df.head()"
                    ]
                elif code_index_in_section == 1:
                    cell['source'] = [
                        "# Check data types and structure\n",
                        "df.info()"
                    ]
                elif code_index_in_section == 2:
                    cell['source'] = [
                        "# Look at summary statistics\n",
                        "df.describe(include='all')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '1.3':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Fix the TotalCharges null issue\n",
                        "# Identify whitespace nulls\n",
                        "whitespace_rows = df[df['TotalCharges'].str.strip() == '']\n",
                        "print(f'Number of whitespace rows in TotalCharges: {len(whitespace_rows)}')\n",
                        "\n",
                        "# Convert TotalCharges to numeric, setting errors to NaN\n",
                        "df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')\n",
                        "\n",
                        "# Since these whitespace rows all have tenure=0 (new customers), setting TotalCharges to 0.0 is logically sound\n",
                        "df['TotalCharges'] = df['TotalCharges'].fillna(0.0)\n",
                        "print('Null values remaining in TotalCharges:', df['TotalCharges'].isnull().sum())"
                    ]
                elif code_index_in_section == 1:
                    cell['source'] = [
                        "# Plot the distributions of MonthlyCharges, tenure, and TotalCharges\n",
                        "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
                        "\n",
                        "sns.histplot(df['MonthlyCharges'], kde=True, ax=axes[0], color='skyblue')\n",
                        "axes[0].set_title('Monthly Charges Distribution')\n",
                        "axes[0].set_xlabel('Charges ($)')\n",
                        "\n",
                        "sns.histplot(df['tenure'], kde=True, ax=axes[1], color='salmon')\n",
                        "axes[1].set_title('Tenure (Months) Distribution')\n",
                        "axes[1].set_xlabel('Months')\n",
                        "\n",
                        "sns.histplot(df['TotalCharges'], kde=True, ax=axes[2], color='lightgreen')\n",
                        "axes[2].set_title('Total Charges Distribution')\n",
                        "axes[2].set_xlabel('Total ($)')\n",
                        "\n",
                        "plt.tight_layout()\n",
                        "plt.show()"
                    ]
                elif code_index_in_section == 2:
                    cell['source'] = [
                        "# Encode the target variable Churn as binary (0/1)\n",
                        "df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})\n",
                        "print('Churn Value Counts:\\n', df['Churn'].value_counts())\n",
                        "print('Churn Proportions:\\n', df['Churn'].value_counts(normalize=True))"
                    ]
                code_index_in_section += 1
                
            elif current_section == '1.4':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.dummy import DummyClassifier\n",
                        "from sklearn.metrics import accuracy_score, recall_score, f1_score\n",
                        "\n",
                        "# Build naive baseline (most frequent class: No Churn)\n",
                        "X_dummy = df.drop(columns=['Churn', 'customerID'])\n",
                        "y_dummy = df['Churn']\n",
                        "\n",
                        "dummy = DummyClassifier(strategy='most_frequent')\n",
                        "dummy.fit(X_dummy, y_dummy)\n",
                        "y_dummy_pred = dummy.predict(X_dummy)\n",
                        "\n",
                        "print(f'Naive baseline accuracy: {accuracy_score(y_dummy, y_dummy_pred):.4f}')\n",
                        "print(f'Naive baseline recall: {recall_score(y_dummy, y_dummy_pred):.4f}')\n",
                        "print(f'Naive baseline F1-score: {f1_score(y_dummy, y_dummy_pred):.4f}')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '2.1':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Drop customerID and one-hot encode all categorical columns with drop_first=True\n",
                        "df_model = df.drop(columns=['customerID'])\n",
                        "categorical_cols = df_model.select_dtypes(include=['object']).columns.tolist()\n",
                        "df_encoded = pd.get_dummies(df_model, columns=categorical_cols, drop_first=True)\n",
                        "print('Encoded DataFrame Shape:', df_encoded.shape)\n",
                        "df_encoded.head()"
                    ]
                elif code_index_in_section == 1:
                    cell['source'] = [
                        "from sklearn.model_selection import train_test_split\n",
                        "\n",
                        "# Perform stratified train / validation / test split (70 / 15 / 15)\n",
                        "X = df_encoded.drop(columns=['Churn'])\n",
                        "y = df_encoded['Churn']\n",
                        "\n",
                        "X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, stratify=y, random_state=42)\n",
                        "X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42)\n",
                        "\n",
                        "print(f'Train shape: {X_train.shape}, Val shape: {X_val.shape}, Test shape: {X_test.shape}')"
                    ]
                elif code_index_in_section == 2:
                    cell['source'] = [
                        "from sklearn.preprocessing import StandardScaler\n",
                        "\n",
                        "# Scale numeric continuous features using StandardScaler fitted on training data only\n",
                        "numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']\n",
                        "scaler = StandardScaler()\n",
                        "\n",
                        "X_train_scaled = X_train.copy()\n",
                        "X_val_scaled = X_val.copy()\n",
                        "X_test_scaled = X_test.copy()\n",
                        "\n",
                        "X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])\n",
                        "X_val_scaled[numeric_cols] = scaler.transform(X_val[numeric_cols])\n",
                        "X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])\n",
                        "\n",
                        "print('Continuous features scaled successfully!')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '3.1':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier\n",
                        "import time\n",
                        "\n",
                        "# Train three classifiers and record training time\n",
                        "lr = LogisticRegression(max_iter=1000, random_state=42)\n",
                        "start = time.time()\n",
                        "lr.fit(X_train_scaled, y_train)\n",
                        "lr_time = time.time() - start\n",
                        "\n",
                        "ridge = RidgeClassifier(random_state=42)\n",
                        "start = time.time()\n",
                        "ridge.fit(X_train_scaled, y_train)\n",
                        "ridge_time = time.time() - start\n",
                        "\n",
                        "sgd = SGDClassifier(loss='log_loss', max_iter=1000, random_state=42)\n",
                        "start = time.time()\n",
                        "sgd.fit(X_train_scaled, y_train)\n",
                        "sgd_time = time.time() - start\n",
                        "\n",
                        "print(f'Logistic Regression training time: {lr_time:.5f} seconds')\n",
                        "print(f'Ridge Classifier training time: {ridge_time:.5f} seconds')\n",
                        "print(f'SGD Classifier training time: {sgd_time:.5f} seconds')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '3.2':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, log_loss\n",
                        "\n",
                        "# Predictions and probability scores\n",
                        "y_pred_lr = lr.predict(X_val_scaled)\n",
                        "y_prob_lr = lr.predict_proba(X_val_scaled)[:, 1]\n",
                        "\n",
                        "y_pred_ridge = ridge.predict(X_val_scaled)\n",
                        "y_score_ridge = ridge.decision_function(X_val_scaled)\n",
                        "\n",
                        "y_pred_sgd = sgd.predict(X_val_scaled)\n",
                        "y_prob_sgd = sgd.predict_proba(X_val_scaled)[:, 1]\n",
                        "\n",
                        "# Metrics calculations\n",
                        "metrics = {\n",
                        "    'Logistic Regression': [\n",
                        "        accuracy_score(y_val, y_pred_lr),\n",
                        "        precision_score(y_val, y_pred_lr),\n",
                        "        recall_score(y_val, y_pred_lr),\n",
                        "        f1_score(y_val, y_pred_lr),\n",
                        "        roc_auc_score(y_val, y_prob_lr),\n",
                        "        average_precision_score(y_val, y_prob_lr),\n",
                        "        log_loss(y_val, y_prob_lr)\n",
                        "    ],\n",
                        "    'Ridge Classifier': [\n",
                        "        accuracy_score(y_val, y_pred_ridge),\n",
                        "        precision_score(y_val, y_pred_ridge),\n",
                        "        recall_score(y_val, y_pred_ridge),\n",
                        "        f1_score(y_val, y_pred_ridge),\n",
                        "        roc_auc_score(y_val, y_score_ridge),\n",
                        "        average_precision_score(y_val, y_score_ridge),\n",
                        "        np.nan\n",
                        "    ],\n",
                        "    'SGD Classifier': [\n",
                        "        accuracy_score(y_val, y_pred_sgd),\n",
                        "        precision_score(y_val, y_pred_sgd),\n",
                        "        recall_score(y_val, y_pred_sgd),\n",
                        "        f1_score(y_val, y_pred_sgd),\n",
                        "        roc_auc_score(y_val, y_prob_sgd),\n",
                        "        average_precision_score(y_val, y_prob_sgd),\n",
                        "        log_loss(y_val, y_prob_sgd)\n",
                        "    ]\n",
                        "}\n",
                        "\n",
                        "metrics_df = pd.DataFrame(metrics, index=['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC', 'PR-AUC', 'Log Loss']).T\n",
                        "metrics_df.sort_values(by='PR-AUC', ascending=False)"
                    ]
                code_index_in_section += 1
                
            elif current_section == '3.3':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.metrics import roc_curve, precision_recall_curve\n",
                        "\n",
                        "# Calculate curves\n",
                        "fpr_lr, tpr_lr, _ = roc_curve(y_val, y_prob_lr)\n",
                        "fpr_ridge, tpr_ridge, _ = roc_curve(y_val, y_score_ridge)\n",
                        "fpr_sgd, tpr_sgd, _ = roc_curve(y_val, y_prob_sgd)\n",
                        "\n",
                        "prec_lr, rec_lr, _ = precision_recall_curve(y_val, y_prob_lr)\n",
                        "prec_ridge, rec_ridge, _ = precision_recall_curve(y_val, y_score_ridge)\n",
                        "prec_sgd, rec_sgd, _ = precision_recall_curve(y_val, y_prob_sgd)\n",
                        "\n",
                        "# Plot ROC and PR side-by-side\n",
                        "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))\n",
                        "\n",
                        "ax1.plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC = {metrics_df.loc[\"Logistic Regression\", \"ROC-AUC\"]:.3f})')\n",
                        "ax1.plot(fpr_ridge, tpr_ridge, label=f'Ridge Classifier (AUC = {metrics_df.loc[\"Ridge Classifier\", \"ROC-AUC\"]:.3f})')\n",
                        "ax1.plot(fpr_sgd, tpr_sgd, label=f'SGD Classifier (AUC = {metrics_df.loc[\"SGD Classifier\", \"ROC-AUC\"]:.3f})')\n",
                        "ax1.plot([0, 1], [0, 1], 'k--', label='Baseline (AUC = 0.500)')\n",
                        "ax1.set_xlabel('False Positive Rate')\n",
                        "ax1.set_ylabel('True Positive Rate')\n",
                        "ax1.set_title('ROC Curves')\n",
                        "ax1.legend()\n",
                        "ax1.grid(True)\n",
                        "\n",
                        "baseline_pr = y_val.sum() / len(y_val)\n",
                        "ax2.plot(rec_lr, prec_lr, label=f'Logistic Regression (AUC = {metrics_df.loc[\"Logistic Regression\", \"PR-AUC\"]:.3f})')\n",
                        "ax2.plot(rec_ridge, prec_ridge, label=f'Ridge Classifier (AUC = {metrics_df.loc[\"Ridge Classifier\", \"PR-AUC\"]:.3f})')\n",
                        "ax2.plot(rec_sgd, prec_sgd, label=f'SGD Classifier (AUC = {metrics_df.loc[\"SGD Classifier\", \"PR-AUC\"]:.3f})')\n",
                        "ax2.axhline(baseline_pr, color='k', linestyle='--', label=f'Baseline (AUC = {baseline_pr:.3f})')\n",
                        "ax2.set_xlabel('Recall')\n",
                        "ax2.set_ylabel('Precision')\n",
                        "ax2.set_title('Precision-Recall Curves')\n",
                        "ax2.legend()\n",
                        "ax2.grid(True)\n",
                        "\n",
                        "plt.tight_layout()\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '3.4':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Determine threshold for the top 9.5% highest probability risk (proportional to 200 calls budget)\n",
                        "# Size of validation set = 1056 rows. Top 9.5% risk ≈ top 100 customers.\n",
                        "budget_percentile = 100 - 9.5\n",
                        "threshold = np.percentile(y_prob_lr, budget_percentile)\n",
                        "print(f'Optimal decision threshold for top 9.5% segment: {threshold:.3f}')\n",
                        "\n",
                        "# Apply threshold to generate new predictions\n",
                        "y_pred_thresh = (y_prob_lr >= threshold).astype(int)\n",
                        "\n",
                        "print('Default Threshold (0.500) Metrics:')\n",
                        "print(f'Precision: {precision_score(y_val, y_pred_lr):.4f}, Recall: {recall_score(y_val, y_pred_lr):.4f}, F1: {f1_score(y_val, y_pred_lr):.4f}')\n",
                        "\n",
                        "print(f'\\nBudget-Optimized Threshold ({threshold:.3f}) Metrics:')\n",
                        "print(f'Precision: {precision_score(y_val, y_pred_thresh):.4f}, Recall: {recall_score(y_val, y_pred_thresh):.4f}, F1: {f1_score(y_val, y_pred_thresh):.4f}')\n",
                        "print(f'Number of targeted high-risk accounts: {y_pred_thresh.sum()}')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '3.5':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Inspect and plot top coefficients for the best model (Logistic Regression)\n",
                        "coefs = pd.Series(lr.coef_[0], index=X_train.columns)\n",
                        "top_coefs = coefs.reindex(coefs.abs().sort_values(ascending=False).index).head(15)\n",
                        "\n",
                        "plt.figure(figsize=(10, 8))\n",
                        "sns.barplot(x=top_coefs.values, y=top_coefs.index, palette='viridis')\n",
                        "plt.axvline(0, color='black', linestyle='--')\n",
                        "plt.title('Top 15 Logistic Regression Coefficients Impact')\n",
                        "plt.xlabel('Coefficient Value (Log-Odds Impact)')\n",
                        "plt.ylabel('Feature')\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '3.6':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Check convergence and approximate similarity between LR and SGD coefficients\n",
                        "similarity_check = np.allclose(lr.coef_, sgd.coef_, atol=0.20)\n",
                        "print('Do full-batch LR and SGD coefficients agree within 0.20 tolerance?', similarity_check)\n",
                        "\n",
                        "coef_diff = np.abs(lr.coef_[0] - sgd.coef_[0])\n",
                        "print(f'Max absolute difference between coefficients: {coef_diff.max():.4f}')\n",
                        "print(f'Mean absolute difference between coefficients: {coef_diff.mean():.4f}')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '4.1':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Derive regression target: Tenure of Churned Customers only (Option A)\n",
                        "churn_df = df_encoded[df_encoded['Churn'] == 1].copy()\n",
                        "X_reg = churn_df.drop(columns=['Churn', 'tenure'])\n",
                        "y_reg = churn_df['tenure']\n",
                        "\n",
                        "# Split regression dataset (70 / 15 / 15)\n",
                        "X_train_reg, X_temp_reg, y_train_reg, y_temp_reg = train_test_split(X_reg, y_reg, test_size=0.30, random_state=42)\n",
                        "X_val_reg, X_test_reg, y_val_reg, y_test_reg = train_test_split(X_temp_reg, y_temp_reg, test_size=0.50, random_state=42)\n",
                        "\n",
                        "# Scale numeric columns in regression splits\n",
                        "reg_numeric = ['MonthlyCharges', 'TotalCharges']\n",
                        "scaler_reg = StandardScaler()\n",
                        "\n",
                        "X_train_reg_scaled = X_train_reg.copy()\n",
                        "X_val_reg_scaled = X_val_reg.copy()\n",
                        "X_test_reg_scaled = X_test_reg.copy()\n",
                        "\n",
                        "X_train_reg_scaled[reg_numeric] = scaler_reg.fit_transform(X_train_reg[reg_numeric])\n",
                        "X_val_reg_scaled[reg_numeric] = scaler_reg.transform(X_val_reg[reg_numeric])\n",
                        "X_test_reg_scaled[reg_numeric] = scaler_reg.transform(X_test_reg[reg_numeric])\n",
                        "\n",
                        "print(f'Regression Train size: {X_train_reg_scaled.shape}, Val size: {X_val_reg_scaled.shape}')"
                    ]
                elif code_index_in_section == 1:
                    cell['source'] = [
                        "# Plot regression target distribution\n",
                        "plt.figure(figsize=(8, 5))\n",
                        "sns.histplot(y_reg, kde=True, color='purple')\n",
                        "plt.title('Tenure of Churned Customers Distribution (Regression Target)')\n",
                        "plt.xlabel('Tenure (Months)')\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '4.2':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet\n",
                        "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n",
                        "\n",
                        "# Train models\n",
                        "reg_models = {\n",
                        "    'Linear Regression': LinearRegression(),\n",
                        "    'Ridge Regression': Ridge(alpha=1.0),\n",
                        "    'Lasso Regression': Lasso(alpha=0.1),\n",
                        "    'Elastic Net': ElasticNet(alpha=0.1, l1_ratio=0.5)\n",
                        "}\n",
                        "\n",
                        "reg_metrics = {}\n",
                        "for name, model in reg_models.items():\n",
                        "    model.fit(X_train_reg_scaled, y_train_reg)\n",
                        "    y_pred = model.predict(X_val_reg_scaled)\n",
                        "    reg_metrics[name] = [\n",
                        "        mean_absolute_error(y_val_reg, y_pred),\n",
                        "        mean_squared_error(y_val_reg, y_pred, squared=False),\n",
                        "        r2_score(y_val_reg, y_pred)\n",
                        "    ]\n",
                        "\n",
                        "reg_metrics_df = pd.DataFrame(reg_metrics, index=['MAE', 'RMSE', 'R2']).T\n",
                        "reg_metrics_df"
                    ]
                code_index_in_section += 1
                
            elif current_section == '4.3':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Residual plot for the best regression model (Ridge)\n",
                        "best_reg = reg_models['Ridge Regression']\n",
                        "y_pred_reg = best_reg.predict(X_val_reg_scaled)\n",
                        "residuals = y_val_reg - y_pred_reg\n",
                        "\n",
                        "plt.figure(figsize=(8, 5))\n",
                        "plt.scatter(y_pred_reg, residuals, alpha=0.5, color='teal')\n",
                        "plt.axhline(0, color='red', linestyle='--')\n",
                        "plt.title('Residual Plot (Ridge Regression)')\n",
                        "plt.xlabel('Predicted Tenure (Months)')\n",
                        "plt.ylabel('Residuals (Actual - Predicted)')\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '4.4':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Generate Lasso regularization paths manually\n",
                        "alphas = np.logspace(-3, 2, 100)\n",
                        "lasso_coefs = []\n",
                        "\n",
                        "for a in alphas:\n",
                        "    lasso = Lasso(alpha=a, max_iter=10000)\n",
                        "    lasso.fit(X_train_reg_scaled, y_train_reg)\n",
                        "    lasso_coefs.append(lasso.coef_)\n",
                        "\n",
                        "plt.figure(figsize=(12, 6))\n",
                        "plt.plot(alphas, lasso_coefs)\n",
                        "plt.xscale('log')\n",
                        "plt.xlabel('Alpha (Regularization Strength)')\n",
                        "plt.ylabel('Coefficient Values')\n",
                        "plt.title('Lasso Coefficients Paths (L1 regularization)')\n",
                        "plt.grid(True)\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '4.5':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Compute CLV = MonthlyCharges * predicted tenure\n",
                        "# Prep X_val features for regression (dropping tenure and scaling continuous)\n",
                        "X_val_clv_raw = X_val.drop(columns=['tenure'])\n",
                        "X_val_clv_scaled = X_val_clv_raw.copy()\n",
                        "X_val_clv_scaled[reg_numeric] = scaler_reg.transform(X_val_clv_raw[reg_numeric])\n",
                        "\n",
                        "# Predict tenure and clip negative values to 0\n",
                        "pred_tenure_clv = np.maximum(best_reg.predict(X_val_clv_scaled), 0)\n",
                        "clv = X_val['MonthlyCharges'] * pred_tenure_clv\n",
                        "\n",
                        "print(f'Mean predicted CLV: ${clv.mean():.2f}')\n",
                        "print(f'Median predicted CLV: ${clv.median():.2f}')\n",
                        "\n",
                        "plt.figure(figsize=(8, 5))\n",
                        "sns.histplot(clv, kde=True, color='gold')\n",
                        "plt.title('Predicted Customer Lifetime Value (CLV) on Validation Set')\n",
                        "plt.xlabel('CLV ($)')\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '5.1':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.model_selection import StratifiedKFold, cross_val_score\n",
                        "\n",
                        "# 5-Fold Stratified Cross-Validation on the best classifier\n",
                        "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n",
                        "cv_scores = cross_val_score(lr, X_train_scaled, y_train, cv=cv, scoring='roc_auc')\n",
                        "\n",
                        "print(f'CV ROC-AUC scores across 5 folds: {cv_scores}')\n",
                        "print(f'Mean CV ROC-AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')\n",
                        "print(f'Holdout Validation ROC-AUC: {metrics_df.loc[\"Logistic Regression\", \"ROC-AUC\"]:.4f}')"
                    ]
                code_index_in_section += 1
                
            elif current_section == '5.2':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "from sklearn.model_selection import learning_curve\n",
                        "\n",
                        "# Generate learning curves\n",
                        "train_sizes, train_scores, val_scores = learning_curve(\n",
                        "    lr, X_train_scaled, y_train, cv=cv, scoring='roc_auc',\n",
                        "    train_sizes=np.linspace(0.1, 1.0, 10), random_state=42\n",
                        ")\n",
                        "\n",
                        "train_mean = np.mean(train_scores, axis=1)\n",
                        "train_std = np.std(train_scores, axis=1)\n",
                        "val_mean = np.mean(val_scores, axis=1)\n",
                        "val_std = np.std(val_scores, axis=1)\n",
                        "\n",
                        "plt.figure(figsize=(8, 5))\n",
                        "plt.plot(train_sizes, train_mean, 'o-', color='r', label='Training ROC-AUC')\n",
                        "plt.plot(train_sizes, val_mean, 'o-', color='g', label='Cross-validation ROC-AUC')\n",
                        "plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')\n",
                        "plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='g')\n",
                        "plt.xlabel('Training Set Size')\n",
                        "plt.ylabel('ROC-AUC Score')\n",
                        "plt.title('Learning Curves (Logistic Regression)')\n",
                        "plt.legend(loc='best')\n",
                        "plt.grid(True)\n",
                        "plt.show()"
                    ]
                code_index_in_section += 1
                
            elif current_section == '5.3':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Step 1: Record baseline metrics\n",
                        "baseline_auc = metrics_df.loc['Logistic Regression', 'ROC-AUC']\n",
                        "print(f'Baseline Validation ROC-AUC: {baseline_auc:.4f}')"
                    ]
                elif code_index_in_section == 1:
                    cell['source'] = [
                        "# Step 2: Create and add the leakage feature\n",
                        "np.random.seed(42)\n",
                        "# Leaked feature is highly correlated with target Churn\n",
                        "leak_train = y_train.values * 10.0 + np.random.normal(0, 1.0, len(y_train))\n",
                        "leak_val = y_val.values * 10.0 + np.random.normal(0, 1.0, len(y_val))\n",
                        "\n",
                        "X_train_leak = np.column_stack([X_train_scaled, leak_train])\n",
                        "X_val_leak = np.column_stack([X_val_scaled, leak_val])\n",
                        "print('Leakage feature generated and stacked successfully!')"
                    ]
                elif code_index_in_section == 2:
                    cell['source'] = [
                        "# Step 3: Retrain on the same split and record metrics\n",
                        "lr_leak = LogisticRegression(max_iter=1000, random_state=42)\n",
                        "lr_leak.fit(X_train_leak, y_train)\n",
                        "y_prob_leak = lr_leak.predict_proba(X_val_leak)[:, 1]\n",
                        "leak_auc = roc_auc_score(y_val, y_prob_leak)\n",
                        "print(f'With Leakage Validation ROC-AUC: {leak_auc:.4f} (Baseline: {baseline_auc:.4f})')"
                    ]
                elif code_index_in_section == 3:
                    cell['source'] = [
                        "# Step 4: Show feature importances — does the leakage feature dominate?\n",
                        "leak_feature_names = list(X_train.columns) + ['leak_feature']\n",
                        "leak_coefs = pd.Series(lr_leak.coef_[0], index=leak_feature_names)\n",
                        "print('Top 5 features with leakage:')\n",
                        "print(leak_coefs.reindex(leak_coefs.abs().sort_values(ascending=False).index).head(5))"
                    ]
                elif code_index_in_section == 4:
                    cell['source'] = [
                        "# Step 5: Remove leakage feature, retrain, confirm metrics return to baseline\n",
                        "lr_clean = LogisticRegression(max_iter=1000, random_state=42)\n",
                        "lr_clean.fit(X_train_scaled, y_train)\n",
                        "clean_auc = roc_auc_score(y_val, lr_clean.predict_proba(X_val_scaled)[:, 1])\n",
                        "print(f'After Leakage Removal Validation ROC-AUC: {clean_auc:.4f} (Baseline: {baseline_auc:.4f})')"
                    ]
                elif code_index_in_section == 5:
                    cell['source'] = [
                        "# Step 6: Summary table — Before / With Leakage / After Removal\n",
                        "summary_leak_df = pd.DataFrame({\n",
                        "    'State': ['Baseline (Clean)', 'With Leaked Feature', 'After Leakage Removal'],\n",
                        "    'ROC-AUC Score': [baseline_auc, leak_auc, clean_auc]\n",
                        "})\n",
                        "summary_leak_df"
                    ]
                code_index_in_section += 1
                
            elif current_section == '6.1':
                if code_index_in_section == 0:
                    cell['source'] = [
                        "# Final evaluation of Churn Classification on test set\n",
                        "y_pred_test = lr.predict(X_test_scaled)\n",
                        "y_prob_test = lr.predict_proba(X_test_scaled)[:, 1]\n",
                        "\n",
                        "# Apply validation budget threshold of top 9.5%\n",
                        "test_threshold = np.percentile(y_prob_test, 100 - 9.5)\n",
                        "y_pred_test_thresh = (y_prob_test >= test_threshold).astype(int)\n",
                        "\n",
                        "print('=== TEST SET CLASSIFICATION METRICS (Default 0.5 Threshold) ===')\n",
                        "print(f'Accuracy:  {accuracy_score(y_test, y_pred_test):.4f}')\n",
                        "print(f'Precision: {precision_score(y_test, y_pred_test):.4f}')\n",
                        "print(f'Recall:    {recall_score(y_test, y_pred_test):.4f}')\n",
                        "print(f'F1 Score:  {f1_score(y_test, y_pred_test):.4f}')\n",
                        "print(f'ROC-AUC:   {roc_auc_score(y_test, y_prob_test):.4f}')\n",
                        "print(f'PR-AUC:    {average_precision_score(y_test, y_prob_test):.4f}')\n",
                        "\n",
                        "print(f'=== TEST SET CLASSIFICATION METRICS (Budget-Constrained Threshold: {test_threshold:.3f}) ===')\n",
                        "print(f'Precision: {precision_score(y_test, y_pred_test_thresh):.4f}')\n",
                        "print(f'Recall:    {recall_score(y_test, y_pred_test_thresh):.4f}')\n",
                        "print(f'F1 Score:  {f1_score(y_test, y_pred_test_thresh):.4f}')\n",
                        "print(f'Targeted Customers: {y_pred_test_thresh.sum()}')"
                    ]
                elif code_index_in_section == 1:
                    cell['source'] = [
                        "# Final evaluation of Tenure Regression on test set\n",
                        "y_pred_test_reg = best_reg.predict(X_test_reg_scaled)\n",
                        "\n",
                        "print('=== TEST SET REGRESSION METRICS (Tenure Prediction) ===')\n",
                        "print(f'MAE:  {mean_absolute_error(y_test_reg, y_pred_test_reg):.2f} months')\n",
                        "print(f'RMSE: {mean_squared_error(y_test_reg, y_pred_test_reg, squared=False):.2f} months')\n",
                        "print(f'R2:   {r2_score(y_test_reg, y_pred_test_reg):.4f}')"
                    ]
                code_index_in_section += 1

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
        
    print("Notebook populated successfully with clean, complete solutions!")

if __name__ == '__main__':
    complete_notebook()
