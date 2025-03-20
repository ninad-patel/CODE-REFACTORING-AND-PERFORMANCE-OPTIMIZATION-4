from flask import Flask, render_template, request, jsonify
import os
import time
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'refactor'))

from refactor import refactor_code, analyze_performance


app = Flask(__name__)

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle code file upload and refactoring
@app.route('/refactor', methods=['POST'])
def refactor():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Refactor the code
    start_time = time.time()
    refactored_code, report = refactor_code(file_path)
    end_time = time.time()
    
    # Analyze performance improvements
    performance_report = analyze_performance(file_path, refactored_code, start_time, end_time)
    
    return jsonify({
        'refactored_code': refactored_code,
        'performance_report': performance_report
    })

if __name__ == '__main__':
    app.run(debug=True)
