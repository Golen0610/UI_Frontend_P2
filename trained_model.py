import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
df = pd.read_csv('csv/Students_Grading_Dataset.csv')

# Rename columns to match expected names
df = df.rename(columns={
    'Study_Hours_per_Week': 'study_hours',
    'Sleep_Hours_per_Night': 'sleep_hours',
    'Attendance (%)': 'attendance',
    'Participation_Score': 'participation'
})

# Convert Grade to Pass/Fail
df['result'] = df['Grade'].apply(lambda grade: 'Pass' if grade in ['A', 'B', 'C'] else 'Fail')

# Confirm required columns
expected_cols = ['study_hours', 'sleep_hours', 'attendance', 'participation', 'result']
if not all(col in df.columns for col in expected_cols):
    raise ValueError(f"Dataset must contain these columns: {expected_cols}")

# Convert result to binary
df['result'] = df['result'].map({'Fail': 0, 'Pass': 1})

# Feature matrix and target
X = df[['study_hours', 'sleep_hours', 'attendance', 'participation']]
y = df['result']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs('trained_data', exist_ok=True)
joblib.dump(model, 'trained_data/student_model.pkl')

print("✅ Model trained and saved to 'trained_data/student_model.pkl'")
