import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("NFL Pizza Chart App"),
    html.P("This will eventually let you compare up to 4 players.")
])

if __name__ == "__main__":
    app.run(debug=True)