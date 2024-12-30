import json
from collections import OrderedDict
import re

# Function to extract attributes from the dataset description
def extract_attributes(dataset_description):
    # Use regex to find the part after "The dataset contains the following information:"
    match = re.search(r"The data table contains the following columns: (.*)", dataset_description)
    if match:
        # Split the found attributes by comma and return the list
        attributes = match.group(1).split(',')
        # Strip any extra whitespace from each attribute
        attributes = [attr.strip() for attr in attributes]
        return attributes
    else:
        return []

# Function to create the configuration file based on user input
def generate_config(dataset_description, library='d3', view_type='static view'):
    # Extract attributes from the dataset description
    attributes = extract_attributes(dataset_description)

    # Pad the attributes list with None if there are fewer than 4 attributes
    while len(attributes) < 4:
        attributes.append(None)

    config = OrderedDict()
    # Extract the first four attributes as default
    config = OrderedDict({
        "dataset_description": dataset_description,
        "LIBRARY": library,
        "ATTRIBUTE": OrderedDict({
            "Categorical Attribute": attributes[1] if attributes[1] else 'None',  # Default: first attribute or None
            "Temporal Attribute": attributes[0] if attributes[0] else 'None',     # Default: second attribute or None
            "Numerical Attribute1": attributes[2] if attributes[2] else 'None',   # Default: third attribute or None
            "Numerical Attribute2": attributes[3] if attributes[3] else 'None',    # Default: fourth attribute or None
            "Existing_Temporal_Value": "Q2-2021"
        })
    })

    # Define default chart types based on view type
    if view_type == 'static view':
        config["CHART TYPE"] = OrderedDict({
            "Chart1": "Scatterplot",
            "Chart2": "Line Chart",
            "Chart3": "Bar Chart",
            "Chart4": "Pie Chart",
            "Chart5": "Donut Chart",
            "Chart6": "Coxcomb Chart(polar area chart)",
            "Chart7": "Radar Chart",
            "Chart8": "Streamgraph",
            "Chart9": "Slopegraph",
            "Chart10": "Heatmap",
            "Chart11": "Stacked Bar Chart",
            "Chart12": "Horizontal Bar Chart"
        })

        # Static view task descriptions for 12 different chart types
        config["TASK"] = [
            "create a {Chart1} that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}.",
            "create a {Chart2} that visualizes the trend of {Numerical Attribute1} over the {Temporal Attribute} for each {Categorical Attribute}.",
            "create a {Chart3} that visualizes the {Numerical Attribute1} for each {Categorical Attribute} in {Existing_Temporal_Value}.",
            "create a {Chart4} that visualizes the proportion of {Numerical Attribute1} contributed by each {Categorical Attribute} in {Existing_Temporal_Value}.",
            "create a {Chart5} that visualizes the distribution of {Numerical Attribute1} among {Categorical Attribute} in {Existing_Temporal_Value}.",
            "create a {Chart6} to compare the {Numerical Attribute1} of different {Categorical Attribute} in {Existing_Temporal_Value}.",
            "create a {Chart7} to compare the {Numerical Attribute1} of different {Categorical Attribute} in {Existing_Temporal_Value}.",
            "create a {Chart8} that visualizes the changes of {Numerical Attribute1} over the {Temporal Attribute} for each {Categorical Attribute}.",
            "create a {Chart9} to compare the {Numerical Attribute1} between Q1-2020 and Q2-2020 for each Education Level.",
            "create a {Chart10} that visualizes the {Numerical Attribute1} across {Categorical Attribute} and {Temporal Attribute}s.",
            "create a {Chart11} that visualizes the given data table.",
            "create a {Chart12} that visualizes the {Numerical Attribute1} for each {Categorical Attribute} in {Existing_Temporal_Value}."
        ]

    elif view_type == 'interactive view':
        config["CHART TYPE"] = OrderedDict({
            "Chart1": "Scatterplot",
            "Chart2": "Line Chart",
            "Chart3": "Bar Chart"
        })

        # Interactive view task descriptions
        config["TASK"] = [
            "create a {Chart1} that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}. And add the following interactive function: when the mouse hovers over a specific data point, the value of the data point will be highlighted on the axis.",
            "create a {Chart1} that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}. And add the following interactive functions: Brushing this {Chart1} will show the selected data points.",
            "create a {Chart1} that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}. And add the following interactive functions: the {Chart1} can be zoomed via the mouse wheel.",
            "create a {Chart1} with external links and tooltips that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}. And add the following interactive functions: opening a Google search for the point that you click on.",
            "create a {Chart1} with query widgets showing the {Numerical Attribute1} and {Numerical Attribute2} of the given dataset. Add a slider to represent the {Temporal Attribute}.",
            "create a {Chart1} showing the {Numerical Attribute1} of Graduate. Add animated transitions that connect these points using lines in order.",
            "create a multi-series {Chart2} with an interactive line highlight showing the {Numerical Attribute1} of the given dataset. Add the following interaction function: when the mouse is hovered over a line, the line will be highlighted.",
            "create a {Chart3} that visualizes the {Numerical Attribute1} for each {Categorical Attribute} in {Existing_Temporal_Value}. And add the following interactive functions: scroll the mouse wheel to zoom the {Chart3}, click the left mouse button and drag to pan the {Chart3}.",
            "create a {Chart3} that visualizes the {Numerical Attribute1} for each {Categorical Attribute} in {Existing_Temporal_Value}. Add the following interactive functions: allows users to drag and drop bars to reorder them, enabling a customized arrangement based on user preferences.",
            "create a {Chart3} that visualizes the {Numerical Attribute1} for each {Categorical Attribute} in {Existing_Temporal_Value}. Add animated transitions and use the drop-down menu to change the sorting order to ascending or descending based on the {Numerical Attribute1}."
        ]

    elif view_type == 'multiple view':
        config["CHART TYPE"] = OrderedDict({
            "Chart1": "Scatterplot",
            "Chart2": "Line Chart",
            "Chart3": "Bar Chart",
            "Chart4": "Pie Chart",
            "Chart5": "Scatterplot Matrix"
        })

        # Multiple view task descriptions
        config["TASK"] = [
            "draw a visual interface consisting of two charts, a {Chart1} on the left that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}, and a {Chart3} on the right that displays {Categorical Attribute} versus {Numerical Attribute1}.",
            "draw a visual interface consisting of two charts, a {Chart1} on the left that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}, and a {Chart3} on the right that displays {Categorical Attribute} versus {Numerical Attribute1}. Enable brushing and linking functionality to enhance interactivity. Add the following interactive features: swipe to select a set of points in the {Chart1}, and the corresponding data in the {Chart3} will be highlighted.",
            "draw a visual interface consisting of two charts, a line chart on the top and a pie chart on the bottom, the line chart positioned above the pie chart. The line chart should display the trend of {Numerical Attribute1} , while the pie chart represents the distribution of {Numerical Attribute2}.",
            "draw a visual interface consisting of two charts, a line chart on the top and a pie chart on the bottom, the line chart positioned above the pie chart. The line chart should display the trend of {Numerical Attribute1} , while the pie chart represents the distribution of {Numerical Attribute2}. Enable brushing and linking functionality to enhance interactivity. Add the following interactive function: select a subset of data points in the line chart, which will dynamically update the pie chart to reflect the distribution of {Numerical Attribute2} for the selected group.",
            "draw a brushable {Chart5} that visualizes the pairwise relationships between Enrollment Number, Revenue, and Profit. Add the following interactive functions: brush to select data points in one cell and highlight them across all other cells.",
            "create a brushable {Chart1} that visualizes the relationship between {Numerical Attribute1} and {Numerical Attribute2}. Add the following interactive functions: Drag the rectangular brush to draw a table on the right side of the {Chart1} that shows the information of the selected points (the first 20).",
            "create a horizontal {Chart3} that shows all the data concerning {Numerical Attribute1}, with a smaller overview representation (called a minimap) displayed on the right."
        ]

    return config