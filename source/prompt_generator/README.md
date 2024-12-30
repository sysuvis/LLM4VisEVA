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

* **data**: The CIFAR-10 dataset and the SCH dataset that we sampled and cleaned.
* **demo**: The demo for interactive ordering across scale and metric using the CIFAR-10 dataset.
* **nets**: The model implementation of VON.
* **pretrained**: The models with trained parameters, that you can use in testing.
* **problems**: The definition of ordering task, including the dataset (input), metric definition, and other utility functions.
* **utils**: The utility functions for training, testing, logging, saving files, and loading parameters.

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







```commandline
def moransi(d):
       ...
       return ...
```

2. To make the metric available in the option list, you may add the metric into the ```get_costs``` function in **problems/order/problem_order.py**. Here is an example:

```commandline
...
elif metric == 'moransI':
       ret_res = torch.zeros(d.size(0))
       for a in range(d.size(0)):
              ret_res[a] = 1 - moransi(d[a, :, :])
       return ret_res, None
```

**Note**: You may need to convert the metric (larges is better) to a loss (smaller is better). Here we use ```1 - moransi(d[a, :, :])```.

### Inferencing

Options:
--```dataset```: the dataset, e.g.,  'CIFAR10', 'fashionmnist';
--```sample_size```: the number of points to be ordered (>=2), e.g. 20, 50, 100...;
--```model```: the trained model used for ordering.

1. Move the trained model to target file(eg. pretrained/)
2. Run: eg.``` python eval.py --model 'pretrained/CIFAR-TSP' --run_mode 'test' --dataset 'CIFAR10' --sample_size 50 ```
   All the options of command can be replaced following your needs.

### Running the interactive demo

1. Start the server for the demo using ```python .\flaskfordemo.py```.
2. Extract the zip package in the **demo/cifar10** folder and use a browser to open **panel.html** in the **/demo** folder to start the front end. Set the path like: **demo/cifar10/images256/...jpg**.
3. Choose a metric in the dropdown list in the top left corner, e.g., 'Moran's I', 'TSP'. The default is 'TSP'.
4. Brush points in the scatter plot on the left, and view the ordered images on the right.

This demo is a quick way to test the performance of VON. You can reproduce the figure 2 in the appendix of our paper by brushing the scatter plot in the same area.