import json
import csv

# Define different task templates
task_templates = {
    "static view": """Now you have the dataset in CSV format: {dataset_description}
Your task is to {task_description}
Use the following visualization library: {library}.
Use the following format:
code: (The code should be complete. And the HTML structure and code should be merged together.)
Please provide only the codes written in the specified library with no other words.""",

    "interactive view": """Now you have the dataset in CSV format: {dataset_description}
Your task is to {task_description}
Use the following visualization library: {library}.
Use the following format:
code: (The code should be complete. And the HTML structure and code should be merged together.)
Please provide only the codes written in the specified library with no other words.""",

    "multiple view": """Now you have the dataset in CSV format: {dataset_description}
Your task is to {task_description}
Use the following visualization library: {library}.
Use the following format:
code: (The code should be complete. And the HTML structure and code should be merged together.)
Please provide only the codes written in the specified library with no other words."""
}


def generate_prompts(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    prompts = []

    # Retrieve attributes, task descriptions, view type, and library
    attributes = config.get("ATTRIBUTE", {})
    chart_types = config.get("CHART TYPE", {})
    library = config.get("LIBRARY", "D3")
    view_type = config.get("VIEW_TYPE", "static view")  # Assuming VIEW_TYPE is provided in the config
    tasks = config.get("TASK", [])
    dataset_description = config.get("dataset_description", "")

    # Get the task template based on the view type
    task_template = task_templates.get(view_type, task_templates["static view"])

    # Define hints for different libraries
    hints = {
        "D3": "Hint: You can use the `d3.csv()` function to load data; when iterating over the data and converting data types, be sure to use square brackets to access property names that contain special characters (such as spaces or symbols).",
        "ECharts": "Hint: You can use the fetch() function to load data.",
        "Vega-Lite": "You can use \"data\": { \"url\": } format to load data. Ensure that all libraries (e.g., Vega, Vega-Lite, Vega-Embed) are compatible versions to prevent runtime issues. "
    }

    # Generate the prompts using task descriptions
    for task in tasks:
        placeholder_mapping = {**attributes, **chart_types}

        # Format task description with chart types and attributes
        task_description = task.format(**placeholder_mapping)

        # Create the full prompt by formatting the task template
        prompt_body = task_template.format(
            dataset_description=dataset_description,
            task_description=task_description,
            library=library
        )

        # Add hint outside the task template based on the library type
        hint = hints.get(library, "")
        prompt = f"{prompt_body}\n{hint}"

        prompts.append(prompt)

    return prompts


def load_config(config_file):
    # Use json to read the local config.json file
    with open(config_file, 'r') as file:
        data = json.load(file)
    return data


def generate_title(view_type, prompt):
    # Case-insensitive
    prompt_lower = prompt.lower()

    # Define chart types and interaction keywords for different views
    chart_keywords = {
        'static view': ["stacked bar chart", "horizontal bar chart", "bar chart", "scatterplot",
                        "line chart", "pie chart", "donut chart", "coxcomb chart",
                        "radar chart", "streamgraph", "slopegraph", "heatmap"],
        'interactive view': ["scatterplot", "line chart", "bar chart", "pie chart", "donut chart", "coxcomb chart",
                          "radar chart", "streamgraph", "slopegraph", "heatmap"],
        'multiple view': ["scatterplot", "bar chart", "line chart", "pie chart", "matrix", "table"]
    }

    interaction_keywords = {
        'interactive view': ["brush", "zoom", "highlight", "tooltip", "animated", "query widgets", "drag"],
        'multiple view': ["brushing and linking", "highlight", "minimap"]
    }

    # Extract chart types
    chart_types = [chart for chart in chart_keywords.get(view_type, []) if chart in prompt_lower]
    interactions = [interaction for interaction in interaction_keywords.get(view_type, []) if
                    interaction in prompt_lower]

    # Generate title based on extracted chart types and interactions
    if view_type == "static view" and chart_types:
        title = "+".join(chart_types[:1])
    elif view_type == "interactive view" and chart_types:
        title = f"{chart_types[0]}+{interactions[0]}" if interactions else chart_types[0]
    elif view_type == "multiple view" and chart_types:
        title = "+".join(chart_types[:2] + interactions[:1])
    else:
        title = "Custom Visualization"  # Default title

    return title


def save_prompts_to_csv(prompts, csv_file):
    fieldnames = ["Prompt Number", "title", "Prompt", "dataset", "library", "view_type"]

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for prompt in prompts:
            writer.writerow(prompt)
