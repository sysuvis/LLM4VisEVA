import os
import time
import pandas as pd
from openai import OpenAI
from config import API_KEY
from flask import Flask, render_template, request, jsonify, send_file
from generate_config import generate_config
from generate_prompt import generate_prompts, save_prompts_to_csv, generate_title
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
EVALUATION_FOLDER = 'evaluations'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['EVALUATION_FOLDER'] = EVALUATION_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(EVALUATION_FOLDER, exist_ok=True)


# Set OpenAI API key
client = OpenAI(api_key= API_KEY)

# Route to the homepage
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_config', methods=['POST'])
def generate_config_route():
    data = request.get_json()
    dataset_description = data.get('dataset_description')
    library = data.get('library')
    view_type = data.get('view_type')

    config = generate_config(dataset_description, library, view_type)

    return app.response_class(
        response=json.dumps(config, indent=4),  # Manually dump the OrderedDict
        mimetype='application/json'
    )

@app.route('/save_config', methods=['POST'])
def save_config_route():
    config_file = request.get_json().get('config_file')

    with open('config.json', 'w') as f:
        json.dump(config_file, f, indent=4)

    return jsonify({'message': 'Config file saved successfully!'})


@app.route('/download_prompts', methods=['POST'])
def download_prompts():
    config_file = 'config.json'
    prompts = generate_prompts(config_file)
    data = request.get_json()
    dataset_description = data.get('dataset_description')
    library = data.get('library')
    view_type = data.get('view_type')

    if not library:
        return jsonify({'error': 'Library not found in config'}), 400
    if not view_type:
        return jsonify({'error': 'View type not found in config'}), 400

    view_type_safe = view_type.replace(" ", "_").lower()
    library_safe = library.replace(" ", "_").lower()

    csv_file = f"prompts_{view_type_safe}_{library_safe}_{int(time.time())}.csv"

    prompts_details = [{"Prompt Number": i+1,
                            "title": generate_title(view_type, prompt),
                            "Prompt": prompt,
                            "dataset": dataset_description,
                            "library": library,
                            "view_type": view_type}
                           for i, prompt in enumerate(prompts)]
    
    save_prompts_to_csv(prompts_details, csv_file)
    
    return send_file(csv_file, as_attachment=True, download_name=csv_file)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    df = pd.read_csv(file_path)

    responses = []
    for index, row in df.iterrows():
        prompt = row['Prompt']
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096
            )
            html_response = response.choices[0].message.content
            responses.append(html_response)
            df.at[index, 'response'] = html_response
        except Exception as e:
            responses.append(f"Error: {str(e)}")
            df.at[index, 'response'] = f"Error: {str(e)}"

    result_filename = f"responses_{file.filename}"
    result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
    df.to_csv(result_path, index=False)

    return jsonify({"responses": responses, "response_filename": result_filename})


@app.route('/results/<filename>', methods=['GET'])
def download_file(filename):
    result_path = os.path.join(app.config['RESULT_FOLDER'], filename)
    if os.path.exists(result_path):
        return send_file(result_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(port=1234,debug=True)