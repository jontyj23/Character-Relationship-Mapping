import pandas as pd
from pyvis.network import Network
import dash
from dash import Dash, dcc, html
import os
import re

# Load names of csv files to create dictionary
csv_load = [csv for csv in os.scandir("relationship_csvs") if ".csv" in csv.name]

# Load relationship data for each book into a dictionary
book_relationships = {}
for idx in range(csv_load):
    csv_name = re.sub(r'\.csv', '', csv_load[idx])
    book_relationships[f'{csv_name}'].append(pd.read_csv(csv_load))

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
        value='Book1',  # Set the default value
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

    net = Network(height='800px', width='100%')
    net.barnes_hut()

    for _, row in df.iterrows():
        source = row['Source']
        target = row['Target']
        weight = row['Weight']
        net.add_node(source, title=source)
        net.add_node(target, title=target)
        net.add_edge(source, target, value=weight)

    net.community_detection()
    html_content = net.get_html()
    return html_content

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
