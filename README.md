# LLM4VisEVA
# Can Large Languages Models Write Visualization Codes? An Evaluation

This repository contains the code package for the paper "Can Large Languages Models Write Visualization Codes? An Evaluation".

## Dependencies

* Python>=3.10
* openai
* flask
* pandas
* os
* json

## Files

### folders

* **prompts**: The prompts files we use in our evaluation.
* **response**: The response files generated by LLMs.
* **evaluation**: The files that contains all our evaluation results.
* **demo**: The demo for interface demonstration, you can use them to try out the interface features.
* **source**: The source code files that implement the interfaces of Prompt Generator and Response Evaluator.
* **report**: The report files that contain all the evaluation results of LLMs we have previously tested.

### sources

* **Prompt Generator**
  * **app.py**: The code to run the server. You need to specify the IP address. If you are running the server locally, you may use "local_host" or "127.0.0.1".
  * **generate_config.py**: The code to generate the configuration file for the visualization tasks.
  * **generate_prompt.py:** The code to generate all the prompts and the task classification information.
  * **config.py:** Provide your API key.
  * **templates & static:** These are the front-end files that manage the user interface. 
* **Response Evaluator** 
  * **app.py**: The code to run the server.
  * **templates & static:** These are the front-end files that manage the user interface.


## Usage

### Prompt Generator

1. Install the required dependencies.
2. Provide your API key in the `API_KEY = 'your_api_key'` section of the **source/prompt_generator/config.py** file.
3. Set the models' names and parameters required for evaluation in the ```upload_file()``` function in **source/prompt_generator/app.py**. Here is an example for setting:

```commandline
...
response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096
            )
...
```

​	4. Run the **flask server** with ``python app.py``, the port is "1234" and you can change it too.

**Note**: Please make sure you have enough balance in your account to call the API of LLMs.

### Response Evaluator

1. Install the required dependencies and run the **flask server** with ``python app.py``. 

```
response_evaluator>python app.py

 * Serving Flask app 'app'
 * Debug mode: on
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5678
```

​	2. Open the **web interface** to evaluate the response.

​	3. **(Option 1)** Upload files that does not yet contain evaluation results to make a new evaluation.

​	4. **(Option 2)** Upload files that already contains evaluation results to view a previous evaluation or modify the results.

**Note**: Please make sure you have evaluated **each** response before submitting your results.
