from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load trained classification model
student_model = joblib.load('trained_data/student_model.pkl')  # adjust if needed

@app.route('/predict', methods=['POST'])
def predict_pass_fail():
    data = request.json

    # Extract input features
    study_hours = data.get('study_hours')
    sleep_hours = data.get('sleep_hours')
    attendance = data.get('attendance')
    participation = data.get('participation')

    # Check for missing fields
    missing_fields = [field for field in ['study_hours', 'sleep_hours', 'attendance', 'participation'] if data.get(field) is None]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Create input DataFrame
    input_df = pd.DataFrame([{
        'study_hours': study_hours,
        'sleep_hours': sleep_hours,
        'attendance': attendance,
        'participation': participation
    }])

    # Predict pass or fail
    prediction = student_model.predict(input_df)[0]
    result = 'Pass' if prediction == 1 else 'Fail'

    return jsonify({
        "study_hours": study_hours,
        "sleep_hours": sleep_hours,
        "attendance": attendance,
        "participation": participation,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
