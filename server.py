from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

logging.basicConfig(level=logging.DEBUG)

# Load student data from Excel file
try:
    df_students = pd.read_excel('students.xlsx.xlsx')
    df_students.columns = [col.lower() for col in df_students.columns]
    app.logger.info(f"Loaded student data with columns: {df_students.columns.tolist()}")
except Exception as e:
    app.logger.error(f"Error loading Excel file: {e}")
    df_students = None

@app.route('/login', methods=['POST'])
def login():
    if df_students is None:
        app.logger.error("Student data not available")
        return jsonify({'success': False, 'message': 'Student data not available'}), 500

    data = request.json
    app.logger.debug(f"Received login data: {data}")

    student_id = data.get('studentId')
    password = data.get('password')

    if not student_id or not password:
        app.logger.warning("Missing studentId or password in request")
        return jsonify({'success': False, 'message': 'Missing studentId or password'}), 400

    matched = df_students[
        (df_students['student_id'].astype(str) == str(student_id)) &
        (df_students['password'].astype(str) == str(password))
    ]

    if not matched.empty:
        app.logger.info(f"Login successful for studentId: {student_id}")
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        app.logger.info(f"Invalid credentials for studentId: {student_id}")
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
