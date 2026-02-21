# ============================================
# Railway Track Event Detection Project:
# Filip Drincic, LTU.Course: Industrial AI
# Goal: Detect transient railway impact events using extracted signal features. Binary classification: normal (0) vs impact/event (1)
#
# Pseudocode:
# 1. Import python libraries
#    Scikit-learn was used to implement preprocessing, classification, feature selection, and evaluation steps due 
#    to its reliability and comprehensive machine learning tools
# 2. Load data from 3 CSV files and combine into one unified dataset
# 3. Remove unnecessary columns and convert event column to binary
# 4. Data Preprocessing (feature separation) + label mapping + data normalization
# 5. 80/20 Data split + 5-fold cross-validation (SVM)
# 6. Simple Feature selection (Correlation, Chi-square, RFE, RF importance)
# 7. Extras: Plots (confusion matrices, CV plot, correlation heatmap, RF importance plot)
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Machine Learning Libraries (scikit-learn)
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_selection import SelectKBest, chi2, RFE
from sklearn.ensemble import RandomForestClassifier


# LOAD DATA (LTU csv files)

print("Current working directory:", os.getcwd())  # for troubleshooting purpose

df1 = pd.read_csv("trail1.csv")
df2 = pd.read_csv("trail2.csv")
df3 = pd.read_csv("trail3.csv")

# Combine datasets into one unified dataset
df = pd.concat([df1, df2, df3], ignore_index=True)
print("Dataset shape:", df.shape)


# DATA PREPROCESSING

# Remove unnecessary columns
columns_to_remove = ['start_time', 'axle', 'cluster', 'tsne_1', 'tsne_2']
df = df.drop(columns=columns_to_remove, errors='ignore')

# Map labels to binary label: normal -> 0, all other events -> 1
df['event'] = df['event'].apply(lambda label: 0 if label == 'normal' else 1)

print("Event distribution:")
print(df['event'].value_counts())

# Separate features (X) and label (y)
X_features = df.drop('event', axis=1)
y_target = df['event']


# DATA NORMALIZATION + TRAIN/TEST SPLIT

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_features)

# Split dataset (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_target,
    test_size=0.2,
    random_state=42,
    stratify=y_target
)

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print(f"Train size: {len(y_train)} samples")
print(f"Test size:  {len(y_test)} samples")


# K-FOLD CROSS VALIDATION (SVM on training set)

svm_cv = SVC(kernel="rbf", random_state=42)
cv_scores_train = cross_val_score(svm_cv, X_train, y_train, cv=5)

print("\n--- 5-Fold Cross Validation (SVM on training set) ---")
print("CV Scores:", cv_scores_train)
print("Mean CV Accuracy:", cv_scores_train.mean())
print("Standard Deviation:", cv_scores_train.std())


# TRAIN SVM (80/20 split) + RESULTS

svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

print("\n--- 80/20 Split Results (SVM) ---")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# PLOT — CONFUSION MATRIX (SVM)

cm = confusion_matrix(y_test, y_pred)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix (SVM)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.xticks([0, 1], ["Normal (0)", "Event (1)"])
plt.yticks([0, 1], ["Normal (0)", "Event (1)"])
plt.tight_layout()
plt.show()


# PLOT — CV ACCURACY PLOT

folds = np.arange(1, len(cv_scores_train) + 1)
mean_score = np.mean(cv_scores_train)
std_score = np.std(cv_scores_train)

plt.figure(figsize=(8, 5))
plt.plot(folds, cv_scores_train, marker='o', linewidth=2, label="Fold Accuracy")
plt.axhline(mean_score, linestyle='--', label=f"Mean = {mean_score:.3f}")

plt.fill_between(
    folds,
    mean_score - std_score,
    mean_score + std_score,
    alpha=0.2,
    label=f"±1 Std ({std_score:.3f})"
)

for fold_idx, acc in zip(folds, cv_scores_train):
    plt.text(fold_idx, acc + 0.005, f"{acc:.3f}", ha='center')

plt.title("5-Fold Cross Validation Accuracy (SVM)")
plt.xlabel("Fold Number")
plt.ylabel("Accuracy")
plt.xticks(folds)
plt.ylim(0.88, 1.01)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()


# CORRELATION HEATMAP + PEARSON CORRELATION

# Compute correlation matrix (numeric only). Includes "event" column so we can see which features correlate with the label
corr_matrix = df.corr(numeric_only=True)

plt.figure(figsize=(11, 8))
plt.imshow(corr_matrix, aspect='auto')
plt.title("Correlation Heatmap (Features + Event)")
plt.colorbar()

cols = corr_matrix.columns.tolist()
plt.xticks(range(len(cols)), cols, rotation=90)
plt.yticks(range(len(cols)), cols)
plt.tight_layout()
plt.show()

# Print top correlations with "event"
pearson_corr = corr_matrix["event"].abs().sort_values(ascending=False)

print("\n--- RESULTS: Top Pearson Correlations with Event ---")
print(pearson_corr.head(10))


# FEATURE SELECTION

print("\n==============================")
print("FEATURE SELECTION METHODS")
print("==============================")

# A. Pearson Correlation (Filter).Using previously computed pearson_corr.
print("\nTop correlated features (Pearson):")
print(pearson_corr.drop("event").head(10))

# B. Chi-Square (Filter) — requires non-negative values, so MinMaxScaler is used
minmax_scaler = MinMaxScaler()
X_minmax = minmax_scaler.fit_transform(X_features)

chi_selector = SelectKBest(chi2, k=10)
chi_selector.fit(X_minmax, y_target)  
chi_features = X_features.columns[chi_selector.get_support()]

print("\nChi-Square Selected Features:")
print(list(chi_features))

# C. Recursive Feature Elimination-RFE (Wrapper) — linear SVM ranks features
svm_linear = SVC(kernel='linear')
rfe = RFE(svm_linear, n_features_to_select=10)
rfe.fit(X_scaled, y_target)  
rfe_features = X_features.columns[rfe.support_]

print("\nRFE Selected Features:")
print(list(rfe_features))

# D. Random Forest Importance (Embedded)
rf = RandomForestClassifier(random_state=42)
rf.fit(X_scaled, y_target)

importances = pd.Series(rf.feature_importances_, index=X_features.columns).sort_values(ascending=False)

print("\nTop Random Forest Important Features:")
print(importances.head(10))


# PLOT — RANDOM FOREST FEATURE IMPORTANCE

top_n = 10
top_features = importances.head(top_n)

plt.figure(figsize=(8, 5))
plt.bar(top_features.index, top_features.values)
plt.title(f"Top {top_n} Feature Importances (Random Forest)")
plt.xlabel("Feature")
plt.ylabel("Importance")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# RANDOM FOREST MODEL EVALUATION (80/20)

# Reuse the same X_scaled and y_target for consistency
X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(
    X_scaled, y_target,
    test_size=0.2,
    random_state=42,
    stratify=y_target
)

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_rf, y_train_rf)
rf_pred = rf_model.predict(X_test_rf)

print("\n--- 80/20 Split Results (Random Forest) ---")
print("Accuracy:", accuracy_score(y_test_rf, rf_pred))
print(classification_report(y_test_rf, rf_pred))

cm_rf = confusion_matrix(y_test_rf, rf_pred)

plt.figure()
plt.imshow(cm_rf)
plt.title("Confusion Matrix (Random Forest)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()

for i in range(cm_rf.shape[0]):
    for j in range(cm_rf.shape[1]):
        plt.text(j, i, cm_rf[i, j], ha="center", va="center")

plt.xticks([0, 1], ["Normal (0)", "Event (1)"])
plt.yticks([0, 1], ["Normal (0)", "Event (1)"])
plt.tight_layout()
plt.show()


# RETRAIN SVM WITH SELECTED FEATURES (RFE)

# Train SVM again using only the features selected by RFE. This often improves accuracy by removing noisy/unimportant features.

X_selected = df[rfe_features]
X_selected_scaled = StandardScaler().fit_transform(X_selected)

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_selected_scaled, y_target,
    test_size=0.2,
    random_state=42,
    stratify=y_target
)

svm_model2 = SVC(kernel='rbf', random_state=42)
svm_model2.fit(X_train2, y_train2)
y_pred2 = svm_model2.predict(X_test2)

print("\n--- SVM After Feature Selection (RFE) ---")
print("Accuracy:", accuracy_score(y_test2, y_pred2))
print(classification_report(y_test2, y_pred2))

print("\nProject completed successfully.")