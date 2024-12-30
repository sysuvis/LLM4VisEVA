import os
import pandas as pd
from openai import OpenAI
from config import API_KEY
from flask import Flask, render_template, request, jsonify, send_file, abort

app = Flask(__name__)

RESULT_FOLDER = 'results'
FINAL_FOLDER = 'final'
MERGED_FILE = 'merged_responses.csv'

app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)

# Set up OpenAI client
client = OpenAI(api_key=API_KEY)


# Route to the homepage
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    files = request.files.getlist('files')
    merged_df = pd.DataFrame()

    for file in files:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)

            if 'Prompt Number' in df.columns:
                df = df.drop(columns=['Prompt Number'])

            if 'evaluation' in df.columns:
                df['evaluation'] = df['evaluation'].fillna('').astype(str)
            else:
                df['evaluation'] = ''

            merged_df = pd.concat([merged_df, df], ignore_index=True)

    merged_df['originalIndex'] = merged_df.index
    merged_df['Prompt Number'] = range(1, len(merged_df) + 1)
    merged_df['evaluation'] = merged_df['evaluation'].fillna('').astype(str)
    merged_filename = os.path.join(app.config['RESULT_FOLDER'], MERGED_FILE)
    merged_df.to_csv(merged_filename, index=False)

    responses = merged_df.to_dict(orient='records')

    return jsonify({
        'response_filename': MERGED_FILE,
        'responses': responses
    })


@app.route('/view_response')
def view_response():
    try:
        index = int(request.args.get('index', 0))
        csv_path = os.path.join(app.config['RESULT_FOLDER'], MERGED_FILE)

        df = pd.read_csv(csv_path)

        if index < 0 or index >= len(df):
            return abort(404, description="Response not found")

        prompt = df.loc[index, 'Prompt']
        response_html = df.loc[index, 'response']

        return render_template('code_preview.html', prompt=prompt, response_html=response_html)

    except Exception as e:
        print(f"Error: {e}")
        return abort(500, description="Internal server error")


@app.route('/submit_evaluation', methods=['POST'])
def submit_evaluation():
    data = request.json
    evaluations = data.get('evaluations', [])
    response_filename = data.get('responseFilename', MERGED_FILE)

    print("Received evaluations:", evaluations)

    if not evaluations:
        return jsonify({'error': 'No evaluations provided'}), 400

    csv_path = os.path.join(RESULT_FOLDER, response_filename)
    df = pd.read_csv(csv_path)

    if 'evaluation' not in df.columns:
        df['evaluation'] = ''
    else:
        df['evaluation'] = df['evaluation'].fillna('').astype(str)

    for evaluation in evaluations:
        response_index = evaluation.get('responseIndex')
        eval_options = evaluation.get('evaluation', [])

        if response_index is None:
            print("Warning: responseIndex is None, skipping this evaluation.")
            continue

        if not isinstance(response_index, int):
            print(f"Warning: responseIndex {response_index} is not an integer, skipping.")
            continue

        if not (0 <= response_index < len(df)):
            print(f"Warning: responseIndex {response_index} out of range, skipping.")
            continue

        eval_string = ', '.join(eval_options)
        df.at[response_index, 'evaluation'] = eval_string

    df.to_csv(csv_path, index=False)

    return jsonify({'message': 'Evaluation submitted and saved!'})


@app.route('/finalize/<filename>', methods=['GET'])
def finalize_file(filename):

    final_path = os.path.join(FINAL_FOLDER, filename)
    csv_path = os.path.join(RESULT_FOLDER, filename)
    df = pd.read_csv(csv_path)
    df.to_csv(final_path, index=False)

    return send_file(final_path, as_attachment=True)


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['RESULT_FOLDER'], filename), as_attachment=True)


@app.route('/evaluation_chart')
def evaluation_chart():
    csv_path = os.path.join(FINAL_FOLDER, MERGED_FILE)
    if not os.path.exists(csv_path):
        return abort(404, description="No data available")

    df = pd.read_csv(csv_path)
    if 'evaluation' not in df.columns:
        return abort(404, description="No evaluations available")

    data = df.to_dict(orient='records')

    for record in data:
        if 'response' in record:
            del record['response']

    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5678, debug=True)