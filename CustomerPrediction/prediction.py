import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

data = {
    'MonthlyCharge': [50, 80, 70, 40, 90, 60, 100, 85, 45, 75],
    'ContractLength': [12, 6, 24, 12, 3, 18, 24, 6, 12, 18],
    'Age': [30, 25, 40, 35, 28, 50, 45, 32, 29, 55],
    'Churn': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0]   # 0 = No Churn, 1 = Churn
}

df = pd.DataFrame(data)

X = df[['MonthlyCharge', 'ContractLength', 'Age']]
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("\nModel Evaluation")
print("-------------------------")
print("Accuracy:", accuracy)

print("\nConfusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(class_report)

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)