import pandas as pd
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import dash
from dash import dcc, html
import os
import re

# Load names of csv files to create dictionary
csv_load = [csv for csv in os.scandir("relationship_csvs") if ".csv" in csv.name]

# Load relationship data for each book into a dictionary
book_relationships = {}
for idx in range(len(csv_load)):
    csv_name = re.sub(r'\.csv', '', csv_load[idx].name)
    book_relationships[f'{csv_name}'] = pd.read_csv(csv_load[idx])

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.Label('Select a book:'),
    dcc.Dropdown(
        id='book-dropdown',
        options=[
            {'label': book, 'value': book} for book in book_relationships.keys()
        ],
        value=f'{csv_name}',  # Set the default value
    ),
    html.Iframe(id='pyvis-graph', width='100%', height='800px')
])

# Callback to update the PyVis graph based on book selection
@app.callback(
    dash.dependencies.Output('pyvis-graph', 'srcDoc'),
    [dash.dependencies.Input('book-dropdown', 'value')]
)
def update_pyvis_graph(selected_book):
    df = book_relationships[selected_book]
    
    # Create a graph from a pandas dataframe
    plt.figure(figsize=(30,30))
    G = nx.from_pandas_edgelist(df, 
                                source = "source", 
                                target = "target",                                
                                create_using = nx.Graph())

    nt = Network(height='800px', width='100%', bgcolor='#222222', font_color='white')
    nt.from_nx(G)

    html_content = nt.generate_html()
    return html_content

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
